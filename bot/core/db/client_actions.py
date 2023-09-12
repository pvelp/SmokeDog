from __future__ import annotations

from loguru import logger

from base.db_connection import get_session
from base.db_models.models import Client
from bot.core.models import ClientModel, StartClientModel


def add_base_client(telegram_id: str):
    with get_session() as session:
        try:
            client = Client()
            client.telegram_id = telegram_id
            session.add(client)
            session.commit()
        except Exception as e:
            logger.critical(e)


def add_new_client(client: ClientModel):
    with get_session() as session:
        try:
            client = Client(**(client.dict()))
            session.add(client)
            session.commit()
        except Exception as e:
            logger.critical(e)


def get_client_by_tg_id(telegram_id: str) -> ClientModel | None:
    with get_session() as session:
        client = session.query(Client).filter(Client.telegram_id == telegram_id).first()

        if client is None:
            logger.error(f"Client with telegram id = {telegram_id} was not found in DB")
            return None
        client_model = ClientModel(
            telegram_id=client.telegram_id,
            id=client.id,
            name=client.name if client.name is not None else "Имя не указано",
            username=client.username if client.username is not None else "Юзернейм не указан",
            phone=client.phone if client.phone is not None else "Номер не указан",
            is_banned=client.is_banned
        )
        # client_model = ClientModel(**client.as_dict())
        return client_model


def get_start_client_by_tg_id(telegram_id: str) -> StartClientModel | None:
    with get_session() as session:
        client = session.query(Client).filter(Client.telegram_id == telegram_id).first()
        if client is None:
            logger.error(f"Client with telegram id = {telegram_id} was not found in DB")
            return None
        start_client_model = StartClientModel(**client.as_dict())
        return start_client_model


def delete_user_by_tg_id(telegram_id: str):
    with get_session() as session:
        client = session.query(Client).filter(Client.telegram_id == telegram_id).first()

        if client is not None:
            session.delete(client)
            session.commit()


def add_client(data):
    with get_session() as session:
        try:
            client = Client(
                telegram_id=data.get("telegram_id"),
                name=data.get("name"),
                username=data.get("username"),
                phone=data.get("phone"),
                is_banned=False,
            )
        except KeyError as e:
            logger.error(e)
        session.add(client)
        session.commit()


def update_client_by_tg_id(telegram_id: str, data):
    with get_session() as session:
        client = session.query(Client).filter(Client.telegram_id == telegram_id).first()
        client.name = data.get("name")
        client.username = data.get("username")
        client.phone = data.get("phone")
        session.commit()
