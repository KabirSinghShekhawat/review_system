from app.database import get_db


def get_db_session():
    with get_db() as db:
        yield db
