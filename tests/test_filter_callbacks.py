"""Tests para dashboard.filter_callbacks.

Cubre el contrato de "Restaurar filtros" (Fase 3a — bug fix):

- valores_default_filtros: función pura, contrato explícito de los
  6 valores por defecto del control center.
- Smoke test de registrar_callbacks_filtros: verifica que los
  callbacks (incluido el de reset con allow_duplicate=True) se
  registran sin explotar por DuplicateCallbackOutput.
"""

from __future__ import annotations

import pandas as pd
from dash import Dash

from dashboard.filter_callbacks import (
    registrar_callbacks_filtros,
    valores_default_filtros,
)


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
    """Las fechas recibidas se propagan tal cual (sin reformateo)."""
    resultado = valores_default_filtros("2020-06-15", "2025-09-30")

    assert resultado[0] == "2020-06-15"
    assert resultado[1] == "2025-09-30"


def test_registrar_callbacks_filtros_smoke():
    """Los callbacks (incluido el reset) se registran sin error.

    Si los allow_duplicate=True faltan en algún Output duplicado,
    Dash lanza DuplicateCallbackOutput durante el registro.
    """
    app = Dash(
        __name__,
        suppress_callback_exceptions=True,
    )
    df = pd.DataFrame(
        {
            "fecha": pd.to_datetime(["2024-01-01"]),
            "linea": ["A"],
            "equipo": ["E1"],
            "turno": ["T1"],
            "operador": ["OP1"],
        }
    )

    def dummy_aplicar_filtros(df, **kwargs):
        return df

    # No debe levantar excepción
    registrar_callbacks_filtros(
        app,
        df,
        dummy_aplicar_filtros,
        fecha_min="2024-01-01",
        fecha_max="2024-12-31",
    )

    # Si llegamos acá, los 5 callbacks (4 cascade + 1 reset) se
    # registraron sin DuplicateCallbackOutput.
    assert True