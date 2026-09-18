"""Smoke tests del layout principal (`dashboard/app_layout.py`).

Verifica que el layout se construye sin errores y que las 6 zonas que
se actualizan con los filtros están envueltas en ``dcc.Loading``
(Fase 3b.1 — loading states).

Por qué estos tests y no otros:
- El layout es HTML puro: testear su estructura pixel a pixel no aporta.
- Lo que SÍ aporta es verificar que no se rompe la envoltura de Loading
  en futuros refactors — es la regresión que importa proteger.
"""

from __future__ import annotations

from dash import dcc

from dashboard.app_layout import crear_app_layout


def _crear_layout_minimo():
    """Layout con el mínimo de argumentos válidos para no acoplar los
    tests a datos del dataset real."""
    return crear_app_layout(
        fecha_min="2024-01-01",
        fecha_max="2024-12-31",
        lineas=["Todas", "L1"],
        equipos=["Todos", "EQ-A"],
        turnos=["Todos", "Mañana"],
        operadores=["Todos", "OP1"],
        variables_criticas={},
        metadata_dataset="2024-01-01",
    )


def test_crear_app_layout_sin_error():
    """Smoke test: el layout debe construirse sin excepciones."""
    layout = _crear_layout_minimo()
    assert layout is not None


def test_app_layout_incluye_6_loading_states():
    """El layout debe envolver 6 zonas en dcc.Loading (Fase 3b.1):

    - 1 para el KPI grid del top.
    - 5 para las secciones de los tabs (diagnóstico, calidad, capacidad,
      control, operacional).

    Sin estos wrappers, los cambios de filtro no tienen feedback visual
    y el operador percibe la app como congelada durante los 4-6 s de
    recálculo.
    """
    layout = _crear_layout_minimo()
    count = _contar_loadings(layout)
    assert count == 6, f"Esperado 6 dcc.Loading, encontrado {count}"


def test_cada_seccion_esta_envuelta_en_loading():
    """Cada uno de los 5 divs de sección debe tener un dcc.Loading como
    hijo directo. Esto garantiza que el spinner aparece SOLO en la
    sección que el usuario está viendo, no en todas a la vez."""
    layout = _crear_layout_minimo()

    ids_esperados = [
        "section-diagnostico",
        "section-calidad",
        "section-capacidad",
        "section-control",
        "section-operacional",
    ]

    for seccion_id in ids_esperados:
        seccion = _buscar_por_id(layout, seccion_id)
        assert seccion is not None, f"Falta la sección {seccion_id}"
        assert isinstance(seccion.children, dcc.Loading), (
            f"La sección {seccion_id} no está envuelta en dcc.Loading"
        )


# ---------------------------------------------------------------------
# Helpers de traversal del árbol de componentes Dash
# ---------------------------------------------------------------------


def _hijos(componente):
    """Devuelve los hijos de un componente Dash siempre como lista."""
    children = getattr(componente, "children", None)
    if children is None:
        return []
    if isinstance(children, (list, tuple)):
        return list(children)
    return [children]


def _contar_loadings(componente) -> int:
    """Cuenta recursivamente todos los dcc.Loading del subárbol."""
    count = 1 if isinstance(componente, dcc.Loading) else 0
    for hijo in _hijos(componente):
        count += _contar_loadings(hijo)
    return count


def _buscar_por_id(componente, target_id):
    """Busca recursivamente un componente por su id."""
    if getattr(componente, "id", None) == target_id:
        return componente
    for hijo in _hijos(componente):
        encontrado = _buscar_por_id(hijo, target_id)
        if encontrado is not None:
            return encontrado
    return None