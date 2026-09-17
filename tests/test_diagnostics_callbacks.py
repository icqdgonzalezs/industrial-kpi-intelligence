from __future__ import annotations

import pandas as pd
import pytest

from dashboard import diagnostics_callbacks as diag_mod
from dashboard.diagnostics_callbacks import (
    crear_resumen_ejecutivo,
    exportar_diagnostico_csv,
)


def _diagnostico(severidades: list[str]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "severidad": severidades,
            "categoria": ["Equipo"] * len(severidades),
            "titulo": ["t"] * len(severidades),
            "mensaje": ["m"] * len(severidades),
            "score": [1.0] * len(severidades),
        }
    )


def test_resumen_ejecutivo_dataset_vacio():
    assert crear_resumen_ejecutivo(pd.DataFrame()) == (
        "No hay datos suficientes para generar un diagnóstico."
    )


def test_resumen_ejecutivo_sin_hallazgos_relevantes():
    diagnostico = _diagnostico(["INFO", "INFO"])
    resumen = crear_resumen_ejecutivo(diagnostico)
    assert "Sin hallazgos" in resumen


def test_resumen_ejecutivo_con_priority_y_watch():
    diagnostico = _diagnostico(["PRIORITY", "WATCH", "WATCH", "INFO"])
    resumen = crear_resumen_ejecutivo(diagnostico)
    assert "1 prioritario" in resumen
    assert "2 en seguimiento" in resumen


def test_resumen_ejecutivo_solo_priority_plural():
    diagnostico = _diagnostico(["PRIORITY", "PRIORITY"])
    resumen = crear_resumen_ejecutivo(diagnostico)
    assert "2 prioritarios" in resumen
    assert "en seguimiento" not in resumen


@pytest.fixture
def dash_app_con_callbacks():
    from dash import Dash, html

    from dashboard.diagnostics_callbacks import registrar_callbacks_diagnostics

    app = Dash(__name__)
    app.layout = html.Div()
    registrar_callbacks_diagnostics(app)
    return app


def test_registrar_callbacks_diagnostics_no_falla(dash_app_con_callbacks):
    assert len(dash_app_con_callbacks.callback_map) >= 1


def _diagnostico_simulado() -> pd.DataFrame:
    """DataFrame de hallazgos predecible para testear el helper de export.

    No se usa el dataset real ni las reglas de src/diagnostics.py:
    el objetivo es aislar `exportar_diagnostico_csv` de sus dependencias.
    """
    return pd.DataFrame(
        {
            "severidad": ["PRIORITY", "WATCH", "INFO"],
            "categoria": ["Equipo", "Línea", "Proceso"],
            "titulo": ["Alto scrap", "Tendencia", "Nota"],
            "mensaje": ["msg 1", "msg 2", "msg 3"],
            "score": [1.5, 0.8, 0.3],
        }
    )


def test_exportar_diagnostico_csv_con_datos(monkeypatch):
    """La descarga contiene content + filename con timestamp.

    `generar_diagnostico` se sustituye por un mock para aislar el
    helper del dataset y de las reglas de negocio.
    """
    monkeypatch.setattr(
        diag_mod,
        "generar_diagnostico",
        lambda filtrado, capacidad: _diagnostico_simulado(),
    )

    df = pd.DataFrame({"peso": [100.0, 101.0, 99.0]})
    data = df.to_json(orient="split", date_format="iso")

    descarga = exportar_diagnostico_csv(data, None)

    assert descarga is not None
    assert "content" in descarga
    assert "filename" in descarga
    assert descarga["filename"].startswith("industrial_kpi_diagnostico_")
    assert descarga["filename"].endswith(".csv")


def test_exportar_diagnostico_csv_incluye_columnas_del_diagnostico(monkeypatch):
    """El CSV expone las columnas del DataFrame de hallazgos.

    Nota: dcc.send_data_frame en Dash 4.x entrega content como bytes
    del CSV crudo (no base64). Se decodifica directamente.
    """
    monkeypatch.setattr(
        diag_mod,
        "generar_diagnostico",
        lambda filtrado, capacidad: _diagnostico_simulado(),
    )

    df = pd.DataFrame({"peso": [100.0, 101.0, 99.0]})
    data = df.to_json(orient="split", date_format="iso")

    descarga = exportar_diagnostico_csv(data, None)

    contenido = descarga["content"]
    if isinstance(contenido, bytes):
        contenido = contenido.decode("utf-8")

    cabecera = contenido.split("\n")[0]

    for columna_esperada in (
        "severidad",
        "categoria",
        "titulo",
        "mensaje",
        "score",
    ):
        assert columna_esperada in cabecera

    # Verificación de contenido: la primera fila debe ser PRIORITY.
    primera_fila_datos = contenido.split("\n")[1]
    assert "PRIORITY" in primera_fila_datos
    assert "Alto scrap" in primera_fila_datos


@pytest.mark.parametrize(
    "data, capacidad_json",
    [
        ("", None),
        ("", "{}"),
        (pd.DataFrame().to_json(orient="split"), None),
    ],
    ids=[
        "string_vacio",
        "string_vacio_con_capacidad",
        "df_vacio",
    ],
)
def test_exportar_diagnostico_csv_sin_datos_devuelve_none(data, capacidad_json):
    assert exportar_diagnostico_csv(data, capacidad_json) is None


def test_exportar_diagnostico_csv_sin_hallazgos_devuelve_none(monkeypatch):
    """Si `generar_diagnostico` devuelve un DataFrame vacío, no se exporta."""
    monkeypatch.setattr(
        diag_mod,
        "generar_diagnostico",
        lambda filtrado, capacidad: pd.DataFrame(),
    )

    df = pd.DataFrame({"peso": [100.0, 101.0]})
    data = df.to_json(orient="split", date_format="iso")

    assert exportar_diagnostico_csv(data, None) is None