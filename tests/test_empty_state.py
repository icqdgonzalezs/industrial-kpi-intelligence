"""Tests del componente SSOT `dashboard/empty_state.py` (Fase 3b.2)."""

from __future__ import annotations

from dash import html

from dashboard.empty_state import ICONO_DEFAULT, empty_state


def test_empty_state_estructura_minima():
    """Mensaje obligatorio + icono default. Sin hint."""
    resultado = empty_state("Sin datos")

    assert isinstance(resultado, html.Div)
    assert resultado.className == "empty-state"
    assert len(resultado.children) == 2  # icono + mensaje


def test_empty_state_con_hint():
    """Hint opcional agrega un tercer hijo."""
    resultado = empty_state("Sin datos", hint="Ajustá los filtros")

    assert len(resultado.children) == 3


def test_empty_state_icono_es_default():
    """Sin icono explícito, se usa el buzón vacío."""
    resultado = empty_state("Sin datos")
    icono = resultado.children[0]

    assert isinstance(icono, html.Div)
    assert icono.className == "empty-state-icon"
    assert icono.children == ICONO_DEFAULT


def test_empty_state_icono_custom():
    """Icono explícito reemplaza el default."""
    resultado = empty_state("Sin datos", icono="🔍")
    icono = resultado.children[0]

    assert icono.children == "🔍"


def test_empty_state_clases_css_correctas():
    """Los 3 elementos llevan las clases del sistema de diseño."""
    resultado = empty_state("Sin datos", hint="Ajustá")

    icono, mensaje, hint = resultado.children

    assert icono.className == "empty-state-icon"
    assert mensaje.className == "empty-state-message"
    assert hint.className == "empty-state-hint"


def test_empty_state_sin_hint_no_incluye_el_hint():
    """Sin hint, no debe aparecer el div de hint."""
    resultado = empty_state("Sin datos")

    clases = [getattr(child, "className", None) for child in resultado.children]
    assert "empty-state-hint" not in clases


def test_empty_state_mensaje_se_preserva_tal_cual():
    """El mensaje no se debe reformatear ni capitalizar."""
    texto = "Sin defectos en el período seleccionado"
    resultado = empty_state(texto)

    assert resultado.children[1].children == texto
