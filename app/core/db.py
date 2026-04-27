from sqlmodel import create_engine

from app.core.config import settings

# A SQLModel engine is what holds the connections to the database.
# One single engine object for all code to connect to the same database.
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI), echo=settings.ECHO_SQL_QUERIES
)
