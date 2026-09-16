"""Callbacks Dash para el análisis de capacidad de proceso (Pp/Ppk).

Callback delgado: toda la matemática vive en src/capability.py (100%
testeado). Aquí solo se orquesta la lectura de datos, el formato de
presentación y la construcción del gráfico Plotly.

Diseño visual (ISA-101 / HMI industrial):
  - Labels LSL/USL/Promedio: blanco (#e6edf3), bold, 16px — legibles a
    1-2 m del monitor.
  - Las 3 líneas de referencia comparten color gris neutro, estilo
    dashed y ancho 1.8px. La diferenciación semántica queda en el
    LABEL y en la POSICIÓN, no en el color.
  - Convención HMI: solo los datos medidos (barras) van en línea sólida.

Clasificación de capacidad (AIAG SPC / NIST 6.1.3 / ISO 22514):
  Ppk >= 1.67 → Clase mundial · 1.33 <= Ppk → Capaz
  1.00 <= Ppk → Marginal     · Ppk < 1.00  → No capaz
Cada mensaje del banner cita el umbral numérico para que el operador
pueda interpretar el dato sin conocer la escala de memoria.

Accesibilidad (WCAG 2.1 §1.4.1):
  Los valores de rendimiento (PPM) se prefijan con un icono Unicode
  (✓ / ⚠ / ✕ / vacío) además del color, para que un operario daltónico
  pueda leer la severidad sin depender del canal cromático. El icono
  se deriva de la severidad CSS (`CSS_CLASS_POR_RENDIMIENTO`), no de
  la clasificación legible, para compartir un único SSOT con los KPI
  del top (ver `dashboard/severity_icons.py`).

Nota técnica sobre bold: Plotly no expone `font.weight` en el schema de
annotations (solo `color`, `family`, `size`). La negrita se logra
envolviendo el texto en `<b>...</b>`.
"""

from __future__ import annotations

import math
from io import StringIO

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, html

from dashboard.severity_icons import prefijar_icono
from dashboard.utils import aplicar_tema_oscuro, leer_dataframe_filtrado
from src.capability import calcular_rendimiento_spec, resumen_capacidad

# ---------------------------------------------------------------------
# Constantes visuales (ISA-101: legibles a 1-2 m de distancia)
# ---------------------------------------------------------------------

COLOR_REFERENCE_LINE = "#8b949e"  # gris neutro para las 3 líneas de referencia
COLOR_LABEL = "#e6edf3"           # blanco primario (mismo que texto del dashboard)
FONT_SIZE_LABEL = 16              # px — mínimo ISA-101 para 1 m
FONT_FAMILY = "Inter, SF Pro Display, Segoe UI, sans-serif"
ANCHO_LINEA_REFERENCIA = 1.8      # px — ISA-101 pide ≥1.5px para dashed a distancia
MARGEN_SUPERIOR_PLOT = 55         # px — espacio para los 3 labels

# Mapeo clasificación de rendimiento → modificador CSS de color
CSS_CLASS_POR_RENDIMIENTO = {
    "world_class": "success",
    "acceptable": "warning",
    "low": "danger",
    "sin_datos": "neutral",
}


# ---------------------------------------------------------------------
# Helpers de formato
# ---------------------------------------------------------------------


def _estado_capacidad(clasificacion: str) -> str:
    """Normaliza la clasificación textual de capability.py a un estado.

    Orden de los checks: 'no capaz' debe evaluarse ANTES de 'capaz'
    porque el primero contiene al segundo como substring.
    """
    texto = str(clasificacion).lower()

    if "clase mundial" in texto:
        return "WORLD_CLASS"
    if "no capaz" in texto:
        return "PRIORITY"
    if "capaz" in texto:
        return "CAPABLE"
    if "marginal" in texto:
        return "WATCH"
    if "insuficientes" in texto or "inválidos" in texto:
        return "NO DATA"
    if "sin variabilidad" in texto:
        return "SPECIAL"
    return "INFO"


