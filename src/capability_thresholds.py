"""Umbrales de capacidad de proceso (Ppk, PPM) — SSOT.

Lee los umbrales desde ``config/quality_config.yaml`` (secciones
``ppk_thresholds`` y ``ppm_thresholds``) y los expone como funciones
puras de clasificación + wrappers que leen del YAML.

Diseño (SOLID/SRP):
    - capability_thresholds.py → clasificación pura + carga YAML (este módulo)
    - capability.py            → cálculo de Pp/Ppk + PPM (consumidor)
    - dashboard/               → presentación (color, iconos, banner)

Convención de umbrales (en YAML):
    ppk_thresholds:
      clase_mundial: 1.67
      capaz: 1.33
      marginal: 1.00

    ppm_thresholds:
      world_class: 100
      acceptable: 1000

Fallback: si el YAML falta o está incompleto, se usan los defaults
del módulo (``DEFAULT_PPK_THRESHOLDS``, ``DEFAULT_PPM_THRESHOLDS``).
Esto evita crash por config rota — comportamiento seguro por defecto.

Backward compatibility (ver TRASPASO_MAESTRO sección 4.2):
    Las constantes históricas ``UMBRAL_PPK_*`` y ``PPM_*`` en
    ``src/capability.py`` migraron aquí como fallback. Los tests
    existentes no las importan, por lo que la migración es transparente.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUALITY_CONFIG_PATH = PROJECT_ROOT / "config" / "quality_config.yaml"

# Defaults — fallback si el YAML falta o está incompleto.
# Valores heredados de la versión hardcodeada previa (Fix #7).
DEFAULT_PPK_THRESHOLDS: dict[str, float] = {
    "clase_mundial": 1.67,
    "capaz": 1.33,
    "marginal": 1.00,
}

DEFAULT_PPM_THRESHOLDS: dict[str, int] = {
    "world_class": 100,
    "acceptable": 1000,
}


# ---------------------------------------------------------------------
# Clasificación pura (sin I/O, 100% testeable)
# ---------------------------------------------------------------------


def clasificar_ppk_puro(ppk: float, umbrales: dict | None) -> str:
    """Clasifica Ppk según escala AIAG SPC / NIST 6.1.3 / ISO 22514.

    Parámetros
    ----------
    ppk : float
        Índice de capacidad real. Puede ser negativo (descentrado) o
        infinito (sigma=0 con media dentro de spec).
    umbrales : dict | None
        Dict con claves ``clase_mundial``, ``capaz``, ``marginal``.
        Si None o vacío, se usan los defaults del módulo.

    Returns
    -------
    str
        "Clase mundial" | "Capaz" | "Marginal" | "No capaz".
    """
    t = umbrales or DEFAULT_PPK_THRESHOLDS

    clase_mundial = t.get("clase_mundial", DEFAULT_PPK_THRESHOLDS["clase_mundial"])
    capaz = t.get("capaz", DEFAULT_PPK_THRESHOLDS["capaz"])
    marginal = t.get("marginal", DEFAULT_PPK_THRESHOLDS["marginal"])

    if ppk >= clase_mundial:
        return "Clase mundial"
    if ppk >= capaz:
        return "Capaz"
    if ppk >= marginal:
        return "Marginal"
    return "No capaz"


def clasificar_rendimiento_ppm_puro(ppm: int, umbrales: dict | None) -> str:
    """Clasifica el rendimiento (PPM total) en world_class/acceptable/low.

    Parámetros
    ----------
    ppm : int
        Piezas fuera de spec por millón.
    umbrales : dict | None
        Dict con claves ``world_class`` y ``acceptable``.
        Si None o vacío, se usan los defaults del módulo.

    Returns
    -------
    str
        "world_class" | "acceptable" | "low".
    """
    t = umbrales or DEFAULT_PPM_THRESHOLDS

    world_class = t.get("world_class", DEFAULT_PPM_THRESHOLDS["world_class"])
    acceptable = t.get("acceptable", DEFAULT_PPM_THRESHOLDS["acceptable"])

    if ppm <= world_class:
        return "world_class"
    if ppm <= acceptable:
        return "acceptable"
    return "low"


# ---------------------------------------------------------------------
# Loaders: leen secciones del YAML (cacheados)
# ---------------------------------------------------------------------


@lru_cache(maxsize=4)
def _leer_seccion_cacheados(path_str: str, seccion: str) -> dict:
    """Lee y cachea una sección del YAML.

    El argumento ``seccion`` permite usar la misma función para
    ``ppk_thresholds`` y ``ppm_thresholds`` sin duplicar el I/O.

    Cacheado por ``(path_str, seccion)`` — ``maxsize=4`` cubre los
    casos típicos: 1 path × 2 secciones + margen para tests.
    """
    ruta = Path(path_str)
    if not ruta.exists():
        return {}

    with ruta.open(encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    return config.get(seccion, {}) or {}


def cargar_umbrales_ppk(path: Path | None = None) -> dict:
    """Carga los umbrales Ppk desde quality_config.yaml.

    Parámetros
    ----------
    path : Path | None
        Ruta alternativa al YAML (útil en tests). Si es None,
        usa el path por defecto del proyecto.

    Returns
    -------
    dict
        Sección ``ppk_thresholds`` del YAML, o {} si no existe/está mal.
    """
    ruta = path if path is not None else QUALITY_CONFIG_PATH
    return _leer_seccion_cacheados(str(ruta), "ppk_thresholds")


def cargar_umbrales_ppm(path: Path | None = None) -> dict:
    """Carga los umbrales PPM desde quality_config.yaml.

    Análogo a ``cargar_umbrales_ppk`` para la sección ``ppm_thresholds``.
    """
    ruta = path if path is not None else QUALITY_CONFIG_PATH
    return _leer_seccion_cacheados(str(ruta), "ppm_thresholds")
