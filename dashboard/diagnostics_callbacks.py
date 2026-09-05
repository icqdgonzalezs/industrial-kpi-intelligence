"""Callbacks Dash del panel de diagnóstico priorizado.

Callback delgado: toda la lógica de reglas vive en src/diagnostics.py
(100% testeado). Reutiliza store-capacidad (ya calculado por el módulo
de capacidad de proceso) para no recalcular Cp/Cpk dos veces.
"""

from __future__ import annotations

from io import StringIO

import pandas as pd
from dash import Input, Output, html

from dashboard.diagnostics_components import crear_tarjeta_hallazgo
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
        filtrado = leer_dataframe_filtrado(data)

        if filtrado.empty:
            return "0", "0", "0", "Sin datos para diagnosticar.", []

        capacidad = _leer_capacidad(capacidad_json)
        diagnostico = generar_diagnostico(filtrado, capacidad)

        if diagnostico.empty:
            return (
                "0",
                "0",
                "0",
                "Sin hallazgos que requieran atención en el período seleccionado.",
                [],
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
