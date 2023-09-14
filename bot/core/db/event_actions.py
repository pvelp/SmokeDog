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


def get_event_by_day(day: str) -> dict | None:
    with get_session() as session:
        event = session.query(Event).filter(Event.day == day).first()
        if event is None:
            logger.error(f"Event in {day} not found")
            return None
    return event.to_dict()


def delete_event_by_day(day: str):
    with get_session() as session:
        event = session.query(Event).filter(Event.day == day).first()

        if event is not None:
            session.delete(event)
            session.commit()
