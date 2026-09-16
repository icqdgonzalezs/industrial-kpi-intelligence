"""Callbacks Dash del análisis operacional comparativo (drill-down).

La agregación por dimensión y el Pareto ya existen en src/kpis.py
(100% testeado). Este módulo reutiliza los umbrales de hotspot de
src/diagnostics.py para que el color del ranking sea consistente con
el motor de diagnóstico — una sola fuente de verdad para "qué es
prioritario".

Barras horizontales según ISA-101: los nombres de equipo/turno/operador
se leen sin rotación, incluso con 17+ categorías. Altura dinámica para
mantener legibilidad a 1-2 m. La peor categoría (mayor tasa de defectos)
queda arriba, primera lectura.

Etiquetas numéricas visibles sin interacción (ISA-101: los datos medidos
deben ser legibles a 1-2 m sin requerir hover). La jerarquía se comunica
por tres canales redundantes —posición (peor arriba), color semántico
(rojo/ámbar/verde por umbral de hotspot) y valor absoluto visible— sin
recurrir a decoraciones adicionales que rompan la consistencia visual.

El callback de clickData se resetea al cambiar de dimensión: sin esto,
Plotly retiene el valor clickeado anterior y el panel de detalle muestra
"Sin datos" sin que el usuario haya interactuado con la nueva dimensión.

Nombres de ejes y títulos de panel delegados a LABELS_EJES_DIMENSION
(SSOT en operational_analysis_components) vía _label_dimension(). Evita
str.capitalize() que producía "Maquina" sin tilde en el eje Y de la
dimensión "Tipo de máquina".
"""

from __future__ import annotations

import plotly.graph_objects as go
from dash import Input, Output, html

from dashboard.operational_analysis_components import LABELS_EJES_DIMENSION
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
COLOR_REFERENCIA = "#8b949e"

ALTURA_POR_CATEGORIA_PX = 35
ALTURA_MARGEN_PX = 120
ALTURA_MINIMA_PX = 300


def _color_por_ratio(ratio: float) -> str:
    """Asigna color según el mismo umbral que usa el motor de diagnóstico."""
    if ratio >= UMBRAL_HOTSPOT_PRIORITY:
        return COLOR_PRIORITY
    if ratio >= UMBRAL_HOTSPOT_WATCH:
        return COLOR_WATCH
    return COLOR_NORMAL


def _label_dimension(dimension: str) -> str:
    """Nombre visible de una dimensión (con tilde, con nombre largo).

    Centraliza el lookup para que eje Y y panel de detalle usen el mismo
    texto. Fallback a str.capitalize() ante dimensiones no registradas
    en DIMENSIONES_DISPONIBLES — robustez por si el dataset incorpora
    una columna nueva antes que la lista de labels.
    """
    return LABELS_EJES_DIMENSION.get(dimension, dimension.capitalize())


def _extraer_valor_seleccionado(click_data: dict | None) -> str | None:
    """Extrae la categoría clickeada desde clickData de Plotly.

    Con orientation='h', Plotly reporta la categoría en 'y'. Esta función
    aísla el contrato del callback para que un cambio futuro de orientación
    no rompa el drill-down de forma silenciosa.
    """
    if not click_data or "points" not in click_data:
        return None
    puntos = click_data["points"]
    if not puntos:
        return None
    return str(puntos[0]["y"])


def _calcular_altura(n_categorias: int) -> int:
    """Altura dinámica: 35px por categoría + margen, mínimo 300px."""
    return max(ALTURA_MINIMA_PX, ALTURA_POR_CATEGORIA_PX * n_categorias + ALTURA_MARGEN_PX)


def crear_figura_ranking(filtrado, dimension: str) -> go.Figure:
    """Construye el ranking comparativo (barras horizontales) por dimensión."""
    if filtrado is None or filtrado.empty:
        return aplicar_tema_oscuro(go.Figure())

    por_dimension = calcular_kpis_por_dimension(filtrado, dimension)

    if por_dimension.empty:
        return aplicar_tema_oscuro(go.Figure())

    # Ascendente: con orientation='h', Plotly dibuja el primer valor abajo.
    # El peor (mayor tasa) queda arriba, primera lectura del operador.
    por_dimension = por_dimension.sort_values(
        "tasa_defectos", ascending=True
    ).reset_index(drop=True)

    promedio_planta = calcular_kpis_globales(filtrado)["tasa_defectos"]

    ratios = (
        por_dimension["tasa_defectos"] / promedio_planta
        if promedio_planta > 0
        else por_dimension["tasa_defectos"] * 0
    )
    colores = [_color_por_ratio(r) for r in ratios]
    valores_pct = (por_dimension["tasa_defectos"] * 100).tolist()

    figura = go.Figure(
        go.Bar(
            x=valores_pct,
            y=por_dimension[dimension].astype(str),
            orientation="h",
            marker_color=colores,
            text=[f"{v:.2f}%" for v in valores_pct],
            textposition="outside",
            textfont=dict(size=12, color="#e6edf3"),
            cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>Tasa de defectos: %{x:.2f}%<extra></extra>",
        )
    )

    figura.add_vline(
        x=promedio_planta * 100,
        line_dash="dash",
        line_color=COLOR_REFERENCIA,
        line_width=1.8,
        annotation_text="Promedio de planta",
        annotation_position="top",
        annotation_font_size=14,
        annotation_font_color="#e6edf3",
    )

    figura.update_layout(
        xaxis_title="Tasa de defectos (%)",
        yaxis_title=_label_dimension(dimension),
        showlegend=False,
        height=_calcular_altura(len(por_dimension)),
        margin=dict(l=180, r=80, t=60, b=60),
        bargap=0.25,
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
                f"{_label_dimension(dimension)}: {valor_seleccionado}",
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
        Output("operational-ranking-chart", "clickData"),
        Input("operational-dimension-selector", "value"),
        prevent_initial_call=True,
    )
    def callback_reset_click_al_cambiar_dimension(_dimension):
        """Resetea la selección al cambiar de dimensión.

        Sin esto, clickData retiene el valor de la dimensión anterior
        (ej: 'EQ-A' tras pasar a 'Turno') y el panel muestra "Sin datos"
        sin que el usuario haya clickeado nada en la nueva dimensión.
        """
        return None

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

        valor_seleccionado = _extraer_valor_seleccionado(click_data)

        if valor_seleccionado is None:
            return "Haz clic en una barra del gráfico para ver el detalle de ese grupo."

        return crear_panel_detalle(filtrado, dimension, valor_seleccionado)