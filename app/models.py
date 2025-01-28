from sqlalchemy import Column, Integer, BigInteger, Text, DateTime, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class Category(Base):
    __tablename__ = "category"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    # Relationship to ReviewHistory
    reviews = relationship("ReviewHistory", back_populates="category")


class ReviewHistory(Base):
    __tablename__ = "review_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    text = Column(VARCHAR, nullable=True)
    stars = Column(Integer, nullable=False)  # Assuming stars are between 1 and 10
    review_id = Column(
        VARCHAR(255), nullable=False
    )  # Identifies the review across versions
    tone = Column(VARCHAR(255), nullable=True)
    sentiment = Column(VARCHAR(255), nullable=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationship to Category
    category = relationship("Category", back_populates="reviews")


class AccessLog(Base):
    __tablename__ = "access_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    text = Column(VARCHAR, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
