"""Utilidades compartidas entre callbacks de Dash.

Centraliza convenciones comunes a todos los callbacks del dashboard,
como la deserialización del DataFrame filtrado que viaja a través de
``store-datos-filtrados``.
"""

from __future__ import annotations

from io import StringIO

import pandas as pd


def leer_dataframe_filtrado(data: str | None) -> pd.DataFrame:
    """Deserializa el DataFrame filtrado almacenado en ``dcc.Store``.

    Convención compartida: los datos filtrados viajan como JSON
    (orient="split") a través de ``store-datos-filtrados``.
    """
    if not data:
        return pd.DataFrame()

    return pd.read_json(StringIO(data), orient="split")
