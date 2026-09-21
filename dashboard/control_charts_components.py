"""Layout Dash de la carta de control estadístico (I-MR).

El bloque de las 2 cartas (I + MR) va envuelto en su propio `dcc.Loading`
para mostrar un spinner único centrado, en vez de dejar que cada
`dcc.Graph` encienda su spinner interno de Dash 4.x (que produce
2 spinners consecutivos).

La sección NO va envuelta por el `dcc.Loading` de `app_layout.py`:
el header, export bar y dropdown quedan siempre visibles mientras
las gráficas se actualizan.

Fase 3b.2: cuando el filtro deja 0 filas o la variable seleccionada
no tiene datos, se oculta `control-normal-content` y se muestra un
empty_state() en `control-empty-content`. Los ids internos
(control-status, control-chart-i, control-chart-mr) NO cambian.
"""

from __future__ import annotations

from dash import dcc, html

from dashboard.export_helpers import boton_export

LOADING_COLOR = "#00d4ff"
LOADING_DELAY_MS = 500


def crear_control_charts_section(variables_config: dict) -> html.Div:
    opciones = [
        {"label": cfg["nombre"], "value": col}
        for col, cfg in variables_config.items()
    ]
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
            # -----------------------------------------------------------------
            # Contenido normal: status + las 2 cartas. Se oculta con style
            # cuando no hay datos. Los IDs internos NO cambian.
            # -----------------------------------------------------------------
            html.Div(
                [
                    html.Div(
                        id="control-status",
                        className="quality-analysis-card",
                    ),
                    dcc.Loading(
                        children=html.Div(
                            [
                                dcc.Graph(id="control-chart-i"),
                                dcc.Graph(id="control-chart-mr"),
                            ],
                        ),
                        type="default",
                        color=LOADING_COLOR,
                        delay_show=LOADING_DELAY_MS,
                    ),
                ],
                id="control-normal-content",
                style={"display": "block"},
            ),
            # -----------------------------------------------------------------
            # Contenido vacío: se llena con empty_state() cuando no hay datos.
            # -----------------------------------------------------------------
            html.Div(id="control-empty-content"),
            dcc.Download(id="download-control"),
        ],
        className="dashboard-section control-performance",
    )
