from typing import Any

from sqlalchemy import create_engine
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

Base = declarative_base()
# Base.metadata.create_all(bind=engine)


def get_db() -> Any:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()
