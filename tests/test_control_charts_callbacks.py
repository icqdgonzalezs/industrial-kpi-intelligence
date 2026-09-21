"""Tests de los callbacks de control I-MR.

Verifica que las figuras se construyan con la estructura correcta y los
colores del tema industrial oscuro (marcador out-of-control rojo,
resto claro sobre fondo oscuro).

Y el export CSV (Fase 3a-γ) + el empty state (Fase 3b.2).
"""

import pandas as pd
import pytest

from dashboard.control_charts_callbacks import (
    construir_outputs_control,
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


# ---------------------------------------------------------------------
# construir_outputs_control (Fase 3b.2 — empty states)
# ---------------------------------------------------------------------


def test_construir_outputs_control_con_datos():
    """Con datos suficientes: 5 outputs, contenido normal visible."""
    df = pd.DataFrame({"peso": [100.0, 101.0, 99.0, 100.0, 101.0, 99.5]})
    data = df.to_json(orient="split", date_format="iso")

    resultado = construir_outputs_control(data, "peso")

    assert len(resultado) == 5
    # status es str
    assert isinstance(resultado[0], str)
    # figuras con datos
    assert len(resultado[1].data) == 1
    assert len(resultado[2].data) == 1
    # contenido normal visible
    assert resultado[3] == {"display": "block"}
    # sin empty
    assert resultado[4] == []


def test_construir_outputs_control_sin_datos_devuelve_empty_state():
    """Con 0 filas: contenido normal oculto, empty_state visible."""
    resultado = construir_outputs_control("", "peso")

    assert len(resultado) == 5
    assert resultado[0] == "Sin datos."
    # contenido normal oculto
    assert resultado[3] == {"display": "none"}
    # empty_state presente
    assert resultado[4].className == "empty-state"
    textos = [child.children for child in resultado[4].children]
    assert "Sin datos para la variable y filtros actuales" in textos


def test_construir_outputs_control_incluye_hint_de_accion():
    """El empty state incluye un hint sugiriendo la acción al operador."""
    resultado = construir_outputs_control("", "peso")

    textos = [child.children for child in resultado[4].children]
    # El hint tiene la acción sugerida
    assert any("Restaurar" in str(t) or "filtros" in str(t) for t in textos)


def test_construir_outputs_control_columna_inexistente():
    """Si la columna no existe en el DataFrame: empty state."""
    df = pd.DataFrame({"otra": [100.0, 101.0]})
    data = df.to_json(orient="split", date_format="iso")

    resultado = construir_outputs_control(data, "peso")

    assert resultado[3] == {"display": "none"}
    assert resultado[4].className == "empty-state"


def test_construir_outputs_control_serie_corta():
    """Con 1 solo punto: empty state (no hay MR posible)."""
    df = pd.DataFrame({"peso": [100.0]})
    data = df.to_json(orient="split", date_format="iso")

    resultado = construir_outputs_control(data, "peso")

    assert resultado[3] == {"display": "none"}
    assert resultado[4].className == "empty-state"


# ---------------------------------------------------------------------
# Export CSV (Fase 3a-γ)
# ---------------------------------------------------------------------


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
