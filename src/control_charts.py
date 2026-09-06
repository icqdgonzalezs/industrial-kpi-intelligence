"""Carta de control estadístico I-MR (Individuals - Moving Range).

Detecta causas asignables de variación: puntos fuera de los límites de
control (calculados desde el proceso mismo, no desde especificación).
Complementa a capability.py: Cp/Cpk mide si el proceso CUMPLE spec;
esto mide si el proceso está EN CONTROL estadístico.
"""

from __future__ import annotations

import pandas as pd

CONSTANTE_D2 = 1.128  # subgrupo n=1 (carta Individuals)


def calcular_moving_range(serie: pd.Series) -> pd.Series:
    """Rango móvil: |x_i - x_(i-1)|."""
    return serie.diff().abs()


def calcular_limites_control(serie: pd.Series) -> dict:
    """Límites de control de la carta I (Individuals) vía rango móvil promedio."""
    if not isinstance(serie, pd.Series):
        raise TypeError("Se requiere un pandas.Series.")
    if serie.dropna().empty:
        raise ValueError("La serie no puede estar vacía.")

    mr = calcular_moving_range(serie).dropna()
    mr_bar = mr.mean() if not mr.empty else 0.0
    media = serie.mean()
    sigma_estimado = mr_bar / CONSTANTE_D2 if mr_bar > 0 else 0.0

    return {
        "media": media,
        "ucl": media + 3 * sigma_estimado,
        "lcl": media - 3 * sigma_estimado,
        "mr_bar": mr_bar,
    }


def detectar_fuera_de_control(serie: pd.Series, limites: dict) -> pd.Series:
    """Regla Western Electric #1: punto más allá de los límites de control (3σ)."""
    return (serie > limites["ucl"]) | (serie < limites["lcl"])
