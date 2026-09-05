from __future__ import annotations

import pandas as pd
import pytest

from dashboard.operational_analysis_callbacks import (
    _color_por_ratio,
    crear_figura_ranking,
    crear_panel_detalle,
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


def test_crear_figura_ranking_con_datos():
    figura = crear_figura_ranking(_dataset(), "equipo")

    assert len(figura.data) == 1
    assert set(figura.data[0].x) == {"EQ-A", "EQ-B"}


def test_crear_figura_ranking_dataset_vacio():
    figura = crear_figura_ranking(pd.DataFrame(), "equipo")

    assert len(figura.data) == 0


def test_crear_figura_ranking_colorea_segun_umbral_hotspot():
    figura = crear_figura_ranking(_dataset(), "equipo")

    colores = dict(zip(figura.data[0].x, figura.data[0].marker.color, strict=True))
    assert colores["EQ-B"] == "#ef4444"
    assert colores["EQ-A"] == "#22c55e"


def test_crear_panel_detalle_grupo_existente():
    panel = crear_panel_detalle(_dataset(), "equipo", "EQ-B")

    texto = str(panel)
    assert "EQ-B" in texto
    assert "Mancha" in texto


def test_crear_panel_detalle_grupo_inexistente():
    panel = crear_panel_detalle(_dataset(), "equipo", "EQ-INEXISTENTE")

    assert "Sin datos" in str(panel)
