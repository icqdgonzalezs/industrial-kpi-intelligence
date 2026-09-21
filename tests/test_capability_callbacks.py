from __future__ import annotations

import pandas as pd
import pytest

from dashboard.capability_callbacks import (
    _estado_capacidad,
    _formatear_indice,
    calcular_resumen_capacidad,
    construir_outputs_capacidad,
    crear_figura_capacidad,
)

VARIABLES_CONFIG = {
    "peso_promedio": {"nombre": "Peso", "lsl": 492.0, "usl": 508.0},
}


def _dataset_json(pesos: list[float]) -> str:
    df = pd.DataFrame({"peso_promedio": pesos})
    return df.to_json(orient="split")


def test_calcular_resumen_capacidad_returns_dataframe():
    data = _dataset_json([498.0, 500.0, 502.0, 499.0, 501.0, 500.5, 499.5])

    resultado = calcular_resumen_capacidad(data, VARIABLES_CONFIG)

    assert not resultado.empty
    assert "ppk" in resultado.columns
    assert resultado.iloc[0]["columna"] == "peso_promedio"


def test_calcular_resumen_capacidad_empty_data_returns_empty_dataframe():
    resultado = calcular_resumen_capacidad(None, VARIABLES_CONFIG)

    assert resultado.empty


@pytest.mark.parametrize(
    ("clasificacion", "esperado"),
    [
        # Escala nueva (Fix #7): 4 niveles AIAG SPC / NIST 6.1.3 / ISO 22514
        ("Clase mundial", "WORLD_CLASS"),
        ("Capaz", "CAPABLE"),
        ("Marginal", "WATCH"),
        ("No capaz", "PRIORITY"),
        # Casos especiales (sin cambios)
        ("No capaz (fuera de especificación)", "PRIORITY"),
        ("Datos insuficientes", "NO DATA"),
        ("Límites inválidos", "NO DATA"),
        ("Sin variabilidad", "SPECIAL"),
    ],
)
def test_estado_capacidad_clasifica_correctamente(clasificacion, esperado):
    assert _estado_capacidad(clasificacion) == esperado


def test_estado_capacidad_orden_no_capaz_antes_que_capaz():
    """Regresión: 'No capaz' contiene 'capaz' como substring.

    El orden de los checks en _estado_capacidad debe evaluar 'no capaz'
    primero para no clasificar erróneamente como CAPABLE.
    """
    assert _estado_capacidad("No capaz") == "PRIORITY"
    assert _estado_capacidad("Capaz") == "CAPABLE"
    assert _estado_capacidad("No capaz (fuera de especificación)") == "PRIORITY"


def test_formatear_indice_valor_normal():
    assert _formatear_indice(1.2345) == "1.23"


def test_formatear_indice_infinito():
    assert _formatear_indice(float("inf")) == "∞"


def test_formatear_indice_none():
    assert _formatear_indice(None) == "Sin datos"


def test_formatear_indice_nan():
    assert _formatear_indice(float("nan")) == "Sin datos"


def test_crear_figura_capacidad_con_datos_suficientes():
    data = _dataset_json([498.0, 500.0, 502.0, 499.0, 501.0, 500.5, 499.5])
    capacidad = calcular_resumen_capacidad(data, VARIABLES_CONFIG)
    fila = capacidad.iloc[0]

    filtrado = pd.read_json(pd.io.common.StringIO(data), orient="split")

    figura = crear_figura_capacidad(filtrado, fila)

    assert len(figura.data) == 1


def test_crear_figura_capacidad_con_datos_insuficientes():
    filtrado = pd.DataFrame({"peso_promedio": [500.0]})
    fila = pd.Series(
        {"columna": "peso_promedio", "lsl": 492.0, "usl": 508.0, "media": 500.0, "variable": "Peso"}
    )

    figura = crear_figura_capacidad(filtrado, fila)

    assert len(figura.data) == 0

# ---------------------------------------------------------------------
# _span_rendimiento (iconografía semáforos, WCAG 2.1 §1.4.1)
# ---------------------------------------------------------------------


def test_span_rendimiento_agrega_icono_success():
    from dashboard.capability_callbacks import _span_rendimiento
    span = _span_rendimiento("55", "world_class")
    assert span.children == "✓ 55"
    assert "quality-metric-value--success" in span.className


