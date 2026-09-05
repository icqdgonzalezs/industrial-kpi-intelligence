"""Utilidades compartidas entre callbacks de Dash.

Centraliza convenciones comunes a todos los callbacks del dashboard:
la deserialización del DataFrame filtrado que viaja a través de
``store-datos-filtrados``, y el tema visual aplicado a cada figura
Plotly (una sola fuente de verdad para que todos los gráficos se vean
consistentes con assets/style.css).
"""

from __future__ import annotations

from io import StringIO

import pandas as pd
import plotly.graph_objects as go

# Paleta compartida con assets/style.css — si cambia una, cambia la otra.
COLOR_FONDO_TARJETA = "#1e293b"
COLOR_TEXTO = "#e2e8f0"
COLOR_GRILLA = "#334155"
COLOR_ACENTO = "#38bdf8"


def leer_dataframe_filtrado(data: str | None) -> pd.DataFrame:
    """Deserializa el DataFrame filtrado almacenado en ``dcc.Store``.

    Convención compartida: los datos filtrados viajan como JSON
    (orient="split") a través de ``store-datos-filtrados``.
    """
    if not data:
        return pd.DataFrame()

    return pd.read_json(StringIO(data), orient="split")


def aplicar_tema_oscuro(figura: go.Figure) -> go.Figure:
    """Aplica el tema oscuro compartido a una figura Plotly, in-place.

    Se llama al final de cada función ``crear_figura_*`` para que todos
    los gráficos del dashboard (Pareto, capacidad, ranking operacional)
    se vean consistentes con el resto de la interfaz, en vez de
    aparecer como recuadros blancos sobre fondo oscuro.
    """
    figura.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=COLOR_FONDO_TARJETA,
        font_color=COLOR_TEXTO,
        margin={"t": 40, "b": 40, "l": 50, "r": 30},
    )
    figura.update_xaxes(gridcolor=COLOR_GRILLA, zerolinecolor=COLOR_GRILLA)
    figura.update_yaxes(gridcolor=COLOR_GRILLA, zerolinecolor=COLOR_GRILLA)

    return figura
