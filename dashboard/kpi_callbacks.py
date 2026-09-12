from __future__ import annotations

from dash import Input, Output, html

from dashboard.kpi_presenter import clasificar_kpis, formatear_kpis
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
        html.Span(produccion, className=f"kpi-value--{clasificacion['produccion']}"),
        html.Span(fpy, className=f"kpi-value--{clasificacion['fpy']}"),
        html.Span(defectos, className=f"kpi-value--{clasificacion['defectos']}"),
        html.Span(scrap, className=f"kpi-value--{clasificacion['scrap']}"),
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