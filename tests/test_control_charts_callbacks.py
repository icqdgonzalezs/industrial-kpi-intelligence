"""Tests de los callbacks de control I-MR.

Verifica que las figuras se construyan con la estructura correcta y los
colores del tema industrial oscuro (marcador out-of-control rojo,
resto claro sobre fondo oscuro).

Y el export CSV (Fase 3a-γ): tabla I-MR unificada con columnas de
límites constantes, o None si no hay datos exportables.
"""

import pandas as pd
import pytest

from dashboard.control_charts_callbacks import (
    crear_figura_i,
    crear_figura_mr,
    exportar_control_csv,
)
from src.control_charts import (
    calcular_limites_control,
    calcular_moving_range,
    detectar_fuera_de_control,
)


def test_crear_figura_i():
    serie = pd.Series([100, 101, 99, 100, 101, 99, 100, 500])
    limites = calcular_limites_control(serie)
    fuera = detectar_fuera_de_control(serie, limites)
    figura = crear_figura_i(serie, limites, fuera)

    assert len(figura.data) == 1
    # El último punto (500) debe estar marcado como fuera de control (rojo).
    assert figura.data[0].marker.color[-1] == "#ef4444"
    # Los puntos normales usan el color de texto claro del tema oscuro.
    assert figura.data[0].marker.color[0] == "#e6edf3"


def test_crear_figura_mr():
    serie = pd.Series([100, 101, 99, 100])
    mr = calcular_moving_range(serie).dropna().reset_index(drop=True)
    figura = crear_figura_mr(mr, mr.mean())

    assert len(figura.data) == 1


def test_exportar_control_csv_con_datos():
    """La descarga contiene content + filename con timestamp."""
    df = pd.DataFrame({"peso": [100.0, 101.0, 99.0, 100.0, 101.0]})
    data = df.to_json(orient="split", date_format="iso")

    descarga = exportar_control_csv(data, "peso")

    assert descarga is not None
    assert "content" in descarga
    assert "filename" in descarga
    assert descarga["filename"].startswith("industrial_kpi_control_")
    assert descarga["filename"].endswith(".csv")


def test_exportar_control_csv_incluye_columnas_del_analisis_imr():
    """El CSV es autocontenido: serie I + MR + límites constantes.

    Nota: dcc.send_data_frame en Dash 4.x entrega el content como
    bytes del CSV crudo (no base64 como en versiones anteriores).
    Se decodifica directamente si viene en bytes.
    """
    df = pd.DataFrame({"peso": [100.0, 101.0, 99.0, 100.0, 101.0]})
    data = df.to_json(orient="split", date_format="iso")

    descarga = exportar_control_csv(data, "peso")
    contenido = descarga["content"]
    if isinstance(contenido, bytes):
        contenido = contenido.decode("utf-8")
    cabecera = contenido.split("\n")[0]

    for columna_esperada in (
        "indice",
        "valor",
        "fuera_control",
        "moving_range",
        "cl",
        "ucl",
        "lcl",
        "mr_bar",
        "ucl_mr",
    ):
        assert columna_esperada in cabecera


@pytest.mark.parametrize(
    "data, columna",
    [
        ("", "peso"),
        (pd.DataFrame().to_json(orient="split"), "peso"),
        (
            pd.DataFrame({"peso": [100, 101]}).to_json(orient="split"),
            None,
        ),
        (
            pd.DataFrame({"peso": [100, 101]}).to_json(orient="split"),
            "inexistente",
        ),
        (
            pd.DataFrame({"peso": [100]}).to_json(orient="split"),
            "peso",
        ),
    ],
    ids=[
        "string_vacio",
        "df_vacio",
        "columna_none",
        "columna_inexistente",
        "serie_corta",
    ],
)
def test_exportar_control_csv_sin_datos_devuelve_none(data, columna):
    assert exportar_control_csv(data, columna) is None