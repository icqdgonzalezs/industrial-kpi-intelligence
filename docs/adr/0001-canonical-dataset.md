# ADR-0001: Dataset canónico de producción

**Estado:** Aceptado — decisión cerrada (Camino A)
**Fecha:** 2026-09-09 (original) · 2026-09-10 (condición de muerte formalizada)
**Decisor:** David González

## Contexto

El repositorio contiene dos datasets de producción incompatibles:

| | `data/calidad_muestra.csv` | `data/raw/synthetic_production_data.csv` |
|---|---|---|
| Filas | 250 | 18,078 |
| Esquema | Español (`lote, linea, maquina, equipo, turno, unidades_producidas...`) | Inglés (`timestamp, line_id, equipment_id, shift, units_produced...`) |
| Generado por | Desconocido / manual (no hay generador en el repo) | `src/data_generator.py` (reproducible, seed=42, documentado) |
| Usado hoy por | `dashboard/data_loader.py:9` (`DATA_PATH`) — **es el que alimenta la app en producción** | Ninguno — huérfano, solo referenciado por `tests/test_data_generator.py` |

La aplicación Dash que un prospecto vería en una demo corre sobre 250 filas genéricas, mientras el generador "realista" de 18k filas descrito en el master plan (líneas, turnos, drift events, eventos de proceso) no está conectado a nada.

## Decisión

**Camino A — Adaptador / patrón strangler.**

`synthetic_production_data.csv` / `src/data_generator.py` (esquema en inglés, reproducible) es el **dataset canónico de producto** desde esta decisión.

`calidad_muestra.csv` queda **retirado como fuente de la aplicación**: se conserva en `data/legacy/calidad_muestra.csv` con nota explicativa.

### Arquitectura del Camino A

1. **Nueva capa `src/schema_adapter.py`**: traduce esquema canónico EN → contrato interno ES en la frontera de carga.
2. **Downstream sin cambios hoy**: `validation.py`, `kpis.py`, `capability.py`, `control_charts.py`, `diagnostics.py` y el dashboard siguen operando con el contrato ES. Los ~150 tests existentes siguen pasando.
3. **El rewiring de `dashboard/data_loader.py`** (apuntar al CSV canónico + aplicar el adapter) se ejecuta en la **Semana 2B**, con CI verde como puerta.
4. **`_validar_equipo` de `validation.py`**: se resolverá su semántica específica para el nuevo formato `equipment_id` compuesto (`"L1-FILL-01"`) durante el rewiring, con test dedicado.

### Condición de muerte del adaptador

El adaptador es **infraestructura transitoria, no permanente**. Se elimina en un commit dedicado cuando:

- **Plazo:** Semanas 3-4 del plan de 8 semanas.
- **Puerta:** CI verde en `main` + ADRs Semana 2 mergeados + suite > 225 tests.
- **Trigger:** `validation.py` fue reescrito para consumir directamente el esquema canónico EN.
- **Commit de eliminación:** un único commit `refactor: remove schema_adapter after validation.py migrated to canonical schema`, con tests que verifican que el pipeline sigue funcionando sin el adapter.

Al cierre de esa eliminación, este ADR pasa a estado **Superseded** y se referencia desde el ADR que documente la migración completa.

## Consecuencias

### Positivas
- Cero retrabajo sobre ~150 tests existentes durante Semanas 2-3.
- Riesgo aislado: si el adapter falla, se corrige localmente sin tocar el motor analítico.
- Decisión documentada con fecha de expiración — no se convierte en deuda silenciosa.

### Negativas (documentadas, no silenciadas)
- El codebase es bilingüe temporalmente (ver ADR-0002 para la convención).
- Existe un componente (el adapter) que tiene fecha de muerte conocida y debe monitorearse.

## Alternativas consideradas

- **Mantener ambos datasets indefinidamente:** descartado — ambigüedad que un auditor técnico penaliza en due diligence.
- **Migrar `calidad_muestra.csv` a inglés:** descartado — perdería volumen (250 vs. 18k) y reproducibilidad (seed fija).
- **Camino B (rewrite directo del motor a inglés):** descartado para Semanas 2-3 por riesgo comercial — toca ~10 archivos y ~150 tests de golpe. Se ejecuta como refactor único en Semana 6 (ver ADR-0002).

## Referencias

- ADR-0002 (convención de nombres y transición bilingüe)
- `docs/industrial-kpi-intelligence-master-plan.md` §14, §63
- `src/schema_adapter.py` (implementación del Camino A)