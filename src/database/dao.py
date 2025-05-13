from sqlalchemy import update, select

from src.database.base_dao import BaseDAO
from src.database.db_settings import async_session
from src.database.models import Client, PurposeCountdown, MotivatingPhrases, ClientsPurposeCountdown


class ClientDAO(BaseDAO):
    model = Client

    @classmethod
    async def update(cls, _id, **data):
        async with async_session() as session:
            q = update(cls.model).values(**data).where(cls.model.tg_user_id == _id)
            await session.execute(q)
            await session.commit()

    @classmethod
    async def get_user_targets(cls):
        async with async_session() as session:
            q = (
                select(cls.model.tg_user_id, PurposeCountdown.name, PurposeCountdown.date)
                .select_from(cls.model)
                .filter_by(is_subscription=True)
                .join(PurposeCountdown, cls.model.tg_user_id == PurposeCountdown.tg_user_id)
            )
            result = await session.execute(q)
            result = result.all()
            return [
                ClientsPurposeCountdown(
                    tg_user_id=result[i][0],
                    name=result[i][1],
                    date=result[i][2],
                )
                for i in range(len(result))
            ]


class PurposeCountdownDAO(BaseDAO):
    model = PurposeCountdown


class MotivatingPhrasesDAO(BaseDAO):
    model = MotivatingPhrases
