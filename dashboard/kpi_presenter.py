from __future__ import annotations

from typing import Any


def formatear_kpis(kpis: dict[str, Any]) -> dict[str, str]:
    """Convierte el resultado del KPI Engine en valores de presentación."""
    required = {
        "fpy",
        "tasa_defectos",
        "tasa_scrap",
        "tasa_reproceso",
        "total_producidas",
        "total_defectuosas",
        "total_scrap",
        "total_reproceso",
    }

    faltantes = required - set(kpis)

    if faltantes:
        raise ValueError(
            "Faltan KPI requeridos: "
            + ", ".join(sorted(faltantes))
        )

    return {
        "produccion": f"{int(kpis['total_producidas']):,}",
        "fpy": f"{kpis['fpy']:.1%}",
        "defectos": f"{kpis['tasa_defectos']:.1%}",
        "scrap": f"{kpis['tasa_scrap']:.1%}",
        "reproceso": f"{kpis['tasa_reproceso']:.1%}",
        "total_defectuosas": f"{int(kpis['total_defectuosas']):,}",
        "total_scrap": f"{int(kpis['total_scrap']):,}",
        "total_reproceso": f"{int(kpis['total_reproceso']):,}",
    }


# ---------------------------------------------------------------------
# Clasificación semántica de KPIs (success / warning / danger / neutral)
#
# NOTA: estos umbrales están documentados como constantes de este módulo.
# Externalizarlos a config/*.yaml está agendado para Semana 3 (onboarding
# por cliente: un Plant Manager querrá sus propios umbrales sin tocar
# código).
# ---------------------------------------------------------------------

CLASIFICACION_SUCCESS = "success"
CLASIFICACION_WARNING = "warning"
CLASIFICACION_DANGER = "danger"
CLASIFICACION_NEUTRAL = "neutral"

UMBRALES_FPY = {"success": 0.95, "warning": 0.90}  # higher_is_better
UMBRALES_DEFECTOS = {"success": 0.03, "warning": 0.05}  # lower_is_better
UMBRALES_SCRAP = {"success": 0.01, "warning": 0.02}  # lower_is_better


def _clasificar_higher_is_better(
    valor: float, umbral_success: float, umbral_warning: float
) -> str:
    """Ej. FPY: más alto es mejor."""
    if valor >= umbral_success:
        return CLASIFICACION_SUCCESS
    if valor >= umbral_warning:
        return CLASIFICACION_WARNING
    return CLASIFICACION_DANGER


def _clasificar_lower_is_better(
    valor: float, umbral_success: float, umbral_warning: float
) -> str:
    """Ej. Defectos, Scrap: más bajo es mejor."""
    if valor <= umbral_success:
        return CLASIFICACION_SUCCESS
    if valor <= umbral_warning:
        return CLASIFICACION_WARNING
    return CLASIFICACION_DANGER


def clasificar_kpis(kpis: dict[str, Any]) -> dict[str, str]:
    """Clasifica los KPIs del top en success/warning/danger/neutral.

    Parameters
    ----------
    kpis : dict
        Resultado crudo de src.kpis.calcular_kpis_globales (valores
        numéricos, no formateados).

    Returns
    -------
    dict[str, str]
        Claves: produccion, fpy, defectos, scrap.

    Notes
    -----
    "produccion" siempre "neutral": el volumen no tiene umbral universal
    de bueno/malo sin contexto de capacidad de planta.
    """
    required = {"fpy", "tasa_defectos", "tasa_scrap"}
    faltantes = required - set(kpis)

    if faltantes:
        raise ValueError(
            "Faltan KPI requeridos para clasificar: "
            + ", ".join(sorted(faltantes))
        )

    return {
        "produccion": CLASIFICACION_NEUTRAL,
        "fpy": _clasificar_higher_is_better(
            kpis["fpy"], UMBRALES_FPY["success"], UMBRALES_FPY["warning"]
        ),
        "defectos": _clasificar_lower_is_better(
            kpis["tasa_defectos"],
            UMBRALES_DEFECTOS["success"],
            UMBRALES_DEFECTOS["warning"],
        ),
        "scrap": _clasificar_lower_is_better(
            kpis["tasa_scrap"], UMBRALES_SCRAP["success"], UMBRALES_SCRAP["warning"]
        ),
    }