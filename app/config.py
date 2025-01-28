import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://admin:@localhost/reviews_db"
    )
    BROKER_URL: str = os.getenv("BROKER_URL", "redis://localhost:6379/0")
    OPENAI_KEY: str = os.getenv("OPENAI_KEY", "")
    ECHO_SQL: bool = False


settings = Settings()
