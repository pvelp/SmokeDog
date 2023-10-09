from loguru import logger

from base.db_connection import get_session
from base.db_models.models import Event


def add_event(date: str, text: str = None, media_path: str = None):
    with get_session() as session:
        try:
            event = Event()
            event.text = text
            event.media_path = media_path
            event.date = date
            session.add(event)
            session.commit()
        except Exception as e:
            logger.critical(e)


def get_event_by_date(date: str):
    with get_session() as session:
        try:
            event = session.query(Event).filter(Event.date == date).first()
            return event.to_dict()
        except Exception as e:
            logger.error(f"{e}. Event in {date} not found")
            return None


def delete_event_by_date(date: str):
    with get_session() as session:
        event = session.query(Event).filter(Event.date == date).first()

        if event is not None:
            session.delete(event)
            session.commit()


def get_events():
    with get_session() as session:
        events = session.query(Event).all()
        result = [event.to_dict() for event in events]
        return result
