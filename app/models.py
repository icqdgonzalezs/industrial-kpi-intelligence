# app/models.py
"""Modelos SQLModel (tablas de la DB)."""
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class KPI(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    valor: float
    unidad: str
    timestamp: datetime = Field(sa_column=Column(DateTime(timezone=False)))
    linea_produccion: str


class User(SQLModel, table=True):
    """Usuario del sistema.

    Notas de diseño:
        - hashed_password guarda el hash bcrypt (~60 chars), NUNCA el password.
        - is_active permite deshabilitar sin borrar (auditoría).
        - email es unique + index para lookups rápidos en login.
        - created_at con default=datetime.utcnow para auditoría.
    """
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=False), default=datetime.utcnow)
    )
