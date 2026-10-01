# app/schemas.py
"""Schemas Pydantic (contratos de entrada/salida de la API).

Separados de los modelos SQLModel: la validación de entrada (Pydantic)
es responsabilidad de esta capa, no de la capa de persistencia.
"""
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

# ============================================================
# KPIs
# ============================================================

class KPICreate(BaseModel):
    """Schema de entrada para crear un KPI.

    Pydantic convierte el string a datetime automáticamente.
    """
    nombre: str
    valor: float
    unidad: str
    timestamp: datetime
    linea_produccion: str


# ============================================================
# Auth
# ============================================================

class UserLogin(BaseModel):
    """Credenciales de login."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserCreate(BaseModel):
    """Creación de usuario (registro o seed)."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserPublic(BaseModel):
    """Usuario expuesto al cliente. NUNCA incluye hashed_password."""
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime


class Token(BaseModel):
    """Respuesta de login exitoso."""
    access_token: str
    token_type: str = "bearer"
