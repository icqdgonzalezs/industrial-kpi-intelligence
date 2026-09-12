from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

from src.schema_adapter import adaptar_a_esquema_legacy

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ADR-0001 (Camino A): el dataset canónico de producto es el generado por
# src/data_generator.py (esquema en inglés, reproducible). El CSV legacy
# (data/calidad_muestra.csv, esquema en español, 250 filas) queda retirado
# como fuente de la aplicación — ver docs/adr/0001-canonical-dataset.md.
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "synthetic_production_data.csv"
QUALITY_CONFIG_PATH = PROJECT_ROOT / "config" / "quality_config.yaml"


def cargar_datos() -> tuple[pd.DataFrame, dict]:
    """Carga el dataset canónico y lo traduce al contrato analítico interno.

    ADR-0001 (Camino A — patrón strangler): este loader lee el dataset
    canónico en inglés (DATA_PATH, generado por src/data_generator.py) y
    lo traduce inmediatamente con src.schema_adapter.adaptar_a_esquema_legacy()
    al contrato en español que consumen src/validation.py, src/kpis.py,
    src/capability.py y src/diagnostics.py. Ninguno de esos 4 módulos se
    modificó para este cambio.

    Si el dataset canónico aún no existe en disco, generarlo con:
        python -m src.data_generator

    Returns
    -------
    tuple[pd.DataFrame, dict]
        DataFrame en el contrato analítico legacy (español) + config de
        calidad (quality_config.yaml).

    Raises
    ------
    FileNotFoundError
        Si el dataset canónico o la configuración de calidad no existen
        en disco.
    ValueError
        Si el dataset canónico existe pero está vacío, corrupto, o no
        contiene las columnas que el adaptador necesita para traducirlo
        (ver src.schema_adapter.COLUMNAS_CANONICAS_REQUERIDAS) — en vez
        de dejar que el error críptico del adaptador o de pandas suba
        sin contexto.
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
        df = adaptar_a_esquema_legacy(df_canonico)
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