def _mensaje_estado(estado: str) -> str:
    """Mensaje del banner. Cada uno cita el umbral numérico para que
    el operador pueda interpretar el dato sin conocer la escala AIAG.
    """
    return {
        "WORLD_CLASS": (
            "El proceso alcanza clase mundial (Ppk ≥ 1.67). "
            "No requiere inspección 100%."
        ),
        "CAPABLE": (
            "El proceso cumple el criterio industrial (Ppk ≥ 1.33). "
            "Para clase mundial se requiere Ppk ≥ 1.67."
        ),
        "WATCH": (
            "El proceso está en zona marginal (1.00 ≤ Ppk < 1.33). "
            "Requiere seguimiento y reducción de variabilidad."
        ),
        "PRIORITY": (
            "El proceso no demuestra capacidad (Ppk < 1.00). "
            "Se recomienda priorizar la investigación."
        ),
        "NO DATA": "No existe información suficiente para evaluar la capacidad.",
        "SPECIAL": (
            "El proceso presenta una condición especial "
            "que requiere interpretación adicional."
        ),
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


def _span_rendimiento(valor: str, clasificacion: str) -> html.Span:
    """Construye el <span> con clase semántica e icono según clasificación PPM.

    El icono es redundancia no cromática (WCAG 2.1 §1.4.1): un operario
    daltónico puede leer la severidad sin depender del color. Se deriva
    del modificador CSS (success/warning/danger/neutral), no de la
    clasificación legible, para compartir el SSOT `severity_icons`.
    """
    modificador = CSS_CLASS_POR_RENDIMIENTO.get(clasificacion, "neutral")
    return html.Span(
        prefijar_icono(valor, modificador),
        className=f"quality-metric-value quality-metric-value--{modificador}",
    )


# ---------------------------------------------------------------------
# Datos y figura
# ---------------------------------------------------------------------


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
) -> None:
    """Agrega una línea vertical de referencia + label estandarizado.

    Las 3 líneas (LSL, USL, Promedio) comparten color gris neutro, estilo
    dashed y ancho 1.8px. La diferenciación entre ellas se hace por el
    LABEL (blanco, bold, arriba del plot) y por la POSICIÓN en el eje X,
    no por color.

    Bold en el label vía HTML `<b>` — Plotly no expone `font.weight` en
    el schema de annotations (solo color, family, size).

    El label se ancla con yref='paper' en y=1.02 para no superponerse
    con las barras del histograma.

    Requiere reservar margen superior (t) en update_layout; ver
    crear_figura_capacidad para el valor usado.
    """
    figura.add_vline(
        x=x,
        line={
            "color": COLOR_REFERENCE_LINE,
            "dash": "dash",
            "width": ANCHO_LINEA_REFERENCIA,
        },
    )
    figura.add_annotation(
        x=x,
        xref="x",
        y=1.02,
        yref="paper",
        text=f"<b>{texto}</b>",
        showarrow=False,
        font={
            "size": FONT_SIZE_LABEL,
            "color": COLOR_LABEL,
            "family": FONT_FAMILY,
        },
        xanchor="center",
        yanchor="bottom",
    )


def crear_figura_capacidad(filtrado: pd.DataFrame, fila: pd.Series) -> go.Figure:
    """Construye el histograma de distribución con límites de especificación.

    Diseño visual (ISA-101 / HMI):
    - Los labels LSL/USL/Promedio viven ARRIBA del área de trazado
      (yref='paper') para no tapar las barras del histograma.
    - Los 3 labels son blancos, bold, 16px — legibles a 1-2 m.
    - Las 3 LÍNEAS de referencia son grises, dashed y de ancho 1.8px.
      La diferenciación entre ellas la hace el label y la posición.
    - Se reserva margen superior (t=55) para alojar los 3 labels.
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

    _agregar_linea_con_label(figura, x=lsl, texto="LSL")
    _agregar_linea_con_label(figura, x=usl, texto="USL")

    if media is not None:
        _agregar_linea_con_label(figura, x=media, texto="Promedio")

    figura.update_layout(
        height=380,
        xaxis_title=str(fila["variable"]),
        yaxis_title="Frecuencia",
        showlegend=False,
        margin={"t": MARGEN_SUPERIOR_PLOT, "b": 60, "l": 60, "r": 40},
    )

    return aplicar_tema_oscuro(figura)


# ---------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------


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
        Output("capability-pct-dentro", "children"),
        Output("capability-pct-bajo-lsl", "children"),
        Output("capability-pct-sobre-usl", "children"),
        Output("capability-ppm-total", "children"),
        Input("store-capacidad", "data"),
        Input("capability-variable-selector", "value"),
        Input("store-datos-filtrados", "data"),
    )
    def callback_actualizar_variable_seleccionada(capacidad_json, columna, data):
        vacio = (
            "Sin datos", "Sin datos", "Sin datos", "Sin datos",
            "Sin datos para evaluar.",
            aplicar_tema_oscuro(go.Figure()), "",
            _span_rendimiento("—", "sin_datos"),
            _span_rendimiento("—", "sin_datos"),
            _span_rendimiento("—", "sin_datos"),
            _span_rendimiento("—", "sin_datos"),
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

        rendimiento = calcular_rendimiento_spec(
            filtrado[columna] if not filtrado.empty else pd.Series([], dtype=float),
            lsl=float(fila["lsl"]),
            usl=float(fila["usl"]),
        )

        clase = rendimiento["clasificacion"]

        return (
            _formatear_indice(fila["pp"]),
            _formatear_indice(fila["ppk"]),
            f"{media:.3f}" if media is not None else "Sin datos",
            f"{sigma:.4f}" if sigma is not None else "Sin datos",
            mensaje,
            figura,
            observaciones,
            _span_rendimiento(f"{rendimiento['pct_dentro']:.2f}%", clase),
            _span_rendimiento(f"{rendimiento['pct_bajo_lsl']:.2f}%", clase),
            _span_rendimiento(f"{rendimiento['pct_sobre_usl']:.2f}%", clase),
            _span_rendimiento(f"{rendimiento['ppm_total']:,}", clase),
        )
