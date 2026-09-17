"""
Análisis de capacidad de proceso — Pp/Ppk.

Las funciones de este módulo calculan indicadores de capacidad para
variables continuas respecto de límites de especificación definidos
externamente.

Nomenclatura (NIST 6.1.3 / ISO 22514): este módulo calcula sigma a
partir de la desviación estándar TOTAL de la muestra (``ddof=1``, ver
``calcular_pp_ppk``), no de la variación intra-subgrupo (rango móvil
promedio / d2, que es la que ya usa correctamente src/control_charts.py
para las cartas I-MR). Por definición, eso es **Pp/Ppk** (capacidad
"global"/"performance"), no Cp/Cpk (capacidad de "corto plazo"). Antes
de esta versión, este módulo devolvía el mismo cálculo etiquetado como
"Cp/Cpk" — un error de nomenclatura, no de fórmula: el valor numérico
siempre fue correcto para lo que realmente mide.

Pendiente (backlog Semanas 5-6, ver docs/adr — no implementado aquí):
agregar ``calcular_cp_cpk_intragrupo()`` usando la constante d2 y el
rango móvil promedio (reutilizando ``src.control_charts``) para tener
Cp/Cpk real (corto plazo) junto a Pp/Ppk (este módulo).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.capability_thresholds import (
    cargar_umbrales_ppk,
    cargar_umbrales_ppm,
    clasificar_ppk_puro,
    clasificar_rendimiento_ppm_puro,
)

# ---------------------------------------------------------------------
# Clasificación de capacidad: delega al SSOT (capability_thresholds.py).
# Los umbrales viven en config/quality_config.yaml sección ppk_thresholds.
# Este módulo solo CONSUME el SSOT — no define umbrales hardcodeados.
# ---------------------------------------------------------------------


def clasificar_ppk(ppk: float, umbrales: dict | None = None) -> str:
    """Clasifica Ppk según benchmarks AIAG SPC / NIST 6.1.3 / ISO 22514.

    Los umbrales se leen desde ``config/quality_config.yaml`` sección
    ``ppk_thresholds`` (SSOT). Si el YAML falta, se usan defaults de
    ``src.capability_thresholds``.

    Args:
        ppk: índice de capacidad real. Puede ser negativo (proceso
             descentrado) o infinito (sigma=0 con media dentro de spec).
        umbrales: dict opcional con claves ``clase_mundial``, ``capaz``,
             ``marginal``. Si es None, se leen del YAML. Útil en tests
             para inyectar config sin I/O.

    Returns:
        Uno de los 4 niveles de la escala estándar industrial.
    """
    if umbrales is None:
        umbrales = cargar_umbrales_ppk()
    return clasificar_ppk_puro(ppk, umbrales)


def calcular_pp_ppk(
    valores: pd.Series,
    lsl: float,
    usl: float,
) -> dict:
    """Calcula Pp y Ppk para una variable continua.

    Parameters
    ----------
    valores : pd.Series
        Observaciones del proceso.
    lsl : float
        Límite inferior de especificación.
    usl : float
        Límite superior de especificación.

    Returns
    -------
    dict
        Resultados de capacidad y estadísticos descriptivos. Claves:
        pp, ppk, media, sigma, n, clasificacion.

    Notes
    -----
    La interpretación de Pp/Ppk requiere considerar los supuestos
    estadísticos del proceso. Estos índices no demuestran por sí mismos
    que el proceso esté bajo control estadístico (para eso, ver
    src/control_charts.py).
    """
    if not isinstance(valores, pd.Series):
        valores = pd.Series(valores)

    if not np.isfinite(lsl) or not np.isfinite(usl):
        return {
            "pp": None,
            "ppk": None,
            "media": None,
            "sigma": None,
            "n": 0,
            "clasificacion": "Límites inválidos",
        }

    if usl <= lsl:
        return {
            "pp": None,
            "ppk": None,
            "media": None,
            "sigma": None,
            "n": 0,
            "clasificacion": "Límites inválidos",
        }

    valores = pd.to_numeric(valores, errors="coerce")
    valores = valores.replace([np.inf, -np.inf], np.nan).dropna()

    n = len(valores)

    if n < 2:
        return {
            "pp": None,
            "ppk": None,
            "media": None,
            "sigma": None,
            "n": n,
            "clasificacion": "Datos insuficientes",
        }

    media = float(valores.mean())
    sigma = float(valores.std(ddof=1))

    if sigma == 0:
        if lsl <= media <= usl:
            return {
                "pp": float("inf"),
                "ppk": float("inf"),
                "media": round(media, 3),
                "sigma": 0.0,
                "n": n,
                "clasificacion": "Sin variabilidad",
            }

        return {
            "pp": float("inf"),
            "ppk": float("-inf"),
            "media": round(media, 3),
            "sigma": 0.0,
            "n": n,
            "clasificacion": "No capaz (fuera de especificación)",
        }

    pp = (usl - lsl) / (6 * sigma)

    ppk = min(
        (usl - media) / (3 * sigma),
        (media - lsl) / (3 * sigma),
    )

    clasificacion = clasificar_ppk(ppk)

    return {
        "pp": round(pp, 3),
        "ppk": round(ppk, 3),
        "media": round(media, 3),
        "sigma": round(sigma, 4),
        "n": n,
        "clasificacion": clasificacion,
    }


def resumen_capacidad(
    df: pd.DataFrame,
    variables_config: dict,
) -> pd.DataFrame:
    """Calcula Pp/Ppk para las variables definidas en configuración."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("El objeto de entrada debe ser un pandas.DataFrame.")

    if df.empty:
        raise ValueError("El dataset no puede estar vacío.")

    filas = []

    for columna, cfg in variables_config.items():
        if columna not in df.columns:
            raise ValueError(
                f"La columna '{columna}' no existe en el dataset."
            )

        for clave in ("nombre", "lsl", "usl"):
            if clave not in cfg:
                raise ValueError(
                    f"La configuración de '{columna}' no contiene '{clave}'."
                )

        resultado = calcular_pp_ppk(
            df[columna],
            lsl=cfg["lsl"],
            usl=cfg["usl"],
        )

        resultado["variable"] = cfg["nombre"]
        resultado["columna"] = columna
        resultado["lsl"] = cfg["lsl"]
        resultado["usl"] = cfg["usl"]

        filas.append(resultado)

    return pd.DataFrame(filas)





