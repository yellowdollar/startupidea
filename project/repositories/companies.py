from utils.repositories import SQLAlchemyRepository
from models.companies import CompaniesModel


class CompaniesRepository(SQLAlchemyRepository):
    model = CompaniesModel
