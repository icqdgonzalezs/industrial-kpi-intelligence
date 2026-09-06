"""Motor de diagnóstico y priorización de hallazgos operacionales.

Combina KPIs por dimensión, capacidad de proceso (Cp/Cpk) y Pareto de
defectos en una lista de hallazgos rankeados por severidad, replicando
el criterio que seguiría un ingeniero de calidad al revisar el turno:
¿qué amerita atención primero?

Todos los umbrales están documentados y fueron calibrados contra el
dataset sintético del proyecto (ver docstrings de cada regla) — no son
números arbitrarios elegidos para "que se vea bien".
"""

from __future__ import annotations

import pandas as pd

from src.kpis import (
    calcular_kpis_globales,
    calcular_kpis_por_dimension,
    calcular_pareto,
    identificar_lote_critico,
)

SEVERIDAD_ORDEN = {"PRIORITY": 0, "WATCH": 1, "INFO": 2}

# Hotspots de equipo/turno: ratio respecto del promedio de planta.
# Calibrado contra el dataset base: el equipo con peor desempeño
# (tasa_defectos ~5.6% vs. 4.6% promedio) da un ratio ~1.22x.
UMBRAL_HOTSPOT_WATCH = 1.15
UMBRAL_HOTSPOT_PRIORITY = 1.40
MINIMO_LOTES_HOTSPOT = 15  # evita flags con muestras pequeñas/ruidosas

# Pareto: causa dominante vs. concentración en pocas causas.
# Calibrado contra el dataset base: la causa principal ("Mancha")
# concentra ~38.5% individual y las 2 principales ~61.9% acumulado.
UMBRAL_PARETO_DOMINANTE = 35.0
UMBRAL_PARETO_CONCENTRADO = 60.0

# Lote crítico: se reporta siempre como contexto (INFO); se promueve
# a WATCH solo si es un outlier extremo (>= 3x el promedio de planta).
UMBRAL_LOTE_CRITICO_MULTIPLO = 3.0


def _diagnosticar_hotspots(df: pd.DataFrame, dimension: str, etiqueta: str) -> list[dict]:
    """Detecta equipos/turnos con tasa de defectos por sobre el promedio de planta."""
    promedio_planta = calcular_kpis_globales(df)["tasa_defectos"]
    por_dimension = calcular_kpis_por_dimension(df, dimension)

    hallazgos = []

    for _, fila in por_dimension.iterrows():
        if fila["n_lotes"] < MINIMO_LOTES_HOTSPOT:
            continue

        ratio = fila["tasa_defectos"] / promedio_planta if promedio_planta > 0 else 0.0

        if ratio >= UMBRAL_HOTSPOT_PRIORITY:
            severidad = "PRIORITY"
        elif ratio >= UMBRAL_HOTSPOT_WATCH:
            severidad = "WATCH"
        else:
            continue

        hallazgos.append(
            {
                "severidad": severidad,
                "categoria": etiqueta,
                "titulo": f"{etiqueta}: {fila[dimension]}",
                "mensaje": (
                    f"Tasa de defectos {fila['tasa_defectos']:.1%}, "
                    f"{ratio:.2f}x el promedio de planta ({promedio_planta:.1%}). "
                    f"Basado en {int(fila['n_lotes'])} lotes."
                ),
                "score": round(ratio, 4),
            }
        )

    return hallazgos


def _diagnosticar_capacidad(capacidad: pd.DataFrame | None) -> list[dict]:
    """Traduce la clasificación de Cp/Cpk en hallazgos priorizados."""
    if capacidad is None or capacidad.empty:
        return []

    hallazgos = []

    for _, fila in capacidad.iterrows():
        clasificacion = str(fila.get("clasificacion", ""))
        texto = clasificacion.lower()

        if "no capaz" in texto:
            severidad = "PRIORITY"
        elif "marginal" in texto:
            severidad = "WATCH"
        else:
            continue

        cpk = fila.get("cpk")
        cpk_valido = pd.notna(cpk)
        cpk_texto = f"{float(cpk):.2f}" if cpk_valido else "Sin datos"

        hallazgos.append(
            {
                "severidad": severidad,
                "categoria": "Capacidad de proceso",
                "titulo": f"Variable: {fila['variable']}",
                "mensaje": (
                    f"Cpk = {cpk_texto} ({clasificacion}). "
                    f"Límites de especificación: [{fila['lsl']}, {fila['usl']}]."
                ),
                "score": round(max(0.0, 1.33 - float(cpk)), 4) if cpk_valido else 1.33,
            }
        )

    return hallazgos


