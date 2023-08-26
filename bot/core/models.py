import datetime

from pydantic import BaseModel


class ClientModel(BaseModel):
    telegram_id: str
    name: str
    username: str
    phone: str
    birthday: str
    is_banned: bool
    card_hash: str


class PrimeHillModel(BaseModel):
    lastName: str
    firstName: str
    patronymic: str
    birthday: str
    sex: bool
    email: str
    phone: str
