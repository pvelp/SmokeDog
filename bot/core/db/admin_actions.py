from __future__ import annotations

from loguru import logger

from base.db_connection import get_session
from sqlalchemy import insert
from base.db_models.models import Admin
from bot.core.models import AdminModel


def get_all_admins() -> list[AdminModel] | None:
    with get_session() as session:
        admins = session.query(Admin).all()
    result = [admin.to_obj() for admin in admins]
    return result


def add_admin(telegram_id: str, name: str = None):
    with get_session() as session:
        try:
            q = insert(Admin).values(
                telegram_id=telegram_id,
                name=name
            )
            session.execute(q)
            session.commit()
        except Exception as ex:
            logger.critical(ex)

