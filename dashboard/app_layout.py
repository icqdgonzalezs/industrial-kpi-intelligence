from __future__ import annotations

from dash import dcc, html

from dashboard.components_dash import crear_control_center
from dashboard.kpi_components import crear_kpi_grid

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
            # Contenedor único: su contenido se reemplaza por completo en cada
            # cambio de pestaña (ver tabs_callbacks.py). Así el dcc.Graph de la
            # pestaña activa se monta SIEMPRE visible, y Plotly lo mide bien.
            html.Div(id="tab-content-container"),
        ]
    )
