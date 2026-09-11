# ADR-0002: Convención de Nombres y Transición Bilingüe

- **Estado:** Aceptado
- **Fecha:** 2026-09-09
- **Contexto:** Proyecto 01 (ANALYZE) — Industrial KPI Intelligence
- **Decisores:** David González (Ing. Civil Químico + Dev Senior)

## Contexto

El codebase actual mezcla dos convenciones de nombres:
- La API analítica legacy (`kpis.py`, `capability.py`, `control_charts.py`,
  `diagnostics.py`) usa español: `calcular_kpis_globales`, `disponibilidad`,
  `clasificacion`.
- Los módulos nuevos (`oee.py`, `schema_adapter.py`, generador extendido,
  keys de UI) usan inglés: `compute_oee`, `availability`, `world_class`.

Esta mezcla es deuda técnica acumulada, no decisión explícita. Un rename
global inmediato rompería ~225 tests, callbacks y componentes de Dash en un
único commit gigante (patrón "big bang") — exactamente lo que el ADR-0001
prohíbe por riesgo comercial.

## Decisión

**Mantener la convención legacy (español) en la API analítica hoy.** Los
módulos nuevos siguen las siguientes reglas desde ya:

1. **Keys de datos y resultados:** inglés (`world_class`, `availability`,
   `performance`). Esto permite i18n real: el motor entrega keys estables,
   la capa UI traduce a español/inglés según locale.
2. **Nombres de funciones y clases nuevas:** inglés (`compute_oee`,
   `SchemaAdapter`, `check_oee_distribution`).
3. **Docstrings y mensajes de error internos:** inglés (para debugging).
4. **Labels visibles al usuario final:** español por defecto, con mapping
   i18n en `dashboard/oee_presenter.py` (y equivalentes por módulo).

## Consecuencias

### Positivas
- Cero riesgo de romper 225 tests hoy.
- i18n real desde el primer módulo nuevo: el motor no sabe de idiomas.
- Los evaluadores técnicos (LatAm + España + inglés) entienden el código.

### Negativas (deuda documentada)
- El codebase queda bilingüe temporalmente: `kpis.py` (español) convive con
  `oee.py` (inglés) hasta el rename global.
- Los nuevos desarrolladores deben aprender ambas convenciones durante el
  período de transición.

## Condición de muerte del bilingüismo

**El rename global a inglés se ejecuta como refactor único con tests
en la Semana 6 (fase portfolio/docs)** del plan de 8 semanas. Puerta de
entrada: CI verde en `main` + los 12 entregables de Semana 2 mergeados.

Al cierre de ese refactor, este ADR pasa a estado **Superseded** y se
elimina la nota de "transición bilingüe" del README.

## Referencias

- ADR-0001 (dataset canónico)
- Master Plan §14, §15, §43, §49
- Prompt maestro: método §59