"""Layout Dash del análisis operacional comparativo (drill-down por dimensión).

Selector de dimensión como segmented control (RadioItems estilizado con
CSS) en lugar de dropdown: reduce fricción (1 click vs 2) y expone todas
las opciones simultáneamente — patrón ISA-101 para HMI.

"Tipo de máquina" reemplaza a "Máquina" para desambiguar de "Equipo":
Equipo es la instancia física única (L1-FILL-01), Tipo de máquina agrupa
por familia a través de todas las líneas (FILL-01 = todas las llenadoras
número 01).
"""

from __future__ import annotations

from dash import dcc, html

DIMENSIONES_DISPONIBLES = [
    {"label": "Equipo", "value": "equipo"},
    {"label": "Turno", "value": "turno"},
    {"label": "Operador", "value": "operador"},
    {"label": "Línea", "value": "linea"},
    {"label": "Tipo de máquina", "value": "maquina"},
]

MICROCOPY_DIMENSIONES = (
    "Equipo = instancia física única · "
    "Tipo de máquina = familia a través de todas las líneas"
)


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
                        "Clic en una barra para ver el detalle.",
                        className="section-subtitle",
                    ),
                ],
                className="section-header",
            ),
            html.Div(
                [
                    html.Label(
                        "Dimensión",
                        className="filter-label",
                    ),
                    dcc.RadioItems(
                        id="operational-dimension-selector",
                        options=DIMENSIONES_DISPONIBLES,
                        value="equipo",
                        className="dimension-chips",
                        inputClassName="dimension-chip-input",
                        labelClassName="dimension-chip",
                    ),
                    html.P(
                        MICROCOPY_DIMENSIONES,
                        className="filter-help",
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