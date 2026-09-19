"""Callbacks Dash de la pestaña Calidad.

Diagrama de Pareto con eje dual (magnitud + acumulado) calibrado a
estándares de HMI industrial (ISA-101):
  - Barras cian (magnitud) + línea ámbar (acumulado): contraste por
    temperatura, no solo por tono.
  - Marcadores diamante con borde oscuro: señal de "punto relevante".
  - Línea punteada al 80%: regla clásica de Pareto (Quality Manager).
  - Eje secundario fijo 0-105%: escala consistente entre filtros.
  - Anotaciones y ticks a 14px: legibles desde 1m de distancia.

Fase 3b.2: cuando el filtro deja 0 filas, se oculta el contenido normal
y se muestra un empty_state() en su lugar. Los IDs internos no cambian
— los tests de contrato siguen válidos, solo se agregaron 2 outputs.
"""

from __future__ import annotations

import plotly.graph_objects as go
from dash import Input, Output, State

from dashboard.empty_state import empty_state
from dashboard.export_helpers import crear_descarga_csv
from dashboard.kpi_presenter import formatear_kpis
from dashboard.utils import aplicar_tema_oscuro
from dashboard.utils import leer_dataframe_filtrado as _leer_dataframe_filtrado
from src.kpis import (
    calcular_kpis_globales,
    calcular_pareto,
    identificar_lote_critico,
)


def actualizar_quality_performance(data):
    filtrado = _leer_dataframe_filtrado(data)

    if filtrado.empty:
        return "—", "—", "—", "—"

    kpis = calcular_kpis_globales(filtrado)
    presentados = formatear_kpis(kpis)

    return (
        presentados["fpy"],
        presentados["defectos"],
        presentados["scrap"],
        presentados["reproceso"],
    )


def crear_figura_pareto(filtrado):
    """Diagrama de Pareto profesional (magnitud individual + % acumulado)."""
    pareto = calcular_pareto(filtrado)

    if pareto.empty:
        return aplicar_tema_oscuro(go.Figure())

    figura = go.Figure()

    # -----------------------------------------------------------------
    # Barras — magnitud individual (frecuencia de cada causa)
    # -----------------------------------------------------------------
    figura.add_bar(
        x=pareto["defecto"],
        y=pareto["frecuencia"],
        name="Unidades defectuosas",
        marker={
            "color": "#00d4ff",
            "line": {"color": "#38bdf8", "width": 0.5},
        },
        hovertemplate="<b>%{x}</b><br>%{y:,.0f} unidades<extra></extra>",
        yaxis="y",
    )

    # -----------------------------------------------------------------
    # Línea acumulada — ámbar para contraste por temperatura
    # -----------------------------------------------------------------
    figura.add_scatter(
        x=pareto["defecto"],
        y=pareto["porcentaje_acumulado"],
        name="% acumulado",
        mode="lines+markers",
        line={"color": "#fbbf24", "width": 2.5, "shape": "linear"},
        marker={
            "color": "#fbbf24",
            "size": 9,
            "symbol": "diamond",
            "line": {"color": "#0a0e14", "width": 1.5},
        },
        hovertemplate="<b>%{x}</b><br>Acumulado: %{y:.1f}%<extra></extra>",
        yaxis="y2",
    )

    # -----------------------------------------------------------------
    # Línea de referencia al 80% (regla clásica de Pareto)
    # Anotación a 14px para legibilidad industrial.
    # annotation_position="top right" eleva el texto sobre la línea
    # para no colisionar con el tick "80%" del eje secundario.
    # -----------------------------------------------------------------
    figura.add_hline(
        y=80,
        line={"color": "#fbbf24", "width": 1, "dash": "dot"},
        opacity=0.6,
        yref="y2",
        annotation_text="Umbral 80%",
        annotation_position="top right",
        annotation_font_size=14,
        annotation_font_color="#fbbf24",
    )

    # -----------------------------------------------------------------
    # Layout general
    # -----------------------------------------------------------------
    figura.update_layout(
        title={
            "text": "Pareto de defectos — concentración de causas",
            "font": {"size": 18, "color": "#e6edf3"},
            "x": 0.02,
            "xanchor": "left",
        },
        bargap=0.35,
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "font": {"size": 14, "color": "#e6edf3"},
            "bgcolor": "rgba(0,0,0,0)",
        },
        hovermode="x unified",
        yaxis_title="Unidades defectuosas",
        yaxis2={
            "title": "% acumulado",
            "overlaying": "y",
            "side": "right",
            "range": [0, 105],
            "showgrid": False,
            "zeroline": False,
            "ticksuffix": "%",
        },
    )

    # Sin grid vertical en el eje X (menos ruido visual)
    figura.update_xaxes(showgrid=False)

    return aplicar_tema_oscuro(figura)


