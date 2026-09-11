# Changelog

Todo lo registrado aquí corresponde a commits reales del repositorio,
verificados con `pytest` y `ruff` en cada paso. No hay entradas
reconstruidas ni inferidas.

---

## Semana 2 — Cierre de deuda técnica y puente de unificación (2026-09-10)

### Decisiones arquitectónicas (ADRs)

- **ADR-0001 actualizado** (`docs/adr/0001-canonical-dataset.md`): se formaliza
  la decisión Camino A (adaptador / patrón strangler). El adaptador traduce
  esquema canónico EN → legacy ES en la frontera de carga; el downstream
  (validation, kpis, capability, control_charts, diagnostics, dashboard) no
  cambia hoy. Condición de muerte: Semanas 3-4, cuando `validation.py` hable
  esquema canónico EN nativo; se elimina en un commit con tests. Puerta: CI verde.

- **ADR-0002 nuevo** (`docs/adr/0002-naming-convention.md`): se documenta el
  bilingüismo actual del codebase y la regla para módulos nuevos (keys de
  datos en inglés, labels i18n en la capa UI). El rename global a inglés se
  agenda como refactor único con tests en Semana 6.

### Unificación de datasets

- **Schema adapter** (`src/schema_adapter.py` + `tests/test_schema_adapter.py`):
  traduce esquema canónico EN → legacy ES sin tocar una línea de
  `validation.py`, `kpis.py` ni `capability.py`. 11 tests propios. Verificado
  end-to-end contra el pipeline real.

### Motor OEE — i18n y separación de capas

- **Keys estables** (`src/oee.py`, `tests/test_oee.py`): `clasificar_oee`
  devuelve `world_class` / `acceptable` / `low`. El motor ya no contiene
  labels en español — el dato es idioma-agnóstico.
- **Presenter** (`dashboard/oee_presenter.py`): mapping de keys estables a
  texto español/inglés. El único lugar del codebase que conoce idiomas para OEE.
- **Tests:** 31 pasan tras el refactor.

### Capacidad de proceso — rename Pp/Ppk

- **Rename aplicado** (`src/capability.py`, `dashboard/capability_callbacks.py`,
  `dashboard/capability_components.py`, tests): lo que estaba etiquetado
  Cp/Cpk (sigma overall, `ddof=1`) se etiqueta correctamente **Pp/Ppk**, según
  NIST 6.1.3 / ISO 22514.
- **Documentado:** los Cp/Cpk reales (sigma within, MRbar/d2) se agregan en
  Semanas 5-6. Ticket abierto, no deuda silenciosa.

### Generador de datos

- **Fix de acoplamiento** (`src/data_generator.py`): `units_produced` nace del
  tiempo operativo real (`run_min × 60 / ideal_cycle × efficiency + ruido
  documentado`), en vez de generarse independiente del paro no planificado.
  Elimina el hallazgo de Performance saturado en 1.0.
- **Test de distribución** (`tests/test_data_generator.py`): verifica
  `0.50 < mean(performance) < 0.95` y `std(performance) > 0.05` sobre el
  dataset completo. Sin esto, un KPI sin variación no informa.
- **Script de evidencia** (`scripts/check_oee_distribution.py`): imprime
  stats (mean/std/min/max) de performance y availability + histograma ASCII
  de 10 bins. Evidencia ANTES/DESPUÉS del fix de acoplamiento.

### Infraestructura y CI

- **Pin de ruff** (`.github/workflows/tests.yml`): se fija `ruff==0.16.6`
  (versión que pasa local y CI). El workflow ya no instala "la última
  disponible", eliminando la deuda de reproducibilidad que causó el lint rojo
  de Semana 1.

### Estado de tests

- Suite total actualizada: base 225 + nuevos de adapter, presenter, rename
  Pp/Ppk, distribución. Verde en CI.

---

## Semana 1 — Licencia comercial, ADR-0001, motor OEE y schema extendido (2026-09-09)

### Licencia

- **MIT → Elastic License 2.0 (ELv2).** El README agrega la sección
  "Licencia y Uso" (qué puede hacer un evaluador técnico vs. un cliente
  pagando) y el badge de licencia queda actualizado. Decisión de modelo de
  negocio: proteger el SaaS sin cerrar el código a evaluación.

### Decisiones arquitectónicas (ADRs)

- **ADR-0001** (`docs/adr/0001-canonical-dataset.md`): dataset canónico =
  `synthetic_production_*.csv` (esquema inglés, ~18k registros);
  `calidad_muestra.csv` queda como legacy documentado. La unificación del
  loader se resuelve por Camino A (adaptador / patrón strangler) con condición
  de muerte del adaptador en semanas 3-4.

### Motor OEE — implementación inicial

