"""KPIs agregados para el reporte ejecutivo (IA.3).

Orquesta las funciones de dominio de ``src/`` y devuelve un dict
plano listo para serializar al prompt del LLM.

No reimplementa cálculo: delega 100% en ``src.kpis`` y ``src.oee``.

Diseño:
    - ``calcular_kpis_ejecutivos`` es puro (sin HTTP, sin DB, sin LLM).
    - Deriva ``ppm`` a partir de ``tasa_defectos`` (KPI estándar de
      negocio que no viene explícito en ``src.kpis``). Se calcula acá,
      no en el prompt: el LLM no debería multiplicar.
    - ``top_defectos`` usa ``calcular_pareto`` y corta a TOP_DEFECTOS.
      Si no hay defectos, Pareto viene vacío y se devuelve ``[]``.
"""
from __future__ import annotations

from typing import Any

import pandas as pd

from src.kpis import calcular_kpis_globales, calcular_pareto
from src.oee import adaptar_contrato_canonico, calcular_oee_ponderado

# Cantidad de defectos a incluir en el reporte ejecutivo.
# Decisión de producto: 3 es el mínimo accionable. Cambiar acá si
# negocio pide otro número.
TOP_DEFECTOS = 3


def calcular_kpis_ejecutivos(df: pd.DataFrame) -> dict[str, Any]:
    """Agrega los KPIs de negocio del período filtrado.

    Args:
        df: DataFrame filtrado en contrato analítico legacy
            (columnas en español). No debe estar vacío.

    Returns:
        Dict con tres bloques + un contador:
        - ``oee``: dict de ``src.oee.calcular_oee_ponderado``
          (disponibilidad, rendimiento, calidad, oee, clasificacion,
          n_registros, units_produced_total, units_defective_total).
        - ``operacional``: dict de ``src.kpis.calcular_kpis_globales``
          + ``ppm`` derivado.
        - ``top_defectos``: list[dict] con los TOP_DEFECTOS defectos
          por frecuencia (vacío si no hay defectos en el período).
        - ``n_registros``: cantidad de filas del DataFrame filtrado.

    Raises:
        ValueError: si el DataFrame no cumple el contrato de ``src/``
            (propaga el error de las validaciones internas).
    """
    oee = calcular_oee_ponderado(adaptar_contrato_canonico(df))
    operacional = calcular_kpis_globales(df)

    # PPM = partes por millón. Es tasa_defectos * 1e6.
    # ``tasa_defectos`` viene en [0,1] desde src.kpis.
    ppm = round(float(operacional["tasa_defectos"]) * 1_000_000, 1)

    pareto = calcular_pareto(df)
    top_defectos = (
        pareto.head(TOP_DEFECTOS).to_dict("records")
        if not pareto.empty
        else []
    )

    return {
        "oee": oee,
        "operacional": {**operacional, "ppm": ppm},
        "top_defectos": top_defectos,
        "n_registros": int(len(df)),
    }
