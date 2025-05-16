from app.database import async_session_maker
from app.repository import AbstractRepository, SQLAlchemyRepository
from app.user.model import UserInfoModel, UserModel
from app.user.repository import UserInfoRepository
from app.user.schemas import AllUsersShow, UserCreate, UserCreated, UserShow
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError


class UserService:
    def __init__(self, repository: type[SQLAlchemyRepository[UserModel]]) -> None:
        self.user_repository: SQLAlchemyRepository[UserModel] = repository(
            async_session_maker,
            model=UserModel,
        )
        self.user_info_repository: AbstractRepository[UserInfoModel] = (
            UserInfoRepository(
                async_session_maker,
                model=UserInfoModel,
            )
        )

    async def add_user(self, user_data: UserCreate) -> UserCreated:
        try:
            user_id = await self.user_repository.add_one(user_data.model_dump())
            return UserCreated(id=user_id)
        except IntegrityError:
            raise Exception("User already exist") from None

    async def get_user_info(self, username: str) -> UserShow:
        user_id = await self.user_repository.get_id_by_username(username=username)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        user_info = await self.user_repository.find_one(user_id)
        if user_info is None:
            raise Exception("User not found")
        print(user_id)
        filter = UserInfoModel.user_id == user_id
        time_data = await self.user_info_repository.find_all(filter)
        return UserShow(
            username=user_info.username, time=user_info.time, time_data=time_data
        )

    async def get_all_users(self) -> AllUsersShow:
        user_models = await self.user_repository.find_all()
        users = [user.to_read_model() for user in user_models]
        return AllUsersShow(data=users)

    async def change_time(self, username: str, time: int) -> UserShow:
        user_id = await self.user_repository.get_id_by_username(username=username)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        user_old = await self.user_repository.find_one(id=user_id)
        if user_old is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        data = {"time": user_old.time + time}
        await self.user_repository.update_one(id=user_id, data=data)
        user_new = await self.user_repository.find_one(id=user_id)
        if user_new is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserShow(
            username=user_new.username,
            time=user_new.time,
            time_data=None,
        )
