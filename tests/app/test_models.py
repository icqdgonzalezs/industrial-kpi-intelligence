# tests/app/test_models.py
"""Tests del modelo SQLModel KPI.

Nota de diseño: SQLModel con `table=True` NO ejecuta validadores de Pydantic
en la construcción. La validación de entrada es responsabilidad de
`KPICreate` (ver tests/app/test_schemas.py). Estos tests documentan el
contrato real del modelo de tabla.
"""
from datetime import datetime

from app.models import KPI


def test_kpi_creacion_valida():
    """Un KPI con todos los campos correctos se instancia."""
    kpi = KPI(
        nombre="OEE",
        valor=85.5,
        unidad="%",
        timestamp=datetime(2026, 9, 23, 12, 0),
        linea_produccion="L1",
    )
    assert kpi.nombre == "OEE"
    assert kpi.valor == 85.5
    assert kpi.unidad == "%"
    assert kpi.linea_produccion == "L1"
    assert kpi.id is None


def test_kpi_timestamp_naive_se_acepta():
    """El modelo acepta datetime naive por sa_column=DateTime(timezone=False)."""
    kpi = KPI(
        nombre="OEE",
        valor=85.5,
        unidad="%",
        timestamp=datetime(2026, 9, 23, 12, 0),
        linea_produccion="L1",
    )
    assert kpi.timestamp.tzinfo is None


def test_kpi_no_valida_en_construccion():
    """SQLModel table=True NO valida en construcción — contrato conocido.

    La validación de entrada la hace KPICreate (Pydantic BaseModel) ANTES
    de construir el KPI. Este test documenta esa separación de capas
    (decisión 4.26 del TRASPASO).
    """
    # Sin nombre: no debe fallar (SQLModel no valida acá)
    kpi = KPI(
        valor=85.5,
        unidad="%",
        timestamp=datetime(2026, 9, 23),
        linea_produccion="L1",
    )
    assert kpi.nombre is None  # se construyó sin validar

    # valor no numérico: tampoco falla en construcción
    kpi2 = KPI(
        nombre="OEE",
        valor="no-es-numero",
        unidad="%",
        timestamp=datetime(2026, 9, 23),
        linea_produccion="L1",
    )
    assert kpi2.valor == "no-es-numero"
