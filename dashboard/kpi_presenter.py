from __future__ import annotations

from typing import Any

from src.kpi_thresholds import clasificar_kpi_por_nombre


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
# Clasificación semántica de KPIs (delegada a src/kpi_thresholds).
#
# Los umbrales viven en config/quality_config.yaml (sección
# `kpi_thresholds`), no en este módulo. Este presenter solo consume
# la clasificación — la lógica de clasificar es responsabilidad de
# src/kpi_thresholds.clasificar_kpi_por_nombre.
# ---------------------------------------------------------------------


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
    de bueno/malo sin contexto de capacidad de planta. Este es un caso
    de uso donde la ausencia de umbral es una decisión de negocio, no
    un olvido.
    """
    required = {"fpy", "tasa_defectos", "tasa_scrap"}
    faltantes = required - set(kpis)

    if faltantes:
        raise ValueError(
            "Faltan KPI requeridos para clasificar: "
            + ", ".join(sorted(faltantes))
        )

    return {
        "produccion": "neutral",
        "fpy": clasificar_kpi_por_nombre("fpy", kpis["fpy"]),
        "defectos": clasificar_kpi_por_nombre("tasa_defectos", kpis["tasa_defectos"]),
        "scrap": clasificar_kpi_por_nombre("tasa_scrap", kpis["tasa_scrap"]),
    }