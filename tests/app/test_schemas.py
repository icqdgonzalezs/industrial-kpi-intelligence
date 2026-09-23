# tests/app/test_schemas.py
"""Tests del schema Pydantic KPICreate."""
from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas import KPICreate


def test_kpicreate_campos_validos():
    """Construcción con datos completos."""
    payload = KPICreate(
        nombre="OEE",
        valor=85.5,
        unidad="%",
        timestamp="2026-09-23T12:00:00",
        linea_produccion="L1",
    )
    assert payload.nombre == "OEE"
    assert isinstance(payload.timestamp, datetime)
    assert payload.timestamp.year == 2026


def test_kpicreate_parsea_timestamp_iso():
    """String ISO 8601 → datetime automáticamente."""
    payload = KPICreate(
        nombre="Tasa",
        valor=2.1,
        unidad="%",
        timestamp="2026-09-23T08:30:00",
        linea_produccion="L2",
    )
    assert payload.timestamp == datetime(2026, 9, 23, 8, 30)


def test_kpicreate_rechaza_timestamp_invalido():
    """String no parseable → ValidationError."""
    with pytest.raises(ValidationError):
        KPICreate(
            nombre="OEE",
            valor=85.5,
            unidad="%",
            timestamp="no-es-una-fecha",
            linea_produccion="L1",
        )


def test_kpicreate_coacciona_string_numerico_a_float():
    """Pydantic v2 no estricto: '85.5' → 85.5."""
    payload = KPICreate(
        nombre="OEE",
        valor="85.5",
        unidad="%",
        timestamp="2026-09-23T12:00:00",
        linea_produccion="L1",
    )
    assert payload.valor == 85.5
    assert isinstance(payload.valor, float)


def test_kpicreate_no_tiene_id():
    """El schema de creación no incluye id (autoincremental)."""
    payload = KPICreate(
        nombre="OEE",
        valor=85.5,
        unidad="%",
        timestamp="2026-09-23T12:00:00",
        linea_produccion="L1",
    )
    assert "id" not in KPICreate.model_fields
    assert "id" not in payload.model_dump()
