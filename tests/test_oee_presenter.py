"""Tests para el presenter OEE (dashboard/oee_presenter.py)."""

from __future__ import annotations

import pytest

from dashboard.oee_presenter import formatear_clasificacion_oee


@pytest.mark.parametrize(
    ("clave", "esperado"),
    [
        ("world_class", "Clase mundial"),
        ("acceptable", "Aceptable (mejorable)"),
        ("low", "Bajo (acción requerida)"),
    ],
)
def test_formatear_clasificacion_oee_es(clave, esperado):
    assert formatear_clasificacion_oee(clave, idioma="es") == esperado


def test_formatear_clasificacion_oee_idioma_por_defecto_es_espanol():
    assert formatear_clasificacion_oee("world_class") == "Clase mundial"


def test_formatear_clasificacion_oee_idioma_no_soportado():
    with pytest.raises(ValueError, match="Idioma no soportado"):
        formatear_clasificacion_oee("world_class", idioma="fr")


def test_formatear_clasificacion_oee_clave_desconocida():
    with pytest.raises(ValueError, match="Clave de clasificación OEE desconocida"):
        formatear_clasificacion_oee("unknown_key", idioma="es")