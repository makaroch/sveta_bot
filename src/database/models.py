from datetime import date

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, BigInteger, TEXT, Date


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "clients"

    tg_user_id = Column(BigInteger, primary_key=True, autoincrement=False)
    username = Column(String(255))
    is_subscription = Column(Boolean, default=True)

    def __str__(self):
        return f"Клиент: {self.username} | {self.tg_user_id}"


class PurposeCountdown(Base):
    __tablename__ = "purpose_countdown"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255))
    date = Column(Date)
    sent_notification_today = Column(Boolean, default=False)
    tg_user_id = Column(BigInteger, ForeignKey("clients.tg_user_id"))

    def __str__(self):
        return f"Цель: {self.name} | {self.date}"


class MotivatingPhrases(Base):
    __tablename__ = "motivating_phrases"

    id = Column(BigInteger, primary_key=True)
    phrase = Column(TEXT)
    # tg_user_id = Column(BigInteger, ForeignKey("clients.tg_user_id"))


class ClientsPurposeCountdown(BaseModel):
    tg_user_id: int
    name: str
    date: date