- **`src/oee.py` + `tests/test_oee.py`:** Availability × Performance × Quality
  según ISA-95/TPM.
  - Disponibilidad excluye paro planificado.
  - Performance capado a 1.0 (un ciclo ideal mal configurado es error de
    config, no ganancia).
  - Quality reusa el FPY de `kpis.py` (una sola definición en el codebase).
  - Agregación de planta ponderada por tiempo operativo, nunca promedio simple
    de OEE.
  - Lanza `ValueError` si el schema no trae las columnas de tiempo: no inventa
    KPIs (regla de oro §58).

### Schema extendido

- **`config/generator_config.yaml` + `src/data_generator.py`:**
  `planned_time_min`, `planned_downtime_min`, `unplanned_downtime_min`,
  `ideal_cycle_time_sec`, con `units_produced` acoplado al tiempo operativo
  real (fix del hallazgo de Performance saturado en 1.0).

### Documentación

- Master plan versionado en `docs/`.
- Referencias NIST 6.1.3 / 6.3.1 / 6.3.2 en `docs/nist_references/`.
- Se retira el manual cross-project de quality-kpi-dashboard.
- `estructura.txt` excluido vía `.gitignore`.

### Estado de tests

- 225 passing tras integrar motor OEE y generador extendido.

---

## Migración Streamlit → Dash

- Arquitectura Dash completa: `src/` (lógica pura, sin Dash) + `dashboard/`
  (callbacks delgados) + tests por módulo.
- Eliminación completa del código legacy de Streamlit (`app.py` y
  `components/`) una vez alcanzada paridad funcional en Dash.
- `requirements.txt` limpio (sin Streamlit), `pyproject.toml` con
  configuración real de Ruff y pytest.

---

## Motor de diagnóstico priorizado (`src/diagnostics.py`)

- Combina hotspots de equipo/turno, capacidad de proceso (Cp/Cpk) y
  concentración de Pareto en hallazgos rankeados por severidad
  (PRIORITY / WATCH / INFO).
- Umbrales documentados y calibrados contra el dataset real del
  proyecto (no arbitrarios).
- Panel Dash con resumen ejecutivo automático y tarjetas por hallazgo.

---

## Capacidad de proceso (Cp/Cpk)

- `src/capability.py` (ya existente) conectado a Dash: selector de
  variable, histograma con LSL/USL/Promedio, clasificación Six Sigma.
- Bug real corregido: `config/quality_config.yaml` no tenía la sección
  `quality.variables_criticas` que el módulo necesitaba — la capacidad
  de proceso devolvía 0 variables hasta corregirlo.

---

## Control estadístico de proceso (`src/control_charts.py`)

- Carta I-MR (Individuals — Moving Range): límites de control
  calculados desde el rango móvil, detección de puntos fuera de
  control (regla Western Electric #1).
- Complementa a Cp/Cpk: Cp/Cpk mide si el proceso cumple especificación;
  esto mide si el proceso está en control estadístico.

---

## Análisis operacional con drill-down

- Ranking comparativo por línea/máquina/turno/operador, color-codificado
  con los mismos umbrales del motor de diagnóstico.
- Clic en una barra muestra el detalle (FPY, defectos, causa principal)
  de ese grupo específico.

---

## Interfaz y experiencia visual

- Tema oscuro "sala de control industrial" (`assets/style.css`),
  aplicado también a las figuras Plotly vía helper compartido
  (`aplicar_tema_oscuro`).
- Navegación por pestañas (Diagnóstico / Calidad / Capacidad / Control /
  Operacional) en vez de scroll largo — filtros globales siempre visibles.
- Pasada de minimalismo: sin degradados decorativos, jerarquía
  tipográfica clara (números grandes, etiquetas discretas).

---

## Bugs reales encontrados y corregidos (con evidencia)

- **CSS no cargaba**: Dash resolvía `assets/` relativo al módulo
  equivocado — corregido con `assets_folder` explícito.
- **Error de React** ("objects are not valid as a React child"): un
  callback enviaba una figura Plotly completa a la prop `children` de
  un `html.Div` en vez de a la prop `figure` de un `dcc.Graph`.
  Verificado y corregido a nivel de servidor (petición HTTP real al
  endpoint de callback de Dash).
- **"N/D" traducido como "Dakota del Norte"** por el traductor del
  navegador — reemplazado por texto sin ambigüedad ("Sin datos").

---

## Infraestructura

- CI en GitHub Actions: `ruff check` + `pytest --cov` en cada push.
- Deploy listo para Render (`Procfile`, `render.yaml`, `gunicorn`),
  probado con una petición HTTP real al servidor de producción.

---

## Estado actual

- **225 tests**, 100% pasando.
- Cobertura: última medida ~91% (pre-Semana 1); re-medir con
  `pytest --cov` tras el merge de Semana 1.
- `ruff check .`: limpio en CI; re-verificar en el push de Semana 1.