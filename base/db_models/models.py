from __future__ import annotations

from sqlalchemy.orm import relationship, backref
from sqlalchemy import (
    Column,
    Text,
    Date,
    DateTime,
    Integer,
    Float,
    Boolean,
    ForeignKey
    )

from base.db_models.base import Base


class Client(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    telegram_id = Column(Text(), nullable=False, unique=True)
    name = Column(Text(), nullable=False)
    surname = Column(Text(), nullable=False)
    phone = Column(Text(), nullable=False)

    def __repr__(self):
        return f"<Client(fio='{self.name} {self.surname}', phone={self.phone}, id='{self.id}'"


