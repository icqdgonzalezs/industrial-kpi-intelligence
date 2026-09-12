from __future__ import annotations

from dash import Input, Output, html

from dashboard.kpi_presenter import clasificar_kpis, formatear_kpis
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


def construir_kpi_cards(data):
    """Construye los 4 valores del KPI top como html.Span con color semántico.

    Envuelve actualizar_kpis() sin modificarla: actualizar_kpis() sigue
    devolviendo strings planas (así lo esperan los tests existentes en
    tests/test_dash_app.py — cambiar su firma los habría roto). Esta
    función es la que efectivamente se conecta al Output de Dash.

    Nota de diseño: recalcula calcular_kpis_globales() sobre el mismo
    DataFrame que ya calculó actualizar_kpis() internamente. Es
    redundante (dos pasadas sobre los mismos datos), pero es el precio
    deliberado de no tocar la función ya probada — para un dataset de
    este tamaño el costo es despreciable; si se vuelve un cuello de
    botella real, se revisita con un perfil de performance real, no
    especulativamente.
    """
    produccion, fpy, defectos, scrap = actualizar_kpis(data)

    filtrado = leer_dataframe_filtrado(data)

    if filtrado.empty:
        clasificacion = {
            "produccion": "neutral",
            "fpy": "neutral",
            "defectos": "neutral",
            "scrap": "neutral",
        }
    else:
        kpis = calcular_kpis_globales(filtrado)
        clasificacion = clasificar_kpis(kpis)

    return (
        html.Span(produccion, className=f"kpi-value--{clasificacion['produccion']}"),
        html.Span(fpy, className=f"kpi-value--{clasificacion['fpy']}"),
        html.Span(defectos, className=f"kpi-value--{clasificacion['defectos']}"),
        html.Span(scrap, className=f"kpi-value--{clasificacion['scrap']}"),
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
        return construir_kpi_cards(data)
