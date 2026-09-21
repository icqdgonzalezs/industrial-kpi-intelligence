"""Tests del layout principal (`dashboard/app_layout.py`).

Verifica que el layout se construye sin errores y que las zonas que
se actualizan con los filtros tienen los `dcc.Loading` esperados.

Arquitectura de Loading (Fase 3b.1 + fix UX Control + fix doble spinner):
- 4 secciones (Diagnóstico, Calidad, Capacidad, Operacional) tienen
  `dcc.Loading` externo envuelto en `app_layout.py`.
- La sección Control gestiona su propio `dcc.Loading` interno (solo
  sobre las 2 cartas I-MR).
- El KPI grid del top NO tiene Loading: con el caché JSON los KPIs
  actualizan en ~200-500ms y los valores cambiantes ya son feedback
  visual suficiente. Un spinner ahí produce ruido visual.
Total: 4 externos + 1 interno en Control = 5 Loadings.
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


def test_app_layout_incluye_5_loading_states():
    """El layout debe incluir 5 dcc.Loading en total:

    - 4 externos para las secciones Diagnóstico/Calidad/Capacidad/Operacional.
    - 1 interno de Control (sobre las 2 cartas I-MR).

    El KPI grid del top NO tiene Loading a propósito: el callback es
    rápido con el caché JSON (~200-500ms) y los valores cambiantes ya
    son feedback visual. Un spinner ahí sería ruido visual (doble spinner
    visible durante los cambios de filtro).
    """
    layout = _crear_layout_minimo()
    count = _contar_por_tipo(layout, dcc.Loading)
    assert count == 5, f"Esperado 5 dcc.Loading, encontrado {count}"


def test_cuatro_secciones_envueltas_en_loading_externo():
    """Las 4 secciones sin Loading interno tienen `dcc.Loading` como hijo
    directo.

    Nota: `section-control` NO se testea acá porque gestiona su propio
    `dcc.Loading` internamente (ver test_control_tiene_loading_interno).
    """
    layout = _crear_layout_minimo()

    ids_esperados = [
        "section-diagnostico",
        "section-calidad",
        "section-capacidad",
        "section-operacional",
    ]

    for seccion_id in ids_esperados:
        seccion = _buscar_por_id(layout, seccion_id)
        assert seccion is not None, f"Falta la sección {seccion_id}"
        assert isinstance(seccion.children, dcc.Loading), (
            f"La sección {seccion_id} no está envuelta en dcc.Loading"
        )


def test_control_tiene_loading_interno_sobre_las_2_cartas():
    """La sección Control gestiona su propio dcc.Loading.

    Dash 4.x renderiza un spinner interno por cada dcc.Graph, y Control
    tiene 2 (carta I + carta MR). Al dejarlos sin envolver, se veían 2
    spinners consecutivos. El fix: un solo dcc.Loading que envuelve las
    2 cartas. Este test verifica esa estructura.
    """
    layout = _crear_layout_minimo()

    seccion = _buscar_por_id(layout, "section-control")
    assert seccion is not None, "Falta la sección section-control"

    # La sección Control NO debe tener Loading como hijo directo
    assert not isinstance(seccion.children, dcc.Loading), (
        "Control NO debe tener dcc.Loading externo — lo gestiona internamente"
    )

    # Pero SÍ debe tener un dcc.Loading descendiente (el interno)
    loading = _buscar_por_tipo(seccion, dcc.Loading)
    assert loading is not None, "Control no tiene dcc.Loading interno"

    # Ese Loading debe envolver los 2 dcc.Graph
    graficos = _contar_por_tipo(loading, dcc.Graph)
    assert graficos == 2, (
        f"Esperado 2 dcc.Graph dentro del Loading de Control, "
        f"encontrado {graficos}"
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


def _contar_por_tipo(componente, tipo) -> int:
    """Cuenta recursivamente todos los componentes del tipo dado."""
    count = 1 if isinstance(componente, tipo) else 0
    for hijo in _hijos(componente):
        count += _contar_por_tipo(hijo, tipo)
    return count


def _buscar_por_tipo(componente, tipo):
    """Busca recursivamente el primer componente del tipo dado."""
    if isinstance(componente, tipo):
        return componente
    for hijo in _hijos(componente):
        encontrado = _buscar_por_tipo(hijo, tipo)
        if encontrado is not None:
            return encontrado
    return None


def _buscar_por_id(componente, target_id):
    """Busca recursivamente un componente por su id."""
    if getattr(componente, "id", None) == target_id:
        return componente
    for hijo in _hijos(componente):
        encontrado = _buscar_por_id(hijo, target_id)
        if encontrado is not None:
            return encontrado
    return None
