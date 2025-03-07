from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base


class UsersModel(Base):
    __tablename__ = 'tb_user'

    id: Mapped[int] = mapped_column(primary_key = True)
    login: Mapped[str] = mapped_column(nullable = False, unique = True)
    password: Mapped[str] = mapped_column(nullable = False)
    level: Mapped[int] = mapped_column(default = 0)

















    
