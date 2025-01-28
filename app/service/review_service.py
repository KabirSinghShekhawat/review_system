from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models import Category, ReviewHistory
from app.utils.llm_integration import analyze_tone_and_sentiment


def get_reviews(db: Session, category_id: int, offset: int, page_size: int):
    latest_reviews_subquery = (
        db.query(
            ReviewHistory.review_id,
            func.max(ReviewHistory.created_at).label("latest_created_at"),
        )
        .filter(ReviewHistory.category_id == category_id)
        .group_by(ReviewHistory.review_id)
        .subquery()
    )

    latest_reviews = (
        db.query(ReviewHistory)
        .join(
            latest_reviews_subquery,
            (ReviewHistory.review_id == latest_reviews_subquery.c.review_id)
            & (ReviewHistory.created_at == latest_reviews_subquery.c.latest_created_at),
        )
        .order_by(ReviewHistory.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    for review in latest_reviews:
        if review.tone is None or review.sentiment is None:
            tone, sentiment = analyze_tone_and_sentiment(review.text, review.stars)
            review.tone = tone
            review.sentiment = sentiment
            db.commit()

    result = [
        {
            "id": review.id,
            "text": review.text,
            "stars": review.stars,
            "review_id": review.review_id,
            "created_at": review.created_at,
            "tone": review.tone,
            "sentiment": review.sentiment,
            "category_id": review.category_id,
        }
        for review in latest_reviews
    ]

    return result


def get_review_trends(db: Session):
    latest_reviews_subquery = (
        db.query(
            ReviewHistory.review_id,
            func.max(ReviewHistory.created_at).label("latest_created_at"),
        )
        .group_by(ReviewHistory.review_id)
        .subquery()
    )

    latest_reviews = (
        db.query(ReviewHistory)
        .join(
            latest_reviews_subquery,
            (ReviewHistory.review_id == latest_reviews_subquery.c.review_id)
            & (ReviewHistory.created_at == latest_reviews_subquery.c.latest_created_at),
        )
        .subquery()
    )

    category_stats = (
        db.query(
            Category.id,
            Category.name,
            Category.description,
            func.avg(latest_reviews.c.stars).label("average_stars"),
            func.count(latest_reviews.c.id).label("total_reviews"),
        )
        .join(latest_reviews, Category.id == latest_reviews.c.category_id)
        .group_by(Category.id)
        .order_by(desc("average_stars"))
        .limit(5)
        .all()
    )

    result = [
        {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "average_stars": round(category.average_stars, 2),
            "total_reviews": category.total_reviews,
        }
        for category in category_stats
    ]

    return result
