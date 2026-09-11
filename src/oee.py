"""OEE (Overall Equipment Effectiveness) engine — ISA-95 / TPM compliant.

Design principle (matches src/kpis.py):
    validation.py   -> protects data quality
    oee.py          -> protects calculation integrity
    dashboard/*.py  -> presents results (no math lives there)

OEE = Availability x Performance x Quality

Definitions (ISA-95 / TPM, non-negotiable per project convention):

    Availability = Run Time / Planned Production Time
        Planned Production Time = Total Time - Planned Downtime
        Run Time = Planned Production Time - Unplanned Downtime
        -> Availability EXCLUDES planned downtime (changeovers, breaks,
           scheduled maintenance) from the denominator. Planned downtime
           is not a loss; only unplanned downtime is.

    Performance = (Ideal Cycle Time x Total Units Produced) / Run Time
        -> Compares actual output rate against the equipment's rated
           (ideal) cycle time. Capped at 1.0: a process cannot be
           credited for running "faster than physically possible" —
           values above 1.0 indicate a bad ideal_cycle_time assumption
           in configuration, not real overperformance.

    Quality = Good Units / Total Units Produced
        Good Units = Total Units Produced - Defective Units
        -> This is exactly First-Pass Yield (see src/kpis.py fpy),
           reused here for consistency: one FPY definition in the
           whole codebase, not two.

    OEE = Availability x Performance x Quality

World-class benchmark (TPM convention used for classification in this
project, NOT a universal law):
    OEE >= 0.85           -> "world_class"
    0.60 <= OEE < 0.85     -> "acceptable"
    OEE < 0.60             -> "low"

H2 (stable keys): clasificar_oee() returns a stable, language-independent
key, not display text. Translation to Spanish (or any other language)
happens exclusively in the UI presentation layer — see
dashboard/oee_presenter.py. This module never imports Dash and never
decides how a result is displayed; it only decides what the result IS.

Required input columns per equipment/period record:
    planned_time_min        : float  (total scheduled time, minutes)
    planned_downtime_min     : float  (changeovers, breaks, scheduled PM)
    unplanned_downtime_min   : float  (breakdowns, unplanned stops)
    ideal_cycle_time_sec     : float  (rated cycle time per unit, seconds)
    units_produced           : int
    units_defective          : int

These columns do not exist yet in data/calidad_muestra.csv. Until the
data model is extended (see Fix #1 recommendation), calcular_oee() will
raise ValueError rather than silently fabricating a number — consistent
with the project's golden rule #5 ("No calcular KPIs con denominadores
invalidos") and rule #58 in the master plan ("no calcularemos OEE si no
tenemos los componentes necesarios").
"""

from __future__ import annotations

import pandas as pd

REQUIRED_OEE_COLUMNS = [
    "planned_time_min",
    "planned_downtime_min",
    "unplanned_downtime_min",
    "ideal_cycle_time_sec",
    "units_produced",
    "units_defective",
]

UMBRAL_OEE_CLASE_MUNDIAL = 0.85
UMBRAL_OEE_ACEPTABLE = 0.60

CLASIFICACION_WORLD_CLASS = "world_class"
CLASIFICACION_ACCEPTABLE = "acceptable"
CLASIFICACION_LOW = "low"


