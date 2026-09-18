"""Layout Dash del análisis operacional comparativo (drill-down por dimensión).

Selector de dimensión como segmented control (RadioItems estilizado con
CSS) en lugar de dropdown: reduce fricción (1 click vs 2) y expone todas
las opciones simultáneamente — patrón ISA-101 para HMI.

"Tipo de máquina" reemplaza a "Máquina" para desambiguar de "Equipo":
Equipo es la instancia física única (L1-FILL-01), Tipo de máquina agrupa
por familia a través de todas las líneas (FILL-01 = todas las llenadoras
número 01).

LABELS_EJES_DIMENSION expone DIMENSIONES_DISPONIBLES como mapping
value→label. Es la única fuente de verdad del nombre visible de cada
dimensión. El eje Y del ranking y el título del panel de detalle lo
consumen vía _label_dimension() en operational_analysis_callbacks,
evitando strings hardcodeados como "Maquina" (sin tilde) que aparecían
por usar str.capitalize() sobre el value del dataset.
"""

from __future__ import annotations

from dash import dcc, html

from dashboard.export_helpers import boton_export

DIMENSIONES_DISPONIBLES = [
    {"label": "Equipo", "value": "equipo"},
    {"label": "Turno", "value": "turno"},
    {"label": "Operador", "value": "operador"},
    {"label": "Línea", "value": "linea"},
    {"label": "Tipo de máquina", "value": "maquina"},
]

# SSOT del nombre visible por dimensión. Derivado de la lista de arriba
# para que agregar/quitar dimensiones no requiera tocar dos lugares.
LABELS_EJES_DIMENSION = {d["value"]: d["label"] for d in DIMENSIONES_DISPONIBLES}

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
                [boton_export("operacional")],
                className="section-export-bar",
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
            dcc.Download(id="download-operacional"),
        ],
        className="dashboard-section operational-performance",
    )