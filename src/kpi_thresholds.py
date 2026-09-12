"""Clasificación de KPIs industriales según umbrales declarativos.

Lógica pura sin dependencias de Dash. Lee la configuración de umbrales
desde el YAML (quality_config.yaml) y clasifica cada KPI en uno de 3
estados: SUCCESS (verde), WARNING (ámbar), DANGER (rojo) o NEUTRAL
(sin umbral — siempre blanco).

Diseño (SOLID/SRP):
    - kpi_thresholds.py   → clasificación de estado (este módulo)
    - kpi_presenter.py    → formateo + clase CSS resultante
    - components          → renderizado visual

Convención de umbrales (en YAML):
    Cada KPI que tenga `thresholds` se clasifica así:
      - FPY:              verde si ≥success_min, ámbar si ≥warning_min
      - Defectos/Scrap:   verde si ≤success_max, ámbar si ≤warning_max
      - Sin `thresholds`: NEUTRAL (sin color semántico)
"""

from __future__ import annotations

from typing import Literal

StatusType = Literal["success", "warning", "danger", "neutral"]


def clasificar_kpi(
    valor: float,
    thresholds: dict | None,
    direccion: Literal["higher_is_better", "lower_is_better"] | None = None,
) -> StatusType:
    """Clasifica un valor de KPI en SUCCESS / WARNING / DANGER / NEUTRAL.

    Parameters
    ----------
    valor : float
        Valor numérico del KPI (0.954 = 95.4%).
    thresholds : dict | None
        Diccionario con claves `success` y `warning` (opcionalmente `danger`).
        Ejemplo para FPY: {"success": 0.95, "warning": 0.90}
        Ejemplo para Defectos: {"success": 0.03, "warning": 0.05}
        Si es None → NEUTRAL (sin clasificación).
    direccion : str | None
        "higher_is_better" (FPY) o "lower_is_better" (Defectos).
        Obligatorio si thresholds no es None.

    Returns
    -------
    StatusType
        "success", "warning", "danger" o "neutral".
    """
    if thresholds is None or direccion is None:
        return "neutral"

    if direccion == "higher_is_better":
        if valor >= thresholds.get("success", float("inf")):
            return "success"
        if valor >= thresholds.get("warning", float("-inf")):
            return "warning"
        return "danger"

    if direccion == "lower_is_better":
        if valor <= thresholds.get("success", float("-inf")):
            return "success"
        if valor <= thresholds.get("warning", float("inf")):
            return "warning"
        return "danger"

    return "neutral"