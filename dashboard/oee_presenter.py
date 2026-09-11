"""Presentación de resultados OEE para la capa Dash.

H2 (claves estables): src/oee.py devuelve claves estables e
independientes del idioma ("world_class", "acceptable", "low") para que
el motor de cálculo nunca dependa de cómo se presenta el resultado. Este
módulo traduce esas claves a texto de UI (español por defecto).

Mismo patrón que dashboard/kpi_presenter.py: src/ calcula, dashboard/
presenta.
"""

from __future__ import annotations

LABELS_ES: dict[str, str] = {
    "world_class": "Clase mundial",
    "acceptable": "Aceptable (mejorable)",
    "low": "Bajo (acción requerida)",
}

_TABLAS_POR_IDIOMA: dict[str, dict[str, str]] = {
    "es": LABELS_ES,
}


def formatear_clasificacion_oee(clave: str, idioma: str = "es") -> str:
    """Traduce la clave estable de clasificación OEE a texto de UI.

    Parameters
    ----------
    clave : str
        Una de las claves devueltas por src.oee.clasificar_oee():
        "world_class", "acceptable", "low".
    idioma : str
        Idioma de presentación. Solo "es" soportado hoy.

    Returns
    -------
    str
        Texto localizado listo para mostrar en la UI.

    Raises
    ------
    ValueError
        Si el idioma no está soportado o la clave es desconocida.
    """
    tabla = _TABLAS_POR_IDIOMA.get(idioma)

    if tabla is None:
        raise ValueError(
            f"Idioma no soportado: '{idioma}'. Disponibles: "
            + ", ".join(_TABLAS_POR_IDIOMA)
        )

    if clave not in tabla:
        raise ValueError(f"Clave de clasificación OEE desconocida: '{clave}'")

    return tabla[clave]