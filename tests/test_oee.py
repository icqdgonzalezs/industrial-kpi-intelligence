"""Tests para el motor OEE (Overall Equipment Effectiveness)."""

from __future__ import annotations

import pandas as pd
import pytest

from src.oee import (
    calcular_oee,
    calcular_oee_fila,
    calcular_oee_ponderado,
    clasificar_oee,
)


# ---------------------------------------------------------------------
# calcular_oee_fila — caso base y componentes
# ---------------------------------------------------------------------


def test_calcular_oee_fila_caso_conocido():
    """Verifica un caso con numeros redondos, calculable a mano.

    planned_time = 480 min, planned_downtime = 60 min (colacion)
    -> tiempo_produccion_planificado = 420 min
    unplanned_downtime = 42 min (fallas)
    -> tiempo_operativo = 378 min = 22,680 seg

    ideal_cycle_time = 10 seg/unidad, units_produced = 2000
    -> rendimiento = (10 * 2000) / 22680 = 20000/22680 = 0.8818...

    units_defective = 100
    -> calidad = (2000-100)/2000 = 0.95

    disponibilidad = 378/420 = 0.9
    oee = 0.9 * 0.8818 * 0.95 = 0.7539 (aprox) -> "Aceptable (mejorable)"
    """
    resultado = calcular_oee_fila(
        planned_time_min=480,
        planned_downtime_min=60,
        unplanned_downtime_min=42,
        ideal_cycle_time_sec=10,
        units_produced=2000,
        units_defective=100,
    )

    assert resultado["disponibilidad"] == pytest.approx(0.9, rel=1e-3)
    assert resultado["rendimiento"] == pytest.approx(0.8818, rel=1e-3)
    assert resultado["calidad"] == pytest.approx(0.95, rel=1e-3)
    assert resultado["oee"] == pytest.approx(0.9 * 0.8818 * 0.95, rel=1e-3)
    assert resultado["clasificacion"] == "Aceptable (mejorable)"


def test_calcular_oee_fila_clase_mundial():
    resultado = calcular_oee_fila(
        planned_time_min=480,
        planned_downtime_min=0,
        unplanned_downtime_min=5,
        ideal_cycle_time_sec=10,
        units_produced=2850,
        units_defective=5,
    )

    assert resultado["oee"] >= 0.85
    assert resultado["clasificacion"] == "Clase mundial"


def test_calcular_oee_fila_disponibilidad_excluye_paro_planificado():
    """Regla de oro del proyecto: Disponibilidad NUNCA penaliza paro planificado."""
    sin_paro_planificado = calcular_oee_fila(
        planned_time_min=480,
        planned_downtime_min=0,
        unplanned_downtime_min=48,
        ideal_cycle_time_sec=10,
        units_produced=2000,
        units_defective=0,
    )

    con_paro_planificado_equivalente = calcular_oee_fila(
        planned_time_min=480,
        planned_downtime_min=60,
        unplanned_downtime_min=42,  # 10% del tiempo de produccion restante (420 min)
        ideal_cycle_time_sec=10,
        units_produced=2000,
        units_defective=0,
    )

    assert sin_paro_planificado["disponibilidad"] == pytest.approx(0.9, rel=1e-3)
    assert con_paro_planificado_equivalente["disponibilidad"] == pytest.approx(
        0.9, rel=1e-3
    )


def test_calcular_oee_fila_rendimiento_se_limita_a_uno():
    """Un ideal_cycle_time mal configurado no debe generar rendimiento > 1.0."""
    resultado = calcular_oee_fila(
        planned_time_min=480,
        planned_downtime_min=0,
        unplanned_downtime_min=0,
        ideal_cycle_time_sec=1000,  # deliberadamente irreal / mal configurado
        units_produced=2000,
        units_defective=0,
    )

    assert resultado["rendimiento"] == 1.0


def test_calcular_oee_fila_sin_produccion_da_componentes_cero():
    resultado = calcular_oee_fila(
        planned_time_min=480,
        planned_downtime_min=0,
        unplanned_downtime_min=480,
        ideal_cycle_time_sec=10,
        units_produced=0,
        units_defective=0,
    )

    assert resultado["disponibilidad"] == 0.0
    assert resultado["rendimiento"] == 0.0
    assert resultado["calidad"] == 0.0
    assert resultado["oee"] == 0.0


def test_calcular_oee_fila_rechaza_downtime_planificado_igual_al_total():
    with pytest.raises(ValueError, match="planned_downtime_min"):
        calcular_oee_fila(
            planned_time_min=480,
            planned_downtime_min=480,
            unplanned_downtime_min=0,
            ideal_cycle_time_sec=10,
            units_produced=0,
            units_defective=0,
        )


def test_calcular_oee_fila_rechaza_downtime_no_planificado_excesivo():
    with pytest.raises(ValueError, match="unplanned_downtime_min"):
        calcular_oee_fila(
            planned_time_min=480,
            planned_downtime_min=60,
            unplanned_downtime_min=500,  # > 420 min disponibles
            ideal_cycle_time_sec=10,
            units_produced=0,
            units_defective=0,
        )


