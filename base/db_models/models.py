from __future__ import annotations

from sqlalchemy import Column, Text, Integer, Boolean

from base.db_models.base import Base


class Client(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    telegram_id = Column(Text(), unique=True, nullable=False)
    name = Column(Text())
    username = Column(Text())
    phone = Column(Text())
    birthday = Column(Text())
    is_banned = Column(Boolean())
    prime_hill_card = Column(Text(), unique=True)

    def __repr__(self):
        return f"<Client(fio='{self.name} {self.username}', phone={self.phone}, telegram_id='{self.telegram_id}'"
