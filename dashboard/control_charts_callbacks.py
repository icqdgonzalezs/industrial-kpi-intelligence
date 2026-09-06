"""Callbacks de la carta de control I-MR. Toda la matemática vive en src/control_charts.py."""

from __future__ import annotations

import plotly.graph_objects as go
from dash import Input, Output

from dashboard.utils import aplicar_tema_oscuro, leer_dataframe_filtrado
from src.control_charts import (
    calcular_limites_control,
    calcular_moving_range,
    detectar_fuera_de_control,
)

COLOR_OOC = "#ef4444"
COLOR_NORMAL = "#38bdf8"


def crear_figura_i(serie, limites, fuera_control) -> go.Figure:
    colores = [COLOR_OOC if f else COLOR_NORMAL for f in fuera_control]
    figura = go.Figure(go.Scatter(x=list(range(len(serie))), y=serie, mode="lines+markers", marker_color=colores))
    figura.add_hline(y=limites["media"], line_color="#94a3b8", annotation_text="CL")
    figura.add_hline(y=limites["ucl"], line_dash="dash", annotation_text="UCL")
    figura.add_hline(y=limites["lcl"], line_dash="dash", annotation_text="LCL")
    figura.update_layout(title="Carta I (Individuals)", yaxis_title="Valor")
    return aplicar_tema_oscuro(figura)


def crear_figura_mr(mr, mr_bar) -> go.Figure:
    ucl_mr = mr_bar * 3.267
    figura = go.Figure(go.Scatter(x=list(range(len(mr))), y=mr, mode="lines+markers"))
    figura.add_hline(y=mr_bar, line_color="#94a3b8", annotation_text="MR-bar")
    figura.add_hline(y=ucl_mr, line_dash="dash", annotation_text="UCL")
    figura.update_layout(title="Carta MR (Rango Móvil)", yaxis_title="Rango móvil")
    return aplicar_tema_oscuro(figura)


def registrar_callbacks_control_charts(app) -> None:
    @app.callback(
        Output("control-status", "children"),
        Output("control-chart-i", "figure"),
        Output("control-chart-mr", "figure"),
        Input("store-datos-filtrados", "data"),
        Input("control-variable-selector", "value"),
    )
    def callback_actualizar_control(data, columna):
        filtrado = leer_dataframe_filtrado(data)
        vacio = ("Sin datos.", aplicar_tema_oscuro(go.Figure()), aplicar_tema_oscuro(go.Figure()))

        if filtrado.empty or not columna or columna not in filtrado.columns:
            return vacio

        serie = filtrado[columna].dropna().reset_index(drop=True)
        if len(serie) < 2:
            return vacio

        limites = calcular_limites_control(serie)
        fuera_control = detectar_fuera_de_control(serie, limites)
        mr = calcular_moving_range(serie).dropna().reset_index(drop=True)

        n_fuera = int(fuera_control.sum())
        estado = (
            f"{n_fuera} punto(s) fuera de control (Regla Western Electric #1)."
            if n_fuera
            else "Proceso en control estadístico — sin puntos fuera de límites."
        )

        return (
            estado,
            crear_figura_i(serie, limites, fuera_control),
            crear_figura_mr(mr, limites["mr_bar"]),
        )
