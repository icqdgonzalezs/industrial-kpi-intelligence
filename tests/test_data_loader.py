from __future__ import annotations

import pandas as pd
import pytest

import dashboard.data_loader as data_loader
from dashboard.data_loader import _adaptar_a_esquema_legacy


def _escribir_csv_canonico(path, n_filas: int = 2) -> None:
    """Escribe un CSV canónico mínimo pero válido (todas las columnas que
    ``dashboard.data_loader._COLUMNAS_CANONICAS_REQUERIDAS`` exige, más
    los 4 campos OEE), para tests rápidos que no dependen de generar el
    dataset completo de 18,078 filas."""
    filas = []
    for i in range(n_filas):
        filas.append(
            {
                "lote": f"LOT-{i:06d}",
                "date": "2024-01-01",
                "line_id": "L1",
                "equipment_id": "L1-FILL-01",
                "shift": "Mañana",
                "operator_id": "OP001",
                "units_produced": 1000,
                "units_defective": 40,
                "units_scrap": 12,
                "units_rework": 28,
                "defect_type": "Bajo peso",
                "peso_promedio": 500.0,
                "longitud_promedio": 120.0,
                "planned_time_min": 480,
                "planned_downtime_min": 45,
                "unplanned_downtime_min": 30,
                "ideal_cycle_time_sec": 6.4,
            }
        )
    pd.DataFrame(filas).to_csv(path, index=False)


def _df_canonico(**overrides) -> pd.DataFrame:
    """DataFrame canónico en memoria (sin pasar por CSV) para tests
    unitarios de la traducción EN→ES."""
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


# ---------------------------------------------------------------------
# Carga real contra el dataset canónico en disco (ADR-0001)
# ---------------------------------------------------------------------


def test_cargar_datos_returns_dataframe_and_config():
    df, config = data_loader.cargar_datos()

    assert isinstance(df, pd.DataFrame)
    assert isinstance(config, dict)
    assert not df.empty


def test_cargar_datos_parses_fecha_column():
    df, _ = data_loader.cargar_datos()

    assert "fecha" in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df["fecha"])


def test_cargar_datos_aplica_el_adaptador_de_esquema():
    """El DataFrame devuelto debe hablar el contrato analítico legacy
    (español) que consumen validation.py/kpis.py/capability.py, no el
    esquema canónico crudo (inglés) del CSV en disco."""
    df, _ = data_loader.cargar_datos()

    columnas_contrato_legacy = {
        "lote", "fecha", "linea", "maquina", "equipo", "turno", "operador",
        "unidades_producidas", "unidades_defectuosas", "unidades_reproceso",
        "unidades_scrap", "defecto_tipo", "peso_promedio", "longitud_promedio",
    }
    assert columnas_contrato_legacy.issubset(df.columns)

    # No deben sobrevivir columnas del esquema canonico sin traducir.
    assert "units_produced" not in df.columns
    assert "line_id" not in df.columns


def test_cargar_datos_preserva_columnas_oee():
    """Las 4 columnas OEE deben pasar intactas por el adaptador — no
    forman parte del contrato legacy en español, pero src/oee.py las
    necesita en inglés tal cual."""
    df, _ = data_loader.cargar_datos()

    for columna in (
        "planned_time_min",
        "planned_downtime_min",
        "unplanned_downtime_min",
        "ideal_cycle_time_sec",
    ):
        assert columna in df.columns


def test_cargar_datos_produce_dataset_valido_segun_validation_py():
    """Integración real: lo que devuelve el loader debe pasar
    validation.py sin que validation.py se haya modificado."""
    from src.validation import obtener_errores_validacion

    df, _ = data_loader.cargar_datos()

    errores = obtener_errores_validacion(df)

    assert not any("equipo no coincide" in error for error in errores)


def test_cargar_datos_es_compatible_con_calcular_kpis_globales():
    """Integración real: el resultado del loader debe poder alimentar
    directamente src.kpis.calcular_kpis_globales sin adaptación adicional."""
    from src.kpis import calcular_kpis_globales

    df, _ = data_loader.cargar_datos()

    kpis = calcular_kpis_globales(df)

    assert kpis["total_producidas"] > 0


# ---------------------------------------------------------------------
# Manejo de errores (archivo faltante, CSV vacío, esquema incompatible)
# ---------------------------------------------------------------------


def test_cargar_datos_raises_when_dataset_is_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(
        data_loader,
        "DATA_PATH",
        tmp_path / "missing.csv",
    )

    with pytest.raises(FileNotFoundError, match="No existe el dataset"):
        data_loader.cargar_datos()


def test_cargar_datos_raises_when_config_is_missing(monkeypatch, tmp_path):
    dataset_path = tmp_path / "data.csv"
    _escribir_csv_canonico(dataset_path)

    monkeypatch.setattr(data_loader, "DATA_PATH", dataset_path)
    monkeypatch.setattr(data_loader, "QUALITY_CONFIG_PATH", tmp_path / "missing.yaml")

    with pytest.raises(FileNotFoundError, match="No existe la configuración"):
        data_loader.cargar_datos()


