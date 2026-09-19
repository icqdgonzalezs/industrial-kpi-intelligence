"""Callbacks de la carta de control I-MR.

Toda la matemática vive en src/control_charts.py. Este módulo solo
orquesta la lectura de datos y la construcción de las figuras Plotly.

Tipografía de anotaciones calibrada según ISA-101 (HMI industrial):
CL, UCL, LCL y MR-bar usan 14px para ser legibles desde 1m de distancia.
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State

from dashboard.export_helpers import crear_descarga_csv
from dashboard.utils import aplicar_tema_oscuro, leer_dataframe_filtrado
from src.control_charts import (
    calcular_limites_control,
    calcular_moving_range,
    detectar_fuera_de_control,
    resumen_control_estadistico,
)

COLOR_OOC = "#ef4444"
COLOR_NORMAL = "#e6edf3"

# Constante Shewhart para carta MR (d2 = 1.128, factor UCL = 3.267).
# Ver src/control_charts.py para la derivación.
FACTOR_UCL_MR = 3.267


def crear_figura_i(serie, limites, fuera_control) -> go.Figure:
    colores = [COLOR_OOC if f else COLOR_NORMAL for f in fuera_control]
    figura = go.Figure(
        go.Scattergl(
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
    ucl_mr = mr_bar * FACTOR_UCL_MR
    figura = go.Figure(
        go.Scattergl(
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


def exportar_control_csv(data, columna):
    """Construye la descarga CSV del análisis I-MR.

    Función pura (sin Dash): recibe el JSON del store de datos filtrados
    y la columna seleccionada, devuelve el dict de descarga, o None si
    no hay nada que exportar.

    Estructura del CSV: una fila por observación de la serie I, con MR
    alineado (primera fila vacía — no hay punto previo). Las constantes
    del análisis (CL, UCL, LCL, MR-bar, UCL_MR) se repiten como columnas
    para que el CSV sea autocontenido y parseable en pandas/Excel.

    Parameters
    ----------
    data : str | None
        JSON orient='split' del DataFrame filtrado (store-datos-filtrados).
    columna : str | None
        Nombre de la columna (variable) seleccionada en el dropdown.

    Returns
    -------
    dict | None
        Dict {content, filename} listo para Output de dcc.Download,
        o None si el filtrado está vacío, la columna no existe o la
        serie tiene menos de 2 puntos.
    """
    filtrado = leer_dataframe_filtrado(data)

    if filtrado.empty or not columna or columna not in filtrado.columns:
        return None

    serie = filtrado[columna].dropna().reset_index(drop=True)

    if len(serie) < 2:
        return None

    limites = calcular_limites_control(serie)
    fuera_control = detectar_fuera_de_control(serie, limites)
    mr = calcular_moving_range(serie).dropna().reset_index(drop=True)

    # MR tiene N-1 elementos; alinear con serie I (N elementos) con
    # None en la primera fila — no hay rango móvil para el punto 0.
    mr_alineado = [None, *[float(v) for v in mr]]

    df_export = pd.DataFrame(
        {
            "indice": list(range(len(serie))),
            "valor": [float(v) for v in serie],
            "fuera_control": [bool(f) for f in fuera_control],
            "moving_range": mr_alineado,
            "cl": float(limites["media"]),
            "ucl": float(limites["ucl"]),
            "lcl": float(limites["lcl"]),
            "mr_bar": float(limites["mr_bar"]),
            "ucl_mr": float(limites["mr_bar"] * FACTOR_UCL_MR),
        }
    )

    json_data = df_export.to_json(orient="split", date_format="iso")
    return crear_descarga_csv(json_data, "control")


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
        vacio = (
            "Sin datos.",
            aplicar_tema_oscuro(go.Figure()),
            aplicar_tema_oscuro(go.Figure()),
        )

        if filtrado.empty or not columna or columna not in filtrado.columns:
            return vacio

        serie = filtrado[columna].dropna().reset_index(drop=True)
        if len(serie) < 2:
            return vacio

        limites = calcular_limites_control(serie)
        fuera_control = detectar_fuera_de_control(serie, limites)
        mr = calcular_moving_range(serie).dropna().reset_index(drop=True)

        estado = resumen_control_estadistico(serie, limites)["mensaje"]

        return (
            estado,
            crear_figura_i(serie, limites, fuera_control),
            crear_figura_mr(mr, limites["mr_bar"]),
        )

    @app.callback(
        Output("download-control", "data"),
        Input("btn-export-control", "n_clicks"),
        State("control-variable-selector", "value"),
        State("store-datos-filtrados", "data"),
        prevent_initial_call=True,
    )
    def callback_export_control(n_clicks, columna, data):
        if not n_clicks:
            return None
        return exportar_control_csv(data, columna)