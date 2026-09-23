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