def test_cargar_datos_raises_when_csv_is_completely_empty(monkeypatch, tmp_path):
    """Archivo existe pero no tiene ni encabezado (0 bytes) -> mensaje
    claro, no el traceback críptico de pandas.errors.EmptyDataError."""
    dataset_path = tmp_path / "data.csv"
    dataset_path.write_text("", encoding="utf-8")

    config_path = tmp_path / "config.yaml"
    config_path.write_text("test: true\n", encoding="utf-8")

    monkeypatch.setattr(data_loader, "DATA_PATH", dataset_path)
    monkeypatch.setattr(data_loader, "QUALITY_CONFIG_PATH", config_path)

    with pytest.raises(ValueError, match="vacío o corrupto"):
        data_loader.cargar_datos()


def test_cargar_datos_raises_when_csv_has_header_but_no_rows(monkeypatch, tmp_path):
    """Archivo con encabezado pero cero filas de datos."""
    dataset_path = tmp_path / "data.csv"
    pd.DataFrame(columns=["lote", "date", "line_id"]).to_csv(dataset_path, index=False)

    config_path = tmp_path / "config.yaml"
    config_path.write_text("test: true\n", encoding="utf-8")

    monkeypatch.setattr(data_loader, "DATA_PATH", dataset_path)
    monkeypatch.setattr(data_loader, "QUALITY_CONFIG_PATH", config_path)

    with pytest.raises(ValueError, match="no contiene registros"):
        data_loader.cargar_datos()


def test_cargar_datos_raises_with_clear_message_when_canonical_columns_missing(
    monkeypatch, tmp_path
):
    """CSV con datos pero sin las columnas que la traducción EN→ES necesita
    -> mensaje que menciona el contrato analítico interno, no un KeyError
    críptico."""
    dataset_path = tmp_path / "data.csv"
    pd.DataFrame({"fecha": ["2024-01-01"], "valor": [1]}).to_csv(dataset_path, index=False)

    config_path = tmp_path / "config.yaml"
    config_path.write_text("test: true\n", encoding="utf-8")

    monkeypatch.setattr(data_loader, "DATA_PATH", dataset_path)
    monkeypatch.setattr(data_loader, "QUALITY_CONFIG_PATH", config_path)

    with pytest.raises(ValueError, match="no es compatible con el contrato analítico interno"):
        data_loader.cargar_datos()


def test_cargar_datos_handles_empty_yaml(monkeypatch, tmp_path):
    dataset_path = tmp_path / "data.csv"
    config_path = tmp_path / "config.yaml"

    _escribir_csv_canonico(dataset_path)
    config_path.write_text("", encoding="utf-8")

    monkeypatch.setattr(data_loader, "DATA_PATH", dataset_path)
    monkeypatch.setattr(data_loader, "QUALITY_CONFIG_PATH", config_path)

    df, config = data_loader.cargar_datos()

    assert isinstance(df, pd.DataFrame)
    assert config == {}


def test_cargar_datos_preserva_numero_de_filas_del_csv_canonico(monkeypatch, tmp_path):
    """El adaptador traduce columnas, no filas: el número de registros
    debe conservarse exactamente."""
    dataset_path = tmp_path / "data.csv"
    _escribir_csv_canonico(dataset_path, n_filas=7)

    config_path = tmp_path / "config.yaml"
    config_path.write_text("test: true\n", encoding="utf-8")

    monkeypatch.setattr(data_loader, "DATA_PATH", dataset_path)
    monkeypatch.setattr(data_loader, "QUALITY_CONFIG_PATH", config_path)

    df, _ = data_loader.cargar_datos()

    assert len(df) == 7


# ---------------------------------------------------------------------
# Traducción EN→ES (consolidada en data_loader desde la Opción D, ADR-0001)
#
# Tests unitarios de `_adaptar_a_esquema_legacy`. Cubren lógica no trivial
# (derivación de columnas, validación de consistencia) que no conviene
# duplicar desde los tests end-to-end de `cargar_datos`.
# ---------------------------------------------------------------------


def test_adaptar_deriva_linea_maquina_equipo_correctamente():
    resultado = _adaptar_a_esquema_legacy(_df_canonico())

    assert resultado.loc[0, "linea"] == "L1"
    assert resultado.loc[0, "equipo"] == "L1-FILL-01"
    assert resultado.loc[0, "maquina"] == "FILL-01"
    assert resultado.loc[1, "linea"] == "L2"
    assert resultado.loc[1, "equipo"] == "L2-CAPPER-01"
    assert resultado.loc[1, "maquina"] == "CAPPER-01"


def test_adaptar_renombra_columnas_directas():
    resultado = _adaptar_a_esquema_legacy(_df_canonico())

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
    resultado = _adaptar_a_esquema_legacy(df)

    for columna in (
        "planned_time_min",
        "planned_downtime_min",
        "unplanned_downtime_min",
        "ideal_cycle_time_sec",
    ):
        assert columna in resultado.columns


def test_adaptar_rechaza_equipment_id_inconsistente_con_line_id():
    df = _df_canonico()
    df.loc[0, "equipment_id"] = "L9-FILL-01"

    with pytest.raises(ValueError, match="no comienza con"):
        _adaptar_a_esquema_legacy(df)