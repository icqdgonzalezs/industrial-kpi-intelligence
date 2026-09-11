"""Adaptador de esquema (ADR-0001, Camino A — patron strangler).

Traduce el dataset canonico de producto (esquema en ingles: timestamp,
line_id, equipment_id, units_produced... generado por src/data_generator.py)
al contrato analitico interno que YA consumen src/kpis.py, src/validation.py,
src/capability.py y src/diagnostics.py (esquema en espanol: lote, linea,
maquina, equipo, turno, unidades_producidas...).

CONDICION DE MUERTE: se elimina en un unico commit, con CI en verde, cuando
src/validation.py, src/kpis.py, src/capability.py y src/diagnostics.py
hablen el esquema canonico en ingles directamente (ver ADR-0001).

Regla de derivacion clave (evita tocar validation.py._validar_equipo):
    equipo  = equipment_id
    linea   = line_id
    maquina = equipment_id sin el prefijo "{line_id}-"
"""

from __future__ import annotations

import pandas as pd

COLUMNAS_CANONICAS_REQUERIDAS = [
    "lote",
    "date",
    "line_id",
    "equipment_id",
    "shift",
    "operator_id",
    "units_produced",
    "units_defective",
    "units_scrap",
    "units_rework",
    "defect_type",
    "peso_promedio",
    "longitud_promedio",
]

RENOMBRE_DIRECTO = {
    "date": "fecha",
    "shift": "turno",
    "operator_id": "operador",
    "units_produced": "unidades_producidas",
    "units_defective": "unidades_defectuosas",
    "units_scrap": "unidades_scrap",
    "units_rework": "unidades_reproceso",
    "defect_type": "defecto_tipo",
}

COLUMNAS_OEE_OPCIONALES = [
    "planned_time_min",
    "planned_downtime_min",
    "unplanned_downtime_min",
    "ideal_cycle_time_sec",
]

COLUMNAS_CONTRATO_LEGACY = [
    "lote",
    "fecha",
    "linea",
    "maquina",
    "equipo",
    "turno",
    "operador",
    "unidades_producidas",
    "unidades_defectuosas",
    "unidades_reproceso",
    "unidades_scrap",
    "defecto_tipo",
    "peso_promedio",
    "longitud_promedio",
]


def _validar_entrada(df: pd.DataFrame) -> None:
    """Valida tipo y columnas canonicas requeridas antes de adaptar."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("El objeto de entrada debe ser un pandas.DataFrame.")

    if df.empty:
        raise ValueError("El dataset no puede estar vacio.")

    faltantes = [
        columna
        for columna in COLUMNAS_CANONICAS_REQUERIDAS
        if columna not in df.columns
    ]

    if faltantes:
        raise ValueError(
            "Faltan columnas del esquema canonico requeridas por el "
            "adaptador: " + ", ".join(faltantes)
        )


def _derivar_linea_maquina_equipo(df: pd.DataFrame) -> pd.DataFrame:
    """Deriva 'linea', 'maquina' y 'equipo' preservando la regla de
    consistencia de validation.py._validar_equipo, sin modificarla.
    """
    resultado = df.copy()

    line_id = resultado["line_id"].astype(str)
    equipment_id = resultado["equipment_id"].astype(str)

    prefijo_no_removido = pd.Series(
        [
            not equipo.startswith(f"{linea}-")
            for equipo, linea in zip(equipment_id, line_id, strict=True)
        ],
        index=resultado.index,
    )

    if prefijo_no_removido.any():
        raise ValueError(
            "Existen registros donde equipment_id no comienza con "
            "'{line_id}-'. El adaptador no puede derivar 'maquina' de "
            "forma segura para esos registros."
        )

    resultado["equipo"] = equipment_id
    resultado["linea"] = line_id
    resultado["maquina"] = [
        equipo[len(linea) + 1 :]
        for equipo, linea in zip(equipment_id, line_id, strict=True)
    ]

    return resultado


def adaptar_a_esquema_legacy(df: pd.DataFrame) -> pd.DataFrame:
    """Traduce el dataset canonico (ingles) al contrato legacy (espanol).

    Parameters
    ----------
    df : pd.DataFrame
        Dataset tal como lo entrega src/data_generator.py o se lee desde
        data/raw/synthetic_production_data.csv.

    Returns
    -------
    pd.DataFrame
        DataFrame con exactamente las columnas de COLUMNAS_CONTRATO_LEGACY,
        mas las columnas OEE presentes en la entrada, sin traducir.

    Raises
    ------
    TypeError
        Si df no es un pandas.DataFrame.
    ValueError
        Si faltan columnas canonicas requeridas, o si algun equipment_id
        no es consistente con su line_id.
    """
    _validar_entrada(df)

    resultado = _derivar_linea_maquina_equipo(df)
    resultado = resultado.rename(columns=RENOMBRE_DIRECTO)

    columnas_oee_presentes = [
        columna for columna in COLUMNAS_OEE_OPCIONALES if columna in resultado.columns
    ]

    return resultado[COLUMNAS_CONTRATO_LEGACY + columnas_oee_presentes].reset_index(
        drop=True
    )