def _diagnosticar_pareto(df: pd.DataFrame) -> list[dict]:
    """Detecta concentración de causas de defecto (análisis Pareto)."""
    pareto = calcular_pareto(df)

    if pareto.empty:
        return []

    principal = pareto.iloc[0]
    top_1_pct = float(principal["porcentaje"])
    top_2_cumulado = float(pareto.iloc[: min(2, len(pareto))]["porcentaje"].sum())

    if top_1_pct >= UMBRAL_PARETO_DOMINANTE:
        return [
            {
                "severidad": "PRIORITY",
                "categoria": "Pareto de defectos",
                "titulo": f"Causa dominante: {principal['defecto']}",
                "mensaje": (
                    f"'{principal['defecto']}' concentra el {top_1_pct:.1f}% "
                    "de las unidades defectuosas — una sola causa explica "
                    "la mayor parte del problema de calidad."
                ),
                "score": round(top_1_pct, 2),
            }
        ]

    if top_2_cumulado >= UMBRAL_PARETO_CONCENTRADO:
        return [
            {
                "severidad": "WATCH",
                "categoria": "Pareto de defectos",
                "titulo": "Defectos concentrados en pocas causas",
                "mensaje": (
                    f"Las 2 causas principales acumulan {top_2_cumulado:.1f}% "
                    "de las unidades defectuosas."
                ),
                "score": round(top_2_cumulado, 2),
            }
        ]

    return []


def _diagnosticar_lote_critico(df: pd.DataFrame) -> list[dict]:
    """Contextualiza el lote con peor desempeño del período."""
    lote = identificar_lote_critico(df)
    promedio_planta = calcular_kpis_globales(df)["tasa_defectos"]

    tasa_lote = float(lote["tasa_defectos_lote"])
    ratio = tasa_lote / promedio_planta if promedio_planta > 0 else 0.0

    severidad = "WATCH" if ratio >= UMBRAL_LOTE_CRITICO_MULTIPLO else "INFO"

    return [
        {
            "severidad": severidad,
            "categoria": "Lote crítico",
            "titulo": f"Lote {lote['lote']}",
            "mensaje": f"Tasa de defectos {tasa_lote:.1%}, {ratio:.1f}x el promedio de planta.",
            "score": round(ratio, 4),
        }
    ]


def generar_diagnostico(
    df: pd.DataFrame,
    capacidad: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Genera el panel de diagnóstico priorizado.

    Combina 4 fuentes de señal — hotspots de equipo, hotspots de turno,
    capacidad de proceso (Cp/Cpk) y concentración de Pareto — más el
    lote crítico como contexto, y devuelve los hallazgos ordenados por
    severidad (PRIORITY > WATCH > INFO) y, dentro de cada nivel, por
    ``score`` descendente.

    Notes
    -----
    ``score`` no es comparable entre categorías (mezcla ratios, puntos
    porcentuales y déficit de Cpk): solo ordena hallazgos dentro del
    mismo nivel de severidad, nunca entre categorías distintas.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset filtrado (mismo universo que alimenta KPIs y Pareto).
    capacidad : pd.DataFrame, optional
        Resultado de ``src.capability.resumen_capacidad``. Si no se
        provee, se omiten los hallazgos de capacidad de proceso.

    Returns
    -------
    pd.DataFrame
        Columnas: severidad, categoria, titulo, mensaje, score.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("El objeto de entrada debe ser un pandas.DataFrame.")

    if df.empty:
        raise ValueError("El dataset no puede estar vacío.")

    hallazgos: list[dict] = []

    hallazgos += _diagnosticar_hotspots(df, "equipo", "Equipo")
    hallazgos += _diagnosticar_hotspots(df, "turno", "Turno")
    hallazgos += _diagnosticar_capacidad(capacidad)
    hallazgos += _diagnosticar_pareto(df)
    hallazgos += _diagnosticar_lote_critico(df)

    resultado = pd.DataFrame(
        hallazgos,
        columns=["severidad", "categoria", "titulo", "mensaje", "score"],
    )

    if resultado.empty:
        return resultado

    resultado["_orden_severidad"] = resultado["severidad"].map(SEVERIDAD_ORDEN)

    resultado = (
        resultado.sort_values(["_orden_severidad", "score"], ascending=[True, False])
        .drop(columns="_orden_severidad")
        .reset_index(drop=True)
    )

    return resultado
