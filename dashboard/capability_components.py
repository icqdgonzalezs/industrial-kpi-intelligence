"""Layout Dash para el análisis de capacidad de proceso (Cp/Cpk)."""

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
                        "Evaluación de capacidad (Cp/Cpk) respecto de los "
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
                            html.Div("Cpk mínimo", className="quality-metric-label"),
                            html.Div(id="capability-cpk-minimo", className="quality-metric-value"),
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
                            html.Div("Cp", className="quality-metric-label"),
                            html.Div(id="capability-cp", className="quality-metric-value"),
                        ],
                        className="quality-metric-card",
                    ),
                    html.Div(
                        [
                            html.Div("Cpk", className="quality-metric-label"),
                            html.Div(id="capability-cpk", className="quality-metric-value"),
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
