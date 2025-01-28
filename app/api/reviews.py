from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db_session
from app.service import review_service
from app.tasks import log_access

router = APIRouter()


@router.get("/reviews")
def get_reviews(
    category_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=15, le=100),
    db: Session = Depends(get_db_session),
):
    offset = (page - 1) * page_size
    reviews = review_service.get_reviews(db, category_id, offset, page_size)
    log_access.delay(f"GET /reviews/?category_id={category_id}")
    return reviews


@router.get("/reviews/trends")
def get_review_trends(db: Session = Depends(get_db_session)):
    categories = review_service.get_review_trends(db)

    log_access.delay("GET /reviews/trends")

    return categories
