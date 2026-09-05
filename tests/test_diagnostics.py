from __future__ import annotations

import pandas as pd
import pytest

from src.diagnostics import generar_diagnostico

COLUMNAS_BASE = [
    "lote",
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
]


def _fila(
    lote,
    equipo,
    turno,
    producidas,
    defectuosas,
    defecto_tipo="Mancha",
):
    return {
        "lote": lote,
        "linea": "L1",
        "maquina": "M01",
        "equipo": equipo,
        "turno": turno,
        "operador": "OP1",
        "unidades_producidas": producidas,
        "unidades_defectuosas": defectuosas,
        "unidades_reproceso": defectuosas,
        "unidades_scrap": 0,
        "defecto_tipo": defecto_tipo,
    }


def test_generar_diagnostico_rechaza_no_dataframe():
    with pytest.raises(TypeError):
        generar_diagnostico([1, 2, 3])


def test_generar_diagnostico_rechaza_dataset_vacio():
    with pytest.raises(ValueError):
        generar_diagnostico(pd.DataFrame(columns=COLUMNAS_BASE))


def test_hotspot_equipo_se_detecta_como_priority():
    filas = []
    # Equipo A: 20 lotes al 3% de defectos
    for i in range(20):
        filas.append(_fila(f"L{i:03d}", "EQ-A", "Mañana", 1000, 30))
    # Equipo B: 20 lotes al 10% de defectos.
    # Promedio de planta resultante = 6.5% -> ratio EQ-B = 10/6.5 = 1.54x (>= 1.40 -> PRIORITY)
    for i in range(20, 40):
        filas.append(_fila(f"L{i:03d}", "EQ-B", "Mañana", 1000, 100))

    df = pd.DataFrame(filas)

    resultado = generar_diagnostico(df)

    equipo_b = resultado[resultado["titulo"] == "Equipo: EQ-B"]
    assert not equipo_b.empty
    assert equipo_b.iloc[0]["severidad"] == "PRIORITY"


def test_hotspot_ignora_muestras_pequenas():
    filas = []
    for i in range(20):
        filas.append(_fila(f"L{i:03d}", "EQ-A", "Mañana", 1000, 30))
    # Solo 5 lotes (< MINIMO_LOTES_HOTSPOT) con tasa altísima -> no debe flaggear
    for i in range(20, 25):
        filas.append(_fila(f"L{i:03d}", "EQ-RUIDO", "Mañana", 1000, 900))

    df = pd.DataFrame(filas)

    resultado = generar_diagnostico(df)

    assert resultado[resultado["titulo"] == "Equipo: EQ-RUIDO"].empty


def test_sin_hotspots_no_genera_hallazgos_de_equipo_ni_turno():
    filas = []
    for i in range(40):
        equipo = "EQ-A" if i % 2 == 0 else "EQ-B"
        filas.append(_fila(f"L{i:03d}", equipo, "Mañana", 1000, 30))

    df = pd.DataFrame(filas)

    resultado = generar_diagnostico(df)

    assert resultado[resultado["categoria"].isin(["Equipo", "Turno"])].empty


def test_capacidad_no_capaz_es_priority():
    df = pd.DataFrame([_fila(f"L{i:03d}", "EQ-A", "Mañana", 1000, 30) for i in range(20)])
    capacidad = pd.DataFrame(
        [
            {
                "variable": "Peso",
                "columna": "peso_promedio",
                "lsl": 492.0,
                "usl": 508.0,
                "cp": 0.8,
                "cpk": 0.6,
                "clasificacion": "No capaz (acción requerida)",
            }
        ]
    )

    resultado = generar_diagnostico(df, capacidad)

    hallazgo = resultado[resultado["categoria"] == "Capacidad de proceso"]
    assert not hallazgo.empty
    assert hallazgo.iloc[0]["severidad"] == "PRIORITY"


