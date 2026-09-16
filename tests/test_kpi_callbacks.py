"""Tests para dashboard.kpi_callbacks (iconografía de semáforos)."""

from __future__ import annotations

from dash import html

from dashboard.kpi_callbacks import _span_kpi


def test_span_kpi_es_html_span():
    span = _span_kpi("97.2%", "success")
    assert isinstance(span, html.Span)


def test_span_kpi_incluye_icono_en_el_hijo():
    span = _span_kpi("97.2%", "success")
    assert span.children == "✓ 97.2%"


def test_span_kpi_incluye_clase_css_correcta():
    span = _span_kpi("97.2%", "danger")
    assert span.className == "kpi-value--danger"


def test_span_kpi_neutral_no_lleva_icono():
    span = _span_kpi("1,234", "neutral")
    assert span.children == "1,234"
    assert span.className == "kpi-value--neutral"
