from database.database import async_session
from abc import abstractmethod

from sqlalchemy import insert, select, update, delete


class AbstractRepository:
    
    @abstractmethod 
    async def add():
        return NotImplementedError
    
    @abstractmethod
    async def update():
        return NotImplementedError
    
    @abstractmethod
    async def delete():
        return NotImplementedError
    
    @abstractmethod
    async def select():
        return NotImplementedError
    
class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add(self, data: dict):
        async with async_session() as session:
            stmt = (
                insert(self.model)
                .values(**data)
                .returning(self.model)
            )

            try:
                result = await session.execute(stmt)
                await session.commit()

                return result.scalar_one()
            except Exception as error:
                await session.rollback()
                raise ValueError(f"Error while additing: {str(error)}")

            
    async def update(self, id: int, data: dict):
        async with async_session() as session:
            stmt = (
                update(self.model)
                .values(**data)
                .where(self.model.id == id)
                .returning(self.model)
            )

            try:
                result = await session.execute(stmt)
                await session.commit()

                return result.scalar_one()
            except Exception as error:
                await session.rollback()
                raise ValueError(f"Error while updating: {str(error)}")


    async def delete(self, id: int):
        async with async_session() as session:
            stmt = (
                delete(self.model)
                .where(self.model.id == id)
                .returning(self.model)
            )

            try:
                result = await session.execute(stmt)
                await session.commit()

                return result.scalar_one()
            except Exception as error:
                await session.rollback()
                raise ValueError(f"Error while deleting: {str(error)}")

            
    async def select(self, filters: dict):
        async with async_session() as session:
            stmt = (
                select(self.model)
                .filter_by(**filters)
            )

            try:
                result = await session.execute(stmt)
                await session.commit()

                return result.scalars().all()
            except Exception as error:
                await session.rollback()
                raise ValueError(f"Error while getting: {str(error)}")


