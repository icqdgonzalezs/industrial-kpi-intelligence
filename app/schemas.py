from datetime import datetime

from pydantic import BaseModel


class KPICreate(BaseModel):
    """Schema de entrada para crear un KPI. Pydantic convierte el string a datetime automáticamente."""
    nombre: str
    valor: float
    unidad: str
    timestamp: datetime
    linea_produccion: str