# ---------------------------------------------------------------------
# clasificar_oee
# ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("oee", "esperado"),
    [
        (0.90, "Clase mundial"),
        (0.85, "Clase mundial"),
        (0.70, "Aceptable (mejorable)"),
        (0.60, "Aceptable (mejorable)"),
        (0.45, "Bajo (accion requerida)"),
        (0.0, "Bajo (accion requerida)"),
    ],
)
def test_clasificar_oee(oee, esperado):
    assert clasificar_oee(oee) == esperado


# ---------------------------------------------------------------------
# calcular_oee (DataFrame) — validaciones de entrada
# ---------------------------------------------------------------------


@pytest.fixture
def df_oee_valido() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "planned_time_min": [480, 480],
            "planned_downtime_min": [60, 30],
            "unplanned_downtime_min": [42, 20],
            "ideal_cycle_time_sec": [10, 12],
            "units_produced": [2000, 1800],
            "units_defective": [100, 50],
        }
    )


def test_calcular_oee_dataframe_agrega_columnas_esperadas(df_oee_valido):
    resultado = calcular_oee(df_oee_valido)

    for columna in ("disponibilidad", "rendimiento", "calidad", "oee", "clasificacion"):
        assert columna in resultado.columns

    assert len(resultado) == 2


def test_calcular_oee_rechaza_no_dataframe():
    with pytest.raises(TypeError, match="pandas.DataFrame"):
        calcular_oee([1, 2, 3])


def test_calcular_oee_rechaza_dataset_vacio():
    with pytest.raises(ValueError, match="vacio"):
        calcular_oee(pd.DataFrame(columns=["planned_time_min"]))


def test_calcular_oee_rechaza_columnas_faltantes(df_oee_valido):
    df = df_oee_valido.drop(columns=["ideal_cycle_time_sec"])

    with pytest.raises(ValueError, match="Faltan columnas requeridas para calcular OEE"):
        calcular_oee(df)


def test_calcular_oee_rechaza_nulos(df_oee_valido):
    df = df_oee_valido.copy()
    df.loc[0, "units_produced"] = None

    with pytest.raises(ValueError, match="no pueden contener valores nulos"):
        calcular_oee(df)


def test_calcular_oee_rechaza_defectuosas_mayor_que_producidas(df_oee_valido):
    df = df_oee_valido.copy()
    df.loc[0, "units_defective"] = 999999

    with pytest.raises(ValueError, match="units_defective no puede superar"):
        calcular_oee(df)


def test_calcular_oee_rechaza_planned_time_no_positivo(df_oee_valido):
    df = df_oee_valido.copy()
    df.loc[0, "planned_time_min"] = 0

    with pytest.raises(ValueError, match="planned_time_min"):
        calcular_oee(df)


def test_calcular_oee_rechaza_ideal_cycle_time_no_positivo(df_oee_valido):
    df = df_oee_valido.copy()
    df.loc[0, "ideal_cycle_time_sec"] = 0

    with pytest.raises(ValueError, match="ideal_cycle_time_sec"):
        calcular_oee(df)


def test_calcular_oee_rechaza_downtime_negativo(df_oee_valido):
    df = df_oee_valido.copy()
    df.loc[0, "unplanned_downtime_min"] = -1

    with pytest.raises(ValueError, match="unplanned_downtime_min"):
        calcular_oee(df)


# ---------------------------------------------------------------------
# calcular_oee_ponderado — agregacion de planta
# ---------------------------------------------------------------------


def test_calcular_oee_ponderado_no_promedia_oee_directamente(df_oee_valido):
    """El OEE ponderado no debe ser el promedio simple de OEE por fila.

    Es la misma trampa de agregacion documentada en kpis.py: promediar
    tasas sin considerar volumen produce un numero sesgado.
    """
    detalle = calcular_oee(df_oee_valido)
    promedio_simple = detalle["oee"].mean()

    ponderado = calcular_oee_ponderado(df_oee_valido)

    # No exigimos que sean distintos siempre (podrian coincidir por
    # casualidad con datos simetricos), pero s? que el resultado se
    # derive de componentes agregados, no de un .mean() de la columna oee.
    assert ponderado["oee"] == pytest.approx(
        ponderado["disponibilidad"] * ponderado["rendimiento"] * ponderado["calidad"],
        abs=1e-3,  # tolerancia por redondeo a 4 decimales de cada componente
    )
    assert isinstance(promedio_simple, float)  # sanity check de que existe


def test_calcular_oee_ponderado_incluye_totales(df_oee_valido):
    resultado = calcular_oee_ponderado(df_oee_valido)

    assert resultado["units_produced_total"] == 3800
    assert resultado["units_defective_total"] == 150
    assert resultado["n_registros"] == 2
    assert 0.0 <= resultado["oee"] <= 1.0


def test_calcular_oee_ponderado_clasificacion_consistente(df_oee_valido):
    resultado = calcular_oee_ponderado(df_oee_valido)

    assert resultado["clasificacion"] == clasificar_oee(resultado["oee"])