def _validar_dataframe(df: pd.DataFrame) -> None:
    """Valida que la entrada sea un DataFrame no vacio."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("El objeto de entrada debe ser un pandas.DataFrame.")

    if df.empty:
        raise ValueError("El dataset no puede estar vacio.")


def _validar_columnas_oee(df: pd.DataFrame) -> None:
    """Valida la existencia y tipo de las columnas requeridas para OEE."""
    _validar_dataframe(df)

    faltantes = [
        columna for columna in REQUIRED_OEE_COLUMNS if columna not in df.columns
    ]

    if faltantes:
        raise ValueError(
            "Faltan columnas requeridas para calcular OEE: "
            + ", ".join(faltantes)
            + ". El dataset actual no soporta OEE hasta extender el schema "
            "con tiempos de paro planificado/no planificado y tiempo de "
            "ciclo ideal."
        )

    if not df[REQUIRED_OEE_COLUMNS].apply(
        lambda serie: pd.api.types.is_numeric_dtype(serie)
    ).all():
        raise ValueError("Todas las columnas de OEE deben ser numericas.")

    if df[REQUIRED_OEE_COLUMNS].isna().any().any():
        raise ValueError("Las columnas de OEE no pueden contener valores nulos.")


def _validar_integridad_oee(df: pd.DataFrame) -> None:
    """Valida relaciones fisicas basicas necesarias para que OEE sea valido."""
    if (df["planned_time_min"] <= 0).any():
        raise ValueError("planned_time_min debe ser mayor que cero en todos los registros.")

    if (df["planned_downtime_min"] < 0).any():
        raise ValueError("planned_downtime_min no puede ser negativo.")

    if (df["unplanned_downtime_min"] < 0).any():
        raise ValueError("unplanned_downtime_min no puede ser negativo.")

    if (df["ideal_cycle_time_sec"] <= 0).any():
        raise ValueError("ideal_cycle_time_sec debe ser mayor que cero.")

    if (df["units_produced"] < 0).any():
        raise ValueError("units_produced no puede ser negativo.")

    if (df["units_defective"] < 0).any():
        raise ValueError("units_defective no puede ser negativo.")

    if (df["units_defective"] > df["units_produced"]).any():
        raise ValueError("units_defective no puede superar units_produced.")

    tiempo_planificado_produccion = (
        df["planned_time_min"] - df["planned_downtime_min"]
    )

    if (tiempo_planificado_produccion <= 0).any():
        raise ValueError(
            "planned_downtime_min no puede ser mayor o igual que planned_time_min "
            "(no queda tiempo de produccion planificado)."
        )

    if (df["unplanned_downtime_min"] > tiempo_planificado_produccion).any():
        raise ValueError(
            "unplanned_downtime_min no puede superar el tiempo de produccion "
            "planificado (planned_time_min - planned_downtime_min)."
        )


def clasificar_oee(oee: float) -> str:
    """Clasifica un valor de OEE segun la convencion TPM del proyecto.

    Devuelve una clave estable en ingles ("world_class", "acceptable",
    "low"), NUNCA texto de presentacion. La traduccion a texto de UI
    vive en dashboard/oee_presenter.py (ver H2 en el docstring del
    modulo). Esto evita que el motor de calculo dependa del idioma en
    que se muestra el resultado.

    Nota: es una convencion de reporting interna del proyecto (igual que
    la clasificacion de Ppk en capability.py), no una ley universal.
    """
    if oee >= UMBRAL_OEE_CLASE_MUNDIAL:
        return CLASIFICACION_WORLD_CLASS
    if oee >= UMBRAL_OEE_ACEPTABLE:
        return CLASIFICACION_ACCEPTABLE
    return CLASIFICACION_LOW


def calcular_oee_fila(
    planned_time_min: float,
    planned_downtime_min: float,
    unplanned_downtime_min: float,
    ideal_cycle_time_sec: float,
    units_produced: int,
    units_defective: int,
) -> dict:
    """Calcula OEE y sus 3 componentes para un unico registro (equipo/periodo).

    Parameters
    ----------
    planned_time_min : float
        Tiempo total programado para el equipo, en minutos.
    planned_downtime_min : float
        Paros planificados (cambios de formato, colacion, mantenimiento
        programado). Se EXCLUYE del denominador de Disponibilidad.
    unplanned_downtime_min : float
        Paros no planificados (fallas, esperas no programadas).
    ideal_cycle_time_sec : float
        Tiempo de ciclo ideal (nominal) del equipo, en segundos/unidad.
    units_produced : int
        Unidades totales producidas en el periodo.
    units_defective : int
        Unidades defectuosas dentro de las producidas.

    Returns
    -------
    dict
        disponibilidad, rendimiento, calidad, oee, clasificacion.

    Notes
    -----
    Rendimiento se limita a un maximo de 1.0: un ideal_cycle_time_sec
    mal configurado (demasiado bajo) puede producir rendimiento > 1.0,
    lo cual es fisicamente imposible y por lo tanto se trata como un
    error de configuracion, no como una ganancia real de desempeno.
    """
    tiempo_produccion_planificado_min = (
        planned_time_min - planned_downtime_min
    )

    if tiempo_produccion_planificado_min <= 0:
        raise ValueError(
            "planned_downtime_min no puede ser mayor o igual que planned_time_min."
        )

    tiempo_operativo_min = (
        tiempo_produccion_planificado_min - unplanned_downtime_min
    )

    if tiempo_operativo_min < 0:
        raise ValueError(
            "unplanned_downtime_min no puede superar el tiempo de "
            "produccion planificado."
        )

    disponibilidad = (
        tiempo_operativo_min / tiempo_produccion_planificado_min
        if tiempo_produccion_planificado_min > 0
        else 0.0
    )

    tiempo_operativo_seg = tiempo_operativo_min * 60.0

    if tiempo_operativo_seg > 0:
        rendimiento = min(
            1.0,
            (ideal_cycle_time_sec * units_produced) / tiempo_operativo_seg,
        )
    else:
        rendimiento = 0.0

    calidad = (
        (units_produced - units_defective) / units_produced
        if units_produced > 0
        else 0.0
    )

    oee = disponibilidad * rendimiento * calidad

    return {
        "disponibilidad": round(disponibilidad, 4),
        "rendimiento": round(rendimiento, 4),
        "calidad": round(calidad, 4),
        "oee": round(oee, 4),
        "clasificacion": clasificar_oee(oee),
    }


def calcular_oee(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula OEE fila a fila para un DataFrame de registros equipo/periodo.

    Cada fila del DataFrame debe representar un periodo de tiempo para
    un equipo especifico (ej. un turno de un dia). No se agrega entre
    equipos automaticamente: si se necesita OEE de planta, se debe
    decidir explicitamente la ponderacion (por tiempo operativo, no
    promedio simple de OEE — mismo principio que kpis.py usa para
    tasa_defectos: nunca promediar tasas sin considerar volumen).

    Parameters
    ----------
    df : pd.DataFrame
        Debe contener REQUIRED_OEE_COLUMNS.

    Returns
    -------
    pd.DataFrame
        Copia de ``df`` con las columnas agregadas:
        disponibilidad, rendimiento, calidad, oee, clasificacion.

    Raises
    ------
    TypeError
        Si ``df`` no es un pandas.DataFrame.
    ValueError
        Si faltan columnas, hay nulos, o los datos violan restricciones
        fisicas (ver _validar_integridad_oee).
    """
    _validar_columnas_oee(df)
    _validar_integridad_oee(df)

    resultado = df.copy()

    calculos = resultado.apply(
        lambda fila: calcular_oee_fila(
            planned_time_min=float(fila["planned_time_min"]),
            planned_downtime_min=float(fila["planned_downtime_min"]),
            unplanned_downtime_min=float(fila["unplanned_downtime_min"]),
            ideal_cycle_time_sec=float(fila["ideal_cycle_time_sec"]),
            units_produced=int(fila["units_produced"]),
            units_defective=int(fila["units_defective"]),
        ),
        axis=1,
        result_type="expand",
    )

    return pd.concat([resultado, calculos], axis=1)


