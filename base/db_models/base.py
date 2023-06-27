from datetime import datetime

from sqlalchemy import Column, DateTime, MetaData
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session

metadata = MetaData()


@as_declarative(metadata=metadata)
class Base:
    created_at = Column(DateTime(timezone=False), default=datetime.now)
    updated_at = Column(
        DateTime(timezone=False),
        onupdate=datetime.now,
        default=datetime.now,
    )

    def create(self, session: Session):
        session.add(self)
        session.commit()
        session.refresh(self)
        return self

    @declared_attr
    def __tablename__(cls):
        return str(cls.__name__).lower() + "s"

    _secret_columns = []

    def as_dict(self):
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name not in self._secret_columns
        }
