"""Clasificación de KPIs industriales según umbrales declarativos.

Lee la configuración de umbrales desde config/quality_config.yaml
(sección `kpi_thresholds`) y clasifica cada KPI en uno de 3 estados:
SUCCESS (verde), WARNING (ámbar), DANGER (rojo) o NEUTRAL (sin umbral).

Diseño (SOLID/SRP):
    - kpi_thresholds.py   → clasificación de estado (este módulo)
    - kpi_presenter.py    → formateo + consumo
    - components          → renderizado visual

Convención de umbrales (en YAML):
    kpi_thresholds:
      <nombre_kpi>:
        direction: higher_is_better | lower_is_better
        success: <float>
        warning: <float>

    - higher_is_better (ej. FPY): verde si valor >= success, ámbar si >= warning
    - lower_is_better  (ej. Scrap): verde si valor <= success, ámbar si <= warning
    - Sin umbral para el KPI dado: NEUTRAL
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

import yaml

StatusType = Literal["success", "warning", "danger", "neutral"]
DireccionType = Literal["higher_is_better", "lower_is_better"]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUALITY_CONFIG_PATH = PROJECT_ROOT / "config" / "quality_config.yaml"


# ---------------------------------------------------------------------
# Núcleo: clasificación pura (sin I/O, 100% testeable)
# ---------------------------------------------------------------------


def clasificar_kpi(
    valor: float,
    thresholds: dict | None,
    direccion: DireccionType | None = None,
) -> StatusType:
    """Clasifica un valor de KPI en SUCCESS / WARNING / DANGER / NEUTRAL.

    Parameters
    ----------
    valor : float
        Valor numérico del KPI (0.954 = 95.4%).
    thresholds : dict | None
        Dict con claves `success` y `warning`.
        Ejemplo FPY: {"success": 0.95, "warning": 0.90}
        Si es None → NEUTRAL (sin clasificación).
    direccion : str | None
        "higher_is_better" (FPY) o "lower_is_better" (Defectos/Scrap).
        Obligatorio si thresholds no es None.

    Returns
    -------
    StatusType
        "success", "warning", "danger" o "neutral".
    """
    if not thresholds or direccion is None:
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


# ---------------------------------------------------------------------
# Loader: lee umbrales desde YAML (cacheado)
# ---------------------------------------------------------------------


@lru_cache(maxsize=1)
def _leer_umbrales_cacheados(path_str: str) -> dict:
    """Lee y cachea la sección `kpi_thresholds` del YAML.

    Separado de `cargar_umbrales_kpi` para poder cachear por path (str)
    sin romper si el caller pasa un Path no-hashable.
    """
    ruta = Path(path_str)
    if not ruta.exists():
        return {}

    with ruta.open(encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    return config.get("kpi_thresholds", {}) or {}


def cargar_umbrales_kpi(path: Path | None = None) -> dict:
    """Carga los umbrales de KPI desde quality_config.yaml.

    Parameters
    ----------
    path : Path | None
        Ruta alternativa al YAML (útil en tests). Si es None, usa
        el path por defecto del proyecto.

    Returns
    -------
    dict
        Sección kpi_thresholds del YAML, o {} si no existe/está mal.
    """
    ruta = path if path is not None else QUALITY_CONFIG_PATH
    return _leer_umbrales_cacheados(str(ruta))


# ---------------------------------------------------------------------
# Wrapper: clasifica por nombre, resolviendo umbrales automáticamente
# ---------------------------------------------------------------------


def clasificar_kpi_por_nombre(
    nombre: str,
    valor: float,
    umbrales: dict | None = None,
) -> StatusType:
    """Clasifica un KPI por nombre, resolviendo sus umbrales del YAML.

    Ejemplo:
        clasificar_kpi_por_nombre("fpy", 0.97) -> "success"
        clasificar_kpi_por_nombre("tasa_scrap", 0.005) -> "success"

    Parameters
    ----------
    nombre : str
        Clave del KPI en la sección kpi_thresholds (ej. "fpy").
    valor : float
        Valor numérico a clasificar.
    umbrales : dict | None
        Dict de umbrales pre-cargado (útil en tests para inyectar
        config sin I/O). Si es None, lee del YAML del proyecto.

    Returns
    -------
    StatusType
        "success" | "warning" | "danger" | "neutral".
    """
    config_umbrales = umbrales if umbrales is not None else cargar_umbrales_kpi()
    config_kpi = config_umbrales.get(nombre)

    if not config_kpi:
        return "neutral"

    return clasificar_kpi(
        valor,
        {"success": config_kpi["success"], "warning": config_kpi["warning"]},
        config_kpi["direction"],
    )