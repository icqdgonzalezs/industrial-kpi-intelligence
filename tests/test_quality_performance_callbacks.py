import pandas as pd
import pytest

from dashboard.quality_performance_callbacks import (
    actualizar_quality_performance,
    construir_outputs_calidad,
    crear_caption_pareto,
    crear_figura_pareto,
    exportar_pareto_calidad,
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
    """El callback registrado devuelve 9 outputs (Fase 3b.2):

    0-3: 4 métricas · 4: figura · 5: caption · 6: lote crítico
    7: style del contenido normal · 8: children del empty

    Verifica que la figura NUNCA va a un 'children' (bug real previo).
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

    resultado = construir_outputs_calidad(data)

    assert len(resultado) == 9
    assert resultado[:4] == (
        "90.0%",
        "10.0%",
        "3.0%",
        "7.0%",
    )
    assert len(resultado[4].data) == 2
    assert isinstance(resultado[5], str)
    assert isinstance(resultado[6], str)
    assert resultado[7] == {"display": "block"}
    assert resultado[8] == []


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

    resultado = construir_outputs_calidad(data)

    assert len(resultado) == 9

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

    assert resultado[7] == {"display": "block"}
    assert resultado[8] == []


def test_quality_performance_empty_state_when_filtrado_vacio():
    """Con 0 filas, se oculta el contenido normal y aparece el empty state.

    Fase 3b.2: el bloque de KPIs + chart + analysis se reemplaza por
    un mensaje único y claro, en vez de mostrar 4 valores en "—" y un
    gráfico vacío. El operador entiende de un vistazo qué pasó.
    """
    resultado = construir_outputs_calidad("")

    assert len(resultado) == 9
    assert resultado[:4] == ("—", "—", "—", "—")
    assert resultado[7] == {"display": "none"}
    assert resultado[8].className == "empty-state"
    # Mensaje del dominio preservado
    textos = [child.children for child in resultado[8].children]
    assert "Sin datos de calidad con los filtros actuales" in textos


def test_quality_performance_empty_state_incluye_hint_de_accion():
    """El empty state incluye un hint sugiriendo la acción al operador."""
    resultado = construir_outputs_calidad("")

    textos = [child.children for child in resultado[8].children]
    # El hint tiene la acción sugerida (Restaurar filtros)
    assert any("Restaurar" in str(t) for t in textos)


def test_exportar_pareto_calidad_con_datos():
    """La descarga contiene content y filename con timestamp.

    Verifica presencia de las keys que son NUESTRO contrato, no
    igualdad estricta sobre el dict completo: dcc.send_data_frame()
    agrega keys internas ('base64', 'type') que son detalle de Dash.
    Mismo estándar que tests/test_export_helpers.py.
    """
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
    data = df.to_json(orient="split", date_format="iso")

    descarga = exportar_pareto_calidad(data)

    assert descarga is not None
    assert "content" in descarga
    assert "filename" in descarga
    assert descarga["filename"].startswith("industrial_kpi_calidad_")
    assert descarga["filename"].endswith(".csv")


@pytest.mark.parametrize(
    "data",
    [
        "",
        pd.DataFrame().to_json(orient="split"),
    ],
    ids=["string_vacio", "df_vacio"],
)
def test_exportar_pareto_calidad_sin_datos_devuelve_none(data):
    assert exportar_pareto_calidad(data) is None
