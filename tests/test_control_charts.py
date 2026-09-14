import pandas as pd
import pytest

from src.control_charts import (
    calcular_limites_control,
    calcular_moving_range,
    detectar_fuera_de_control,
    resumen_control_estadistico,
)


def test_calcular_moving_range():
    serie = pd.Series([10, 12, 9, 15])
    mr = calcular_moving_range(serie)
    assert mr.tolist()[1:] == [2, 3, 6]


def test_calcular_limites_control_proceso_estable():
    serie = pd.Series([100, 101, 99, 102, 98, 100, 101])
    limites = calcular_limites_control(serie)
    assert limites["lcl"] < limites["media"] < limites["ucl"]


def test_calcular_limites_control_rechaza_no_series():
    with pytest.raises(TypeError):
        calcular_limites_control([1, 2, 3])


def test_calcular_limites_control_rechaza_vacio():
    with pytest.raises(ValueError):
        calcular_limites_control(pd.Series([], dtype=float))


def test_detectar_fuera_de_control_detecta_outlier():
    serie = pd.Series([100, 101, 99, 100, 101, 99, 100, 500])
    limites = calcular_limites_control(serie)
    fuera = detectar_fuera_de_control(serie, limites)
    assert fuera.iloc[-1]
    assert not fuera.iloc[0]


def test_detectar_fuera_de_control_proceso_estable_sin_alertas():
    serie = pd.Series([100, 101, 99, 100, 101, 99, 100])
    limites = calcular_limites_control(serie)
    fuera = detectar_fuera_de_control(serie, limites)
    assert not fuera.any()


def _serie_estable(n: int = 200) -> pd.Series:
    """Serie determinística con variación pequeña alrededor de 100.
    Patrón repetitivo que produce MR_bar estable."""
    return pd.Series([100 + (i % 5) - 2 for i in range(n)], dtype=float)


def test_resumen_control_estadistico_retorna_claves_esperadas():
    serie = _serie_estable()
    limites = calcular_limites_control(serie)

    resumen = resumen_control_estadistico(serie, limites)

    assert set(resumen.keys()) == {
        "observados",
        "esperados",
        "ratio",
        "n",
        "estado",
        "mensaje",
    }


def test_resumen_control_estadistico_calcula_esperados_correctamente():
    serie = _serie_estable(n=1000)
    limites = calcular_limites_control(serie)

    resumen = resumen_control_estadistico(serie, limites)

    assert resumen["esperados"] == round(1000 * 0.0027, 1)
    assert resumen["n"] == 1000


def test_resumen_control_estadistico_proceso_estable():
    serie = _serie_estable(n=200)
    limites = calcular_limites_control(serie)

    resumen = resumen_control_estadistico(serie, limites)

    assert resumen["estado"] == "estable"
    assert "dentro del rango esperado" in resumen["mensaje"]


def test_resumen_control_estadistico_ignora_nan():
    serie = pd.Series([100, 101, 99, None, 100, 101, 99, 100], dtype=float)
    limites = calcular_limites_control(serie.dropna())

    resumen = resumen_control_estadistico(serie, limites)

    assert resumen["n"] == 7