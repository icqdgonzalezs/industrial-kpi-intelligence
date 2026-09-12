"""Callback de navegación: alterna la visibilidad de la pestaña activa.

Decisión de arquitectura: las 5 secciones se pre-montan al arranque y el
callback solo alterna `display` entre "block" y "none". Esto resuelve el
problema inverso del patrón "montar bajo demanda":

- Montar bajo demanda: la primera vez que se entra a una pestaña funciona,
  pero los callbacks registrados al arranque referencian componentes que
  aún no existen → ReferenceError de Dash ("nonexistent object was used in
  an Input of a Dash callback").

- Pre-montar + alternar display: todos los componentes existen siempre,
  los callbacks encuentran sus Input/Output, y los dcc.Graph con altura
  explícita no miden 0x0 porque su altura viene del layout, no del padre
  oculto. Plotly respeta esa altura cuando el contenedor pasa a "block".
"""

from __future__ import annotations

from dash import Input, Output

SECCIONES = ("diagnostico", "calidad", "capacidad", "control", "operacional")

TAB_A_SECCION = {
    "tab-diagnostico": "diagnostico",
    "tab-calidad": "calidad",
    "tab-capacidad": "capacidad",
    "tab-control": "control",
    "tab-operacional": "operacional",
}


def registrar_callbacks_tabs(app, variables_criticas: dict) -> None:
    @app.callback(
        [Output(f"section-{seccion}", "style") for seccion in SECCIONES],
        Input("tabs-principal", "value"),
    )
    def callback_cambiar_tab(tab_activo):
        seccion_activa = TAB_A_SECCION.get(tab_activo, "diagnostico")
        return [
            {"display": "block"} if seccion == seccion_activa else {"display": "none"}
            for seccion in SECCIONES
        ]