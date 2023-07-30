import datetime

from pydantic import BaseModel


class ClientModel(BaseModel):
    name: str
    username: str
    phone: str
    birthday: datetime.date
    last_visit: datetime.date
