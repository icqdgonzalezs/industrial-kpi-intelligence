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
# NOTA HONESTA: estos umbrales NO existían en ningún YAML del proyecto
# antes de este cambio (se verificó con grep contra config/*.yaml antes
# de escribir esto). Se introducen aquí, como constantes documentadas
# en este módulo — no en config/, porque esta tarea restringe
# explícitamente no tocar esa carpeta. Si más adelante se quiere
# externalizar a YAML (para que un Plant Manager pueda ajustar sus
# propios umbrales sin tocar código), es un cambio de alcance distinto,
# no asumido aquí.
# ---------------------------------------------------------------------

CLASIFICACION_SUCCESS = "success"
CLASIFICACION_WARNING = "warning"
CLASIFICACION_DANGER = "danger"
CLASIFICACION_NEUTRAL = "neutral"

# (success_at, warning_at): el límite en el que empieza cada tramo.
UMBRALES_FPY = {"success": 0.95, "warning": 0.90}  # higher_is_better
UMBRALES_DEFECTOS = {"success": 0.03, "warning": 0.05}  # lower_is_better
UMBRALES_SCRAP = {"success": 0.01, "warning": 0.02}  # lower_is_better


def _clasificar_higher_is_better(valor: float, umbral_success: float, umbral_warning: float) -> str:
    """Ej. FPY: más alto es mejor."""
    if valor >= umbral_success:
        return CLASIFICACION_SUCCESS
    if valor >= umbral_warning:
        return CLASIFICACION_WARNING
    return CLASIFICACION_DANGER


def _clasificar_lower_is_better(valor: float, umbral_success: float, umbral_warning: float) -> str:
    """Ej. Tasa de defectos, tasa de scrap: más bajo es mejor."""
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
        Resultado crudo de src.kpis.calcular_kpis_globales (NO el
        resultado ya formateado de formatear_kpis — se necesitan los
        valores numéricos, no strings con "%").

    Returns
    -------
    dict[str, str]
        Claves: produccion, fpy, defectos, scrap. Cada valor es una de
        "success"/"warning"/"danger"/"neutral" — pensado para usarse
        directamente como sufijo de className: f"kpi-value--{clave}".

    Raises
    ------
    ValueError
        Si faltan los KPI numéricos requeridos (fpy, tasa_defectos,
        tasa_scrap).

    Notes
    -----
    "produccion" siempre clasifica como "neutral": el volumen de
    producción no tiene un umbral universal de bueno/malo sin contexto
    de capacidad de planta (una producción "baja" puede ser exactamente
    la esperada si hubo menos turnos programados). No se inventa un
    umbral para eso aquí.
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
            kpis["tasa_defectos"], UMBRALES_DEFECTOS["success"], UMBRALES_DEFECTOS["warning"]
        ),
        "scrap": _clasificar_lower_is_better(
            kpis["tasa_scrap"], UMBRALES_SCRAP["success"], UMBRALES_SCRAP["warning"]
        ),
    }
