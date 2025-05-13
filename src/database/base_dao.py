from sqlalchemy import select, insert, update

from src.database.models import Base
from src.database.db_settings import async_session


class BaseDAO:
    model: Base | None = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session() as session:
            q = select(cls.model).filter_by(id=model_id)
            result = await session.execute(q)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **kwargs):
        async with async_session() as session:
            q = select(cls.model).filter_by(**kwargs)
            result = await session.execute(q)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **kwargs):
        async with async_session() as session:
            q = select(cls.model).filter_by(**kwargs)
            result = await session.execute(q)
            return result.scalars().all()

    @classmethod
    async def create(cls, **data):
        async with async_session() as session:
            q = insert(cls.model).values(**data)
            await session.execute(q)
            await session.commit()
