from __future__ import annotations

import plotly.graph_objects as go
from dash import Input, Output

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
    pareto = calcular_pareto(filtrado)

    if pareto.empty:
        return aplicar_tema_oscuro(go.Figure())

    figura = go.Figure()

    figura.add_bar(
        x=pareto["defecto"],
        y=pareto["frecuencia"],
        name="Defectos",
    )

    figura.add_scatter(
        x=pareto["defecto"],
        y=pareto["porcentaje_acumulado"],
        name="% acumulado",
        mode="lines+markers",
        yaxis="y2",
    )

    figura.update_layout(
        title="Pareto de defectos",
        yaxis_title="Unidades defectuosas",
        yaxis2={
            "title": "% acumulado",
            "overlaying": "y",
            "side": "right",
            "range": [0, 100],
        },
    )

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
    """Resume en una frase cuál causa concentra más defectos (para el Div de texto)."""
    if pareto.empty:
        return "Sin defectos en el período seleccionado."

    principal = pareto.iloc[0]

    return (
        f"Causa principal: '{principal['defecto']}' concentra "
        f"{principal['porcentaje']:.1f}% de las unidades defectuosas."
    )


def registrar_callbacks_quality_performance(app) -> None:
    @app.callback(
        Output("quality-fpy", "children"),
        Output("quality-defect-rate", "children"),
        Output("quality-scrap-rate", "children"),
        Output("quality-rework-rate", "children"),
        Output("quality-pareto-chart", "figure"),
        Output("quality-pareto", "children"),
        Output("quality-critical-lot", "children"),
        Input("store-datos-filtrados", "data"),
    )
    def callback_actualizar_quality_performance(data):
        metricas = actualizar_quality_performance(data)

        filtrado = _leer_dataframe_filtrado(data)

        if filtrado.empty:
            return (
                *metricas,
                aplicar_tema_oscuro(go.Figure()),
                "Sin defectos en el período seleccionado.",
                "Sin datos para identificar un lote crítico.",
            )

        pareto = calcular_pareto(filtrado)
        figura_pareto = crear_figura_pareto(filtrado)
        caption_pareto = crear_caption_pareto(pareto)
        lote_critico = crear_lote_critico(filtrado)

        return (
            *metricas,
            figura_pareto,
            caption_pareto,
            lote_critico,
        )
