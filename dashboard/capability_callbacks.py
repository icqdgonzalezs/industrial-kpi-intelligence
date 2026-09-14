"""Callbacks Dash para el análisis de capacidad de proceso (Pp/Ppk).

Callback delgado: toda la matemática vive en src/capability.py (100%
testeado). Aquí solo se orquesta la lectura de datos, el formato de
presentación y la construcción del gráfico Plotly.

IDs alineados a Pp/Ppk: `capability-pp`, `capability-ppk`,
`capability-ppk-minimo` (sincronizados con dashboard/capability_components.py).

Tipografía de anotaciones calibrada según ISA-101 (HMI industrial):
los labels LSL, USL y Promedio usan 13px y viven ARRIBA del área de
trazado (yref='paper') para no superponerse con las barras del
histograma. Ver _agregar_linea_con_label para la justificación técnica.
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


def _agregar_linea_con_label(
    figura: go.Figure,
    x: float,
    texto: str,
    color_linea: str,
    color_label: str,
) -> None:
    """Agrega una línea vertical + label anclado FUERA del área de trazado.

    El label se ancla con yref='paper' en y=1.02 (2% por encima del borde
    superior del plot) para no superponerse con las barras del histograma.
    add_vline(annotation_text=...) coloca la anotación DENTRO del plot al
    tope de la línea — con distribuciones centradas, ese tope cae sobre
    las barras más altas y el texto se vuelve ilegible.

    Requiere reservar margen superior (t) en update_layout; ver
    crear_figura_capacidad para el valor usado.
    """
    figura.add_vline(
        x=x,
        line={"color": color_linea, "dash": "dash", "width": 1.2},
    )
    figura.add_annotation(
        x=x,
        xref="x",
        y=1.02,
        yref="paper",
        text=texto,
        showarrow=False,
        font={"size": 13, "color": color_label},
        xanchor="center",
        yanchor="bottom",
    )


def crear_figura_capacidad(filtrado: pd.DataFrame, fila: pd.Series) -> go.Figure:
    """Construye el histograma de distribución con límites de especificación.

    Diseño visual (ISA-101 / HMI):
    - Los labels LSL/USL/Promedio viven ARRIBA del área de trazado
      (yref='paper') para no tapar las barras del histograma.
    - Promedio en cian (acento del histograma) para distinguirlo
      visualmente de los límites de especificación (LSL/USL en gris).
    - Se reserva margen superior (t=50) para alojar los 3 labels.
    """
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
    media = float(fila["media"]) if pd.notna(fila["media"]) else None

    _agregar_linea_con_label(
        figura,
        x=lsl,
        texto="LSL",
        color_linea="#8b949e",
        color_label="#8b949e",
    )
    _agregar_linea_con_label(
        figura,
        x=usl,
        texto="USL",
        color_linea="#8b949e",
        color_label="#8b949e",
    )

    if media is not None:
        _agregar_linea_con_label(
            figura,
            x=media,
            texto="Promedio",
            color_linea="#00d4ff",
            color_label="#00d4ff",
        )

    figura.update_layout(
        height=380,
        xaxis_title=str(fila["variable"]),
        yaxis_title="Frecuencia",
        showlegend=False,
        margin={"t": 50, "b": 60, "l": 60, "r": 40},
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