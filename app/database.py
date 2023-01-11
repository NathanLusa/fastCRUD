from datetime import timezone, datetime

from typing import Any

from sqlalchemy import create_engine, Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    "sqlite:///./app.db",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class BaseModels(object):
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True),
                        default=lambda: datetime.now(timezone.utc))


Base = declarative_base(cls=BaseModels)


def get_db() -> Any:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()
