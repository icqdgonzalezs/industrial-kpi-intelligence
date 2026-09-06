from __future__ import annotations

import pandas as pd
import pytest

from dashboard.capability_callbacks import (
    _estado_capacidad,
    _formatear_indice,
    calcular_resumen_capacidad,
    crear_figura_capacidad,
)

VARIABLES_CONFIG = {
    "peso_promedio": {"nombre": "Peso", "lsl": 492.0, "usl": 508.0},
}


def _dataset_json(pesos: list[float]) -> str:
    df = pd.DataFrame({"peso_promedio": pesos})
    return df.to_json(orient="split")


def test_calcular_resumen_capacidad_returns_dataframe():
    data = _dataset_json([498.0, 500.0, 502.0, 499.0, 501.0, 500.5, 499.5])

    resultado = calcular_resumen_capacidad(data, VARIABLES_CONFIG)

    assert not resultado.empty
    assert "cpk" in resultado.columns
    assert resultado.iloc[0]["columna"] == "peso_promedio"


def test_calcular_resumen_capacidad_empty_data_returns_empty_dataframe():
    resultado = calcular_resumen_capacidad(None, VARIABLES_CONFIG)

    assert resultado.empty


@pytest.mark.parametrize(
    ("clasificacion", "esperado"),
    [
        ("Capaz (excelente)", "EXCELLENT"),
        ("Marginal (monitorear)", "WATCH"),
        ("No capaz (acción requerida)", "PRIORITY"),
        ("Datos insuficientes", "NO DATA"),
        ("Límites inválidos", "NO DATA"),
        ("Sin variabilidad", "SPECIAL"),
    ],
)
def test_estado_capacidad_clasifica_correctamente(clasificacion, esperado):
    assert _estado_capacidad(clasificacion) == esperado


def test_formatear_indice_valor_normal():
    assert _formatear_indice(1.2345) == "1.23"


def test_formatear_indice_infinito():
    assert _formatear_indice(float("inf")) == "∞"


def test_formatear_indice_none():
    assert _formatear_indice(None) == "Sin datos"


def test_formatear_indice_nan():
    assert _formatear_indice(float("nan")) == "Sin datos"


def test_crear_figura_capacidad_con_datos_suficientes():
    data = _dataset_json([498.0, 500.0, 502.0, 499.0, 501.0, 500.5, 499.5])
    capacidad = calcular_resumen_capacidad(data, VARIABLES_CONFIG)
    fila = capacidad.iloc[0]

    filtrado = pd.read_json(pd.io.common.StringIO(data), orient="split")

    figura = crear_figura_capacidad(filtrado, fila)

    assert len(figura.data) == 1


def test_crear_figura_capacidad_con_datos_insuficientes():
    filtrado = pd.DataFrame({"peso_promedio": [500.0]})
    fila = pd.Series(
        {"columna": "peso_promedio", "lsl": 492.0, "usl": 508.0, "media": 500.0, "variable": "Peso"}
    )

    figura = crear_figura_capacidad(filtrado, fila)

    assert len(figura.data) == 0
