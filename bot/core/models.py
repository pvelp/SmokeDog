import datetime

from pydantic import BaseModel


class ClientModel(BaseModel):
    telegram_id: str
    name: str
    username: str
    phone: str
    birthday: datetime.date
    is_banned: bool
    # last_visit: datetime.date
