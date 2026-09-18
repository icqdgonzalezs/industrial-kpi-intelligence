from __future__ import annotations

import pandas as pd
import pytest

from dashboard.operational_analysis_callbacks import (
    ALTURA_MARGEN_PX,
    ALTURA_MINIMA_PX,
    ALTURA_POR_CATEGORIA_PX,
    _color_por_ratio,
    _extraer_valor_seleccionado,
    _label_dimension,
    crear_figura_ranking,
    crear_panel_detalle,
    exportar_operacional_csv,
)
from dashboard.operational_analysis_components import (
    DIMENSIONES_DISPONIBLES,
    LABELS_EJES_DIMENSION,
    MICROCOPY_DIMENSIONES,
)


def _fila(lote, equipo, turno, producidas, defectuosas, defecto_tipo="Mancha"):
    return {
        "lote": lote,
        "linea": "L1",
        "maquina": "M01",
        "equipo": equipo,
        "turno": turno,
        "operador": "OP1",
        "unidades_producidas": producidas,
        "unidades_defectuosas": defectuosas,
        "unidades_reproceso": defectuosas,
        "unidades_scrap": 0,
        "defecto_tipo": defecto_tipo,
    }


def _dataset():
    filas = []
    for i in range(20):
        filas.append(_fila(f"L{i:03d}", "EQ-A", "Mañana", 1000, 30))
    for i in range(20, 40):
        filas.append(_fila(f"L{i:03d}", "EQ-B", "Noche", 1000, 100))
    return pd.DataFrame(filas)


def _dataset_muchos_equipos(n: int = 20):
    filas = []
    for i in range(n):
        for j in range(5):
            filas.append(_fila(f"L{i:03d}{j}", f"EQ-{i:02d}", "Mañana", 1000, 10 + i))
    return pd.DataFrame(filas)


# --- _color_por_ratio ---

@pytest.mark.parametrize(
    ("ratio", "color_esperado"),
    [
        (1.50, "#ef4444"),
        (1.40, "#ef4444"),
        (1.20, "#f59e0b"),
        (1.15, "#f59e0b"),
        (1.00, "#22c55e"),
        (0.80, "#22c55e"),
    ],
)
def test_color_por_ratio(ratio, color_esperado):
    assert _color_por_ratio(ratio) == color_esperado


# --- _extraer_valor_seleccionado ---

def test_extraer_valor_seleccionado_horizontal():
    click_data = {"points": [{"x": 3.0, "y": "EQ-A"}]}
    assert _extraer_valor_seleccionado(click_data) == "EQ-A"


def test_extraer_valor_seleccionado_sin_click():
    assert _extraer_valor_seleccionado(None) is None
    assert _extraer_valor_seleccionado({}) is None
    assert _extraer_valor_seleccionado({"points": []}) is None


# --- _label_dimension (SSOT de nombres visibles) ---

def test_label_dimension_maquina_es_tipo_de_maquina():
    """Regresión: 'maquina' debe mapear a 'Tipo de máquina', con tilde.

    El bug original del Fix #5.6 usaba str.capitalize() sobre el value
    del dataset, produciendo 'Maquina' (sin tilde, sin 'Tipo de') en el
    eje Y del ranking. Este test blinda el lookup contra el SSOT.
    """
    assert _label_dimension("maquina") == "Tipo de máquina"


def test_label_dimension_restantes_conservan_tilde_y_mayuscula():
    """Los labels del SSOT se respetan tal cual, incluyendo tildes."""
    assert _label_dimension("equipo") == "Equipo"
    assert _label_dimension("turno") == "Turno"
    assert _label_dimension("operador") == "Operador"
    assert _label_dimension("linea") == "Línea"


def test_label_dimension_fallback_para_desconocida():
    """Dimensiones no registradas caen a str.capitalize() por robustez."""
    assert _label_dimension("columna_nueva") == "Columna_nueva"


# --- LABELS_EJES_DIMENSION (contrato del SSOT) ---

def test_labels_ejes_dimension_cubre_todas_las_dimensiones():
    """El mapping debe tener exactamente los values de DIMENSIONES_DISPONIBLES."""
    values_dimensiones = {d["value"] for d in DIMENSIONES_DISPONIBLES}
    assert set(LABELS_EJES_DIMENSION.keys()) == values_dimensiones


def test_labels_ejes_dimension_no_contiene_maquina_sin_tilde():
    """Regresión: ninguna label visible debe ser 'Maquina' sin tilde."""
    assert "Maquina" not in LABELS_EJES_DIMENSION.values()


# --- crear_figura_ranking ---

def test_crear_figura_ranking_con_datos():
    figura = crear_figura_ranking(_dataset(), "equipo")

    assert len(figura.data) == 1
    assert figura.data[0].orientation == "h"
    assert set(figura.data[0].y) == {"EQ-A", "EQ-B"}


def test_crear_figura_ranking_ordenado_peor_arriba():
    figura = crear_figura_ranking(_dataset(), "equipo")

    assert list(figura.data[0].y) == ["EQ-A", "EQ-B"]


def test_crear_figura_ranking_altura_dinamica_minima():
    figura = crear_figura_ranking(_dataset(), "equipo")
    assert figura.layout.height == ALTURA_MINIMA_PX


def test_crear_figura_ranking_altura_dinamica_escala():
    figura = crear_figura_ranking(_dataset_muchos_equipos(20), "equipo")
    esperado = ALTURA_POR_CATEGORIA_PX * 20 + ALTURA_MARGEN_PX
    assert figura.layout.height == esperado


def test_crear_figura_ranking_dataset_vacio():
    figura = crear_figura_ranking(pd.DataFrame(), "equipo")
    assert len(figura.data) == 0


