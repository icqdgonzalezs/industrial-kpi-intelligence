"""Layout Dash de la carta de control estadístico (I-MR)."""

from __future__ import annotations

from dash import dcc, html

from dashboard.export_helpers import boton_export


def crear_control_charts_section(variables_config: dict) -> html.Div:
    opciones = [{"label": cfg["nombre"], "value": col} for col, cfg in variables_config.items()]
    valor_inicial = opciones[0]["value"] if opciones else None

    return html.Div(
        [
            html.Div(
                [html.H2("Statistical Process Control", className="section-title")],
                className="section-header",
            ),
            html.Div(
                [boton_export("control")],
                className="section-export-bar",
            ),
            dcc.Dropdown(
                id="control-variable-selector",
                options=opciones,
                value=valor_inicial,
                clearable=False,
                className="filter-control",
            ),
            html.Div(id="control-status", className="quality-analysis-card"),
            dcc.Graph(id="control-chart-i"),
            dcc.Graph(id="control-chart-mr"),
            dcc.Download(id="download-control"),
        ],
        className="dashboard-section control-performance",
    )