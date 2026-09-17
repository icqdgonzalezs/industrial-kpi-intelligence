"""Layout Dash para el análisis de capacidad de proceso (Pp/Ppk).

Nota de nomenclatura (NIST 6.1.3 / ISO 22514): los índices mostrados
son Pp/Ppk (sigma overall, ddof=1), no Cp/Cpk (sigma within, MRbar/d2).
Ver src/capability.py para la justificación técnica.

IDs alineados a la nomenclatura correcta: `capability-pp`,
`capability-ppk`, `capability-ppk-minimo`. Este rename se aplicó en el
Bloque UX-1/UX-2 para sincronizar layout y callbacks con el mismo
naming (ver docs/adr/0002-naming-convention.md).

Incluye 4 KPIs de rendimiento respecto a especificación (% dentro,
% bajo LSL, % sobre USL, PPM total) que convierten el histograma en
herramienta de decisión — ver src/capability.calcular_rendimiento_spec.

Fase 3a: incluye botón "📥 Exportar CSV" que descarga el resumen
completo de Pp/Ppk (con filtros aplicados).
"""

from __future__ import annotations

from dash import dcc, html

from dashboard.export_helpers import boton_export


def _crear_card_metrica(
    label: str,
    componente_id: str,
) -> html.Div:
    """Helper: card estándar (label arriba, valor debajo)."""
    return html.Div(
        [
            html.Div(label, className="quality-metric-label"),
            html.Div(id=componente_id, className="quality-metric-value"),
        ],
        className="quality-metric-card",
    )


def crear_capability_section(variables_config: dict) -> html.Div:
    """Construye la sección de capacidad de proceso.

    Parameters
    ----------
    variables_config : dict
        Diccionario columna -> {"nombre", "lsl", "usl"}, tal como se
        define en config/quality_config.yaml (quality.variables_criticas).
    """
    opciones_variable = [
        {"label": cfg["nombre"], "value": columna}
        for columna, cfg in variables_config.items()
    ]

    valor_inicial = opciones_variable[0]["value"] if opciones_variable else None

    return html.Div(
        [
            html.Div(
                [
                    html.H2(
                        "Process Capability",
                        className="section-title",
                    ),
                    html.P(
                        "Evaluación de capacidad (Pp/Ppk) respecto de los "
                        "límites de especificación definidos en configuración.",
                        className="section-subtitle",
                    ),
                ],
                className="section-header",
            ),
            html.Div(
                [boton_export("capacidad")],
                className="section-export-bar",
            ),
            dcc.Download(id="download-capacidad"),
            dcc.Store(id="store-capacidad"),
            html.Div(
                [
                    _crear_card_metrica("Variables evaluadas", "capability-total-variables"),
                    _crear_card_metrica("Ppk mínimo", "capability-ppk-minimo"),
                    _crear_card_metrica("Variables marginales", "capability-marginales"),
                    _crear_card_metrica("Variables no capaces", "capability-no-capaces"),
                ],
                className="quality-metrics-grid",
            ),
            html.Div(
                [
                    html.Label("Variable"),
                    dcc.Dropdown(
                        id="capability-variable-selector",
                        options=opciones_variable,
                        value=valor_inicial,
                        clearable=False,
                    ),
                ],
                className="filter-control",
            ),
            html.Div(
                [
                    _crear_card_metrica("Pp", "capability-pp"),
                    _crear_card_metrica("Ppk", "capability-ppk"),
                    _crear_card_metrica("Promedio", "capability-media"),
                    html.Div(
                        [
                            html.Div(
                                "σ",
                                className="quality-metric-label quality-metric-label--symbol",
                            ),
                            html.Div(id="capability-sigma", className="quality-metric-value"),
                        ],
                        className="quality-metric-card",
                    ),
                ],
                className="quality-metrics-grid",
            ),
            html.Div(
                [
                    _crear_card_metrica("Dentro de spec", "capability-pct-dentro"),
                    _crear_card_metrica("Bajo LSL", "capability-pct-bajo-lsl"),
                    _crear_card_metrica("Sobre USL", "capability-pct-sobre-usl"),
                    _crear_card_metrica("PPM total", "capability-ppm-total"),
                ],
                className="quality-metrics-grid",
            ),
            html.Div(id="capability-estado", className="quality-analysis-card"),
            dcc.Graph(id="capability-grafico"),
            html.Div(id="capability-observaciones", className="section-subtitle"),
        ],
        className="dashboard-section capability-performance",
    )
