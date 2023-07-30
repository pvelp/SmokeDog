from __future__ import annotations

from sqlalchemy import Column, Text, Integer, Boolean

from base.db_models.base import Base


class Client(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    telegram_id = Column(Text(), nullable=False, unique=True)
    name = Column(Text(), nullable=False)
    username = Column(Text(), nullable=False)
    phone = Column(Text(), nullable=False)
    birthday = Column(Text(), nullable=False)
    last_visit = Column(Text(), nullable=False)
    is_banned = Column(Boolean(), nullable=False)

    def __repr__(self):
        return f"<Client(fio='{self.name} {self.surname}', phone={self.phone}, telegram_id='{self.telegram_id}'"
