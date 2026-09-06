from __future__ import annotations

from dash import dcc, html

from dashboard.capability_components import crear_capability_section
from dashboard.components_dash import crear_control_center
from dashboard.control_charts_components import crear_control_charts_section
from dashboard.diagnostics_components import crear_diagnostics_section
from dashboard.kpi_components import crear_kpi_grid
from dashboard.operational_analysis_components import crear_operational_analysis_section
from dashboard.quality_performance_components import crear_quality_performance

TABS = [
    ("tab-diagnostico", "Diagnóstico"),
    ("tab-calidad", "Calidad"),
    ("tab-capacidad", "Capacidad"),
    ("tab-control", "Control"),
    ("tab-operacional", "Operacional"),
]


def crear_app_layout(
    fecha_min: str,
    fecha_max: str,
    lineas: list[str],
    equipos: list[str],
    turnos: list[str],
    operadores: list[str],
    variables_criticas: dict,
):
    contenido_por_tab = {
        "tab-diagnostico": crear_diagnostics_section(),
        "tab-calidad": crear_quality_performance(),
        "tab-capacidad": crear_capability_section(variables_criticas),
        "tab-control": crear_control_charts_section(variables_criticas),
        "tab-operacional": crear_operational_analysis_section(),
    }

    return html.Div(
        [
            html.Div(
                [
                    html.Div("INDUSTRIAL ANALYTICS PLATFORM", className="platform-label"),
                    html.H1("🏭 Industrial KPI Intelligence", className="hero-title"),
                ],
                className="app-header",
            ),
            dcc.Store(id="store-datos-filtrados", storage_type="memory"),
            crear_kpi_grid(),
            crear_control_center(
                (fecha_min, fecha_max), lineas, equipos, turnos, operadores
            ),
            dcc.Tabs(
                id="tabs-principal",
                value=TABS[0][0],
                children=[dcc.Tab(label=label, value=tab_id) for tab_id, label in TABS],
            ),
            html.Div(
                [
                    html.Div(
                        contenido_por_tab[tab_id],
                        id=f"{tab_id}-content",
                        style={"display": "block" if tab_id == TABS[0][0] else "none"},
                    )
                    for tab_id, _ in TABS
                ]
            ),
        ]
    )
