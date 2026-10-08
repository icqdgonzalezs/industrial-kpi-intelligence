# app/models.py
"""Modelos SQLModel (tablas de la DB).

Multi-tenant readiness:
    - `tenant_id` en `User` y `KPI` con default "default".
    - Preparado para filtrar por tenant cuando llegue el cliente #2.
    - Schema-first: agregar la columna ya, activar el filtrado después.
"""
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class KPI(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tenant_id: str = Field(default="default", index=True)
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
        - tenant_id prepara multi-tenant (default "default" = single-tenant).
    """
    id: int | None = Field(default=None, primary_key=True)
    tenant_id: str = Field(default="default", index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=False), default=datetime.utcnow)
    )