import datetime

from pydantic import BaseModel


class ClientModel(BaseModel):
    telegram_id: str
    name: str
    username: str
    phone: str
    birthday: str
    is_banned: bool
    # last_visit: datetime.date