# ---------------------------------------------------------------------
# Rendimiento respecto a especificación (% dentro, PPM)
#
# Complementa a Pp/Ppk con el dato operativo que un ingeniero de calidad
# usa para decidir acción: cuántas piezas cumplen spec y cuántas no.
# ---------------------------------------------------------------------

def calcular_rendimiento_spec(
    valores: pd.Series,
    lsl: float,
    usl: float,
    umbrales_ppm: dict | None = None,
) -> dict:
    """Calcula el rendimiento respecto a especificación.

    Parameters
    ----------
    valores : pd.Series
        Observaciones del proceso.
    lsl : float
        Límite inferior de especificación (inclusive).
    usl : float
        Límite superior de especificación (inclusive).
    umbrales_ppm : dict | None
        Umbrales de clasificación PPM (``world_class``, ``acceptable``).
        Si es None, se leen del YAML (SSOT). Útil en tests.

    Returns
    -------
    dict
        n             : int — observaciones válidas
        dentro        : int — piezas dentro de [LSL, USL]
        bajo_lsl      : int — piezas < LSL
        sobre_usl     : int — piezas > USL
        pct_dentro    : float — % dentro de spec
        pct_bajo_lsl  : float — % bajo LSL
        pct_sobre_usl : float — % sobre USL
        ppm_total     : int — piezas fuera por millón
        clasificacion : str — "world_class" | "acceptable" | "low" | "sin_datos"

    Notes
    -----
    Los bordes (x == LSL, x == USL) se cuentan como DENTRO de spec, según
    la convención industrial de límites inclusivos.
    """
    if not isinstance(valores, pd.Series):
        valores = pd.Series(valores)

    vacio = {
        "n": 0,
        "dentro": 0,
        "bajo_lsl": 0,
        "sobre_usl": 0,
        "pct_dentro": 0.0,
        "pct_bajo_lsl": 0.0,
        "pct_sobre_usl": 0.0,
        "ppm_total": 0,
        "clasificacion": "sin_datos",
    }

    if not np.isfinite(lsl) or not np.isfinite(usl) or usl <= lsl:
        return vacio

    valores = pd.to_numeric(valores, errors="coerce")
    valores = valores.replace([np.inf, -np.inf], np.nan).dropna()

    n = len(valores)
    if n == 0:
        return vacio

    bajo_lsl_mask = valores < lsl
    sobre_usl_mask = valores > usl
    dentro_mask = ~(bajo_lsl_mask | sobre_usl_mask)

    bajo_lsl = int(bajo_lsl_mask.sum())
    sobre_usl = int(sobre_usl_mask.sum())
    dentro = int(dentro_mask.sum())

    pct_dentro = round(dentro / n * 100, 3)
    pct_bajo_lsl = round(bajo_lsl / n * 100, 3)
    pct_sobre_usl = round(sobre_usl / n * 100, 3)

    fuera = bajo_lsl + sobre_usl
    ppm_total = round(fuera / n * 1_000_000)

    if umbrales_ppm is None:
        umbrales_ppm = cargar_umbrales_ppm()

    clasificacion = clasificar_rendimiento_ppm_puro(ppm_total, umbrales_ppm)

    return {
        "n": n,
        "dentro": dentro,
        "bajo_lsl": bajo_lsl,
        "sobre_usl": sobre_usl,
        "pct_dentro": pct_dentro,
        "pct_bajo_lsl": pct_bajo_lsl,
        "pct_sobre_usl": pct_sobre_usl,
        "ppm_total": ppm_total,
        "clasificacion": clasificacion,
    }