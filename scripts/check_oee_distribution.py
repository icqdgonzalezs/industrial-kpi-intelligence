"""Script de evidencia: distribuciones de OEE sobre el dataset sintético.

Uso:
    python scripts/check_oee_distribution.py

Imprime mean/std/min/max de Performance y Availability + histograma ASCII
de 10 bins. Sirve como evidencia ANTES/DESPUÉS del fix de acoplamiento
generador ↔ OEE (Semana 2, regla C.1: sin números no hay cierre).

Este script es parte del entregable Semana 2 y queda versionado en el repo
como evidencia verificable de que el fix del generador funciona.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

# Asegurar que src/ esté en sys.path al ejecutar como script directo
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data_generator import generate_production_data
from src.oee import calcular_oee


def _histograma_ascii(valores: np.ndarray, bins: int = 10, ancho: int = 40) -> str:
    """Histograma simple en texto para inspección visual rápida."""
    counts, edges = np.histogram(valores, bins=bins)
    max_count = int(counts.max()) if counts.max() > 0 else 1
    lineas = []
    for i, count in enumerate(counts):
        barra = "█" * int(round(count / max_count * ancho))
        lineas.append(f"  [{edges[i]:.3f} - {edges[i + 1]:.3f}] {barra} {int(count)}")
    return "\n".join(lineas)


def _reporte(nombre: str, valores: np.ndarray) -> None:
    print(f"\n=== {nombre} ===")
    print(f"  mean: {valores.mean():.4f}")
    print(f"  std:  {valores.std():.4f}")
    print(f"  min:  {valores.min():.4f}")
    print(f"  max:  {valores.max():.4f}")
    print("  histograma (10 bins):")
    print(_histograma_ascii(valores, bins=10))


def main() -> None:
    print("Generando dataset sintético (seed=42)...")
    df = generate_production_data()
    print(f"Registros generados: {len(df)}")

    df_oee = calcular_oee(df)

    _reporte("Performance (rendimiento)", df_oee["rendimiento"].to_numpy())
    _reporte("Availability (disponibilidad)", df_oee["disponibilidad"].to_numpy())

    print("\n=== Criterios del test de distribución ===")
    perf = df_oee["rendimiento"]
    ok_mean = 0.50 < perf.mean() < 0.95
    ok_std = perf.std() > 0.05
    print(
        f"  0.50 < mean(Performance) < 0.95: "
        f"{'✅ CUMPLE' if ok_mean else '❌ FALLA'} ({perf.mean():.4f})"
    )
    print(
        f"  std(Performance) > 0.05:         "
        f"{'✅ CUMPLE' if ok_std else '❌ FALLA'} ({perf.std():.4f})"
    )

    print("\nHistograma ANTES (referencia histórica del bug):")
    print("  Antes del fix: performance ≈ 0.9999 para todas las filas (saturado).")
    print("  Después del fix: distribución centrada con variabilidad real (arriba).")


if __name__ == "__main__":
    main()