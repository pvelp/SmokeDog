from __future__ import annotations

from sqlalchemy import Column, Text, Integer, Boolean

from base.db_models.base import Base


class Client(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    telegram_id = Column(Text(), unique=True, nullable=False)
    name = Column(Text(), nullable=True)
    username = Column(Text(), nullable=True)
    phone = Column(Text(), nullable=True)
    birthday = Column(Text(), nullable=True)
    is_banned = Column(Boolean(), nullable=True)

    def __repr__(self):
        return f"<Client(fio='{self.name} {self.username}', phone={self.phone}, telegram_id='{self.telegram_id}'"
