from __future__ import annotations

from sqlalchemy import Column, Text, Integer, Boolean

from base.db_models.base import Base
from bot.core.models import AdminModel, ClientModel


class Client(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    telegram_id = Column(Text(), unique=True, nullable=False)
    name = Column(Text(), nullable=True)
    username = Column(Text(), nullable=True)
    phone = Column(Text(), nullable=True)
    is_banned = Column(Boolean(), nullable=True)

    def __repr__(self):
        return f"<Client(fio='{self.name} {self.username}', phone={self.phone}, telegram_id='{self.telegram_id}'"

    def to_obj(self):
        return ClientModel(
            telegram_id=str(self.telegram_id),
            name=self.name if self.name is not None else "Имя не указано",
            username=self.username if self.username is not None else "Юзернейм не указан",
            phone=self.phone if self.phone is not None else "Телефон не указан",
            is_banned=self.is_banned,
        )


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer(), primary_key=True)
    telegram_id = Column(Text(), unique=True, nullable=False)
    name = Column(Text(), nullable=True)

    def __repr__(self):
        return f"<Admin(telegram_id='{self.telegram_id}', name='{self.name}')"

    def to_obj(self):
        return AdminModel(telegram_id=str(self.telegram_id), name=self.name)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer(), primary_key=True)
    text = Column(Text(), nullable=True)
    media_path = Column(Text, nullable=True)
    date = Column(Text, nullable=False)

    def to_dict(self):
        return {"text": self.text, "media": self.media_path, "date": self.date}