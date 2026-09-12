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
            # Pre-montamos las 5 secciones al arranque y solo alternamos su
            # visibilidad con `display`. Cada dcc.Graph lleva altura explícita
            # en su propio layout, así que no mide 0x0 aunque el padre esté
            # oculto — y los callbacks encuentran sus componentes siempre.
            html.Div(
                [
                    html.Div(
                        crear_diagnostics_section(),
                        id="section-diagnostico",
                        style={"display": "block"},
                    ),
                    html.Div(
                        crear_quality_performance(),
                        id="section-calidad",
                        style={"display": "none"},
                    ),
                    html.Div(
                        crear_capability_section(variables_criticas),
                        id="section-capacidad",
                        style={"display": "none"},
                    ),
                    html.Div(
                        crear_control_charts_section(variables_criticas),
                        id="section-control",
                        style={"display": "none"},
                    ),
                    html.Div(
                        crear_operational_analysis_section(),
                        id="section-operacional",
                        style={"display": "none"},
                    ),
                ],
                id="tab-content-container",
            ),
        ]
    )