from loguru import logger

from base.db_connection import get_session
from base.db_models.models import Event


def add_event(day: str, text: str = None, media_path: str = None):
    with get_session() as session:
        try:
            event = Event()
            event.text = text
            event.media_path = media_path
            event.day = day
            session.add(event)
            session.commit()
        except Exception as e:
            logger.critical(e)


def get_event_by_day(day: str):
    with get_session() as session:
        try:
            event = session.query(Event).filter(Event.day == day).first()
            return event.to_dict()
        except Exception as e:
            logger.error(f"{e}. Event in {day} not found")
            return None


def delete_event_by_day(day: str):
    with get_session() as session:
        event = session.query(Event).filter(Event.day == day).first()

        if event is not None:
            session.delete(event)
            session.commit()
