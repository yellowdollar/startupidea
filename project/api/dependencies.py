from repositories.users import UsersRepository
from services.users import UsersService


def users_service():
    return UsersService(UsersRepository)