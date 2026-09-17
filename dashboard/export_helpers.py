"""Helpers de exportación CSV para tabs del dashboard (Fase 3a).

Centraliza:
- Generación de nombre de archivo con timestamp (SSOT).
- Botón estándar "📥 Exportar CSV" con id uniforme.
- Función pura para convertir JSON de DataFrame en descarga CSV.

Convención de IDs (para callbacks):
    botón:    btn-export-<tab>    (ej. "btn-export-capacidad")
    download: download-<tab>      (ej. "download-capacidad")

Uso típico en un callback:
    @app.callback(
        Output("download-<tab>", "data"),
        Input("btn-export-<tab>", "n_clicks"),
        State("store-<tab>", "data"),
        prevent_initial_call=True,
    )
    def callback(n_clicks, json_data):
        if not n_clicks:
            return None
        return crear_descarga_csv(json_data, "capacidad")
"""

from __future__ import annotations

from datetime import datetime
from io import StringIO

import pandas as pd
from dash import dcc, html


def nombre_csv(tab: str) -> str:
    """Genera 'industrial_kpi_<tab>_YYYYMMDD_HHMMSS.csv'.

    Parameters
    ----------
    tab : str
        Identificador corto del tab (ej. "capacidad").

    Returns
    -------
    str
        Nombre listo para descarga, con timestamp para evitar
        colisiones cuando el usuario exporta múltiples veces.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"industrial_kpi_{tab}_{timestamp}.csv"


def boton_export(tab: str) -> html.Button:
    """Construye el botón estándar 'Exportar CSV' para un tab.

    Parameters
    ----------
    tab : str
        Identificador corto del tab. Define el ID del botón como
        ``btn-export-<tab>``.

    Returns
    -------
    html.Button
        Botón con el estilo estándar del dashboard.
    """
    return html.Button(
        "📥 Exportar CSV",
        id=f"btn-export-{tab}",
        n_clicks=0,
        className="btn-export",
        title="Descarga los datos de esta pestaña en formato CSV",
    )


def crear_descarga_csv(json_data: str | None, tab: str):
    """Convierte JSON de DataFrame en descarga CSV para ``dcc.Download``.

    Función pura (sin estado) para poder testear sin simular Dash.
    Retorna None si no hay datos — el callback entonces no dispara
    ninguna descarga.

    Parameters
    ----------
    json_data : str | None
        JSON en formato orient='split' (tal como se guarda en dcc.Store).
    tab : str
        Identificador corto del tab, para el nombre del archivo.

    Returns
    -------
    dict | None
        Dict con ``content`` (base64) y ``filename``, o None si no hay
        datos para exportar.
    """
    if not json_data:
        return None

    df = pd.read_json(StringIO(json_data), orient="split")
    return dcc.send_data_frame(df.to_csv, nombre_csv(tab), index=False)
