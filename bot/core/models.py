import datetime

from pydantic import BaseModel


class ClientModel(BaseModel):
    telegram_id: str
    name: str
    username: str = None
    phone: str = None
    birthday: str = None
    is_banned: bool = None
    # card_hash: str


class StartClientModel(BaseModel):
    id: int
    telegram_id: str


class PrimeHillModel(BaseModel):
    lastName: str
    firstName: str
    patronymic: str
    birthday: str
    sex: bool
    email: str
    phone: str
