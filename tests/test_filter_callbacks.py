"""Tests para dashboard.filter_callbacks.

Cubre el contrato de los cascades de filtros y de "Restaurar filtros".
"""

from __future__ import annotations

import pandas as pd
from dash import Dash

from dashboard.filter_callbacks import (
    registrar_callbacks_filtros,
    valores_default_filtros,
)


def _df_prueba():
    return pd.DataFrame(
        {
            "fecha": pd.to_datetime(["2024-01-01"] * 6),
            "linea": ["L1", "L1", "L1", "L2", "L2", "L3"],
            "equipo": [
                "L1-FILL-01",
                "L1-FILL-01",
                "L1-CHECK-01",
                "L2-FILL-01",
                "L2-CAPPER-01",
                "L3-SEAL-01",
            ],
            "turno": ["Mañana", "Noche", "Mañana", "Mañana", "Noche", "Mañana"],
            "operador": ["OP1", "OP2", "OP1", "OP3", "OP4", "OP5"],
        }
    )


def _aplicar_filtros(df, **kwargs):
    """Simula el filtrado real sin depender de src/filter_engine."""
    resultado = df.copy()
    if "fecha_inicio" in kwargs and kwargs["fecha_inicio"]:
        resultado = resultado[resultado["fecha"] >= pd.to_datetime(kwargs["fecha_inicio"])]
    if "fecha_fin" in kwargs and kwargs["fecha_fin"]:
        resultado = resultado[resultado["fecha"] <= pd.to_datetime(kwargs["fecha_fin"])]
    for col, val in [("linea", "Todas"), ("equipo", "Todos"), ("turno", "Todos"), ("operador", "Todos")]:
        key = col
        valor = kwargs.get(key)
        if valor and valor != val:
            resultado = resultado[resultado[col] == valor]
    return resultado.reset_index(drop=True)


# ---------------------------------------------------------------------
# valores_default_filtros
# ---------------------------------------------------------------------


def test_valores_default_filtros_contrato():
    """Los 6 valores por defecto, en el orden exacto de los Outputs."""
    resultado = valores_default_filtros("2024-01-01", "2024-12-31")

    assert resultado == (
        "2024-01-01",
        "2024-12-31",
        "Todas",
        "Todos",
        "Todos",
        "Todos",
    )


def test_valores_default_filtros_propaga_fechas():
    resultado = valores_default_filtros("2020-06-15", "2025-09-30")

    assert resultado[0] == "2020-06-15"
    assert resultado[1] == "2025-09-30"


# ---------------------------------------------------------------------
# Smoke test de registro
# ---------------------------------------------------------------------


def test_registrar_callbacks_filtros_smoke():
    """Los 5 callbacks (4 cascades + 1 reset) se registran sin error."""
    app = Dash(__name__, suppress_callback_exceptions=True)
    df = _df_prueba()

    registrar_callbacks_filtros(
        app,
        df,
        _aplicar_filtros,
        fecha_min="2024-01-01",
        fecha_max="2024-12-31",
    )

    # 5 callbacks registrados
    assert len(app.callback_map) == 5


def test_cascade_callbacks_registrados():
    """Verificar que los 5 callbacks están presentes por sus outputs."""
    app = Dash(__name__, suppress_callback_exceptions=True)
    df = _df_prueba()

    registrar_callbacks_filtros(
        app,
        df,
        _aplicar_filtros,
        fecha_min="2024-01-01",
        fecha_max="2024-12-31",
    )

    outputs = set(app.callback_map.keys())

    # Cascade de línea
    assert any("filtro-linea.options" in str(o) for o in outputs)
    # Cascade de equipo
    assert any("filtro-equipo.options" in str(o) for o in outputs)
    # Cascade de turno
    assert any("filtro-turno.options" in str(o) for o in outputs)
    # Cascade de operador
    assert any("filtro-operador.options" in str(o) for o in outputs)
    # Reset
    assert any("filtro-periodo.start_date" in str(o) for o in outputs)
