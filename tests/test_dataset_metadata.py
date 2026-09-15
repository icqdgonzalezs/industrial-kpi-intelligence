from __future__ import annotations

import os
from datetime import datetime, timedelta

import pytest

from src.dataset_metadata import (
    formatear_frescura,
    formatear_metadata_dataset,
    formatear_timestamp_absoluto,
    obtener_timestamp_dataset,
)

AHORA = datetime(2026, 9, 15, 18, 30, 0)


# --- formatear_frescura ---

@pytest.mark.parametrize(
    ("delta", "esperado"),
    [
        (timedelta(seconds=5), "hace unos segundos"),
        (timedelta(seconds=59), "hace unos segundos"),
        (timedelta(minutes=1), "hace 1 minuto"),
        (timedelta(minutes=5), "hace 5 minutos"),
        (timedelta(minutes=59), "hace 59 minutos"),
        (timedelta(hours=1), "hace 1 hora"),
        (timedelta(hours=5), "hace 5 horas"),
        (timedelta(hours=23), "hace 23 horas"),
        (timedelta(days=1), "hace 1 día"),
        (timedelta(days=2), "hace 2 días"),
        (timedelta(days=29), "hace 29 días"),
        (timedelta(days=30), "hace 1 mes"),
        (timedelta(days=60), "hace 2 meses"),
        (timedelta(days=364), "hace 12 meses"),
        (timedelta(days=365), "hace 1 año"),
        (timedelta(days=730), "hace 2 años"),
    ],
)
def test_formatear_frescura(delta, esperado):
    ts = AHORA - delta
    assert formatear_frescura(ts, AHORA) == esperado


def test_formatear_frescura_timestamp_futuro():
    """Reloj desincronizado o archivo del futuro → 'justo ahora'."""
    ts = AHORA + timedelta(hours=3)
    assert formatear_frescura(ts, AHORA) == "justo ahora"


# --- formatear_timestamp_absoluto ---

def test_formatear_timestamp_absoluto():
    ts = datetime(2024, 12, 31, 18, 30)
    assert formatear_timestamp_absoluto(ts) == "2024-12-31 18:30"


# --- obtener_timestamp_dataset ---

def test_obtener_timestamp_dataset(tmp_path):
    archivo = tmp_path / "dataset.csv"
    archivo.write_text("col1,col2\n1,2\n")

    ts = obtener_timestamp_dataset(archivo)

    assert isinstance(ts, datetime)
    assert abs((datetime.now() - ts).total_seconds()) < 5


def test_obtener_timestamp_dataset_archivo_inexistente(tmp_path):
    archivo = tmp_path / "no-existe.csv"
    with pytest.raises(FileNotFoundError):
        obtener_timestamp_dataset(archivo)


# --- formatear_metadata_dataset ---

def test_formatear_metadata_dataset(tmp_path):
    archivo = tmp_path / "dataset.csv"
    archivo.write_text("col1,col2\n1,2\n")

    mtime = (AHORA - timedelta(days=2)).timestamp()
    os.utime(archivo, (mtime, mtime))

    resultado = formatear_metadata_dataset(archivo, ahora=AHORA)

    assert "2026-09-13 18:30" in resultado
    assert "hace 2 días" in resultado
    assert " · " in resultado