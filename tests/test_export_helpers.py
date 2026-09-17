"""Tests para dashboard.export_helpers (Fase 3a).

Cubre:
- nombre_csv: formato esperado + unicidad por timestamp.
- boton_export: ID uniforme, texto, estado inicial, clase CSS.
- crear_descarga_csv: caso vacío (None) y caso con datos (dict).
"""

from __future__ import annotations

import re
import time

import pandas as pd

from dashboard.export_helpers import (
    boton_export,
    crear_descarga_csv,
    nombre_csv,
)

# ---------------------------------------------------------------------
# nombre_csv
# ---------------------------------------------------------------------


def test_nombre_csv_incluye_tab():
    nombre = nombre_csv("capacidad")
    assert "capacidad" in nombre


def test_nombre_csv_tiene_formato_esperado():
    """Formato: industrial_kpi_<tab>_YYYYMMDD_HHMMSS.csv."""
    nombre = nombre_csv("capacidad")
    patron = r"^industrial_kpi_capacidad_\d{8}_\d{6}\.csv$"
    assert re.match(patron, nombre), f"Formato inesperado: {nombre}"


def test_nombre_csv_termina_en_punto_csv():
    assert nombre_csv("capacidad").endswith(".csv")


def test_nombre_csv_usa_tab_en_el_nombre():
    """El tab se interpola en el nombre para distinguir exports."""
    assert "capacidad" in nombre_csv("capacidad")
    assert "calidad" in nombre_csv("calidad")
    assert "control" in nombre_csv("control")


def test_nombre_csv_es_unico_por_llamada_en_segundos_distintos():
    """Dos llamadas consecutivas en segundos distintos dan nombres distintos.

    Esto evita que el usuario sobrescriba archivos al exportar varias veces.
    """
    n1 = nombre_csv("capacidad")
    time.sleep(1.1)
    n2 = nombre_csv("capacidad")
    assert n1 != n2


# ---------------------------------------------------------------------
# boton_export
# ---------------------------------------------------------------------


def test_boton_export_tiene_id_correcto():
    boton = boton_export("capacidad")
    assert boton.id == "btn-export-capacidad"


def test_boton_export_incluye_texto_exportar():
    boton = boton_export("capacidad")
    assert "Exportar" in boton.children


def test_boton_export_inicia_sin_clicks():
    boton = boton_export("capacidad")
    assert boton.n_clicks == 0


def test_boton_export_tiene_clase_css_estandar():
    boton = boton_export("capacidad")
    assert boton.className == "btn-export"


def test_boton_export_tiene_tooltip():
    boton = boton_export("capacidad")
    assert boton.title
    assert "CSV" in boton.title


def test_boton_export_id_es_dinamico_por_tab():
    """Cada tab genera un ID distinto para evitar colisiones en Dash."""
    assert boton_export("capacidad").id == "btn-export-capacidad"
    assert boton_export("calidad").id == "btn-export-calidad"
    assert boton_export("control").id == "btn-export-control"


# ---------------------------------------------------------------------
# crear_descarga_csv
# ---------------------------------------------------------------------


def test_crear_descarga_csv_sin_datos_devuelve_none():
    assert crear_descarga_csv(None, "capacidad") is None


def test_crear_descarga_csv_con_string_vacio_devuelve_none():
    assert crear_descarga_csv("", "capacidad") is None


def test_crear_descarga_csv_con_datos_retorna_dict():
    df = pd.DataFrame({"variable": ["Peso"], "ppk": [1.33]})
    json_str = df.to_json(orient="split")

    resultado = crear_descarga_csv(json_str, "capacidad")

    assert resultado is not None
    assert isinstance(resultado, dict)
    assert "filename" in resultado
    assert "content" in resultado


def test_crear_descarga_csv_incluye_tab_en_filename():
    df = pd.DataFrame({"variable": ["Peso"], "ppk": [1.33]})
    json_str = df.to_json(orient="split")

    resultado = crear_descarga_csv(json_str, "capacidad")

    assert "capacidad" in resultado["filename"]
    assert resultado["filename"].endswith(".csv")


def test_crear_descarga_csv_con_multiples_filas():
    """Caso real: capacidad exporta 2+ variables (Peso, Longitud)."""
    df = pd.DataFrame(
        {
            "variable": ["Peso", "Longitud"],
            "columna": ["peso_promedio", "longitud_promedio"],
            "pp": [1.33, 1.33],
            "ppk": [1.33, 1.33],
        }
    )
    json_str = df.to_json(orient="split")

    resultado = crear_descarga_csv(json_str, "capacidad")

    assert resultado is not None
    assert "content" in resultado