def test_crear_figura_ranking_colorea_segun_umbral_hotspot():
    figura = crear_figura_ranking(_dataset(), "equipo")

    colores = dict(zip(figura.data[0].y, figura.data[0].marker.color, strict=True))
    assert colores["EQ-B"] == "#ef4444"
    assert colores["EQ-A"] == "#22c55e"


def test_crear_figura_ranking_referencia_es_vertical():
    figura = crear_figura_ranking(_dataset(), "equipo")
    shapes_verticales = [s for s in figura.layout.shapes if s.x0 == s.x1]
    assert len(shapes_verticales) == 1


def test_crear_figura_ranking_etiquetas_numericas_visibles():
    """ISA-101: datos medidos legibles sin hover."""
    figura = crear_figura_ranking(_dataset(), "equipo")

    assert all(t.endswith("%") for t in figura.data[0].text)
    assert figura.data[0].textposition == "outside"
    assert figura.data[0].cliponaxis is False


def test_crear_figura_ranking_sin_bordes_extra():
    """Consistencia visual: ninguna barra lleva borde decorativo.

    La jerarquía se comunica por posición (peor arriba), color semántico
    y valor absoluto visible. Un borde blanco en la peor categoría rompía
    la consistencia y era redundante con las 3 señales ya existentes.
    """
    figura = crear_figura_ranking(_dataset(), "equipo")

    assert figura.data[0].marker.line.width is None
    assert figura.data[0].marker.line.color is None


def test_crear_figura_ranking_hovertemplate_html():
    """El tooltip usa <b> para negrita (HTML en Plotly, no font.weight)."""
    figura = crear_figura_ranking(_dataset(), "equipo")

    assert "<b>" in figura.data[0].hovertemplate


def test_crear_figura_ranking_yaxis_usa_label_maquina():
    """Regresión Fix #5.6: eje Y de 'maquina' dice 'Tipo de máquina'."""
    figura = crear_figura_ranking(_dataset(), "maquina")

    assert figura.layout.yaxis.title.text == "Tipo de máquina"


def test_crear_figura_ranking_yaxis_usa_label_linea_con_tilde():
    """Regresión Fix #5.6: 'linea' → 'Línea' con tilde."""
    figura = crear_figura_ranking(_dataset(), "linea")

    assert figura.layout.yaxis.title.text == "Línea"


# --- crear_panel_detalle ---

def test_crear_panel_detalle_grupo_existente():
    panel = crear_panel_detalle(_dataset(), "equipo", "EQ-B")

    texto = str(panel)
    assert "EQ-B" in texto
    assert "Mancha" in texto


def test_crear_panel_detalle_grupo_inexistente():
    panel = crear_panel_detalle(_dataset(), "equipo", "EQ-INEXISTENTE")

    assert "Sin datos" in str(panel)


def test_crear_panel_detalle_titulo_usa_label_maquina():
    """Regresión Fix #5.6: título del panel usa 'Tipo de máquina', no 'Maquina'."""
    panel = crear_panel_detalle(_dataset(), "maquina", "M01")

    texto = str(panel)
    assert "Tipo de máquina" in texto
    assert "Maquina:" not in texto


# --- Contrato de la sección (layout) ---

def test_dimensiones_disponibles_renombra_maquina():
    """'Máquina' pasa a 'Tipo de máquina' para desambiguar de 'Equipo'."""
    labels = [d["label"] for d in DIMENSIONES_DISPONIBLES]
    values = [d["value"] for d in DIMENSIONES_DISPONIBLES]

    assert "Tipo de máquina" in labels
    assert "Máquina" not in labels
    assert "maquina" in values


def test_microcopy_dimensiones_documenta_ambiguedad():
    """El microcopy bajo el selector explica Equipo vs Tipo de máquina."""
    assert "instancia física" in MICROCOPY_DIMENSIONES
    assert "familia" in MICROCOPY_DIMENSIONES


# --- exportar_operacional_csv (Fase 3a-ε) ---


def test_exportar_operacional_csv_con_datos():
    """La descarga contiene content + filename con timestamp."""
    df = _dataset()
    data = df.to_json(orient="split", date_format="iso")

    descarga = exportar_operacional_csv(data, "equipo")

    assert descarga is not None
    assert "content" in descarga
    assert "filename" in descarga
    assert descarga["filename"].startswith("industrial_kpi_operacional_")
    assert descarga["filename"].endswith(".csv")


def test_exportar_operacional_csv_incluye_columnas_del_ranking():
    """El CSV expone la dimensión y la tasa de defectos.

    Nota: dcc.send_data_frame en Dash 4.x entrega content como bytes
    del CSV crudo (no base64). Se decodifica directamente.
    """
    df = _dataset()
    data = df.to_json(orient="split", date_format="iso")

    descarga = exportar_operacional_csv(data, "equipo")
    contenido = descarga["content"]
    if isinstance(contenido, bytes):
        contenido = contenido.decode("utf-8")

    cabecera = contenido.split("\n")[0]

    assert "equipo" in cabecera
    assert "tasa_defectos" in cabecera

    # Verificación de contenido: el dataset tiene EQ-A y EQ-B.
    assert "EQ-A" in contenido
    assert "EQ-B" in contenido


@pytest.mark.parametrize(
    "data, dimension",
    [
        ("", "equipo"),
        (pd.DataFrame().to_json(orient="split"), "equipo"),
        (
            pd.DataFrame({"peso": [100, 101]}).to_json(orient="split"),
            None,
        ),
    ],
    ids=[
        "string_vacio",
        "df_vacio",
        "dimension_none",
    ],
)
def test_exportar_operacional_csv_sin_datos_devuelve_none(data, dimension):
    assert exportar_operacional_csv(data, dimension) is None