def test_capacidad_marginal_es_watch():
    df = pd.DataFrame([_fila(f"L{i:03d}", "EQ-A", "Mañana", 1000, 30) for i in range(20)])
    capacidad = pd.DataFrame(
        [
            {
                "variable": "Longitud",
                "columna": "longitud_promedio",
                "lsl": 117.5,
                "usl": 122.5,
                "cp": 1.1,
                "cpk": 1.05,
                "clasificacion": "Marginal (monitorear)",
            }
        ]
    )

    resultado = generar_diagnostico(df, capacidad)

    hallazgo = resultado[resultado["categoria"] == "Capacidad de proceso"]
    assert not hallazgo.empty
    assert hallazgo.iloc[0]["severidad"] == "WATCH"


def test_capacidad_capaz_no_genera_hallazgo():
    df = pd.DataFrame([_fila(f"L{i:03d}", "EQ-A", "Mañana", 1000, 30) for i in range(20)])
    capacidad = pd.DataFrame(
        [
            {
                "variable": "Peso",
                "columna": "peso_promedio",
                "lsl": 492.0,
                "usl": 508.0,
                "cp": 1.8,
                "cpk": 1.7,
                "clasificacion": "Capaz (excelente)",
            }
        ]
    )

    resultado = generar_diagnostico(df, capacidad)

    assert resultado[resultado["categoria"] == "Capacidad de proceso"].empty


def test_generar_diagnostico_sin_capacidad_no_falla():
    df = pd.DataFrame([_fila(f"L{i:03d}", "EQ-A", "Mañana", 1000, 30) for i in range(20)])

    resultado = generar_diagnostico(df, capacidad=None)

    assert resultado[resultado["categoria"] == "Capacidad de proceso"].empty


def test_pareto_causa_dominante_es_priority():
    filas = []
    for i in range(20):
        filas.append(_fila(f"L{i:03d}", "EQ-A", "Mañana", 1000, 50, defecto_tipo="Mancha"))
    for i in range(20, 24):
        filas.append(_fila(f"L{i:03d}", "EQ-A", "Mañana", 1000, 10, defecto_tipo="Rayadura"))

    df = pd.DataFrame(filas)

    resultado = generar_diagnostico(df)

    hallazgo = resultado[resultado["categoria"] == "Pareto de defectos"]
    assert not hallazgo.empty
    assert hallazgo.iloc[0]["severidad"] == "PRIORITY"


def test_lote_critico_siempre_presente_como_contexto():
    df = pd.DataFrame([_fila(f"L{i:03d}", "EQ-A", "Mañana", 1000, 30) for i in range(20)])

    resultado = generar_diagnostico(df)

    hallazgo = resultado[resultado["categoria"] == "Lote crítico"]
    assert not hallazgo.empty


def test_orden_prioriza_severidad_sobre_todo_lo_demas():
    filas = []
    for i in range(20):
        filas.append(_fila(f"L{i:03d}", "EQ-A", "Mañana", 1000, 30))
    for i in range(20, 40):
        filas.append(_fila(f"L{i:03d}", "EQ-B", "Mañana", 1000, 90))

    df = pd.DataFrame(filas)
    capacidad = pd.DataFrame(
        [
            {
                "variable": "Peso",
                "columna": "peso_promedio",
                "lsl": 492.0,
                "usl": 508.0,
                "cp": 1.1,
                "cpk": 1.05,
                "clasificacion": "Marginal (monitorear)",
            }
        ]
    )

    resultado = generar_diagnostico(df, capacidad)

    severidades = resultado["severidad"].tolist()
    ordenes = [{"PRIORITY": 0, "WATCH": 1, "INFO": 2}[s] for s in severidades]

    assert ordenes == sorted(ordenes)


def test_dataset_real_produce_diagnostico_valido():
    from dashboard.data_loader import cargar_datos
    from src.capability import resumen_capacidad

    df, config = cargar_datos()
    capacidad = resumen_capacidad(df, config["quality"]["variables_criticas"])

    resultado = generar_diagnostico(df, capacidad)

    assert not resultado.empty
    assert set(resultado.columns) == {"severidad", "categoria", "titulo", "mensaje", "score"}
    assert resultado["severidad"].isin(["PRIORITY", "WATCH", "INFO"]).all()
