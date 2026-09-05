"""Layout Dash del análisis operacional comparativo (drill-down por dimensión)."""

from __future__ import annotations

from dash import dcc, html

DIMENSIONES_DISPONIBLES = [
    {"label": "Equipo", "value": "equipo"},
    {"label": "Turno", "value": "turno"},
    {"label": "Operador", "value": "operador"},
    {"label": "Línea", "value": "linea"},
    {"label": "Máquina", "value": "maquina"},
]


def crear_operational_analysis_section() -> html.Div:
    """Construye la sección de análisis operacional comparativo."""
    return html.Div(
        [
            html.Div(
                [
                    html.H2(
                        "Operational Analysis",
                        className="section-title",
                    ),
                    html.P(
                        "Ranking comparativo por dimensión operacional. "
                        "Haz clic en una barra para ver el detalle de ese grupo.",
                        className="section-subtitle",
                    ),
                ],
                className="section-header",
            ),
            html.Div(
                [
                    html.Label("Dimensión"),
                    dcc.Dropdown(
                        id="operational-dimension-selector",
                        options=DIMENSIONES_DISPONIBLES,
                        value="equipo",
                        clearable=False,
                    ),
                ],
                className="filter-control",
            ),
            dcc.Graph(id="operational-ranking-chart"),
            html.Div(
                id="operational-detail-panel",
                className="quality-analysis-card",
            ),
        ],
        className="dashboard-section operational-performance",
    )
