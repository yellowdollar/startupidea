from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base


class CompaniesModel(Base):
    __tablename__ = 'tb_company'

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(nullable = False)
