"""Layout Dash para el análisis de capacidad de proceso (Pp/Ppk).

Nota de nomenclatura (NIST 6.1.3 / ISO 22514): los índices mostrados
son Pp/Ppk (sigma overall, ddof=1), no Cp/Cpk (sigma within, MRbar/d2).
Ver src/capability.py para la justificación técnica.

IDs alineados a la nomenclatura correcta: `capability-pp`,
`capability-ppk`, `capability-ppk-minimo`. Este rename se aplicó en el
Bloque UX-1/UX-2 para sincronizar layout y callbacks con el mismo
naming (ver docs/adr/0002-naming-convention.md).
"""

from __future__ import annotations

from dash import dcc, html


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
            dcc.Store(id="store-capacidad"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("Variables evaluadas", className="quality-metric-label"),
                            html.Div(id="capability-total-variables", className="quality-metric-value"),
                        ],
                        className="quality-metric-card",
                    ),
                    html.Div(
                        [
                            html.Div("Ppk mínimo", className="quality-metric-label"),
                            html.Div(id="capability-ppk-minimo", className="quality-metric-value"),
                        ],
                        className="quality-metric-card",
                    ),
                    html.Div(
                        [
                            html.Div("Variables marginales", className="quality-metric-label"),
                            html.Div(id="capability-marginales", className="quality-metric-value"),
                        ],
                        className="quality-metric-card",
                    ),
                    html.Div(
                        [
                            html.Div("Variables no capaces", className="quality-metric-label"),
                            html.Div(id="capability-no-capaces", className="quality-metric-value"),
                        ],
                        className="quality-metric-card",
                    ),
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
                    html.Div(
                        [
                            html.Div("Pp", className="quality-metric-label"),
                            html.Div(id="capability-pp", className="quality-metric-value"),
                        ],
                        className="quality-metric-card",
                    ),
                    html.Div(
                        [
                            html.Div("Ppk", className="quality-metric-label"),
                            html.Div(id="capability-ppk", className="quality-metric-value"),
                        ],
                        className="quality-metric-card",
                    ),
                    html.Div(
                        [
                            html.Div("Promedio", className="quality-metric-label"),
                            html.Div(id="capability-media", className="quality-metric-value"),
                        ],
                        className="quality-metric-card",
                    ),
                    html.Div(
                        [
                            html.Div("σ", className="quality-metric-label"),
                            html.Div(id="capability-sigma", className="quality-metric-value"),
                        ],
                        className="quality-metric-card",
                    ),
                ],
                className="quality-metrics-grid",
            ),
            html.Div(id="capability-estado", className="quality-analysis-card"),
            dcc.Graph(id="capability-grafico"),
            html.Div(id="capability-observaciones", className="section-subtitle"),
        ],
        className="dashboard-section capability-performance",
    )