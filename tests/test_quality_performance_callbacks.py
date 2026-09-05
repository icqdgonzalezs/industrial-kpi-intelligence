import pandas as pd
import pytest

from dashboard.quality_performance_callbacks import (
    _leer_dataframe_filtrado,
    actualizar_quality_performance,
    crear_caption_pareto,
    crear_figura_pareto,
    crear_lote_critico,
)
from src.kpis import calcular_pareto


def test_crear_figura_pareto():
    df = pd.DataFrame(
        {
            "defecto_tipo": [
                "Mancha",
                "Rayadura",
                "Mancha",
            ],
            "unidades_defectuosas": [
                40,
                10,
                20,
            ],
        }
    )

    figura = crear_figura_pareto(df)

    assert len(figura.data) == 2
    assert list(figura.data[0].x) == [
        "Mancha",
        "Rayadura",
    ]
    assert list(figura.data[0].y) == [
        60,
        10,
    ]
    assert figura.data[1].y[0] == pytest.approx(
        85.71428571428571
    )
    assert figura.data[1].y[1] == pytest.approx(
        100.0
    )


def test_crear_caption_pareto_con_datos():
    df = pd.DataFrame(
        {
            "defecto_tipo": ["Mancha", "Rayadura", "Mancha"],
            "unidades_defectuosas": [40, 10, 20],
        }
    )
    pareto = calcular_pareto(df)

    caption = crear_caption_pareto(pareto)

    assert "Mancha" in caption
    assert "%" in caption


def test_crear_caption_pareto_sin_datos():
    caption = crear_caption_pareto(pd.DataFrame())

    assert caption == "Sin defectos en el período seleccionado."


def test_quality_performance_empty_data():
    metricas = actualizar_quality_performance("")

    assert metricas == (
        "—",
        "—",
        "—",
        "—",
    )


def test_quality_performance_metrics_and_pareto_are_consistent():
    df = pd.DataFrame(
        {
            "lote": ["L1", "L2", "L3"],
            "unidades_producidas": [100, 200, 100],
            "unidades_defectuosas": [10, 20, 30],
            "unidades_scrap": [3, 6, 9],
            "unidades_reproceso": [7, 14, 21],
            "defecto_tipo": ["Mancha", "Rayadura", "Mancha"],
        }
    )

    data = df.to_json(
        orient="split",
        date_format="iso",
    )

    metricas = actualizar_quality_performance(data)
    figura = crear_figura_pareto(df)

    assert metricas == (
        "85.0%",
        "15.0%",
        "4.5%",
        "10.5%",
    )

    assert list(figura.data[0].x) == [
        "Mancha",
        "Rayadura",
    ]

    assert list(figura.data[0].y) == [
        40,
        20,
    ]


def test_quality_performance_callback_contract():
    """El callback registrado devuelve 7 outputs: 4 métricas + figura + caption + lote crítico.

    Reproduce exactamente lo que hace callback_actualizar_quality_performance, verificando
    que la figura NUNCA va a un 'children' (ese fue el bug real que rompía el render).
    """
    df = pd.DataFrame(
        {
            "lote": ["L1", "L2"],
            "unidades_producidas": [100, 200],
            "unidades_defectuosas": [10, 20],
            "unidades_scrap": [3, 6],
            "unidades_reproceso": [7, 14],
            "defecto_tipo": ["Mancha", "Rayadura"],
        }
    )

    data = df.to_json(
        orient="split",
        date_format="iso",
    )

    metricas = actualizar_quality_performance(data)
    filtrado = _leer_dataframe_filtrado(data)
    pareto = calcular_pareto(filtrado)
    figura = crear_figura_pareto(filtrado)
    caption = crear_caption_pareto(pareto)
    lote_critico = crear_lote_critico(filtrado)

    resultado = (*metricas, figura, caption, lote_critico)

    assert len(resultado) == 7
    assert resultado[:4] == (
        "90.0%",
        "10.0%",
        "3.0%",
        "7.0%",
    )
    assert len(resultado[4].data) == 2
    assert isinstance(resultado[5], str)
    assert isinstance(resultado[6], str)


def test_quality_performance_rejects_invalid_schema():
    df = pd.DataFrame(
        {
            "lote": ["L1"],
            "unidades_producidas": [100],
            "unidades_defectuosas": [10],
        }
    )

    data = df.to_json(
        orient="split",
        date_format="iso",
    )

    with pytest.raises(
        ValueError,
        match="Faltan columnas requeridas",
    ):
        actualizar_quality_performance(data)


def test_quality_performance_rejects_zero_production():
    df = pd.DataFrame(
        {
            "lote": ["L1"],
            "unidades_producidas": [0],
            "unidades_defectuosas": [0],
            "unidades_scrap": [0],
            "unidades_reproceso": [0],
        }
    )

    data = df.to_json(
        orient="split",
        date_format="iso",
    )

    with pytest.raises(ValueError):
        actualizar_quality_performance(data)


def test_quality_performance_rejects_defects_above_production():
    df = pd.DataFrame(
        {
            "lote": ["L1"],
            "unidades_producidas": [100],
            "unidades_defectuosas": [101],
            "unidades_scrap": [0],
            "unidades_reproceso": [101],
        }
    )

    data = df.to_json(
        orient="split",
        date_format="iso",
    )

    with pytest.raises(ValueError):
        actualizar_quality_performance(data)


def test_quality_performance_full_contract():
    df = pd.DataFrame(
        {
            "lote": ["L1", "L2", "L3"],
            "unidades_producidas": [100, 200, 100],
            "unidades_defectuosas": [10, 20, 30],
            "unidades_scrap": [3, 6, 9],
            "unidades_reproceso": [7, 14, 21],
            "defecto_tipo": ["Mancha", "Rayadura", "Mancha"],
        }
    )

    data = df.to_json(
        orient="split",
        date_format="iso",
    )

    metricas = actualizar_quality_performance(data)
    filtrado = _leer_dataframe_filtrado(data)
    pareto_df = calcular_pareto(filtrado)
    pareto = crear_figura_pareto(filtrado)
    caption = crear_caption_pareto(pareto_df)
    lote_critico = crear_lote_critico(filtrado)

    resultado = (
        *metricas,
        pareto,
        caption,
        lote_critico,
    )

    assert len(resultado) == 7

    assert resultado[:4] == (
        "85.0%",
        "15.0%",
        "4.5%",
        "10.5%",
    )

    assert len(resultado[4].data) == 2

    assert "Mancha" in resultado[5]

    assert resultado[6] == (
        "Lote crítico: L3 · Tasa de defectos: 30.0%"
    )
