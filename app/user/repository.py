from app.repository import SQLAlchemyRepository
from app.user.model import UserInfoModel, UserModel


class UserRepository(SQLAlchemyRepository):
    model = UserModel


class UserInfoRepository(SQLAlchemyRepository):
    model = UserInfoModel
