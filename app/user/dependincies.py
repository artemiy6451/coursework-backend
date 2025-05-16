from app.user.repository import UserRepository
from app.user.service import UserService


def user_service() -> UserService:
    return UserService(UserRepository)
