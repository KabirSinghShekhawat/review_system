from datetime import datetime, timezone

from celery import Celery
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings
from app.database import get_db
from app.models import AccessLog

celery_app = Celery("tasks", broker=settings.BROKER_URL)


@celery_app.task(bind=True, max_retries=3)
def log_access(self, text: str):
    try:
        with get_db() as db:
            access_log = AccessLog(text=text, created_at=datetime.now(timezone.utc))
            db.add(access_log)
            db.commit()

    except SQLAlchemyError as exc:
        # Rollback the transaction
        db.rollback()

        # Retry the task with exponential backoff
        retry_in = 60 * (2**self.request.retries)  # 60s, 120s, 240s
        raise self.retry(exc=exc, countdown=retry_in)
