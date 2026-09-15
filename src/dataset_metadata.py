"""Metadatos del dataset canónico: timestamp de última modificación.

Proporciona la fecha de última modificación del CSV y la formatea
como texto relativo en español para el header del dashboard.

Funciones puras (sin estado) para testabilidad completa. La lectura
de mtime es la única operación de IO y se aísla en
obtener_timestamp_dataset() para poder mockearla si es necesario.

Patrón GitHub/Vercel: se muestra timestamp absoluto + relativo en
una sola línea. "2024-12-31 18:30 · hace 2 días" — precisión para
auditoría, contexto inmediato para el operador.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

SEGUNDOS_EN_MINUTO = 60
SEGUNDOS_EN_HORA = 3600
SEGUNDOS_EN_DIA = 86400
DIAS_EN_MES = 30
DIAS_EN_ANIO = 365


def obtener_timestamp_dataset(ruta: Path) -> datetime:
    """Devuelve el mtime del dataset como datetime en hora local.

    Args:
        ruta: Path al archivo CSV del dataset.

    Returns:
        datetime naive en zona horaria local del sistema.

    Raises:
        FileNotFoundError: si la ruta no existe.
    """
    return datetime.fromtimestamp(ruta.stat().st_mtime)


def formatear_frescura(timestamp: datetime, ahora: datetime) -> str:
    """Formatea la antigüedad de un timestamp como texto relativo.

    Ejemplos: "hace unos segundos", "hace 5 minutos", "hace 2 horas",
    "hace 3 días", "hace 2 meses", "hace 1 año".

    Si el timestamp es futuro (reloj desincronizado), devuelve
    "justo ahora" — evita "hace -3 horas".

    Args:
        timestamp: momento a describir.
        ahora: momento de referencia (típicamente datetime.now()).

    Returns:
        Texto relativo en español, sin mayúscula inicial.
    """
    delta_segundos = (ahora - timestamp).total_seconds()

    if delta_segundos < 0:
        return "justo ahora"

    if delta_segundos < SEGUNDOS_EN_MINUTO:
        return "hace unos segundos"

    if delta_segundos < SEGUNDOS_EN_HORA:
        minutos = int(delta_segundos // SEGUNDOS_EN_MINUTO)
        return f"hace {minutos} minuto{'s' if minutos != 1 else ''}"

    if delta_segundos < SEGUNDOS_EN_DIA:
        horas = int(delta_segundos // SEGUNDOS_EN_HORA)
        return f"hace {horas} hora{'s' if horas != 1 else ''}"

    dias = int(delta_segundos // SEGUNDOS_EN_DIA)

    if dias < DIAS_EN_MES:
        return f"hace {dias} día{'s' if dias != 1 else ''}"

    if dias < DIAS_EN_ANIO:
        meses = dias // DIAS_EN_MES
        return f"hace {meses} mes{'es' if meses != 1 else ''}"

    anios = dias // DIAS_EN_ANIO
    return f"hace {anios} año{'s' if anios != 1 else ''}"


def formatear_timestamp_absoluto(timestamp: datetime) -> str:
    """Formatea un timestamp como 'YYYY-MM-DD HH:MM'."""
    return timestamp.strftime("%Y-%m-%d %H:%M")


def formatear_metadata_dataset(ruta: Path, ahora: datetime | None = None) -> str:
    """Compone la línea completa para el header.

    Ejemplo: "2024-12-31 18:30 · hace 2 días"

    Args:
        ruta: Path al dataset.
        ahora: momento de referencia. None → datetime.now().

    Returns:
        String listo para mostrar en el header.
    """
    ts = obtener_timestamp_dataset(ruta)
    ref = ahora if ahora is not None else datetime.now()
    return f"{formatear_timestamp_absoluto(ts)} · {formatear_frescura(ts, ref)}"