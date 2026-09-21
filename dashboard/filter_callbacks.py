"""Callbacks de filtros del Control Center.

Fase 3b.2 final (fix raíz): se restauran los 4 cascades de dropdowns.
Los filtros encadenados garantizan que el usuario solo vea opciones
válidas para la combinación actual.

El doble spinner que aparecía antes era mitigado por la lentitud del
callback de datos. Con el caché JSON + pre-binning + WebGL, los
cascades completan en ~10-50ms. Con delay_show=500ms en los Loading,
los cascades rápidos no muestran spinner. Solo el store callback
(el largo) lo muestra.

Arquitectura:
- 4 callbacks de cascade (línea, equipo, turno, operador). Cada uno
  actualiza las opciones del dropdown siguiente + resetea su value.
- 1 callback de reset que escribe los 6 filtros al default.
- 1 callback de datos (en data_callbacks.py) que escucha los 6 valores
  y escribe el store.
"""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd
from dash import Input, Output
from dash.exceptions import PreventUpdate

_DF: pd.DataFrame | None = None
_APLICAR_FILTROS: Callable | None = None


def configurar_callbacks_filtros(
    df: pd.DataFrame,
    aplicar_filtros: Callable,
) -> None:
    global _DF, _APLICAR_FILTROS
    _DF = df
    _APLICAR_FILTROS = aplicar_filtros


def _obtener_dependencias() -> tuple[pd.DataFrame, Callable]:
    if _DF is None or _APLICAR_FILTROS is None:
        raise RuntimeError(
            "Los callbacks de filtros no han sido configurados."
        )
    return _DF, _APLICAR_FILTROS


def valores_default_filtros(fecha_min: str, fecha_max: str) -> tuple:
    """Valores por defecto del control center, en orden de Outputs.

    Returns
    -------
    tuple
        (start_date, end_date, linea, equipo, turno, operador)
    """
    return (
        fecha_min,
        fecha_max,
        "Todas",
        "Todos",
        "Todos",
        "Todos",
    )


def _filtrar_por_periodo(start_date, end_date):
    df, aplicar_filtros = _obtener_dependencias()
    return aplicar_filtros(
        df,
        fecha_inicio=start_date,
        fecha_fin=end_date,
    )


def actualizar_lineas(start_date, end_date):
    filtrado = _filtrar_por_periodo(start_date, end_date)

    opciones = [
        {"label": "Todas", "value": "Todas"},
        *[
            {"label": valor, "value": valor}
            for valor in sorted(
                filtrado["linea"].dropna().astype(str).unique()
            )
        ],
    ]

    return opciones, "Todas"


def actualizar_equipos(linea, start_date, end_date):
    df, aplicar_filtros = _obtener_dependencias()

    filtrado = aplicar_filtros(
        df,
        fecha_inicio=start_date,
        fecha_fin=end_date,
        linea=linea or "Todas",
    )

    opciones = [
        {"label": "Todos", "value": "Todos"},
        *[
            {"label": valor, "value": valor}
            for valor in sorted(
                filtrado["equipo"].dropna().astype(str).unique()
            )
        ],
    ]

    return opciones, "Todos"


def actualizar_turnos(equipo, linea, start_date, end_date):
    df, aplicar_filtros = _obtener_dependencias()

    filtrado = aplicar_filtros(
        df,
        fecha_inicio=start_date,
        fecha_fin=end_date,
        linea=linea or "Todas",
        equipo=equipo or "Todos",
    )

    opciones = [
        {"label": "Todos", "value": "Todos"},
        *[
            {"label": valor, "value": valor}
            for valor in sorted(
                filtrado["turno"].dropna().astype(str).unique()
            )
        ],
    ]

    return opciones, "Todos"


def actualizar_operadores(turno, equipo, linea, start_date, end_date):
    df, aplicar_filtros = _obtener_dependencias()

    filtrado = aplicar_filtros(
        df,
        fecha_inicio=start_date,
        fecha_fin=end_date,
        linea=linea or "Todas",
        equipo=equipo or "Todos",
        turno=turno or "Todos",
    )

    opciones = [
        {"label": "Todos", "value": "Todos"},
        *[
            {"label": valor, "value": valor}
            for valor in sorted(
                filtrado["operador"].dropna().astype(str).unique()
            )
        ],
    ]

    return opciones, "Todos"


def registrar_callbacks_filtros(
    app,
    df: pd.DataFrame,
    aplicar_filtros: Callable,
    fecha_min: str,
    fecha_max: str,
) -> None:
    configurar_callbacks_filtros(df, aplicar_filtros)

    @app.callback(
        Output("filtro-linea", "options"),
        Output("filtro-linea", "value", allow_duplicate=True),
        Input("filtro-periodo", "start_date"),
        Input("filtro-periodo", "end_date"),
        prevent_initial_call=True,
    )
    def callback_actualizar_lineas(start_date, end_date):
        return actualizar_lineas(start_date, end_date)

    @app.callback(
        Output("filtro-equipo", "options"),
        Output("filtro-equipo", "value", allow_duplicate=True),
        Input("filtro-linea", "value"),
        Input("filtro-periodo", "start_date"),
        Input("filtro-periodo", "end_date"),
        prevent_initial_call=True,
    )
    def callback_actualizar_equipos(linea, start_date, end_date):
        return actualizar_equipos(linea, start_date, end_date)

    @app.callback(
        Output("filtro-turno", "options"),
        Output("filtro-turno", "value", allow_duplicate=True),
        Input("filtro-equipo", "value"),
        Input("filtro-linea", "value"),
        Input("filtro-periodo", "start_date"),
        Input("filtro-periodo", "end_date"),
        prevent_initial_call=True,
    )
    def callback_actualizar_turnos(equipo, linea, start_date, end_date):
        return actualizar_turnos(equipo, linea, start_date, end_date)

    @app.callback(
        Output("filtro-operador", "options"),
        Output("filtro-operador", "value", allow_duplicate=True),
        Input("filtro-turno", "value"),
        Input("filtro-equipo", "value"),
        Input("filtro-linea", "value"),
        Input("filtro-periodo", "start_date"),
        Input("filtro-periodo", "end_date"),
        prevent_initial_call=True,
    )
    def callback_actualizar_operadores(turno, equipo, linea, start_date, end_date):
        return actualizar_operadores(turno, equipo, linea, start_date, end_date)

    @app.callback(
        Output("filtro-periodo", "start_date", allow_duplicate=True),
        Output("filtro-periodo", "end_date", allow_duplicate=True),
        Output("filtro-linea", "value", allow_duplicate=True),
        Output("filtro-equipo", "value", allow_duplicate=True),
        Output("filtro-turno", "value", allow_duplicate=True),
        Output("filtro-operador", "value", allow_duplicate=True),
        Input("btn-reset-filtros", "n_clicks"),
        prevent_initial_call=True,
    )
    def callback_restaurar_filtros(n_clicks):
        if not n_clicks:
            raise PreventUpdate
        return valores_default_filtros(fecha_min, fecha_max)
