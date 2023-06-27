from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import Engine


def set_settings_file_for_db(settings):
    global settings_file
    settings_file = settings


def create_session() -> Session:
    engine: Engine = create_engine(settings_file.db_url, pool_pre_ping=True)
    session_marker = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

    return session_marker()


@contextmanager
def get_session():
    session: Session = create_session()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
