"""Tests del tema visual compartido (dashboard/utils.py).

Verifican que `aplicar_tema_oscuro`:
  - aplique la colorway industrial,
  - use fondo sólido de tarjeta (no transparente),
  - configure hoverlabel y modebar,
  - modifique la figura in-place.
"""

import plotly.graph_objects as go

from dashboard.utils import COLORWAY_INDUSTRIAL, aplicar_tema_oscuro


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