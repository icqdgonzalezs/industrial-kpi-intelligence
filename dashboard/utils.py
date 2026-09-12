"""Utilidades compartidas entre callbacks de Dash.

Centraliza convenciones comunes a todos los callbacks del dashboard:
la deserialización del DataFrame filtrado que viaja a través de
``store-datos-filtrados``, y el tema visual aplicado a cada figura
Plotly.

Tipografía calibrada según ISA-101 (HMI) y guías Siemens/Rockwell para
legibilidad en sala de control: mínimo 14px en ticks, 16px en títulos
de eje, 18px en títulos de gráfico. Legible desde 1m de distancia.
"""

from __future__ import annotations

from io import StringIO

import pandas as pd
import plotly.graph_objects as go

# Paleta compartida con assets/style.css — si cambia una, cambia la otra.
COLOR_FONDO_APP = "#0a0e14"
COLOR_FONDO_TARJETA = "#131820"
COLOR_ACENTO = "#00d4ff"
COLOR_TEXTO = "#e6edf3"
COLOR_TEXTO_TENUE = "#8b949e"
COLOR_GRILLA = "rgba(255,255,255,0.06)"
COLOR_LINEA_CERO = "rgba(255,255,255,0.15)"
COLOR_BORDE_HOVER = "#1f2733"

COLORWAY_INDUSTRIAL = [
    "#00d4ff",
    "#22c55e",
    "#f59e0b",
    "#ef4444",
    "#a78bfa",
    "#14b8a6",
    "#f472b6",
]

FAMILIA_TIPOGRAFICA = "Inter, SF Pro Display, Segoe UI, system-ui, sans-serif"

# ---------------------------------------------------------------------------
# Escala tipográfica industrial (ISA-101 / Siemens HMI guidelines)
# ---------------------------------------------------------------------------
FONT_SIZE_BASE = 14       # Texto general
FONT_SIZE_TICK = 14       # Números en los ejes (lectura desde 1m)
FONT_SIZE_AXIS_TITLE = 16 # Títulos de eje ("Unidades defectuosas", "Peso"...)
FONT_SIZE_CHART_TITLE = 18 # Título del gráfico
FONT_SIZE_LEGEND = 14     # Leyenda
FONT_SIZE_HOVER = 15      # Tooltip al pasar el mouse
FONT_SIZE_ANNOTATION = 14 # Anotaciones (LSL, USL, CL, UCL, etc.)


def leer_dataframe_filtrado(data: str | None) -> pd.DataFrame:
    """Deserializa el DataFrame filtrado almacenado en ``dcc.Store``."""
    if not data:
        return pd.DataFrame()

    return pd.read_json(StringIO(data), orient="split")


def aplicar_tema_oscuro(figura: go.Figure) -> go.Figure:
    """Aplica el tema oscuro industrial compartido a una figura Plotly, in-place.

    Tipografía calibrada para sala de control: legible desde 1m de distancia,
    consistente con guías ISA-101 y HMI de Siemens/Rockwell.
    """
    figura.update_layout(
        paper_bgcolor=COLOR_FONDO_TARJETA,
        plot_bgcolor=COLOR_FONDO_TARJETA,
        colorway=COLORWAY_INDUSTRIAL,
        font={
            "color": COLOR_TEXTO,
            "family": FAMILIA_TIPOGRAFICA,
            "size": FONT_SIZE_BASE,
        },
        title={
            "font": {"color": COLOR_TEXTO, "size": FONT_SIZE_CHART_TITLE},
            "x": 0.02,
            "xanchor": "left",
        },
        legend={
            "bgcolor": "rgba(0,0,0,0)",
            "font": {"color": COLOR_TEXTO, "size": FONT_SIZE_LEGEND},
        },
        hoverlabel={
            "bgcolor": COLOR_FONDO_TARJETA,
            "bordercolor": COLOR_BORDE_HOVER,
            "font": {"color": COLOR_TEXTO, "size": FONT_SIZE_HOVER},
        },
        modebar={
            "bgcolor": "rgba(0,0,0,0)",
            "color": COLOR_TEXTO_TENUE,
            "activecolor": COLOR_ACENTO,
        },
        margin={"r": 24, "t": 64, "b": 72, "l": 88},
        autosize=True,
    )

    figura.update_xaxes(
        gridcolor=COLOR_GRILLA,
        zerolinecolor=COLOR_LINEA_CERO,
        linecolor=COLOR_BORDE_HOVER,
        tickfont={"color": COLOR_TEXTO_TENUE, "size": FONT_SIZE_TICK},
        title_font={"color": COLOR_TEXTO, "size": FONT_SIZE_AXIS_TITLE},
    )
    figura.update_yaxes(
        gridcolor=COLOR_GRILLA,
        zerolinecolor=COLOR_LINEA_CERO,
        linecolor=COLOR_BORDE_HOVER,
        tickfont={"color": COLOR_TEXTO_TENUE, "size": FONT_SIZE_TICK},
        title_font={"color": COLOR_TEXTO, "size": FONT_SIZE_AXIS_TITLE},
    )

    return figura