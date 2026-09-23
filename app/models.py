from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class KPI(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    valor: float
    unidad: str
    timestamp: datetime = Field(sa_column=Column(DateTime(timezone=False)))
    linea_produccion: str


