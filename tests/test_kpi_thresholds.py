"""Tests de la clasificación semántica de KPIs."""

from __future__ import annotations

import pytest

from src.kpi_thresholds import clasificar_kpi

# ---------------------------------------------------------------------
# Sin umbrales → siempre NEUTRAL
# ---------------------------------------------------------------------


def test_sin_umbrales_retorna_neutral():
    assert clasificar_kpi(0.95, None) == "neutral"


def test_sin_direccion_retorna_neutral():
    assert clasificar_kpi(0.95, {"success": 0.90}) == "neutral"


# ---------------------------------------------------------------------
# higher_is_better (FPY)
# ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (0.98, "success"),
        (0.95, "success"),         # borde exacto de success
        (0.92, "warning"),
        (0.90, "warning"),         # borde exacto de warning
        (0.85, "danger"),
        (0.50, "danger"),
    ],
)
def test_higher_is_better_fpy(valor, esperado):
    resultado = clasificar_kpi(
        valor,
        {"success": 0.95, "warning": 0.90},
        "higher_is_better",
    )
    assert resultado == esperado


# ---------------------------------------------------------------------
# lower_is_better (Defectos, Scrap, Reproceso)
# ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        (0.01, "success"),
        (0.03, "success"),         # borde exacto de success
        (0.04, "warning"),
        (0.05, "warning"),         # borde exacto de warning
        (0.08, "danger"),
        (0.15, "danger"),
    ],
)
def test_lower_is_better_defectos(valor, esperado):
    resultado = clasificar_kpi(
        valor,
        {"success": 0.03, "warning": 0.05},
        "lower_is_better",
    )
    assert resultado == esperado




# ---------------------------------------------------------------------
# Loader de umbrales desde YAML
# ---------------------------------------------------------------------


def test_cargar_umbrales_kpi_lee_del_yaml_del_proyecto():
    from src.kpi_thresholds import cargar_umbrales_kpi

    umbrales = cargar_umbrales_kpi()

    assert "fpy" in umbrales
    assert "tasa_defectos" in umbrales
    assert "tasa_scrap" in umbrales
    assert umbrales["fpy"]["direction"] == "higher_is_better"


def test_cargar_umbrales_kpi_retorna_dict_vacio_si_no_existe(tmp_path):
    from src.kpi_thresholds import cargar_umbrales_kpi

    umbrales = cargar_umbrales_kpi(path=tmp_path / "no_existe.yaml")

    assert umbrales == {}



# ---------------------------------------------------------------------
# Wrapper por nombre (clasificar_kpi_por_nombre)
# ---------------------------------------------------------------------


def test_clasificar_kpi_por_nombre_usa_yaml_por_defecto():
    from src.kpi_thresholds import clasificar_kpi_por_nombre

    assert clasificar_kpi_por_nombre("fpy", 0.97) == "success"
    assert clasificar_kpi_por_nombre("tasa_scrap", 0.005) == "success"
    assert clasificar_kpi_por_nombre("tasa_defectos", 0.10) == "danger"


def test_clasificar_kpi_por_nombre_retorna_neutral_si_kpi_no_existe():
    from src.kpi_thresholds import clasificar_kpi_por_nombre

    assert clasificar_kpi_por_nombre("kpi_inventado", 0.5) == "neutral"


def test_clasificar_kpi_por_nombre_acepta_umbrales_inyectados():
    from src.kpi_thresholds import clasificar_kpi_por_nombre

    umbrales_test = {
        "mi_kpi": {
            "direction": "higher_is_better",
            "success": 0.99,
            "warning": 0.95,
        }
    }

    assert (
        clasificar_kpi_por_nombre("mi_kpi", 0.995, umbrales=umbrales_test)
        == "success"
    )
    assert (
        clasificar_kpi_por_nombre("mi_kpi", 0.80, umbrales=umbrales_test)
        == "danger"
    )