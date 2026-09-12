"""Tests de la clasificación semántica de KPIs."""

from __future__ import annotations

import pytest

from src.kpi_thresholds import clasificar_kpi

# ---------------------------------------------------------------------
# Sin umbrales → siempre NEUTRAL
# ---------------------------------------------------------------------


def test_sin_umbrales_retorna_neutral():
    assert clasificar_kpi(0.95, None) == "neutral"


def test_sin_direccion_retorna_neutral():
    assert clasificar_kpi(0.95, {"success": 0.90}) == "neutral"


# ---------------------------------------------------------------------
# higher_is_better (FPY)
# ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (0.98, "success"),
        (0.95, "success"),         # borde exacto de success
        (0.92, "warning"),
        (0.90, "warning"),         # borde exacto de warning
        (0.85, "danger"),
        (0.50, "danger"),
    ],
)
def test_higher_is_better_fpy(valor, esperado):
    resultado = clasificar_kpi(
        valor,
        {"success": 0.95, "warning": 0.90},
        "higher_is_better",
    )
    assert resultado == esperado


# ---------------------------------------------------------------------
# lower_is_better (Defectos, Scrap, Reproceso)
# ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (0.01, "success"),
        (0.03, "success"),         # borde exacto de success
        (0.04, "warning"),
        (0.05, "warning"),         # borde exacto de warning
        (0.08, "danger"),
        (0.15, "danger"),
    ],
)
def test_lower_is_better_defectos(valor, esperado):
    resultado = clasificar_kpi(
        valor,
        {"success": 0.03, "warning": 0.05},
        "lower_is_better",
    )
    assert resultado == esperado