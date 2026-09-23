# app/db.py
from typing import Generator

from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///./kpi_database.db"
engine = create_engine(DATABASE_URL)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise

