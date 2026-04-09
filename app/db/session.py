from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# The engine is the actual connection to PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    # Number of persistent connections kept open
    pool_size=5,
    # Extra connections allowed under heavy load
    max_overflow=10,
)

# Factory that creates new DB sessions on demand
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,  # We manage transactions manually
    autoflush=False,   # We decide when to flush to DB
)


def get_db():
    """
    FastAPI dependency that provides a DB session per request.
    Automatically closes the session when the request ends.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()