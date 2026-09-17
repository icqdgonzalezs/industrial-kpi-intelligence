"""Tests del tema visual compartido (dashboard/utils.py).

Verifican que `aplicar_tema_oscuro`:
  - aplique la colorway industrial,
  - use fondo sólido de tarjeta (no transparente),
  - configure hoverlabel y modebar,
  - modifique la figura in-place.

Y el fix de performance (Fase 3b) sobre `leer_dataframe_filtrado`:
  - cachea el parseo JSON → DataFrame (lru_cache),
  - retorna copia defensiva para no envenenar el caché compartido.
"""

import pandas as pd
import plotly.graph_objects as go

from dashboard.utils import (
    COLORWAY_INDUSTRIAL,
    _parse_json_cached,
    aplicar_tema_oscuro,
    leer_dataframe_filtrado,
)


def test_aplicar_tema_oscuro_usa_colorway_industrial():
    figura = go.Figure()
    resultado = aplicar_tema_oscuro(figura)

    assert list(resultado.layout.colorway) == COLORWAY_INDUSTRIAL


def test_aplicar_tema_oscuro_fondo_solido_de_tarjeta():
    """El fondo es SÓLIDO (#131820), no transparente.

    Cambio deliberado del bloque UX: se abandonó el fondo transparente
    porque causaba que los gráficos heredaran colores internos del
    contenedor padre (invisibles sobre el fondo oscuro). El fondo sólido
    garantiza legibilidad consistente en cualquier contexto.
    """
    figura = aplicar_tema_oscuro(go.Figure())

    assert figura.layout.paper_bgcolor == "#131820"
    assert figura.layout.plot_bgcolor == "#131820"


def test_aplicar_tema_oscuro_usa_template_plotly_dark_como_base():
    figura = aplicar_tema_oscuro(go.Figure())

    # Plotly normaliza el template a un objeto; verificamos que no quedó
    # en el default ("plotly") sino que se aplicó explícitamente.
    assert figura.layout.template is not None


def test_aplicar_tema_oscuro_configura_hoverlabel_y_modebar():
    figura = aplicar_tema_oscuro(go.Figure())

    assert figura.layout.hoverlabel.bgcolor == "#131820"
    assert figura.layout.modebar.activecolor == "#00d4ff"


def test_aplicar_tema_oscuro_retorna_la_misma_figura_modificada_in_place():
    figura = go.Figure()
    resultado = aplicar_tema_oscuro(figura)

    assert resultado is figura


def test_leer_dataframe_filtrado_usa_cache_en_llamadas_repetidas():
    """El segundo parseo del mismo JSON es un cache hit.

    Protege contra regresión del fix de performance (Fase 3b):
    sin caché, cada callback re-parsearía el JSON de 18k filas.
    """
    _parse_json_cached.cache_clear()

    df = pd.DataFrame({"a": [1, 2, 3]})
    json_data = df.to_json(orient="split", date_format="iso")

    leer_dataframe_filtrado(json_data)
    info_tras_primera = _parse_json_cached.cache_info()
    assert info_tras_primera.misses == 1
    assert info_tras_primera.hits == 0

    leer_dataframe_filtrado(json_data)
    info_tras_segunda = _parse_json_cached.cache_info()
    assert info_tras_segunda.misses == 1   # sin nuevos parseos
    assert info_tras_segunda.hits == 1     # segundo fue cache hit


def test_leer_dataframe_filtrado_retorna_copia_defensiva():
    """Mutar el DataFrame devuelto no envenena el caché.

    Si un consumidor modifica su copia, el siguiente consumidor debe
    recibir el DataFrame original intacto.
    """
    _parse_json_cached.cache_clear()

    df = pd.DataFrame({"a": [1, 2, 3]})
    json_data = df.to_json(orient="split", date_format="iso")

    primera = leer_dataframe_filtrado(json_data)
    primera["a"] = [10, 20, 30]              # mutación del consumidor

    segunda = leer_dataframe_filtrado(json_data)
    assert list(segunda["a"]) == [1, 2, 3]   # caché intacto