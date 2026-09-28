# app/db.py
"""Configuración de la base de datos.

Lee DATABASE_URL de las variables de entorno. Si no está definida,
usa SQLite local (fallback para desarrollo).

- Local (sin env var): sqlite:///./kpi_database.db
- Docker Compose:       postgresql://kpi:dev@db:5432/kpi
- Railway (addon):      postgresql://...  (seteado automáticamente)
"""
import os
from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kpi_database.db")

# pool_pre_ping: verifica que la conexión esté viva antes de usarla.
# Necesario para Postgres en producción, que cierra conexiones inactivas.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise
