"""Tests de integración del dashboard Dash — contrato de callbacks.

Cubren KPIs agregados, filtros encadenados (línea → equipo → turno →
operador) y tolerancia a entradas vacías o mal formadas.

PRODUCCION_TOTAL_ESPERADA es la suma de units_produced del dataset
canónico en disco (18,078 filas, seed 42). Recalcular con:
    df["units_produced"].sum()  # formateado con separador de miles
"""

import pandas as pd
import pytest

from dashboard.dash_app import (
    actualizar_datos_filtrados,
    actualizar_equipos,
    actualizar_kpis,
    actualizar_lineas,
    actualizar_operadores,
    actualizar_turnos,
)

# Suma de units_produced del dataset canónico (18,078 filas, seed 42).
# Cambia si se regenera el dataset con otro schema o seed.
PRODUCCION_TOTAL_ESPERADA = "53,587,651"


@pytest.fixture
def data_completa():
    """Dataset completo sin filtros, para alimentar actualizar_kpis."""
    return actualizar_datos_filtrados(
        "2024-01-01",
        "2025-12-31",
        "Todas",
        "Todos",
        "Todos",
        "Todos",
    )


# ---------------------------------------------------------------------
# KPIs agregados
# ---------------------------------------------------------------------


def test_actualizar_kpis_returns_expected_values(data_completa):
    valores = actualizar_kpis(data_completa)

    assert valores == (
        PRODUCCION_TOTAL_ESPERADA,
        "98.7%",
        "1.3%",
        "0.5%",
    )


def test_actualizar_kpis_handles_empty_data():
    assert actualizar_kpis(None) == ("0", "—", "—", "—")


def test_actualizar_kpis_rejects_missing_columns():
    data = pd.DataFrame({"otra_columna": [1, 2]}).to_json(orient="split")

    with pytest.raises(ValueError, match="Faltan columnas requeridas"):
        actualizar_kpis(data)


def test_actualizar_kpis_produccion_is_positive(data_completa):
    valores = actualizar_kpis(data_completa)

    assert int(valores[0].replace(",", "")) > 0


def test_actualizar_kpis_returns_percentage_values(data_completa):
    produccion, fpy, defectos, scrap = actualizar_kpis(data_completa)

    assert produccion == PRODUCCION_TOTAL_ESPERADA
    assert fpy.endswith("%")
    assert defectos.endswith("%")
    assert scrap.endswith("%")


# ---------------------------------------------------------------------
# Datos filtrados
# ---------------------------------------------------------------------


def test_actualizar_datos_filtrados_returns_json():
    data = actualizar_datos_filtrados(
        "2024-01-01",
        "2025-12-31",
        "Todas",
        "Todos",
        "Todos",
        "Todos",
    )

    assert isinstance(data, str)
    assert len(data) > 0


def test_actualizar_datos_filtrados_with_specific_line():
    data = actualizar_datos_filtrados(
        "2024-01-01",
        "2025-12-31",
        "Línea 1",
        "Todos",
        "Todos",
        "Todos",
    )

    assert isinstance(data, str)
    assert len(data) > 0


# ---------------------------------------------------------------------
# Filtros encadenados
# ---------------------------------------------------------------------


def test_actualizar_lineas_returns_options():
    options, value = actualizar_lineas("2024-01-01", "2025-12-31")

    assert options
    assert options[0] == {"label": "Todas", "value": "Todas"}
    assert value == "Todas"


def test_actualizar_equipos_returns_options():
    options, value = actualizar_equipos("Todas", "2024-01-01", "2025-12-31")

    assert options
    assert options[0] == {"label": "Todos", "value": "Todos"}
    assert value == "Todos"


def test_actualizar_turnos_returns_options():
    options, value = actualizar_turnos(
        "Todos", "Todas", "2024-01-01", "2025-12-31"
    )

    assert options
    assert options[0] == {"label": "Todos", "value": "Todos"}
    assert value == "Todos"


def test_actualizar_operadores_returns_options():
    options, value = actualizar_operadores(
        "Todos", "Todos", "Todas", "2024-01-01", "2025-12-31"
    )

    assert options
    assert options[0] == {"label": "Todos", "value": "Todos"}
    assert value == "Todos"