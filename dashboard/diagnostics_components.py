"""Layout Dash del panel de diagnóstico priorizado."""

from __future__ import annotations

from dash import html


def crear_diagnostics_section() -> html.Div:
    """Construye la sección de diagnóstico (motor de hallazgos priorizados)."""
    return html.Div(
        [
            html.Div(
                [
                    html.H2(
                        "Diagnostics",
                        className="section-title",
                    ),
                    html.P(
                        "Hallazgos priorizados por severidad.",
                        className="section-subtitle",
                    ),
                ],
                className="section-header",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("Prioritarios", className="quality-metric-label"),
                            html.Div(id="diagnostics-count-priority", className="quality-metric-value"),
                        ],
                        className="quality-metric-card severity-priority",
                    ),
                    html.Div(
                        [
                            html.Div("En seguimiento", className="quality-metric-label"),
                            html.Div(id="diagnostics-count-watch", className="quality-metric-value"),
                        ],
                        className="quality-metric-card severity-watch",
                    ),
                    html.Div(
                        [
                            html.Div("Informativos", className="quality-metric-label"),
                            html.Div(id="diagnostics-count-info", className="quality-metric-value"),
                        ],
                        className="quality-metric-card severity-info",
                    ),
                ],
                className="quality-metrics-grid",
            ),
            html.Div(
                id="diagnostics-resumen-ejecutivo",
                className="quality-analysis-card",
            ),
            html.Div(
                id="diagnostics-lista-hallazgos",
                className="diagnostics-findings-list",
            ),
        ],
        className="dashboard-section diagnostics-performance",
    )


def crear_tarjeta_hallazgo(severidad: str, categoria: str, titulo: str, mensaje: str) -> html.Div:
    """Construye una tarjeta individual de hallazgo, color-codificada por severidad."""
    clase_severidad = {
        "PRIORITY": "finding-priority",
        "WATCH": "finding-watch",
        "INFO": "finding-info",
    }.get(severidad, "finding-info")

    return html.Div(
        [
            html.Div(
                [
                    html.Span(severidad, className="finding-badge"),
                    html.Span(categoria, className="finding-category"),
                ],
                className="finding-header",
            ),
            html.Div(titulo, className="finding-title"),
            html.Div(mensaje, className="finding-message"),
        ],
        className=f"finding-card {clase_severidad}",
    )