def crear_lote_critico(filtrado):
    if filtrado.empty:
        return "Sin datos para identificar un lote crítico."

    lote_critico = identificar_lote_critico(filtrado)

    return (
        f"Lote crítico: {lote_critico['lote']} "
        f"· Tasa de defectos: "
        f"{lote_critico['tasa_defectos_lote']:.1%}"
    )


def crear_caption_pareto(pareto) -> str:
    """Resume en una frase cuál causa concentra más defectos."""
    if pareto.empty:
        return "Sin defectos en el período seleccionado."

    principal = pareto.iloc[0]

    return (
        f"Causa principal: '{principal['defecto']}' concentra "
        f"{principal['porcentaje']:.1f}% de las unidades defectuosas."
    )


def construir_outputs_calidad(data) -> tuple:
    """Función pura: produce la tupla de 9 outputs del callback principal.

    Orden de outputs (contrato fijo):
        0-3:  4 métricas (FPY, defectos, scrap, reproceso)
        4:    figura del Pareto (go.Figure)
        5:    caption del Pareto (str)
        6:    lote crítico (str)
        7:    style del contenedor normal (dict) — display block/none
        8:    children del contenedor vacío (list[html.Component])

    Cuando el filtro deja 0 filas, el contenedor normal se oculta y el
    vacío muestra un empty_state() con el mensaje del dominio. Los ids
    de los 4 KPIs y el chart siguen existiendo — solo quedan ocultos.

    Extraída del callback para testear el contrato sin instanciar Dash.
    """
    metricas = actualizar_quality_performance(data)
    filtrado = _leer_dataframe_filtrado(data)

    if filtrado.empty:
        return (
            *metricas,
            aplicar_tema_oscuro(go.Figure()),
            "",
            "",
            {"display": "none"},
            empty_state(
                "Sin datos de calidad con los filtros actuales",
                hint="Ajustá los filtros o tocá 'Restaurar filtros'.",
            ),
        )

    pareto = calcular_pareto(filtrado)

    return (
        *metricas,
        crear_figura_pareto(filtrado),
        crear_caption_pareto(pareto),
        crear_lote_critico(filtrado),
        {"display": "block"},
        [],
    )


def exportar_pareto_calidad(data):
    """Construye la descarga CSV del Pareto de defectos de Calidad.

    Función pura (sin Dash): recibe el JSON del store de datos
    filtrados y devuelve el dict de descarga, o None si no hay
    nada que exportar.
    """
    filtrado = _leer_dataframe_filtrado(data)

    if filtrado.empty:
        return None

    pareto = calcular_pareto(filtrado)

    if pareto.empty:
        return None

    json_data = pareto.to_json(orient="split", date_format="iso")
    return crear_descarga_csv(json_data, "calidad")


def registrar_callbacks_quality_performance(app) -> None:
    @app.callback(
        Output("quality-fpy", "children"),
        Output("quality-defect-rate", "children"),
        Output("quality-scrap-rate", "children"),
        Output("quality-rework-rate", "children"),
        Output("quality-pareto-chart", "figure"),
        Output("quality-pareto", "children"),
        Output("quality-critical-lot", "children"),
        Output("quality-normal-content", "style"),
        Output("quality-empty-content", "children"),
        Input("store-datos-filtrados", "data"),
    )
    def callback_actualizar_quality_performance(data):
        return construir_outputs_calidad(data)

    @app.callback(
        Output("download-calidad", "data"),
        Input("btn-export-calidad", "n_clicks"),
        State("store-datos-filtrados", "data"),
        prevent_initial_call=True,
    )
    def callback_export_calidad(n_clicks, data):
        if not n_clicks:
            return None
        return exportar_pareto_calidad(data)
