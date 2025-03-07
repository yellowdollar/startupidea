from utils.repositories import SQLAlchemyRepository
from models.users import UsersModel


class UsersRepository(SQLAlchemyRepository):
    model = UsersModel