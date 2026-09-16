"""Tests para dashboard.severity_icons (WCAG 2.1 §1.4.1)."""

from __future__ import annotations

import pytest

from dashboard.severity_icons import (
    ICONO_POR_SEVERIDAD,
    SEVERIDADES_VALIDAS,
    prefijar_icono,
)


def test_icono_por_severidad_tiene_las_4_claves_canonicas():
    assert set(ICONO_POR_SEVERIDAD.keys()) == {
        "success",
        "warning",
        "danger",
        "neutral",
    }


def test_severidades_validas_es_frozenset():
    assert isinstance(SEVERIDADES_VALIDAS, frozenset)
    assert frozenset(ICONO_POR_SEVERIDAD.keys()) == SEVERIDADES_VALIDAS


@pytest.mark.parametrize(
    ("severidad", "icono"),
    [("success", "✓"), ("warning", "⚠"), ("danger", "✕")],
)
def test_prefijar_icono_agrega_icono_correcto(severidad, icono):
    assert prefijar_icono("97.2%", severidad) == f"{icono} 97.2%"


def test_prefijar_icono_neutral_no_agrega_icono():
    assert prefijar_icono("97.2%", "neutral") == "97.2%"


def test_prefijar_icono_severidad_desconocida_no_agrega_icono():
    """Comportamiento seguro: severidad desconocida = sin icono, no crash."""
    assert prefijar_icono("97.2%", "catastrofico") == "97.2%"


def test_prefijar_icono_valor_vacio_devuelve_vacio():
    """Un valor vacío no se contamina con un icono huérfano."""
    assert prefijar_icono("", "success") == ""
    assert prefijar_icono("", "neutral") == ""


def test_prefijar_icono_preserva_valor_con_espacios_internos():
    assert prefijar_icono("55 PPM total", "danger") == "✕ 55 PPM total"
