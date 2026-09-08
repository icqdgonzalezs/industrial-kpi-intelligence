"""Callback de navegación: renderiza el contenido de la pestaña activa.

Decisión de arquitectura importante: el contenido de cada pestaña se monta
bajo demanda (Output "children"), no se pre-monta y se esconde con CSS.
Un dcc.Graph dentro de un contenedor con display:none mide 0x0 al momento
de dibujarse y queda invisible para siempre, incluso al volverse visible
después. Montar el contenido solo cuando la pestaña está activa evita ese
problema de raíz.
"""

from __future__ import annotations

from dash import Input, Output

from dashboard.capability_components import crear_capability_section
from dashboard.control_charts_components import crear_control_charts_section
from dashboard.diagnostics_components import crear_diagnostics_section
from dashboard.operational_analysis_components import crear_operational_analysis_section
from dashboard.quality_performance_components import crear_quality_performance


def registrar_callbacks_tabs(app, variables_criticas: dict) -> None:
    constructores = {
        "tab-diagnostico": crear_diagnostics_section,
        "tab-calidad": crear_quality_performance,
        "tab-capacidad": lambda: crear_capability_section(variables_criticas),
        "tab-control": lambda: crear_control_charts_section(variables_criticas),
        "tab-operacional": crear_operational_analysis_section,
    }

    @app.callback(
        Output("tab-content-container", "children"),
        Input("tabs-principal", "value"),
    )
    def callback_cambiar_tab(tab_activo):
        constructor = constructores.get(tab_activo)
        if constructor is None:
            return None
        return constructor()
