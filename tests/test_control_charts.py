import pandas as pd
import pytest

from src.control_charts import (
    calcular_limites_control,
    calcular_moving_range,
    detectar_fuera_de_control,
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
