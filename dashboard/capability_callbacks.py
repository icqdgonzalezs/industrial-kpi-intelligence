"""Callbacks Dash para el análisis de capacidad de proceso (Pp/Ppk).

Callback delgado: toda la matemática vive en src/capability.py (100%
testeado). Aquí solo se orquesta la lectura de datos, el formato de
presentación y la construcción del gráfico Plotly.

IDs alineados a Pp/Ppk: `capability-pp`, `capability-ppk`,
`capability-ppk-minimo` (sincronizados con dashboard/capability_components.py).

Tipografía de anotaciones calibrada según ISA-101 (HMI industrial):
LSL, USL y Promedio usan 14px para ser legibles desde 1m de distancia.
"""

from __future__ import annotations

import math
from io import StringIO

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output

from dashboard.utils import aplicar_tema_oscuro, leer_dataframe_filtrado
from src.capability import resumen_capacidad


def _estado_capacidad(clasificacion: str) -> str:
    """Normaliza la clasificación textual de capability.py a un estado."""
    texto = str(clasificacion).lower()

    if "excelente" in texto:
        return "EXCELLENT"
    if "capaz" in texto and "no capaz" not in texto:
        return "CAPABLE"
    if "marginal" in texto:
        return "WATCH"
    if "no capaz" in texto:
        return "PRIORITY"
    if "insuficientes" in texto or "inválidos" in texto:
        return "NO DATA"
    if "sin variabilidad" in texto:
        return "SPECIAL"
    return "INFO"


def _mensaje_estado(estado: str) -> str:
    return {
        "EXCELLENT": "El proceso presenta una capacidad robusta respecto de las especificaciones.",
        "CAPABLE": "El proceso cumple el criterio de capacidad establecido para Ppk.",
        "WATCH": "El proceso requiere seguimiento para reducir el riesgo de incumplimiento.",
        "PRIORITY": "El proceso no demuestra capacidad suficiente. Se recomienda priorizar la investigación.",
        "NO DATA": "No existe información suficiente para evaluar la capacidad.",
        "SPECIAL": "El proceso presenta una condición especial que requiere interpretación adicional.",
        "INFO": "Revisar los indicadores estadísticos disponibles.",
    }.get(estado, "Revisar los indicadores estadísticos.")


def _formatear_indice(valor) -> str:
    """Formatea Pp/Ppk incluyendo valores infinitos."""
    if valor is None:
        return "Sin datos"

    try:
        valor_float = float(valor)
    except (TypeError, ValueError):
        return "Sin datos"

    if pd.isna(valor_float):
        return "Sin datos"

    if math.isinf(valor_float):
        return "∞"

    return f"{valor_float:.2f}"


def calcular_resumen_capacidad(data, variables_config: dict) -> pd.DataFrame:
    """Calcula Pp/Ppk para el universo filtrado actual."""
    filtrado = leer_dataframe_filtrado(data)

    if filtrado.empty:
        return pd.DataFrame()

    return resumen_capacidad(filtrado, variables_config)


def crear_figura_capacidad(filtrado: pd.DataFrame, fila: pd.Series) -> go.Figure:
    """Construye el histograma de distribución con límites de especificación."""
    columna = str(fila["columna"])
    serie = pd.to_numeric(filtrado[columna], errors="coerce").dropna()

    figura = go.Figure()

    if len(serie) < 2:
        return figura

    figura.add_trace(
        go.Histogram(
            x=serie,
            nbinsx=24,
            name="Observaciones",
            opacity=0.85,
            marker={
                "color": "#00d4ff",
                "line": {"color": "#38bdf8", "width": 1},
            },
        )
    )

    lsl = float(fila["lsl"])
    usl = float(fila["usl"])

    figura.add_vline(
        x=lsl,
        line_dash="dash",
        annotation_text="LSL",
        annotation_font_size=14,
        annotation_font_color="#e6edf3",
    )
    figura.add_vline(
        x=usl,
        line_dash="dash",
        annotation_text="USL",
        annotation_font_size=14,
        annotation_font_color="#e6edf3",
    )

    media = float(fila["media"]) if pd.notna(fila["media"]) else None
    if media is not None:
        figura.add_vline(
            x=media,
            annotation_text="Promedio",
            annotation_font_size=14,
            annotation_font_color="#e6edf3",
        )

    figura.update_layout(
        height=380,
        xaxis_title=str(fila["variable"]),
        yaxis_title="Frecuencia",
        showlegend=False,
    )

    return aplicar_tema_oscuro(figura)


def registrar_callbacks_capability(app, variables_config: dict) -> None:
    @app.callback(
        Output("store-capacidad", "data"),
        Output("capability-total-variables", "children"),
        Output("capability-ppk-minimo", "children"),
        Output("capability-marginales", "children"),
        Output("capability-no-capaces", "children"),
        Input("store-datos-filtrados", "data"),
    )
    def callback_actualizar_resumen_capacidad(data):
        capacidad = calcular_resumen_capacidad(data, variables_config)

        if capacidad.empty:
            return None, "0", "Sin datos", "0", "0"

        ppk = pd.to_numeric(capacidad["ppk"], errors="coerce").dropna()
        ppk_min = float(ppk.min()) if not ppk.empty else None

        marginales = int(
            capacidad["clasificacion"]
            .astype(str)
            .str.contains("Marginal", case=False, na=False)
            .sum()
        )
        no_capaces = int(
            capacidad["clasificacion"]
            .astype(str)
            .str.contains("No capaz", case=False, na=False)
            .sum()
        )

        return (
            capacidad.to_json(orient="split"),
            str(len(capacidad)),
            _formatear_indice(ppk_min),
            str(marginales),
            str(no_capaces),
        )

    @app.callback(
        Output("capability-pp", "children"),
        Output("capability-ppk", "children"),
        Output("capability-media", "children"),
        Output("capability-sigma", "children"),
        Output("capability-estado", "children"),
        Output("capability-grafico", "figure"),
        Output("capability-observaciones", "children"),
        Input("store-capacidad", "data"),
        Input("capability-variable-selector", "value"),
        Input("store-datos-filtrados", "data"),
    )
    def callback_actualizar_variable_seleccionada(capacidad_json, columna, data):
        vacio = (
            "Sin datos", "Sin datos", "Sin datos", "Sin datos",
            "Sin datos para evaluar.",
            aplicar_tema_oscuro(go.Figure()), "",
        )

        if not capacidad_json or not columna:
            return vacio

        capacidad = pd.read_json(StringIO(capacidad_json), orient="split")
        filas = capacidad[capacidad["columna"] == columna]

        if filas.empty:
            return vacio

        fila = filas.iloc[0]

        media = float(fila["media"]) if pd.notna(fila["media"]) else None
        sigma = float(fila["sigma"]) if pd.notna(fila["sigma"]) else None

        estado = _estado_capacidad(str(fila["clasificacion"]))
        mensaje = f"{fila['clasificacion']} · {_mensaje_estado(estado)}"

        filtrado = leer_dataframe_filtrado(data)
        figura = go.Figure() if filtrado.empty else crear_figura_capacidad(filtrado, fila)

        n = int(fila["n"]) if pd.notna(fila["n"]) else 0
        observaciones = f"{n:,} observaciones utilizadas en el cálculo."

        return (
            _formatear_indice(fila["pp"]),
            _formatear_indice(fila["ppk"]),
            f"{media:.3f}" if media is not None else "Sin datos",
            f"{sigma:.4f}" if sigma is not None else "Sin datos",
            mensaje,
            figura,
            observaciones,
        )