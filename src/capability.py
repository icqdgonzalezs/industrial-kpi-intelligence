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

    if ppk >= 1.33:
        clasificacion = "Capaz (excelente)"
    elif ppk >= 1.00:
        clasificacion = "Marginal (monitorear)"
    else:
        clasificacion = "No capaz (acción requerida)"

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