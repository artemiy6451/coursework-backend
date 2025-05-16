from typing import Annotated

from app.user.dependincies import user_service
from app.user.schemas import AllUsersShow, UserCreate, UserCreated, UserShow
from app.user.service import UserService
from fastapi import APIRouter, Depends, status

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post(
    "/add_user",
    status_code=status.HTTP_201_CREATED,
)
async def add_user(
    user: UserCreate, service: Annotated[UserService, Depends(user_service)]
) -> UserCreated:
    created_user = await service.add_user(user)
    return created_user


@user_router.get("/get_user/{username}")
async def get_user(
    username: str, service: Annotated[UserService, Depends(user_service)]
) -> UserShow:
    user_info = await service.get_user_info(username=username)
    return user_info


@user_router.get("/get_all_users")
async def get_all_users(
    service: Annotated[UserService, Depends(user_service)],
) -> AllUsersShow:
    all_users = await service.get_all_users()
    return all_users


@user_router.post("/change_time/{username}")
async def change_time(
    username: str,
    time: int,
    service: Annotated[UserService, Depends(user_service)],
) -> UserShow:
    user = await service.change_time(username=username, time=time)
    return user
