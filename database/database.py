import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.core.config import settings

logger = logging.getLogger(__name__)

# Create the SQLAlchemy engine
try:
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True,  # checks connection health
        echo=False
    )
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for models to inherit from
Base = declarative_base()

def get_db():
    """
    Dependency to get the database session.
    Yields a session and closes it after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
