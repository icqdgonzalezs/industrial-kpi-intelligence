from __future__ import annotations

from dash import Input, Output, html

from dashboard.kpi_presenter import clasificar_kpis, formatear_kpis
from dashboard.severity_icons import prefijar_icono
from dashboard.utils import leer_dataframe_filtrado
from src.kpis import calcular_kpis_globales


def actualizar_kpis(data):
    filtrado = leer_dataframe_filtrado(data)

    if filtrado.empty:
        return "0", "—", "—", "—"

    kpis = calcular_kpis_globales(filtrado)
    presentados = formatear_kpis(kpis)

    return (
        presentados["produccion"],
        presentados["fpy"],
        presentados["defectos"],
        presentados["scrap"],
    )


def _span_kpi(valor: str, clasificacion: str) -> html.Span:
    """Construye un <span> de KPI con icono de severidad y clase CSS.

    El icono es redundancia no cromática (WCAG 2.1 §1.4.1): un operario
    daltónico puede leer la severidad sin depender del color.
    """
    return html.Span(
        prefijar_icono(valor, clasificacion),
        className=f"kpi-value--{clasificacion}",
    )


def construir_kpi_cards(data):
    """Construye los 4 valores del KPI top como html.Span con color semántico."""
    produccion, fpy, defectos, scrap = actualizar_kpis(data)

    filtrado = leer_dataframe_filtrado(data)

    if filtrado.empty:
        clasificacion = {
            "produccion": "neutral",
            "fpy": "neutral",
            "defectos": "neutral",
            "scrap": "neutral",
        }
    else:
        kpis = calcular_kpis_globales(filtrado)
        clasificacion = clasificar_kpis(kpis)

    return (
        _span_kpi(produccion, clasificacion["produccion"]),
        _span_kpi(fpy, clasificacion["fpy"]),
        _span_kpi(defectos, clasificacion["defectos"]),
        _span_kpi(scrap, clasificacion["scrap"]),
    )


def registrar_callbacks_kpi(app) -> None:
    @app.callback(
        Output("kpi-produccion-total", "children"),
        Output("kpi-fpy", "children"),
        Output("kpi-defectos", "children"),
        Output("kpi-scrap", "children"),
        Input("store-datos-filtrados", "data"),
    )
    def callback_actualizar_kpis(data):
        return construir_kpi_cards(data)
