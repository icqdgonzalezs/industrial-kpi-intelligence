from __future__ import annotations

from dash import Input, Output

from dashboard.kpi_presenter import formatear_kpis
from dashboard.utils import leer_dataframe_filtrado
from src.kpis import calcular_kpis_globales


def actualizar_kpis(data):
    filtrado = leer_dataframe_filtrado(data)

    if filtrado.empty:
        return "0", "—", "—", "—"

    kpis = calcular_kpis_globales(filtrado)
    presentados = formatear_kpis(kpis)

    return (
        presentados["produccion"],
        presentados["fpy"],
        presentados["defectos"],
        presentados["scrap"],
    )


def registrar_callbacks_kpi(app) -> None:
    @app.callback(
        Output("kpi-produccion-total", "children"),
        Output("kpi-fpy", "children"),
        Output("kpi-defectos", "children"),
        Output("kpi-scrap", "children"),
        Input("store-datos-filtrados", "data"),
    )
    def callback_actualizar_kpis(data):
        return actualizar_kpis(data)