def test_span_rendimiento_agrega_icono_danger():
    from dashboard.capability_callbacks import _span_rendimiento
    span = _span_rendimiento("221", "low")
    assert span.children == "✕ 221"
    assert "quality-metric-value--danger" in span.className


def test_span_rendimiento_sin_datos_no_lleva_icono():
    from dashboard.capability_callbacks import _span_rendimiento
    span = _span_rendimiento("Sin datos", "sin_datos")
    assert span.children == "Sin datos"
    assert "quality-metric-value--neutral" in span.className


# ---------------------------------------------------------------------
# Export CSV (Fase 3a)
# ---------------------------------------------------------------------


def test_crear_descarga_csv_lee_resumen_de_capacidad():
    """El helper de export funciona con la estructura real de store-capacidad.

    Verifica que el JSON que genera `resumen_capacidad()` (con columnas
    variable, columna, pp, ppk, clasificacion) es consumible por el
    helper de export sin transformación.
    """
    from dashboard.export_helpers import crear_descarga_csv

    df = pd.DataFrame(
        {
            "variable": ["Peso", "Longitud"],
            "columna": ["peso_promedio", "longitud_promedio"],
            "pp": [1.33, 1.33],
            "ppk": [1.33, 1.33],
            "clasificacion": ["Capaz", "Capaz"],
        }
    )
    json_str = df.to_json(orient="split")

    resultado = crear_descarga_csv(json_str, "capacidad")

    assert resultado is not None
    assert "filename" in resultado
    assert "capacidad" in resultado["filename"]


def test_crear_descarga_csv_sin_datos():
    """Si store-capacidad está vacío, el export devuelve None (no crash)."""
    from dashboard.export_helpers import crear_descarga_csv

    assert crear_descarga_csv(None, "capacidad") is None


# ---------------------------------------------------------------------
# construir_outputs_capacidad (Fase 3b.2 — empty state)
# ---------------------------------------------------------------------


def test_construir_outputs_capacidad_con_datos():
    """Con datos suficientes: 18 outputs, contenido normal visible."""
    data = _dataset_json([498.0, 500.0, 502.0, 499.0, 501.0, 500.5, 499.5])

    resultado = construir_outputs_capacidad(data, "peso_promedio", VARIABLES_CONFIG)

    assert len(resultado) == 18
    assert resultado[16] == {"display": "block"}
    assert resultado[17] == []


def test_construir_outputs_capacidad_sin_datos_devuelve_empty_state():
    """Con filtrado vacío: contenido normal oculto, empty_state visible.

    Nota (Fase 3b.2): el mensaje del empty_state es "Sin datos suficientes
    para evaluar capacidad" tras unificar el criterio (incluye tanto 0
    filas como n<2). El mensaje anterior ("Sin datos de capacidad con
    los filtros actuales") quedó obsoleto.
    """
    resultado = construir_outputs_capacidad(None, "peso_promedio", VARIABLES_CONFIG)

    assert len(resultado) == 18
    assert resultado[16] == {"display": "none"}
    assert resultado[17].className == "empty-state"
    textos = [child.children for child in resultado[17].children]
    assert "Sin datos suficientes para evaluar capacidad" in textos


def test_construir_outputs_capacidad_empty_state_incluye_hint():
    """El empty state incluye un hint sugiriendo la acción al operador."""
    resultado = construir_outputs_capacidad(None, "peso_promedio", VARIABLES_CONFIG)

    textos = [child.children for child in resultado[17].children]
    assert any("Restaurar" in str(t) or "filtros" in str(t) for t in textos)


def test_construir_outputs_capacidad_con_pocas_filas_devuelve_empty_state():
    """Con 1 sola fila: capacidad no calculable (n < 2) → empty state.

    Regresión: sin este fix, el callback activaba el contenido normal
    y cada KPI mostraba "Sin datos" (confuso para el operador).
    """
    data = _dataset_json([500.0])  # 1 sola observación

    resultado = construir_outputs_capacidad(data, "peso_promedio", VARIABLES_CONFIG)

    assert len(resultado) == 18
    assert resultado[16] == {"display": "none"}
    assert resultado[17].className == "empty-state"
    textos = [child.children for child in resultado[17].children]
    assert "Sin datos suficientes para evaluar capacidad" in textos
