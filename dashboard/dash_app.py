from __future__ import annotations

from pathlib import Path

from dash import Dash

from dashboard.app_layout import crear_app_layout
from dashboard.capability_callbacks import registrar_callbacks_capability
from dashboard.data_callbacks import (
    actualizar_datos_filtrados as _actualizar_datos_filtrados,
)
from dashboard.data_callbacks import (
    registrar_callbacks_datos,
)
from dashboard.data_loader import cargar_datos
from dashboard.diagnostics_callbacks import registrar_callbacks_diagnostics
from dashboard.filter_callbacks import (
    actualizar_equipos,
    actualizar_lineas,
    actualizar_operadores,
    actualizar_turnos,
    registrar_callbacks_filtros,
)
from dashboard.filter_engine import aplicar_filtros
from dashboard.kpi_callbacks import (
    actualizar_kpis as _actualizar_kpis,
)
from dashboard.kpi_callbacks import (
    registrar_callbacks_kpi,
)
from dashboard.operational_analysis_callbacks import registrar_callbacks_operational_analysis
from dashboard.quality_performance_callbacks import registrar_callbacks_quality_performance

__all__ = [
    "app",
    "server",
    "actualizar_datos_filtrados",
    "actualizar_kpis",
    "actualizar_equipos",
    "actualizar_lineas",
    "actualizar_operadores",
    "actualizar_turnos",
]

df, config = cargar_datos()

fecha_min = df["fecha"].min().date()
fecha_max = df["fecha"].max().date()

lineas = ["Todas", *sorted(df["linea"].dropna().astype(str).unique())]
equipos = ["Todos", *sorted(df["equipo"].dropna().astype(str).unique())]
turnos = ["Todos", *sorted(df["turno"].dropna().astype(str).unique())]
operadores = ["Todos", *sorted(df["operador"].dropna().astype(str).unique())]

variables_criticas = config.get("quality", {}).get("variables_criticas", {})

PROJECT_ROOT = Path(__file__).resolve().parent.parent

app = Dash(
    __name__,
    title="Industrial KPI Intelligence",
    suppress_callback_exceptions=True,
    assets_folder=str(PROJECT_ROOT / "assets"),
)
server = app.server  # necesario para gunicorn (Render/Heroku): gunicorn dashboard.dash_app:server

app.layout = crear_app_layout(
    str(fecha_min),
    str(fecha_max),
    lineas,
    equipos,
    turnos,
    operadores,
    variables_criticas,
)

registrar_callbacks_filtros(
    app,
    df,
    aplicar_filtros,
)

registrar_callbacks_datos(
    app,
    df,
    aplicar_filtros,
)

registrar_callbacks_kpi(
    app,
)
registrar_callbacks_quality_performance(
    app,
)
registrar_callbacks_capability(
    app,
    variables_criticas,
)
registrar_callbacks_diagnostics(
    app,
)
registrar_callbacks_operational_analysis(
    app,
)


def actualizar_datos_filtrados(
    start_date,
    end_date,
    linea,
    equipo,
    turno,
    operador,
):
    return _actualizar_datos_filtrados(
        df,
        aplicar_filtros,
        start_date,
        end_date,
        linea,
        equipo,
        turno,
        operador,
    )


def actualizar_kpis(data):
    return _actualizar_kpis(data)


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=True)
