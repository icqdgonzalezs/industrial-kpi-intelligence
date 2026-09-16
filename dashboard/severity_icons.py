"""Iconos Unicode por severidad semántica (WCAG 2.1 §1.4.1).

Redundancia no cromática: el color por sí solo no es accesible para
~8% de los hombres (deuteranopia/protanopia). Cada severidad lleva
un icono distinto que se puede leer en blanco y negro.

Convención ISA-101 / HMI industrial: símbolos universales sin
ambigüedad cultural.
  - ✓ check     → OK (success)
  - ⚠ warning   → atención requerida (warning)
  - ✕ cross     → acción requerida (danger)
  - (vacío)     → neutral: el volumen no tiene umbral universal

SSOT: cualquier consumidor que renderice un valor con severidad debe
usar `prefijar_icono()`. No duplicar el diccionario.
"""

from __future__ import annotations

ICONO_POR_SEVERIDAD: dict[str, str] = {
    "success": "✓",
    "warning": "⚠",
    "danger": "✕",
    "neutral": "",  # sin icono: el neutro no transmite severidad
}

SEVERIDADES_VALIDAS: frozenset[str] = frozenset(ICONO_POR_SEVERIDAD.keys())


def prefijar_icono(valor: str, severidad: str) -> str:
    """Prefija `valor` con el icono Unicode de su severidad.

    Parameters
    ----------
    valor : str
        Texto a mostrar (ej. "97.2%", "55 PPM").
    severidad : str
        Severidad semántica: "success", "warning", "danger" o "neutral".
        Valores desconocidos caen a "sin icono" (comportamiento seguro).

    Returns
    -------
    str
        "✓ 97.2%" si hay icono; el valor sin cambios si es neutral,
        desconocida o vacío.
    """
    if not valor:
        return valor

    icono = ICONO_POR_SEVERIDAD.get(severidad, "")
    return f"{icono} {valor}" if icono else valor
