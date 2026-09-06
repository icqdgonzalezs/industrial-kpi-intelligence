"""Layout Dash de la carta de control estadístico (I-MR)."""

from __future__ import annotations

from dash import dcc, html


def crear_control_charts_section(variables_config: dict) -> html.Div:
    opciones = [{"label": cfg["nombre"], "value": col} for col, cfg in variables_config.items()]
    valor_inicial = opciones[0]["value"] if opciones else None

    return html.Div(
        [
            html.Div(
                [html.H2("Statistical Process Control", className="section-title")],
                className="section-header",
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
        ],
        className="dashboard-section control-performance",
    )
