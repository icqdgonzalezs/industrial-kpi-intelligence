"""Callbacks de la carta de control I-MR.

Toda la matemática vive en src/control_charts.py. Este módulo solo
orquesta la lectura de datos y la construcción de las figuras Plotly.

Tipografía de anotaciones calibrada según ISA-101 (HMI industrial):
CL, UCL, LCL y MR-bar usan 14px para ser legibles desde 1m de distancia.
"""

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
COLOR_NORMAL = "#e6edf3"


def crear_figura_i(serie, limites, fuera_control) -> go.Figure:
    colores = [COLOR_OOC if f else COLOR_NORMAL for f in fuera_control]
    figura = go.Figure(
        go.Scatter(
            x=list(range(len(serie))),
            y=serie,
            mode="lines+markers",
            line={"color": "#00d4ff", "width": 1.5},
            marker={"size": 5, "color": colores},
        )
    )
    figura.add_hline(
        y=limites["media"],
        line={"color": "#8b949e", "dash": "dot"},
        annotation_text="CL",
        annotation_font_size=14,
        annotation_font_color="#e6edf3",
    )
    figura.add_hline(
        y=limites["ucl"],
        line={"color": "#ef4444", "dash": "dash", "width": 1},
        annotation_text="UCL",
        annotation_font_size=14,
        annotation_font_color="#e6edf3",
    )
    figura.add_hline(
        y=limites["lcl"],
        line={"color": "#ef4444", "dash": "dash", "width": 1},
        annotation_text="LCL",
        annotation_font_size=14,
        annotation_font_color="#e6edf3",
    )
    figura.update_layout(title="Carta I (Individuals)", yaxis_title="Valor")
    return aplicar_tema_oscuro(figura)


def crear_figura_mr(mr, mr_bar) -> go.Figure:
    ucl_mr = mr_bar * 3.267
    figura = go.Figure(
        go.Scatter(
            x=list(range(len(mr))),
            y=mr,
            mode="lines+markers",
            line={"color": "#00d4ff", "width": 1.5},
            marker={"size": 5, "color": "#e6edf3"},
        )
    )
    figura.add_hline(
        y=mr_bar,
        line={"color": "#8b949e", "dash": "dot"},
        annotation_text="MR-bar",
        annotation_font_size=14,
        annotation_font_color="#e6edf3",
    )
    figura.add_hline(
        y=ucl_mr,
        line={"color": "#ef4444", "dash": "dash", "width": 1},
        annotation_text="UCL",
        annotation_font_size=14,
        annotation_font_color="#e6edf3",
    )
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