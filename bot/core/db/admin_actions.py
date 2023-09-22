from __future__ import annotations

from loguru import logger

from base.db_connection import get_session
from sqlalchemy import insert
from base.db_models.models import Admin
from bot.core.models import AdminModel


def get_all_admins():
    with get_session() as session:
        admins = session.query(Admin).all()
    result = [admin.to_obj() for admin in admins]
    return result


def get_admin_by_id(telegram_id: str):
    with get_session() as session:
        admin = session.query(Admin).filter(Admin.telegram_id == telegram_id).firtst()
        if admin is None:
            logger.error(f"Admin with telegram id = {telegram_id} was not found in DB")
            return None
        admin_model = AdminModel(
            id=admin.id,
            telegram_id=admin.telegram_id,
            name=admin.name
        )
        return admin_model


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


def delete_admin(telegram_id: str):
    with get_session() as session:
        admin = session.query(Admin).filter(Admin.telegram_id == telegram_id).first()
        
        if admin is not None:
            session.delete(admin)
            session.commit()
