"""Carga y filtrado del dataset canónico para la capa FastAPI.

Wrapper delgado sobre ``src.data_loader.cargar_datos`` (lee CSV + lo
traduce al contrato analítico) y ``src.filter_engine.aplicar_filtros``
(aplica filtros categóricos + rango temporal).

Existe para que el router tenga una sola llamada: ``cargar_dataset_filtrado``.
No reimplementa lógica: delega 100% en los módulos de ``src/`` (SSOT).

Filosofía:
    - ``linea=None`` → sin filtro de línea (mapea al sentinel "Todas"
      que usa ``filter_engine`` para la UI legacy).
    - ``desde``/``hasta`` → opcionales, ``None`` = sin cota.
"""
from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd

from src.data_loader import cargar_datos
from src.filter_engine import aplicar_filtros

# Sentinel que ``aplicar_filtros`` interpreta como "sin filtro".
# No es un valor literal: es la convención de la UI legacy (dropdown
# con opción default "Todas"). Se expone como constante para que el
# resto de la capa ``app/`` no dependa del string mágico.
SIN_FILTRO_LINEA = "Todas"


def cargar_dataset_filtrado(
    linea: str | None = None,
    desde: date | None = None,
    hasta: date | None = None,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Carga el dataset canónico y lo filtra por línea + rango temporal.

    Args:
        linea: Identificador de línea (ej. "L1"). ``None`` = todas.
        desde: Fecha inferior inclusiva. ``None`` = sin cota inferior.
        hasta: Fecha superior inclusiva. ``None`` = sin cota superior.

    Returns:
        Tupla ``(df_filtrado, config_calidad)``:
        - ``df_filtrado``: DataFrame en contrato analítico legacy
          (columnas en español, ``fecha`` como datetime).
        - ``config_calidad``: dict de ``quality_config.yaml``.

    Raises:
        FileNotFoundError: si el dataset canónico o el config no existen.
        ValueError: si el dataset está vacío o no cumple el contrato.
    """
    df, config = cargar_datos()

    return (
        aplicar_filtros(
            df,
            fecha_inicio=desde,
            fecha_fin=hasta,
            linea=linea if linea is not None else SIN_FILTRO_LINEA,
        ),
        config,
    )