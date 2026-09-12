"""Callbacks Dash del análisis operacional comparativo (drill-down).

La agregación por dimensión y el Pareto ya existen en src/kpis.py
(100% testeado). Este módulo reutiliza los umbrales de hotspot de
src/diagnostics.py para que el color del ranking sea consistente con
el motor de diagnóstico — una sola fuente de verdad para "qué es
prioritario".

Anotación "Promedio de planta" a 14px según ISA-101 (legibilidad
industrial desde 1m de distancia).
"""

from __future__ import annotations

import plotly.graph_objects as go
from dash import Input, Output, html

from dashboard.utils import aplicar_tema_oscuro, leer_dataframe_filtrado
from src.diagnostics import UMBRAL_HOTSPOT_PRIORITY, UMBRAL_HOTSPOT_WATCH
from src.kpis import (
    calcular_kpis_globales,
    calcular_kpis_por_dimension,
    calcular_pareto,
)

COLOR_PRIORITY = "#ef4444"
COLOR_WATCH = "#f59e0b"
COLOR_NORMAL = "#22c55e"


def _color_por_ratio(ratio: float) -> str:
    """Asigna color según el mismo umbral que usa el motor de diagnóstico."""
    if ratio >= UMBRAL_HOTSPOT_PRIORITY:
        return COLOR_PRIORITY
    if ratio >= UMBRAL_HOTSPOT_WATCH:
        return COLOR_WATCH
    return COLOR_NORMAL


def crear_figura_ranking(filtrado, dimension: str) -> go.Figure:
    """Construye el ranking comparativo (barras) para la dimensión seleccionada."""
    if filtrado is None or filtrado.empty:
        return aplicar_tema_oscuro(go.Figure())

    por_dimension = calcular_kpis_por_dimension(filtrado, dimension)

    if por_dimension.empty:
        return aplicar_tema_oscuro(go.Figure())

    promedio_planta = calcular_kpis_globales(filtrado)["tasa_defectos"]

    ratios = (
        por_dimension["tasa_defectos"] / promedio_planta
        if promedio_planta > 0
        else por_dimension["tasa_defectos"] * 0
    )
    colores = [_color_por_ratio(r) for r in ratios]

    figura = go.Figure(
        go.Bar(
            x=por_dimension[dimension].astype(str),
            y=por_dimension["tasa_defectos"] * 100,
            marker_color=colores,
        )
    )

    figura.add_hline(
        y=promedio_planta * 100,
        line_dash="dash",
        annotation_text="Promedio de planta",
        annotation_font_size=14,
        annotation_font_color="#e6edf3",
    )

    figura.update_layout(
        yaxis_title="Tasa de defectos (%)",
        xaxis_title=dimension.capitalize(),
        showlegend=False,
    )

    return aplicar_tema_oscuro(figura)


def crear_panel_detalle(filtrado, dimension: str, valor_seleccionado: str) -> html.Div:
    """Construye el panel de detalle (drill-down) para el grupo seleccionado."""
    subconjunto = filtrado[filtrado[dimension].astype(str) == str(valor_seleccionado)]

    if subconjunto.empty:
        return html.Div(
            "Sin datos para este grupo con los filtros actuales.",
            className="finding-message",
        )

    kpis = calcular_kpis_globales(subconjunto)
    pareto = calcular_pareto(subconjunto)
    causa_principal = str(pareto.iloc[0]["defecto"]) if not pareto.empty else "Sin datos"

    return html.Div(
        [
            html.Div(
                f"{dimension.capitalize()}: {valor_seleccionado}",
                className="finding-title",
            ),
            html.Div(
                f"FPY: {kpis['fpy']:.1%} · Tasa de defectos: {kpis['tasa_defectos']:.1%} · "
                f"Scrap: {kpis['tasa_scrap']:.1%} · Reproceso: {kpis['tasa_reproceso']:.1%} · "
                f"Lotes: {len(subconjunto)}",
                className="finding-message",
            ),
            html.Div(
                f"Causa de defecto principal: {causa_principal}",
                className="finding-message",
            ),
        ],
        className="finding-card finding-info",
    )


def registrar_callbacks_operational_analysis(app) -> None:
    @app.callback(
        Output("operational-ranking-chart", "figure"),
        Input("store-datos-filtrados", "data"),
        Input("operational-dimension-selector", "value"),
    )
    def callback_actualizar_ranking(data, dimension):
        filtrado = leer_dataframe_filtrado(data)

        if filtrado.empty or not dimension:
            return aplicar_tema_oscuro(go.Figure())

        return crear_figura_ranking(filtrado, dimension)

    @app.callback(
        Output("operational-detail-panel", "children"),
        Input("operational-ranking-chart", "clickData"),
        Input("operational-dimension-selector", "value"),
        Input("store-datos-filtrados", "data"),
    )
    def callback_actualizar_detalle(click_data, dimension, data):
        filtrado = leer_dataframe_filtrado(data)

        if filtrado.empty or not dimension:
            return "Selecciona una dimensión para ver el detalle."

        if not click_data:
            return "Haz clic en una barra del gráfico para ver el detalle de ese grupo."

        valor_seleccionado = click_data["points"][0]["x"]

        return crear_panel_detalle(filtrado, dimension, valor_seleccionado)