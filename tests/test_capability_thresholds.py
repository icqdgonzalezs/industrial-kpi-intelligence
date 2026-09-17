"""Tests para src.capability_thresholds (SSOT de umbrales Ppk/PPM)."""

from __future__ import annotations

import pytest
import yaml

from src.capability_thresholds import (
    DEFAULT_PPK_THRESHOLDS,
    DEFAULT_PPM_THRESHOLDS,
    cargar_umbrales_ppk,
    cargar_umbrales_ppm,
    clasificar_ppk_puro,
    clasificar_rendimiento_ppm_puro,
)

# ---------------------------------------------------------------------
# clasificar_ppk_puro (función pura)
# ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("ppk", "esperado"),
    [
        (2.50, "Clase mundial"),
        (1.67, "Clase mundial"),  # frontera inferior
        (1.66, "Capaz"),
        (1.33, "Capaz"),          # frontera inferior
        (1.32, "Marginal"),
        (1.00, "Marginal"),       # frontera inferior
        (0.99, "No capaz"),
        (-1.00, "No capaz"),
        (float("inf"), "Clase mundial"),
        (float("-inf"), "No capaz"),
    ],
)
def test_clasificar_ppk_puro_escala_completa(ppk, esperado):
    """Las 4 fronteras AIAG SPC se respetan con umbrales default."""
    assert clasificar_ppk_puro(ppk, None) == esperado


def test_clasificar_ppk_puro_con_umbrales_custom():
    """Permite inyectar umbrales distintos (SaaS multi-cliente)."""
    umbrales_estrictos = {"clase_mundial": 2.00, "capaz": 1.67, "marginal": 1.33}
    assert clasificar_ppk_puro(1.80, umbrales_estrictos) == "Capaz"
    assert clasificar_ppk_puro(1.50, umbrales_estrictos) == "Marginal"
    assert clasificar_ppk_puro(1.00, umbrales_estrictos) == "No capaz"


def test_clasificar_ppk_puro_con_umbrales_vacios_usa_defaults():
    """Dict vacío → fallback a defaults (comportamiento seguro)."""
    assert clasificar_ppk_puro(1.67, {}) == "Clase mundial"


def test_clasificar_ppk_puro_con_umbrales_parciales():
    """Umbrales incompletos → fallback por clave individual."""
    parcial = {"clase_mundial": 2.00}  # faltan capaz, marginal
    assert clasificar_ppk_puro(2.00, parcial) == "Clase mundial"
    assert clasificar_ppk_puro(1.33, parcial) == "Capaz"  # default


# ---------------------------------------------------------------------
# clasificar_rendimiento_ppm_puro (función pura)
# ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("ppm", "esperado"),
    [
        (0, "world_class"),
        (50, "world_class"),
        (100, "world_class"),    # frontera superior inclusiva
        (101, "acceptable"),
        (500, "acceptable"),
        (1000, "acceptable"),    # frontera superior inclusiva
        (1001, "low"),
        (400_000, "low"),
    ],
)
def test_clasificar_rendimiento_ppm_puro_escala_completa(ppm, esperado):
    assert clasificar_rendimiento_ppm_puro(ppm, None) == esperado


def test_clasificar_rendimiento_ppm_puro_con_umbrales_custom():
    estrictos = {"world_class": 10, "acceptable": 100}
    assert clasificar_rendimiento_ppm_puro(50, estrictos) == "acceptable"
    assert clasificar_rendimiento_ppm_puro(200, estrictos) == "low"


# ---------------------------------------------------------------------
# cargar_umbrales_ppk / cargar_umbrales_ppm (I/O desde YAML)
# ---------------------------------------------------------------------


def test_cargar_umbrales_ppk_lee_yaml_del_proyecto():
    """El YAML real del proyecto tiene la escala AIAG correcta."""
    umbrales = cargar_umbrales_ppk()
    assert umbrales["clase_mundial"] == 1.67
    assert umbrales["capaz"] == 1.33
    assert umbrales["marginal"] == 1.00


def test_cargar_umbrales_ppm_lee_yaml_del_proyecto():
    umbrales = cargar_umbrales_ppm()
    assert umbrales["world_class"] == 100
    assert umbrales["acceptable"] == 1000


def test_cargar_umbrales_ppk_con_path_inexistente_devuelve_vacio(tmp_path):
    """Path inexistente → dict vacío (no crash)."""
    fake = tmp_path / "no_existe.yaml"
    assert cargar_umbrales_ppk(fake) == {}


def test_cargar_umbrales_ppm_con_path_inexistente_devuelve_vacio(tmp_path):
    fake = tmp_path / "no_existe.yaml"
    assert cargar_umbrales_ppm(fake) == {}


def test_cargar_umbrales_ppk_con_yaml_custom(tmp_path):
    """Permite inyectar YAML de cliente (SaaS multi-cliente)."""
    custom = tmp_path / "custom.yaml"
    custom.write_text(
        yaml.safe_dump(
            {
                "ppk_thresholds": {
                    "clase_mundial": 2.00,
                    "capaz": 1.67,
                    "marginal": 1.33,
                }
            }
        )
    )
    umbrales = cargar_umbrales_ppk(custom)
    assert umbrales["clase_mundial"] == 2.00


def test_defaults_son_inmutables():
    """Los defaults están definidos a nivel de módulo (no se mutan)."""
    assert DEFAULT_PPK_THRESHOLDS["clase_mundial"] == 1.67
    assert DEFAULT_PPM_THRESHOLDS["world_class"] == 100
