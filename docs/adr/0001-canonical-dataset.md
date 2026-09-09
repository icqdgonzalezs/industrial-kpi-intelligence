# ADR-0001: Dataset canónico de producción

**Estado:** Aceptado
**Fecha:** 2026-09-09
**Decisor:** David González

## Contexto

El repositorio contiene dos datasets de producción incompatibles:

| | `data/calidad_muestra.csv` | `data/raw/synthetic_production_data.csv` |
|---|---|---|
| Filas | 250 | 18,078 |
| Esquema | Español (`lote, linea, maquina, equipo, turno, unidades_producidas...`) | Inglés (`timestamp, line_id, equipment_id, shift, units_produced...`) |
| Generado por | Desconocido / manual (no hay generador en el repo) | `src/data_generator.py` (reproducible, seed=42, documentado) |
| Usado hoy por | `dashboard/data_loader.py:9` (`DATA_PATH`) — **es el que alimenta la app en producción** | Ninguno — huérfano, solo referenciado por `tests/test_data_generator.py` |

Esto significa que la aplicación Dash que un prospecto vería en una demo corre sobre 250 filas genéricas, mientras el generador "realista" de 18k filas descrito en el master plan (líneas, turnos, drift events, eventos de proceso) no está conectado a nada.

## Decisión

`synthetic_production_data.csv` / `src/data_generator.py` (esquema en inglés, reproducible) es el **dataset canónico de producto** en adelante.

`calidad_muestra.csv` queda **retirado como fuente de la aplicación**: se conserva en el repo bajo `data/legacy/calidad_muestra.csv` con una nota en el propio archivo (o un `data/legacy/README.md`) que explique que es un dataset histórico, no usado por `dashboard/data_loader.py`.

## Riesgo de implementación identificado (no resuelto en esta sesión)

Este ADR decide *cuál CSV es la fuente*, pero **no implica que baste con cambiar `DATA_PATH` en `data_loader.py`**. Todo el motor analítico probado y en producción (`kpis.py`, `validation.py`, `capability.py`, `diagnostics.py`, `control_charts.py` — ~150 tests) espera el **contrato interno en español**: `lote, linea, maquina, equipo, turno, operador, unidades_producidas, unidades_defectuosas, unidades_scrap, unidades_reproceso, defecto_tipo, peso_promedio, longitud_promedio`.

El dataset canónico en inglés no tiene hoy: `lote` (identificador de lote), variables continuas de calidad (`peso_promedio`/`longitud_promedio` no existen en `data_generator.py`), ni los 4 campos de OEE. Además, `validation.py`'s `_validar_equipo` reconstruye `equipo` como `f"L{numero_de_linea}-{maquina}"` a partir de `linea` — una regla acoplada a la convención antigua que **no aplica directamente** al esquema nuevo, donde `equipment_id` ya viene compuesto (`"L1-FILL-01"`) y `maquina` como columna separada no existe.

**Dos caminos posibles:**

- **Camino A (recomendado):** mantener el contrato interno en español sin tocarlo. Agregar una capa de *adaptador* en `data_loader.py` que traduzca/renombre las columnas del CSV canónico (inglés) al contrato interno (español) antes de devolver el DataFrame. Cero retrabajo sobre los ~150 tests existentes de `kpis.py/validation.py/capability.py/diagnostics.py`. Costo: escribir y testear el adaptador, y resolver específicamente la semántica de `_validar_equipo` para el nuevo formato de `equipment_id`.
- **Camino B:** reescribir `kpis.py/validation.py/capability.py/diagnostics.py` para usar nombres en inglés directamente. Arquitectura más limpia a largo plazo (un solo esquema, no dos), pero toca ~10 archivos y ~150 tests. No justificado ahora dado el objetivo de venta en 8 semanas.

Este ADR se cierra con la decisión del dataset canónico. La decisión Camino A vs. B, y el rediseño puntual de `_validar_equipo`, quedan como acción explícita pendiente — **no se tocó `validation.py` ni `data_loader.py` en esta sesión** para evitar romper un módulo con cobertura de tests alta sin un diseño verificado.

## Consecuencias

- `src/data_generator.py` se extiende (ver más abajo) para generar `lote`, `peso_promedio`, `longitud_promedio` y los 4 campos de OEE — sin lo cual `capability.py` y `oee.py` no tienen con qué alimentarse en el dataset canónico.
- `dashboard/data_loader.py` **no se modifica todavía** — sigue apuntando a `calidad_muestra.csv` hasta que el Camino A/B esté decidido e implementado. Esto es intencional: cambiar el loader sin el adaptador rompería la app.
- README y CHANGELOG deben documentar este ADR y el estado "pendiente de adaptador" explícitamente, para que no se repita el patrón de "decisión documentada mentalmente pero no reflejada en el código".

## Alternativas consideradas

- Mantener ambos datasets indefinidamente: descartado — es exactamente la ambigüedad que un auditor técnico penaliza en due diligence.
- Migrar `calidad_muestra.csv` a inglés en vez de al revés: descartado — perdería el volumen (250 vs. 18k filas) y la reproducibilidad (seed fija) que ya tiene el generador.
