from pathlib import Path

import pandas as pd

from src.data_generator import (
    DEFECT_TYPE_DIST,
    GENERATOR_CONFIG,
    generate_production_data,
)


def test_generator_config_contains_required_sections():
    required = {
        "generation",
        "shift_effects",
        "generation_limits",
        "scrap_rework",
        "production_per_shift",
        "base_defect_rate_pct",
        "defect_type_distribution",
        "drift_events",
        "product_effect",
    }
    assert required.issubset(GENERATOR_CONFIG)


def test_defect_distributions_sum_to_one():
    for distribution in DEFECT_TYPE_DIST.values():
        assert abs(sum(distribution.values()) - 1.0) < 1e-9


def test_generated_dataset_has_expected_structure():
    df = generate_production_data()

    required_columns = {
        "timestamp",
        "date",
        "year",
        "month",
        "week",
        "shift",
        "operator_id",
        "line_id",
        "equipment_id",
        "equipment_type",
        "product_id",
        "units_produced",
        "units_defective",
        "units_scrap",
        "units_rework",
        "defect_type",
    }

    assert required_columns.issubset(df.columns)
    assert len(df) > 0


def test_generated_dataset_respects_core_constraints():
    df = generate_production_data()

    assert (df["units_produced"] >= 0).all()
    assert (df["units_defective"] <= df["units_produced"]).all()
    assert (df["units_scrap"] <= df["units_defective"]).all()
    assert (df["units_rework"] <= df["units_defective"]).all()
    assert (
        df["units_defective"]
        == df["units_scrap"] + df["units_rework"]
    ).all()


def test_generated_dataset_is_reproducible():
    first = generate_production_data()
    second = generate_production_data()

    pd.testing.assert_frame_equal(first, second)


def test_generator_config_file_exists():
    config_path = Path("config/generator_config.yaml")
    assert config_path.exists()


def test_main_creates_output_file(tmp_path, monkeypatch):
    import src.data_generator as generator

    monkeypatch.chdir(tmp_path)
    generator.main()

    output_path = tmp_path / "data" / "raw" / "synthetic_production_data.csv"

    assert output_path.exists()

    df = pd.read_csv(output_path)

    assert not df.empty
    # 16 columnas originales + 7 nuevas: lote, peso_promedio,
    # longitud_promedio, planned_time_min, planned_downtime_min,
    # unplanned_downtime_min, ideal_cycle_time_sec (ver ADR-0001 / Fix OEE).
    assert len(df.columns) == 23


# ---------------------------------------------------------------------
# NUEVO: columnas de OEE y variables continuas (ADR-0001 / Fix OEE)
# ---------------------------------------------------------------------


def test_generated_dataset_has_oee_columns():
    df = generate_production_data()

    required_oee_columns = {
        "planned_time_min",
        "planned_downtime_min",
        "unplanned_downtime_min",
        "ideal_cycle_time_sec",
    }

    assert required_oee_columns.issubset(df.columns)


def test_generated_dataset_has_lote_column_and_is_unique():
    df = generate_production_data()

    assert "lote" in df.columns
    assert df["lote"].is_unique
    assert df["lote"].iloc[0] == "LOT-000001"


def test_generated_dataset_has_continuous_quality_variables():
    df = generate_production_data()

    assert "peso_promedio" in df.columns
    assert "longitud_promedio" in df.columns
    assert df["peso_promedio"].between(400, 600).all()
    assert df["longitud_promedio"].between(100, 140).all()


def test_generated_dataset_respects_oee_physical_constraints():
    """unplanned_downtime_min nunca puede superar el tiempo de produccion
    planificado (planned_time_min - planned_downtime_min), o Disponibilidad
    en src/oee.py se volveria negativa."""
    df = generate_production_data()

    tiempo_produccion_planificado = (
        df["planned_time_min"] - df["planned_downtime_min"]
    )

    assert (df["unplanned_downtime_min"] >= 0).all()
    assert (df["unplanned_downtime_min"] <= tiempo_produccion_planificado).all()
    assert (df["ideal_cycle_time_sec"] > 0).all()
    assert (df["planned_time_min"] - df["planned_downtime_min"] > 0).all()


def test_generated_dataset_performance_is_not_saturated_at_one():
    """Regresion: una version anterior de este generador producia
    units_produced independiente del paro no planificado, saturando
    Rendimiento en 1.0 para practicamente todas las filas. Verifica que
    exista variabilidad real (no un valor constante)."""
    from src.oee import calcular_oee

    df = generate_production_data()
    resultado = calcular_oee(df)

    assert resultado["rendimiento"].std() > 0.01
    assert resultado["rendimiento"].min() < 0.95


def test_generated_dataset_oee_is_computable_end_to_end():
    """El dataset generado debe poder alimentar src/oee.py sin errores,
    con valores de OEE en un rango fisicamente valido."""
    from src.oee import calcular_oee_ponderado

    df = generate_production_data()
    resultado = calcular_oee_ponderado(df)

    assert 0.0 <= resultado["oee"] <= 1.0
    assert 0.0 <= resultado["disponibilidad"] <= 1.0
    assert 0.0 <= resultado["rendimiento"] <= 1.0
    assert 0.0 <= resultado["calidad"] <= 1.0