def calcular_oee_ponderado(df: pd.DataFrame) -> dict:
    """Calcula OEE agregado de planta, ponderado por tiempo operativo real.

    Nunca promedia OEE fila a fila (ese es el mismo error de agregacion
    documentado en kpis.py para tasa_defectos): un equipo que opero 2
    horas con OEE 0.40 no pesa lo mismo que uno que opero 20 horas con
    OEE 0.90. Se recalculan Disponibilidad, Rendimiento y Calidad sobre
    los totales agregados del periodo, y OEE se deriva de esos 3
    componentes agregados — no del promedio de los OEE individuales.
    """
    detalle = calcular_oee(df)

    planned_time_total = float(df["planned_time_min"].sum())
    planned_downtime_total = float(df["planned_downtime_min"].sum())
    unplanned_downtime_total = float(df["unplanned_downtime_min"].sum())
    units_produced_total = int(df["units_produced"].sum())
    units_defective_total = int(df["units_defective"].sum())

    tiempo_produccion_planificado = planned_time_total - planned_downtime_total
    tiempo_operativo = tiempo_produccion_planificado - unplanned_downtime_total

    disponibilidad = (
        tiempo_operativo / tiempo_produccion_planificado
        if tiempo_produccion_planificado > 0
        else 0.0
    )

    # Tiempo de ciclo ideal ponderado por unidades producidas de cada
    # registro: un promedio simple de ideal_cycle_time_sec sesgaria el
    # resultado si distintos equipos con distinta velocidad nominal se
    # mezclan en el mismo agregado.
    if units_produced_total > 0:
        tiempo_ideal_total_seg = float(
            (df["ideal_cycle_time_sec"] * df["units_produced"]).sum()
        )
    else:
        tiempo_ideal_total_seg = 0.0

    tiempo_operativo_seg = tiempo_operativo * 60.0

    rendimiento = (
        min(1.0, tiempo_ideal_total_seg / tiempo_operativo_seg)
        if tiempo_operativo_seg > 0
        else 0.0
    )

    calidad = (
        (units_produced_total - units_defective_total) / units_produced_total
        if units_produced_total > 0
        else 0.0
    )

    oee = disponibilidad * rendimiento * calidad

    return {
        "disponibilidad": round(disponibilidad, 4),
        "rendimiento": round(rendimiento, 4),
        "calidad": round(calidad, 4),
        "oee": round(oee, 4),
        "clasificacion": clasificar_oee(oee),
        "n_registros": int(len(detalle)),
        "units_produced_total": units_produced_total,
        "units_defective_total": units_defective_total,
    }