import pandas as pd

from dashboard.control_charts_callbacks import crear_figura_i, crear_figura_mr
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
    assert figura.data[0].marker.color[-1] == "#ef4444"
    assert figura.data[0].marker.color[0] == "#38bdf8"


def test_crear_figura_mr():
    serie = pd.Series([100, 101, 99, 100])
    mr = calcular_moving_range(serie).dropna().reset_index(drop=True)
    figura = crear_figura_mr(mr, mr.mean())
    assert len(figura.data) == 1
