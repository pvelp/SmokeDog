import datetime

from pydantic import BaseModel


class ClientModel(BaseModel):
    telegram_id: str
    name: str
    username: str = None
    phone: str = None
    is_banned: bool = None
    # card_hash: str


class StartClientModel(BaseModel):
    id: int
    telegram_id: str


class AdminModel(BaseModel):
    telegram_id: str
    name: str
