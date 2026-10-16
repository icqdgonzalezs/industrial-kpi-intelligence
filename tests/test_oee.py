"""Tests para el motor OEE (Overall Equipment Effectiveness)."""

from __future__ import annotations

import pandas as pd
import pytest

from src.oee import (
    CLASIFICACION_ACCEPTABLE,
    CLASIFICACION_LOW,
    CLASIFICACION_WORLD_CLASS,
    adaptar_contrato_canonico,
    calcular_oee,
    calcular_oee_fila,
    calcular_oee_ponderado,
    clasificar_oee,
)

# ---------------------------------------------------------------------
# calcular_oee_fila — caso base y componentes
# ---------------------------------------------------------------------


def test_calcular_oee_fila_caso_conocido():
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
    assert resultado["clasificacion"] == CLASIFICACION_ACCEPTABLE


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
    assert resultado["clasificacion"] == CLASIFICACION_WORLD_CLASS


def test_calcular_oee_fila_disponibilidad_excluye_paro_planificado():
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
        unplanned_downtime_min=42,
        ideal_cycle_time_sec=10,
        units_produced=2000,
        units_defective=0,
    )
    assert sin_paro_planificado["disponibilidad"] == pytest.approx(0.9, rel=1e-3)
    assert con_paro_planificado_equivalente["disponibilidad"] == pytest.approx(
        0.9, rel=1e-3
    )


def test_calcular_oee_fila_rendimiento_se_limita_a_uno():
    resultado = calcular_oee_fila(
        planned_time_min=480,
        planned_downtime_min=0,
        unplanned_downtime_min=0,
        ideal_cycle_time_sec=1000,
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
            unplanned_downtime_min=500,
            ideal_cycle_time_sec=10,
            units_produced=0,
            units_defective=0,
        )


# ---------------------------------------------------------------------
# clasificar_oee — devuelve keys estables, no labels
# ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("oee", "esperado"),
    [
        (0.90, CLASIFICACION_WORLD_CLASS),
        (0.85, CLASIFICACION_WORLD_CLASS),
        (0.70, CLASIFICACION_ACCEPTABLE),
        (0.60, CLASIFICACION_ACCEPTABLE),
        (0.45, CLASIFICACION_LOW),
        (0.0, CLASIFICACION_LOW),
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
    for columna in (
        "disponibilidad",
        "rendimiento",
        "calidad",
        "oee",
        "clasificacion",
    ):
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
    ponderado = calcular_oee_ponderado(df_oee_valido)
    assert ponderado["oee"] == pytest.approx(
        ponderado["disponibilidad"] * ponderado["rendimiento"] * ponderado["calidad"],
        abs=1e-3,
    )


def test_calcular_oee_ponderado_incluye_totales(df_oee_valido):
    resultado = calcular_oee_ponderado(df_oee_valido)
    assert resultado["units_produced_total"] == 3800
    assert resultado["units_defective_total"] == 150
    assert resultado["n_registros"] == 2
    assert 0.0 <= resultado["oee"] <= 1.0


def test_calcular_oee_ponderado_clasificacion_consistente(df_oee_valido):
    resultado = calcular_oee_ponderado(df_oee_valido)
    assert resultado["clasificacion"] == clasificar_oee(resultado["oee"])

# ---------------------------------------------------------------------
# FRONTERA: adapter del contrato canónico
# ---------------------------------------------------------------------

def test_adaptar_contrato_canonico_renombra_y_no_muta() -> None:
    """Renombra las 2 columnas ES→EN, preserva valores, no muta el input."""
    df = pd.DataFrame(
        {
            "unidades_producidas": [100, 200],
            "unidades_defectuosas": [5, 10],
            "planned_time_min": [480.0, 480.0],
        }
    )

    adaptado = adaptar_contrato_canonico(df)

    assert "units_produced" in adaptado.columns
    assert "units_defective" in adaptado.columns
    assert "unidades_producidas" not in adaptado.columns
    assert "unidades_defectuosas" not in adaptado.columns

    # No mutación del input (regla del proyecto: nada de inplace=True)
    assert "unidades_producidas" in df.columns
    assert "units_produced" not in df.columns

    # Valores preservados
    assert adaptado["units_produced"].tolist() == [100, 200]
    assert adaptado["units_defective"].tolist() == [5, 10]


def test_adaptar_contrato_canonico_falla_si_faltan_columnas() -> None:
    """Sin las columnas canónicas, falla explícito (no fabrica datos)."""
    df = pd.DataFrame({"planned_time_min": [480.0]})

    with pytest.raises(ValueError, match="Faltan columnas canónicas"):
        adaptar_contrato_canonico(df)


def test_frontera_dataset_real_pasa_por_oee() -> None:
    """Frontera real: dataset canónico → adapter → OEE corre sin error.

    Este test es el que hubiera detectado el bug de IA.3. Los tests
    unitarios de test_oee.py usan DataFrames sintéticos en inglés y no
    cruzan la frontera entre data_loader y oee.
    """
    from app.services.dataset_loader import cargar_dataset_filtrado

    df, _ = cargar_dataset_filtrado(linea="L1")
    adaptado = adaptar_contrato_canonico(df)
    resultado = calcular_oee_ponderado(adaptado)

    assert 0.0 <= resultado["oee"] <= 1.0
    assert resultado["n_registros"] > 0
    assert resultado["units_produced_total"] > 0
