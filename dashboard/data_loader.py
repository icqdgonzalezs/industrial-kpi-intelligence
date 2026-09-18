"""Módulo de carga del dataset canónico (ADR-0001, Camino A).

Lee el dataset canónico en inglés (generado por ``src/data_generator.py``)
y lo traduce al contrato analítico interno en español que consumen
``src/validation.py``, ``src/kpis.py``, ``src/capability.py`` y
``src/diagnostics.py``.

La traducción EN→ES está **consolidada en este módulo**. Antes vivía en
``src/schema_adapter.py``; se fusionó acá en la Opción D del ADR-0001
para eliminar un archivo del proyecto sin cambiar el contrato observable.

Deuda residual (ver ADR-0001): los 4 módulos analíticos siguen hablando
español. La traducción se eliminará cuando esos módulos migren a inglés
directamente.

Dataset canónico crudo esperado en ``DATA_PATH``:
``data/raw/synthetic_production_data.csv``. Regenerar con:
    python -m src.data_generator
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "synthetic_production_data.csv"
QUALITY_CONFIG_PATH = PROJECT_ROOT / "config" / "quality_config.yaml"


# ---------------------------------------------------------------------------
# Adaptación EN→ES (consolidado desde src/schema_adapter.py — Opción D, ADR-0001)
# ---------------------------------------------------------------------------

_COLUMNAS_CANONICAS_REQUERIDAS = [
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

_RENOMBRE_DIRECTO = {
    "date": "fecha",
    "shift": "turno",
    "operator_id": "operador",
    "units_produced": "unidades_producidas",
    "units_defective": "unidades_defectuosas",
    "units_scrap": "unidades_scrap",
    "units_rework": "unidades_reproceso",
    "defect_type": "defecto_tipo",
}

_COLUMNAS_OEE_OPCIONALES = [
    "planned_time_min",
    "planned_downtime_min",
    "unplanned_downtime_min",
    "ideal_cycle_time_sec",
]

_COLUMNAS_CONTRATO_LEGACY = [
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
    """Valida tipo y columnas canónicas requeridas antes de adaptar."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("El objeto de entrada debe ser un pandas.DataFrame.")

    if df.empty:
        raise ValueError("El dataset no puede estar vacío.")

    faltantes = [
        columna
        for columna in _COLUMNAS_CANONICAS_REQUERIDAS
        if columna not in df.columns
    ]

    if faltantes:
        raise ValueError(
            "Faltan columnas del esquema canónico requeridas por el "
            "adaptador: " + ", ".join(faltantes)
        )


def _derivar_linea_maquina_equipo(df: pd.DataFrame) -> pd.DataFrame:
    """Deriva 'linea', 'maquina' y 'equipo' preservando la regla de
    consistencia de ``validation.py._validar_equipo`` sin modificarla.

    Reglas:
        equipo  = equipment_id            (instancia física única)
        linea   = line_id
        maquina = equipment_id sin el prefijo ``"{line_id}-"``
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
            "'{line_id}-'. No se puede derivar 'maquina' de forma segura "
            "para esos registros."
        )

    resultado["equipo"] = equipment_id
    resultado["linea"] = line_id
    resultado["maquina"] = [
        equipo[len(linea) + 1 :]
        for equipo, linea in zip(equipment_id, line_id, strict=True)
    ]

    return resultado


def _adaptar_a_esquema_legacy(df: pd.DataFrame) -> pd.DataFrame:
    """Traduce el dataset canónico (inglés) al contrato legacy (español).

    Parameters
    ----------
    df : pd.DataFrame
        Dataset tal como lo entrega ``src/data_generator.py`` o se lee
        desde ``data/raw/synthetic_production_data.csv``.

    Returns
    -------
    pd.DataFrame
        DataFrame con exactamente las columnas de ``_COLUMNAS_CONTRATO_LEGACY``,
        más las columnas OEE presentes en la entrada, sin traducir.

    Raises
    ------
    TypeError
        Si df no es un pandas.DataFrame.
    ValueError
        Si faltan columnas canónicas requeridas, o si algún equipment_id
        no es consistente con su line_id.
    """
    _validar_entrada(df)

    resultado = _derivar_linea_maquina_equipo(df)
    resultado = resultado.rename(columns=_RENOMBRE_DIRECTO)

    columnas_oee_presentes = [
        columna
        for columna in _COLUMNAS_OEE_OPCIONALES
        if columna in resultado.columns
    ]

    return resultado[
        _COLUMNAS_CONTRATO_LEGACY + columnas_oee_presentes
    ].reset_index(drop=True)


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------


def cargar_datos() -> tuple[pd.DataFrame, dict]:
    """Carga el dataset canónico y lo traduce al contrato analítico interno.

    Lee el CSV en inglés (``DATA_PATH``, generado por ``src/data_generator.py``)
    y lo traduce al contrato en español que consumen ``src/validation.py``,
    ``src/kpis.py``, ``src/capability.py`` y ``src/diagnostics.py``.

    Si el dataset canónico aún no existe en disco, generarlo con:
        python -m src.data_generator

    Returns
    -------
    tuple[pd.DataFrame, dict]
        DataFrame en el contrato analítico legacy (español) + config de
        calidad (``quality_config.yaml``).

    Raises
    ------
    FileNotFoundError
        Si el dataset canónico o la configuración de calidad no existen.
    ValueError
        Si el dataset existe pero está vacío, corrupto, o no contiene las
        columnas que la traducción EN→ES necesita para operar.
    """
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"No existe el dataset canónico: {DATA_PATH}. "
            "Genérelo con: python -m src.data_generator"
        )

    if not QUALITY_CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"No existe la configuración: {QUALITY_CONFIG_PATH}"
        )

    try:
        df_canonico = pd.read_csv(DATA_PATH)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(
            f"El dataset canónico está vacío o corrupto (sin encabezado "
            f"legible): {DATA_PATH}"
        ) from exc

    if df_canonico.empty:
        raise ValueError(
            f"El dataset canónico no contiene registros: {DATA_PATH}"
        )

    try:
        df = _adaptar_a_esquema_legacy(df_canonico)
    except ValueError as exc:
        raise ValueError(
            f"El dataset canónico en {DATA_PATH} no es compatible con el "
            f"contrato analítico interno (validation.py/kpis.py/"
            f"capability.py/diagnostics.py): {exc}"
        ) from exc

    if "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(
            df["fecha"],
            errors="coerce",
            format="mixed",
        )

    with QUALITY_CONFIG_PATH.open(encoding="utf-8") as archivo:
        config = yaml.safe_load(archivo)

    if config is None:
        config = {}

    return df, config