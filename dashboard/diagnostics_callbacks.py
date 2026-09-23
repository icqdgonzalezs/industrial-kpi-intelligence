"""Callbacks Dash del panel de diagnóstico priorizado.

Callback delgado: toda la lógica de reglas vive en src/diagnostics.py
(100% testeado). Reutiliza store-capacidad (ya calculado por el módulo
de capacidad de proceso) para no recalcular Cp/Cpk dos veces.
"""

from __future__ import annotations

from io import StringIO

import pandas as pd
from dash import Input, Output, State

from dashboard.diagnostics_components import crear_tarjeta_hallazgo
from dashboard.empty_state import empty_state
from dashboard.export_helpers import crear_descarga_csv
from dashboard.utils import leer_dataframe_filtrado
from src.diagnostics import generar_diagnostico


def _leer_capacidad(capacidad_json) -> pd.DataFrame:
    if not capacidad_json:
        return pd.DataFrame()
    return pd.read_json(StringIO(capacidad_json), orient="split")


def crear_resumen_ejecutivo(diagnostico: pd.DataFrame) -> str:
    """Genera una frase de resumen ejecutivo a partir del conteo de severidades."""
    if diagnostico.empty:
        return "No hay datos suficientes para generar un diagnóstico."

    n_priority = int((diagnostico["severidad"] == "PRIORITY").sum())
    n_watch = int((diagnostico["severidad"] == "WATCH").sum())

    if n_priority == 0 and n_watch == 0:
        return "Sin hallazgos que requieran atención inmediata en el período seleccionado."

    partes = []
    if n_priority:
        partes.append(f"{n_priority} prioritario{'s' if n_priority != 1 else ''}")
    if n_watch:
        partes.append(f"{n_watch} en seguimiento")

    return f"{' y '.join(partes)} requieren revisión en el período seleccionado."


def exportar_diagnostico_csv(data, capacidad_json):
    """Construye la descarga CSV del diagnóstico priorizado.

    Función pura (sin Dash): recibe el JSON del store de datos filtrados
    y el JSON del store de capacidad, devuelve el dict de descarga, o
    None si no hay hallazgos que exportar.

    El CSV contiene una fila por hallazgo con columnas:
    severidad, categoria, titulo, mensaje, score.

    Parameters
    ----------
    data : str | None
        JSON orient='split' del DataFrame filtrado (store-datos-filtrados).
    capacidad_json : str | None
        JSON orient='split' del resumen de capacidad (store-capacidad).

    Returns
    -------
    dict | None
        Dict {content, filename} listo para Output de dcc.Download,
        o None si el filtrado está vacío o no hay hallazgos.
    """
    filtrado = leer_dataframe_filtrado(data)

    if filtrado.empty:
        return None

    capacidad = _leer_capacidad(capacidad_json)
    diagnostico = generar_diagnostico(filtrado, capacidad)

    if diagnostico.empty:
        return None

    json_data = diagnostico.to_json(orient="split", date_format="iso")
    return crear_descarga_csv(json_data, "diagnostico")


def construir_outputs_diagnostico(data, capacidad_json) -> tuple:
    """Función pura: produce la tupla de 5 outputs del callback de Diagnóstico.

    Orden de outputs (contrato fijo):
        0: contador PRIORITY (str)
        1: contador WATCH (str)
        2: contador INFO (str)
        3: resumen ejecutivo (str)
        4: lista de tarjetas de hallazgo o [empty_state] (list)

    Extraída del callback para testear el contrato sin instanciar Dash.

    Decisión de UX (Fase 3b.2): cuando no hay datos, los 3 contadores
    quedan en "0" y el resumen ejecutivo en "". El empty_state del
    quinto output comunica el estado al usuario. Los contadores en "0"
    son informativos (0 hallazgos = período limpio, no app rota).
    """
    filtrado = leer_dataframe_filtrado(data)

    if filtrado.empty:
        return (
            "0", "0", "0", "",
            [empty_state(
                "Sin datos para diagnosticar",
                hint="Ajustá los filtros o tocá 'Restaurar filtros'.",
            )],
        )

    capacidad = _leer_capacidad(capacidad_json)
    diagnostico = generar_diagnostico(filtrado, capacidad)

    if diagnostico.empty:
        return (
            "0", "0", "0", "",
            [empty_state(
                "Sin hallazgos con los filtros actuales",
                hint="Los filtros aplicados no generan datos suficientes para el motor de reglas.",
            )],
        )

    n_priority = int((diagnostico["severidad"] == "PRIORITY").sum())
    n_watch = int((diagnostico["severidad"] == "WATCH").sum())
    n_info = int((diagnostico["severidad"] == "INFO").sum())

    resumen = crear_resumen_ejecutivo(diagnostico)

    tarjetas = [
        crear_tarjeta_hallazgo(
            fila["severidad"],
            fila["categoria"],
            fila["titulo"],
            fila["mensaje"],
        )
        for _, fila in diagnostico.iterrows()
    ]

    return str(n_priority), str(n_watch), str(n_info), resumen, tarjetas


def registrar_callbacks_diagnostics(app) -> None:
    @app.callback(
        Output("diagnostics-count-priority", "children"),
        Output("diagnostics-count-watch", "children"),
        Output("diagnostics-count-info", "children"),
        Output("diagnostics-resumen-ejecutivo", "children"),
        Output("diagnostics-lista-hallazgos", "children"),
        Input("store-datos-filtrados", "data"),
        Input("store-capacidad", "data"),
    )
    def callback_actualizar_diagnostico(data, capacidad_json):
        return construir_outputs_diagnostico(data, capacidad_json)

    @app.callback(
        Output("download-diagnostico", "data"),
        Input("btn-export-diagnostico", "n_clicks"),
        State("store-datos-filtrados", "data"),
        State("store-capacidad", "data"),
        prevent_initial_call=True,
    )
    def callback_export_diagnostico(n_clicks, data, capacidad_json):
        if not n_clicks:
            return None
        return exportar_diagnostico_csv(data, capacidad_json)