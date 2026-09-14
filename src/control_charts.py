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


PROBABILIDAD_FUERA_3_SIGMA = 0.0027
"""P(|z| > 3) en una normal estándar. Falso positivo esperado de la Regla 1."""

UMBRAL_RATIO_ATENCION = 2.0
UMBRAL_RATIO_ALARMA = 5.0


def resumen_control_estadistico(serie: pd.Series, limites: dict) -> dict:
    """Contextualiza la Regla 1 con el número esperado de falsos positivos.

    Bajo la hipótesis de proceso estable, la probabilidad de que un punto
    individual caiga fuera de ±3σ es ~0.27% (P(|z| > 3) de una normal
    estándar). Con n grande, esa tasa produce un número ESPERADO de
    puntos fuera de control aun cuando el proceso esté perfectamente
    estable: reportar ese conteo sin contexto hace que un proceso
    normal parezca catastrófico.

    Criterios de estado (pragmáticos, no test formal):
        ratio <= 2.0  -> "estable"
        ratio <= 5.0  -> "atencion"
        ratio >  5.0  -> "alarma"

    Limitación conocida: asume independencia entre puntos consecutivos
    (sin autocorrelación). Válido para series aleatorias; en series con
    tendencia puede sobreestimar la tasa de outliers.
    """
    mascara = detectar_fuera_de_control(serie, limites)
    observados = int(mascara.sum())
    n = int(serie.dropna().shape[0])
    esperados = round(n * PROBABILIDAD_FUERA_3_SIGMA, 1)
    ratio = round(observados / esperados, 2) if esperados > 0 else 0.0

    if ratio <= UMBRAL_RATIO_ATENCION:
        estado = "estable"
    elif ratio <= UMBRAL_RATIO_ALARMA:
        estado = "atencion"
    else:
        estado = "alarma"

    mensajes = {
        "estable": (
            f"{observados} punto(s) fuera de ±3σ — dentro del rango "
            f"esperado para n={n:,} (~{esperados:.0f}). Proceso estable."
        ),
        "atencion": (
            f"{observados} punto(s) fuera de ±3σ — por encima del rango "
            f"esperado para n={n:,} (~{esperados:.0f}). Revisar."
        ),
        "alarma": (
            f"{observados} punto(s) fuera de ±3σ — muy por encima del "
            f"rango esperado para n={n:,} (~{esperados:.0f}). "
            f"Investigar causas asignables."
        ),
    }

    return {
        "observados": observados,
        "esperados": esperados,
        "ratio": ratio,
        "n": n,
        "estado": estado,
        "mensaje": mensajes[estado],
    }