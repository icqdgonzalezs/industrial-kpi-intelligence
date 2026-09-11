"""Tests para el adaptador de esquema (ADR-0001, Camino A)."""

from __future__ import annotations

import pandas as pd
import pytest

from src.schema_adapter import (
    COLUMNAS_CONTRATO_LEGACY,
    adaptar_a_esquema_legacy,
)


def _df_canonico(**overrides) -> pd.DataFrame:
    base = {
        "lote": ["LOT-000001", "LOT-000002"],
        "date": ["2024-01-01", "2024-01-02"],
        "line_id": ["L1", "L2"],
        "equipment_id": ["L1-FILL-01", "L2-CAPPER-01"],
        "shift": ["Mañana", "Noche"],
        "operator_id": ["OP001", "OP017"],
        "units_produced": [1000, 900],
        "units_defective": [40, 30],
        "units_scrap": [12, 9],
        "units_rework": [28, 21],
        "defect_type": ["Bajo peso", "Defecto de sellado"],
        "peso_promedio": [500.1, 499.5],
        "longitud_promedio": [120.0, 119.8],
    }
    base.update(overrides)
    return pd.DataFrame(base)


def test_adaptar_produce_exactamente_el_contrato_legacy():
    resultado = adaptar_a_esquema_legacy(_df_canonico())
    assert set(COLUMNAS_CONTRATO_LEGACY).issubset(resultado.columns)


def test_adaptar_deriva_linea_maquina_equipo_correctamente():
    resultado = adaptar_a_esquema_legacy(_df_canonico())
    assert resultado.loc[0, "linea"] == "L1"
    assert resultado.loc[0, "equipo"] == "L1-FILL-01"
    assert resultado.loc[0, "maquina"] == "FILL-01"
    assert resultado.loc[1, "linea"] == "L2"
    assert resultado.loc[1, "equipo"] == "L2-CAPPER-01"
    assert resultado.loc[1, "maquina"] == "CAPPER-01"


def test_adaptar_renombra_columnas_directas():
    resultado = adaptar_a_esquema_legacy(_df_canonico())
    assert resultado.loc[0, "fecha"] == "2024-01-01"
    assert resultado.loc[0, "turno"] == "Mañana"
    assert resultado.loc[0, "operador"] == "OP001"
    assert resultado.loc[0, "unidades_producidas"] == 1000
    assert resultado.loc[0, "unidades_defectuosas"] == 40
    assert resultado.loc[0, "unidades_scrap"] == 12
    assert resultado.loc[0, "unidades_reproceso"] == 28
    assert resultado.loc[0, "defecto_tipo"] == "Bajo peso"


def test_adaptar_preserva_columnas_oee_si_estan_presentes():
    df = _df_canonico(
        planned_time_min=[480, 480],
        planned_downtime_min=[45, 45],
        unplanned_downtime_min=[30, 25],
        ideal_cycle_time_sec=[6.4, 5.7],
    )
    resultado = adaptar_a_esquema_legacy(df)
    for columna in (
        "planned_time_min",
        "planned_downtime_min",
        "unplanned_downtime_min",
        "ideal_cycle_time_sec",
    ):
        assert columna in resultado.columns


def test_adaptar_funciona_sin_columnas_oee():
    resultado = adaptar_a_esquema_legacy(_df_canonico())
    assert "planned_time_min" not in resultado.columns


def test_adaptar_produce_dataset_valido_segun_validation_py():
    """Prueba de integracion: el resultado del adaptador debe pasar
    validation.py._validar_equipo SIN que validation.py se modifique."""
    from src.validation import obtener_errores_validacion

    resultado = adaptar_a_esquema_legacy(_df_canonico())
    errores = obtener_errores_validacion(resultado)
    assert not any("equipo no coincide" in error for error in errores)


def test_adaptar_rechaza_no_dataframe():
    with pytest.raises(TypeError, match="pandas.DataFrame"):
        adaptar_a_esquema_legacy([1, 2, 3])


def test_adaptar_rechaza_dataset_vacio():
    with pytest.raises(ValueError, match="vacio"):
        adaptar_a_esquema_legacy(pd.DataFrame(columns=["lote"]))


def test_adaptar_rechaza_columnas_canonicas_faltantes():
    df = _df_canonico().drop(columns=["equipment_id"])
    with pytest.raises(ValueError, match="Faltan columnas del esquema canonico"):
        adaptar_a_esquema_legacy(df)


def test_adaptar_rechaza_equipment_id_inconsistente_con_line_id():
    df = _df_canonico()
    df.loc[0, "equipment_id"] = "L9-FILL-01"
    with pytest.raises(ValueError, match="no comienza con"):
        adaptar_a_esquema_legacy(df)


def test_adaptar_es_idempotente_en_columnas_identicas():
    df = _df_canonico()
    resultado = adaptar_a_esquema_legacy(df)
    assert resultado["lote"].tolist() == df["lote"].tolist()
    assert resultado["peso_promedio"].tolist() == df["peso_promedio"].tolist()
    assert resultado["longitud_promedio"].tolist() == df["longitud_promedio"].tolist()