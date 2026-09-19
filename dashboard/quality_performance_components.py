from __future__ import annotations

from dash import dcc, html

from dashboard.export_helpers import boton_export


def crear_quality_performance():
    return html.Section(
        [
            html.Div(
                [
                    html.H2(
                        "Quality Performance",
                        className="section-title",
                    ),
                    html.P(
                        "Desempeño de calidad y principales fuentes de defectos.",
                        className="section-subtitle",
                    ),
                ],
                className="section-header",
            ),
            html.Div(
                [boton_export("calidad")],
                className="section-export-bar",
            ),
            # -----------------------------------------------------------------
            # Contenido normal: se oculta con style cuando el filtro deja 0
            # filas. Los IDs internos (quality-fpy, quality-pareto-chart, etc.)
            # NO cambian — los callbacks siguen escribiendo en ellos.
            # -----------------------------------------------------------------
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "FPY",
                                        className="quality-metric-label",
                                    ),
                                    html.Div(
                                        id="quality-fpy",
                                        className="quality-metric-value",
                                    ),
                                ],
                                className="quality-metric-card",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        "Tasa de defectos",
                                        className="quality-metric-label",
                                    ),
                                    html.Div(
                                        id="quality-defect-rate",
                                        className="quality-metric-value",
                                    ),
                                ],
                                className="quality-metric-card",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        "Tasa de scrap",
                                        className="quality-metric-label",
                                    ),
                                    html.Div(
                                        id="quality-scrap-rate",
                                        className="quality-metric-value",
                                    ),
                                ],
                                className="quality-metric-card",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        "Tasa de reproceso",
                                        className="quality-metric-label",
                                    ),
                                    html.Div(
                                        id="quality-rework-rate",
                                        className="quality-metric-value",
                                    ),
                                ],
                                className="quality-metric-card",
                            ),
                        ],
                        className="quality-metrics-grid",
                    ),
                    dcc.Graph(id="quality-pareto-chart"),
                    html.Div(
                        [
                            html.Div(
                                id="quality-pareto",
                                children="Sin defectos en el período seleccionado.",
                                className="quality-analysis-card",
                            ),
                            html.Div(
                                id="quality-critical-lot",
                                className="quality-analysis-card",
                            ),
                        ],
                        className="quality-analysis-grid",
                    ),
                ],
                id="quality-normal-content",
                style={"display": "block"},
            ),
            # -----------------------------------------------------------------
            # Contenido vacío: se llena con empty_state() cuando el filtro
            # deja 0 filas. Por defecto vacío (nada visible).
            # -----------------------------------------------------------------
            html.Div(id="quality-empty-content"),
            dcc.Download(id="download-calidad"),
        ],
        className="dashboard-section quality-performance",
    )
