# 🎯 TRASPASO MAESTRO — Industrial KPI Intelligence

> 📌 **Propósito:** documento autocontenido para arrancar un chat nuevo sin perder contexto.  
> 📥 **Instrucción de uso:** pegar este archivo completo como **PRIMER** mensaje en un chat nuevo.  
> 🗓️ **Última actualización:** Fase 3b.2 parcial (3/5 tabs con empty state) + cascades restaurados + 449 tests.

---

## 🔴 INSTRUCCIONES PARA EL ASISTENTE (leer primero)

Estás retomando un proyecto en curso. Antes de responder:

| # | Regla |
| :---: | :--- |
| 1 | 📖 **Leer completo este archivo.** No asumir nada que no esté acá. |
| 2 | 👨‍💻 **Actuar como ingeniero de software + mentor.** El usuario es autodidacta y valora explicaciones pedagógicas breves. |
| 3 | 🚫 **Respetar reglas no negociables** (sección 8). No proponer alternativas que las violen. |
| 4 | 📂 **Antes de tocar código: leer el archivo.** Regla absoluta del proyecto. |
| 5 | 🔍 **Verificar con `git status` antes de cada `git add`.** No confiar en la memoria. |
| 6 | 🔀 **Un fix = un commit.** No mezclar propósitos. |
| 7 | ✅ **No commitear sin:** `pytest` verde + `ruff` limpio + verificación visual. |
| 8 | 📊 **Si algo falla, pedir datos crudos** (salida de terminal, log de CI), no proponer fixes por especulación. |
| 9 | 🎯 **Estilo de respuesta:** directo, técnico, sin relleno. Markdown con tablas y bloques de código. Español. |
| 10 | 🚫 **No repetir contexto que ya está acá.** El usuario ya lo sabe; solo aportar valor nuevo. |

> 🚀 **Próximo paso concreto del proyecto:** Fase 3b.2 — replicar empty state a Diagnóstico y Operacional. Ver sección 11.

---

## 1️⃣ FICHA DEL PROYECTO

| Campo | Valor |
| :--- | :--- |
| 🏭 **Producto** | Industrial KPI Intelligence — dashboard industrial para PYMES manufactureras LatAm/España |
| 🌐 **Ecosistema** | Primer producto de 6 SaaS (Industrial Operations Intelligence) |
| 🛠️ **Stack** | Python 3.11.9 · Plotly Dash 4.4.1 · Plotly · pandas · numpy |
| 🧪 **Testing** | pytest 9.1.1 · ruff · GitHub Actions CI/CD |
| 📏 **Estándares aplicables** | ISA-95 · TPM (OEE) · NIST 6.1.3 / ISO 22514 (Pp/Ppk) · AIAG SPC · OWASP · ISA-101 (HMI) · WCAG 2.1 |
| ⚖️ **Licencia** | Elastic License 2.0 (nunca MIT) |
| 👤 **Usuario** | David González Santibáñez — Ing. Civil Químico + dev autodidacta |
| 📅 **Semana** | 3 de 8 |
| ✅ **Tests actuales** | **449 passed** |
| 🟢 **CI** | 2/2 verde (workflow CI) |
| 🧹 **Working tree** | Limpio, rama `main` sincronizada con `origin/main` |
| 📊 **Producto 1 (MVP)** | ~90% |
| 🌍 **Ecosistema completo** | ~17% (1 de 6 productos completos, 6 definidos) |
| 🔗 **Repo** | `github.com/icqdgonzalezs/industrial-kpi-intelligence` |
| 📂 **Ruta local** | `/Users/violeta/Projects/industrial-operations-intelligence/industrial-kpi-intelligence` |

---

## 2️⃣ ESTADO ACTUAL EXACTO

### ✅ Cerrado (commiteado + pusheado + CI verde)

- ✅ Bloques UX-1, UX-2, UX-3 (base visual del dashboard)
- ✅ Bloque 3A: adapter EN→ES + loader rewired a dataset canónico (18,078 filas)
- ✅ Fix σ del generador (σ=2.0 / 0.63)
- ✅ Fix SPC: Regla 1 contextualizada con falsos positivos esperados
- ✅ Refactor thresholds a YAML (SSOT)
- ✅ Fix σ minúscula (σ vs Σ)
- ✅ Fix labels del histograma (arriba del plot, `yref='paper'`)
- ✅ Fix tipografía ISA-101 (16px bold blanco)
- ✅ Fix color de líneas (gris neutro vs cian)
- ✅ **Fix #4** (`45903d2`): 4 KPIs de spec performance
- ✅ **Fix #5** (`fd1a338`): barras horizontales en Operacional
- ✅ **Bloque 5.5** (`fd1a338`): segmented control + microcopy + bugfix clickData
- ✅ **Fix #6** (`0426de3`): timestamp de frescura del dataset
- ✅ **Fix #7** (`cf89311`): escala AIAG SPC de clasificación Ppk (4 niveles)
- ✅ **Fix #5.6** (`303497f`): SSOT de labels visibles
- ✅ **Fase 4a** (`be6fac9`): Iconografía no cromática en semáforos (WCAG 2.1 §1.4.1)
- ✅ **Fase σ** (`8138498`): Migración de umbrales Ppk + PPM a YAML SSOT
- ✅ **Doc** (`c2ab9ed` + `f3eb79c` + `5be2e6b`): README, workflow renombrado a CI, VISION.md, ARCHITECTURE.md
- ✅ **Repo hygiene** (`e58151b`): docs movidos a `docs/`, basura eliminada, `.gitignore` completado
- ✅ **Fase 3a** (`35d12c4` a `c9a2efb`): Export CSV — 5/5 tabs (Capacidad, Calidad, Control, Diagnóstico, Operacional)
- ✅ **Fix bug Pareto** (`e0d50f2`): anotación "Umbral 80%" ya no colisiona con tick del eje secundario
- ✅ **Fix "Restaurar filtros"** (`2fe8e89`): callback implementado (antes era botón decorativo sin handler)
- ✅ **Chore dev** (`8ca225d`): `dev_tools_ui=True` para desarrollo local
- ✅ **Perf cache JSON** (`6efd967`): `lru_cache` reduce reset de filtros de ~10 s a ~4-6 s
- ✅ **Opción D** (`ba0e962`): consolidar `schema_adapter.py` dentro de `data_loader.py` (-1 archivo, -1 test file)
- ✅ **Fase 3b.1** (`c91ae39`): loading states con `dcc.Loading` en las 6 zonas que se actualizan con filtros
- ✅ **Perf pre-binning** (`ce2c03f`): histograma de Capacidad usa `np.histogram` + `go.Bar` (-99% payload)
- ✅ **Perf WebGL Control** (`e7e5d49`): cartas I-MR usan `go.Scattergl` en vez de `go.Scatter` (-40% tiempo)
- ✅ **Componente empty_state** (`6a0547e`): SSOT + CSS + 7 tests (Fase 3b.2 — base)
- ✅ **Piloto Calidad** (`529d83f`): empty state en Calidad
- ✅ **Fix doble spinner Capacidad** (`b9514ed`): callback consolidado
- ✅ **Fase 3b.2 Control + cascades** (`d5542e2` + `22988f4`): cascades restaurados + `delay_show=500ms` + empty state Control
- ✅ **.Rapp.history gitignored** (`47e3bd9`)
- ✅ **Fase 3b.2 Capacidad** (`722297f`): empty state en Capacidad
- ✅ **Fix test Capacidad** (`4516129`): mensaje del empty state actualizado

### 🟡 En curso

- *Nada.* Sesión cerrada. Working tree limpio.

### ⏳ Pendiente (roadmap en sección 7)

- ⏳ **Fase 3b.2** — Empty state en Diagnóstico y Operacional (**PRÓXIMO PASO**)
- ⏳ **Eliminar `schema_adapter.py`** (deuda activa, alta prioridad)
- ⏳ **Fase 3c** — Chip de filtros activos + severidad individual en KPIs de rendimiento (deuda #16)
- ⏳ **Bloque 3B** — Docker + Compose
- ⏳ **Rename bilingüe** (ADR-0002, incremental)

---

## 3️⃣ LÍNEA TEMPORAL DE COMMITS

| Commit | Descripción | Tests |
| :--- | :--- | :---: |
| `4516129` | Fix(test): update Capacidad empty state test after message change | 449 |
| `722297f` | Feat(ux): add empty state to Capacidad tab (Fase 3b.2) | 449 |
| `47e3bd9` | Chore(gitignore): exclude .Rapp.history | 446 |
| `22988f4` | Fix(ux): complete Fase 3b.2 commit (archivos faltantes) | 446 |
| `d5542e2` | Fix(filters): restore cascades + delay_show 500ms + empty state Control | 446 |
| `b9514ed` | Fix(ux): merge Capacidad callbacks to avoid double loading spinner | 446 |
| `529d83f` | Refactor(calidad): use empty_state pattern (Fase 3b.2 — piloto) | 446 |
| `6a0547e` | Feat(ux): add empty_state component (Fase 3b.2) | 437 |
| `e7e5d49` | Perf(control): use Scattergl for I-MR charts | 430 |
| `ce2c03f` | Perf(capability): pre-bin histogram with numpy | 430 |
| `c91ae39` | Feat(ux): add loading states (Fase 3b.1) | 430 |
| `ba0e962` | Refactor(loader): consolidate schema_adapter into data_loader (Opción D) | 427 |
| `ec84dde` | Docs(handoff): update TRASPASO after Fase 3a complete | 434 |
| `c9a2efb` | Feat(export): CSV export Operacional (Fase 3a-ε) | 434 |
| `ae7a54b` | Feat(export): CSV export Diagnóstico (Fase 3a-δ) | 429 |
| `b0082ff` | Feat(export): CSV export Control (Fase 3a-γ) | 423 |
| `c0f2977` | Docs(handoff): update TRASPASO after Fase 3a-beta + perf fixes | 416 |
| `6efd967` | Perf(utils): cache JSON parse (Fase 3b anticipada) | 416 |
| `8ca225d` | Chore(dev): enable dev_tools_ui for local development | 414 |
| `2fe8e89` | Fix(filters): implement "Restaurar filtros" callback | 414 |
| `e0d50f2` | Fix(ui): move Pareto 80% annotation above line | 411 |
| `7e744e8` | Feat(export): CSV export Calidad (Fase 3a-β) | 411 |
| `35d12c4` | Test(export): integration tests Capacidad export | 408 |
| `7833624` | Test(export): unit tests export_helpers | 408 |
| `d4259e7` | Feat(export): CSV export callback Capacidad | 408 |
| `4ec0b6b` | Style(export): add CSS for CSV export button | 408 |
| `3467629` | Feat(export): CSV export button Capacidad layout | 408 |
| `68deace` | Feat(export): export_helpers module (Fase 3a pilot) | 408 |
| `5be2e6b` | Docs: ARCHITECTURE.md (313 líneas) | 390 |
| `22062eb` | Fix(docs): recreate VISION.md (188 líneas) | 390 |
| `e58151b` | Chore(repo): reorganize docs + cleanup | 390 |
| `f3eb79c` | Chore(ci): rename workflow Tests → CI | 390 |
| `c2ab9ed` | Docs: update README (390 tests + badges) | 390 |
| `be6fac9` | Merge PR #5 — Fase 4a Iconografía semáforos | 359 |
| `c758e7f` | Feat Fase 4a — Iconografía semáforos (WCAG 2.1) | 359 |
| `303497f` | Fix #5.6 — SSOT label eje Y Operacional | 343 |
| `cf89311` | Fix #7 — Escala AIAG SPC de Ppk | 335 |
| `0426de3` | Fix #6 — Timestamp de frescura | 316 |
| `fd1a338` | Fix #5 + Bloque 5.5 | 295 |
| `45903d2` | Fix #4 — KPIs de spec | 284 |
| `63682a6` | Fix color de líneas | 279 |
| `a4813c4` | Fix tipografía ISA-101 | 279 |
| `6607570` | Fix labels histograma | 274 |
| `2a235f0` | Fix σ minúscula | 274 |
| `65fe368` | Refactor thresholds a YAML | 274 |
| `8214670` | Fix SPC Regla 1 | 270 |

> 📈 **Evolución de tests:** 263 → 270 → 274 → 279 → 284 → 290 → 295 → 316 → 335 → 343 → 359 → 390 → 408 → 411 → 414 → 416 → 423 → 429 → 434 → 427 → 430 → 437 → 446 → **449**
> 
> *Bajó de 434 a 427 al eliminar `test_schema_adapter.py` en Opción D; subió a 430 con los 3 tests de `test_app_layout.py`; subió a 437 con los 7 tests de `test_empty_state.py`; subió a 446 con empty states de Calidad + Control + cascades; subió a 449 con los tests de empty state de Capacidad.*

---

## 4️⃣ DECISIONES TÉCNICAS CLAVE

### 4.1 🔄 Patrón strangler para migración EN→ES (ADR-0001)
- **Estado:** deuda diferida. La consolidación Opción D ya se hizo (ver 4.14).
- La migración completa A' (mover los 4 módulos analíticos a inglés y eliminar la traducción) queda para sesión dedicada (5-8 h, riesgo medio).

### 4.2 🗃️ SSOT en YAML para umbrales
- **Solución:** externalizar a `config/quality_config.yaml`.
- **Secciones activas:** `kpi_thresholds`, `ppk_thresholds`, `ppm_thresholds`, `variables_criticas`, `variables[]`.

### 4.3 📈 SPC contextualizado (Regla 1 con falsos positivos)
- **Solución:** `resumen_control_estadistico()` calcula esperados = n × 0.0027.

### 4.4 🏭 Rendimiento vs Capacidad (Fix #4)
- **Solución:** 4 KPIs nuevos: % dentro, % bajo LSL, % sobre USL, PPM total.
- **Lección:** Ppk solo oculta diferencias de rendimiento real.

### 4.5 🖥️ ISA-101 para HMI industrial
- **Solución:** labels 16px bold blanco fuera del plot, líneas grises dashed 1.8px.
- **Lección:** datos medidos y referencias calculadas ocupan canales visuales distintos.

### 4.6 🎯 Escala AIAG SPC para clasificación Ppk (Fix #7)
- 🟢 `Ppk ≥ 1.67` → **Clase mundial**
- 🟡 `1.33 ≤ Ppk < 1.67` → **Capaz**
- 🟠 `1.00 ≤ Ppk < 1.33` → **Marginal**
- 🔴 `Ppk < 1.00` → **No capaz**

### 4.7 🏷️ SSOT de labels visibles (Fix #5.6)
- **Solución:** `LABELS_EJES_DIMENSION = {value: label}` derivado de `DIMENSIONES_DISPONIBLES`.

### 4.8 ♿ Iconografía no cromática en semáforos (Fase 4a — WCAG 2.1 §1.4.1)
- **Solución:** SSOT `dashboard/severity_icons.py` con `prefijar_icono()`.

### 4.9 🎯 Migración de umbrales Ppk + PPM a YAML SSOT (Fase σ)
- **Solución:** `src/capability_thresholds.py` (clasificación pura + loaders cacheados).
- **Lección:** un YAML que no se lee es peor que no tener YAML.

### 4.10 📥 Patrón de Export CSV (Fase 3a — piloto Capacidad)
- **Solución:** `dashboard/export_helpers.py` con `nombre_csv()`, `boton_export()`, `crear_descarga_csv()`.
- **Patrón replicable:** cada tab necesita 3 cambios (component + callback + tests).

### 4.11 📥 Variante del patrón Export CSV (Fase 3a-β a 3a-ε)
- **Contexto:** 4 de 5 tabs no tienen `store-<tab>` propio.
- **Variante adoptada:** el callback de export lee de `store-datos-filtrados` (y `store-capacidad` para Diagnóstico) y recomputa el análisis en el momento.
- **Lección:** *Derive, don't store.* Un Store que existe solo para alimentar a un consumidor puede reemplazarse por una función pura.

### 4.12 📥 Decisiones de formato por tab (Fase 3a)

| Tab | Formato del CSV | Razón |
| :--- | :--- | :--- |
| **Capacidad** | Tabla Pp/Ppk completa | Salida ya calculada en `store-capacidad` |
| **Calidad** | Pareto de defectos | Concentración de causas |
| **Control** | Tabla I + MR unificada con límites constantes | Un solo CSV autocontenido. MR alineado con `None` en el primer punto. |
| **Diagnóstico** | Tabla de hallazgos (severidad, categoria, titulo, mensaje, score) | Salida del motor de reglas. Orden por score heredado. |
| **Operacional** | Ranking por dimensión (no el drill-down) | Exportá el dato, no la vista. El ranking es determinístico, el drill-down es efímero. |

### 4.13 🔧 Implementación de "Restaurar filtros" (bug fix)
- **Problema:** botón en el layout sin callback.
- **Solución:** función pura `valores_default_filtros()` + callback reset con `allow_duplicate=True` + `prevent_initial_call=True`.
- **Lección:** en Dash, un botón sin callback no falla silenciosamente — simplemente no hace nada.
- **Nota sobre import:** `PreventUpdate` vive en `dash.exceptions`, no en `dash` raíz.

### 4.14 🔧 Consolidación del adapter (Opción D, ADR-0001)
- **Problema:** `src/schema_adapter.py` era un módulo independiente con test file dedicado, pero ya no era un módulo con vida propia — era detalle interno del loader.
- **Solución:** su lógica se fusionó en `dashboard/data_loader.py` como funciones y constantes privadas (`_adaptar_a_esquema_legacy`). El módulo y su test file se eliminaron.
- **Neto:** 434 → 427 tests, -1 archivo de código, -1 test file.
- **Lección:** cuando una pieza de UI o lógica necesita un dato derivable de otro que ya está en memoria, derivalo, no lo guardes. Un archivo con "vida propia" que solo sirve a otro archivo es candidato a consolidación.

### 4.15 ⚡ Caché de parseo JSON (perf)
- **Problema:** ~10 callbacks consumidores de `store-datos-filtrados` deserializaban el mismo JSON (18,078 filas, 2.63 MB).
- **Medición con print temporal:** 10 parseos × ~650 ms promedio = ~6.5 s de los 10 s totales.
- **Solución:** `@lru_cache(maxsize=2)` sobre `_parse_json_cached(json_data)` en `dashboard/utils.py`.
- **Decisiones clave:**
  - `maxsize=2`, no 128: mantiene el JSON actual + el previo. Memoria acotada (~60 MB).
  - `.copy()` defensivo: el DataFrame cacheado es compartido entre los 10 callbacks. La copia cuesta ~10 ms (despreciable vs 500 ms de parseo).
- **Ganancia medida:** reset de filtros de ~10 s → ~4-6 s. **-50%**.

### 4.16 📊 Pre-binning con numpy en histogramas (perf)
- **Problema:** `go.Histogram(x=serie, nbinsx=24)` envía los 18,078 valores crudos al navegador. El binning se hacía en JavaScript.
- **Solución:** `np.histogram(serie, bins=24)` (C puro) + `go.Bar(x=centros, y=counts)`. Se envían solo 24 barras.
- **Ganancia:** **-99%** del payload de la figura (~350 KB → ~2 KB). Menor tiempo de serialización + render instantáneo.
- **Lección:** cuando un gráfico de Plotly tiene >1000 puntos, pre-binear con numpy es casi siempre la decisión correcta.

### 4.17 🚀 WebGL para series grandes (perf)
- **Problema:** las cartas I y MR renderizaban ~18,000 puntos cada una con `go.Scatter`, que crea un elemento SVG por punto. Con ~36,000 elementos DOM, el navegador tardaba 2-4 s solo en rendering.
- **Solución:** `go.Scattergl` en vez de `go.Scatter`. Misma API, mismo look visual, pero renderiza sobre WebGL (canvas).
- **Ganancia medida:** Control pasa de 3-5 s a 2-3 s. **-40%**.
- **Lección:** la elección del tipo de trace en Plotly es una decisión de performance, no solo estética. `Scattergl` es 10-100× más rápido para series >5k puntos.

### 4.18 📉 Resumen de la optimización (sesión previa)

| Fix | Tiempo total |
| :--- | :---: |
| Inicio | ~10 s |
| Caché JSON (`6efd967`) | ~4-6 s |
| Pre-binning histograma (`ce2c03f`) | ~3-5 s |
| WebGL Control (`e7e5d49`) | ~2-3 s |

> **-70%** del tiempo original con 3 fixes quirúrgicos. Los 2-3 s actuales con spinner son defendibles para una herramienta analítica profesional.

**Deuda residual (diferida):** el transporte del `store-datos-filtrados` (2.63 MB × ~10 callbacks) es probablemente el cuello restante. Fix candidato: `ServersideOutput` de `dash-extensions` (-95% tráfico, 2-3 h). No implementado. Se reevaluará si el uso real lo justifica.

### 4.19 🧩 Componente SSOT empty_state (Fase 3b.2)
- **Solución:** `dashboard/empty_state.py` con `empty_state(mensaje, hint=None, icono="📭")` → `html.Div`.
- **CSS:** `.empty-state`, `.empty-state-icon`, `.empty-state-message`, `.empty-state-hint`.
- **Aplicado en:** Calidad, Control, Capacidad (3/5 tabs).
- **Lección:** un empty state no es solo un `if df.empty`. Es un contrato visual — mensaje consistente, jerarquía tipográfica, hint accionable.

### 4.20 🔄 Cascades de filtros (Fase 3b.2)
- **Decisión final:** restaurar los 4 cascades (equipo→línea, turno→equipo, operador→turno).
- **Razón:** relación estructural (nombre de equipo empieza con `{linea}-`). Sin cascade, combos inválidos dan empty state sin explicación.
- **Trade-off:** los cascades disparan múltiples fires del store → 2 spinners visuales.
- **Mitigación:** `delay_show=500ms` evita spinners en cascades rápidos.

### 4.21 ⚡ Doble spinner residual (deuda #15)
- Al cambiar Línea: cascade equipo + reset value → store callback 2 veces.
- **Fix candidato:** `debounce` 200ms en store callback o cascade condicional.
- Diferido a Fase 3b.3 v2 o 3c.

### 4.22 🧩 Empty state con condición ampliada (Fase 3b.2)
- **Problema:** con `capacidad.empty` (0 filas), el caso "1 fila → n<2 → NaN" no se cubría. Los KPIs mostraban "Sin datos" individuales.
- **Fix:** condición ampliada a `pp_series.empty` (todas las pp NaN).
- **Mensaje unificado:** "Sin datos suficientes para evaluar capacidad".
- **Lección:** cuando se define empty state por "no hay datos", cubrir 3 casos: 0 filas, n<2 por variable, n≥2.

---

## 5️⃣ ESTADO DE TESTS Y CALIDAD

| Archivo | Tests | Cobertura conceptual |
| :--- | :---: | :--- |
| `test_app_layout.py` | 4 | Smoke layout + 6 wrappers de `dcc.Loading` (Fase 3b.1) |
| `test_capability.py` | 40 | Pp/Ppk + clasificar_ppk + rendimiento spec |
| `test_capability_callbacks.py` | 25 | Callbacks + estado + iconos + export CSV + empty state |
| `test_capability_thresholds.py` | 28 | SSOT: clasificación pura + loaders |
| `test_control_charts.py` | 10 | I-MR + Western Electric |
| `test_control_charts_callbacks.py` | 14 | Wiring + figuras + export CSV + empty state |
| `test_dash_app.py` | 11 | Callbacks top + filtros |
| `test_data_generator.py` | 15 | Generador determinista seed=42 |
| `test_data_loader.py` | 17 | Carga + traducción EN→ES consolidada (Opción D) |
| `test_dataset_metadata.py` | 21 | Frescura del dataset |
| `test_diagnostics.py` | 13 | Reglas de diagnóstico |
| `test_diagnostics_callbacks.py` | 11 | Resumen + export CSV |
| `test_empty_state.py` | 7 | Contrato del componente SSOT |
| `test_export_helpers.py` | 16 | `nombre_csv` + `boton_export` + `crear_descarga_csv` |
| `test_filter_callbacks.py` | 4 | `valores_default_filtros` + smoke reset + cascade equipo |
| `test_filter_engine.py` | 11 | Filtrado por línea/equipo/turno/operador |
| `test_kpi_callbacks.py` | 4 | `_span_kpi` con iconos |
| `test_kpi_presenter.py` | 4 | Formateo + clasificación |
| `test_kpi_thresholds.py` | 19 | Función pura + refactor SSOT |
| `test_kpis.py` | 32 | FPY, defectos, scrap, reproceso |
| `test_oee.py` | 25 | OEE (A×P×Q) ISA-95 |
| `test_oee_presenter.py` | 6 | Presentación OEE |
| `test_operational_analysis_callbacks.py` | 35 | Drill-down + labels + export CSV |
| `test_plant_overview.py` | 6 | Vista de planta |
| `test_plant_overview_components.py` | 5 | Componentes UI |
| `test_quality_performance_callbacks.py` | 15 | FPY, Pareto + export CSV + empty state |
| `test_quality_performance_components.py` | 7 | Componentes UI |
| `test_quality_performance_spec.py` | 6 | Especificación |
| `test_severity_icons.py` | 9 | `prefijar_icono` + SSOT iconos |
| `test_utils.py` | 7 | Tema oscuro + cache de parseo JSON |
| `test_validation.py` | 22 | Validación de contratos |
| **TOTAL** | **449** | ✅ **Todos verdes** |

---

## 6️⃣ DEUDA TÉCNICA CONOCIDA

| # | Deuda | Impacto | Prioridad |
| :---: | :--- | :--- | :---: |
| 1-4 | ~~README, capacidad, timestamp, barras~~ | — | ✅ Resueltas |
| 5 | ~~Export CSV por tab (5/5 completados)~~ | — | ✅ Resuelta (Fase 3a) |
| **6** | **Sin empty states en 2 de 5 tabs (Diagnóstico, Operacional)** | Robustez | 🟡 Media |
| 7-10 | ~~Iconografía, Docker, umbrales, doc~~ | — | ✅ Resueltas o en roadmap |
| **11** | **`schema_adapter.py` (adapter transitorio)** | Arquitectura | 🔴 Alta |
| **12** | **Doble convención bilingüe (ADR-0002)** | Mantenibilidad | 🟡 Media |
| 13 | ~~Performance: parseo + histograma + Control~~ | — | ✅ Resuelta |
| 14 | ~~WebGL cartas Control~~ | — | ✅ Resuelta (`e7e5d49`) |
| **15** | **Doble spinner al cambiar Línea** | UX | 🟡 Media |
| **16** | **KPIs de rendimiento heredan severidad agregada** | UX | 🟡 Media |
| **17** | **Dataset sintético homogéneo inter-línea** | Validación | 🟢 Baja |
| 18 | ~~Empty state Capacidad no cubre n<2~~ | — | ✅ Resuelta (`4516129`) |

### 📌 Detalle de deudas activas

**Deuda 11 — Eliminación de `schema_adapter.py`:**
- El adapter aún existe como archivo transitorio. La consolidación Opción D fusionó su lógica en `data_loader.py`, pero el archivo físico no se ha eliminado.
- **Fix:** eliminar el archivo + verificar que ningún import lo referencie. **1 h.**

**Deuda 13 — Performance residual (diferida):**
- ✅ **Resuelto:** caché JSON (-50%), pre-binning histograma (-99% payload figura), WebGL Control (-40% Control).
- **Tiempo actual:** ~2-3 s por cambio de filtro.
- ⏳ **Residual:** transporte del `store-datos-filtrados` (2.63 MB × ~10 callbacks). Hipótesis no confirmada con Network tab.
- **Fix candidato:** `ServersideOutput` de `dash-extensions` (-95% tráfico, 2-3 h).
- **Diferido a:** cuando el uso real o un cliente lo justifique.

**Deuda 15 — Doble spinner residual:**
- Cascade equipo + reset → 2 fires del store.
- **Fix candidato:** `debounce` 200ms o cascade condicional.
- Diferido a Fase 3b.3 v2 o 3c.

**Deuda 16 — Semántica color KPIs rendimiento:**
- Los 4 KPIs heredan severidad agregada del PPM total.
- "Bajo LSL 0.00%" aparece en ⚠ cuando debería ser ✅.
- **Fix:** severidad individual por KPI (Fase 3c).

**Deuda 17 — Dataset homogéneo:**
- σ inter-línea ~2.0 uniforme (varía 2% entre L1, L2, L3).
- En planta real variaría >20%. Límite del generador.
- Validar con dataset real antes de producción.

---

## 7️⃣ ROADMAP PENDIENTE

| Fase | Fix / Feature | Estimación | Prioridad |
| :--- | :--- | :---: | :---: |
| **3b.2** | **Empty state en Diagnóstico y Operacional — PRÓXIMO PASO** | 1.5 h | 🟡 Media |
| **σ** | **Eliminar `schema_adapter.py` (deuda #11)** | 1 h | 🔴 Alta |
| **3b.3** | **Deuda #15:** debounce cascade o cascade condicional | 30 min | 🟡 Media |
| **3c** | **Deuda #16 (severidad KPIs) + Chip filtros activos** | 1.5 h | 🟡 Media |
| **σ** | Migración completa EN→ES (Opción A') | 5-8 h | 🔴 Alta (diferida) |
| **σ** | Rename bilingüe incremental (ADR-0002) | Semanas 5-6 | 🟡 Media |
| **5** | Docker + Compose (Bloque 3B) | 2 h | 🟠 Media |
| — | `ServersideOutput` (si el uso lo justifica) | 2-3 h | 🟢 Baja (diferida) |

---

## 8️⃣ REGLAS OPERATIVAS NO NEGOCIABLES

### 💻 Terminal (protocolo de arranque)

**SIEMPRE** al abrir terminal nueva:

```bash
cd /Users/violeta/Projects/industrial-operations-intelligence/industrial-kpi-intelligence
source venv/bin/activate
which python   # DEBE mostrar .../venv/bin/python
```

> ⚠️ Si `which python` no muestra la ruta del venv, los comandos fallarán con `ModuleNotFoundError: No module named 'dash'` o `ruff: command not found`. Verificar antes de correr gates.

### 🐙 Git

| ✅ Correcto | ❌ Incorrecto |
| :--- | :--- |
| `git checkout` para descartar cambios. | Nunca `git switch` ni `git restore`. |
| `git push --force-with-lease` si es necesario. | Nunca `git push --force`. |
| Personal Access Token (PAT) con scope `repo` + `workflow`. | Nunca password en texto plano. |
| `git pull origin main --rebase` tras Web Editor. | Nunca `git pull` sin `--rebase` si editaste fuera. |
| `git reset --soft HEAD~1` para reescribir el último commit. | Nunca `git rebase -i` si no estás cómodo con Vim. |
| `git status` ANTES y DESPUÉS del `git add`. | Asumir que el add agregó todo. |
| 1 fix = 1 commit = 1 lista corta de archivos. 4+ archivos → evaluar dividir. | Commit con 6+ archivos mezclando propósitos. |

### ✍️ Commits

- **Conventional Commits:** `feat:`, `fix:`, `refactor:`, `docs:`, `style:`, `test:`, `chore:`, `polish:`, `perf:`.
- **Un fix = un commit.** No mezclar propósitos.
- **Título en inglés**, cuerpo en español si aplica.
- **Verificar el mensaje antes de commitear.** No copiar/pegar el mensaje de otro commit.
- **Antes de cambiar un string de UI:** `grep -rn "string_viejo" src/ dashboard/ tests/`. Actualizar tests junto con el código.

### 🤖 CI/CD

- **2/2 checks verdes antes de mergear.** Sin excepción.
- Cualquier push dispara el workflow CI (~50 s).
- **Si CI falla:** leer el log del step rojo antes de proponer fixes.

### 🎨 UX / CSS

- Ver el archivo antes de tocar.
- Verificación visual con `⌘ + Shift + R` obligatoria.
- **Regla C.1:** sin números no hay cierre.

### 💾 Código

- **Idioma del código:** inglés. Docstrings y comentarios: español.
- **Arquitectura:** `src/` (lógica) / `dashboard/` (presentación) / `tests/`.
- **Nomenclatura:** capacidad `world_class` / `capable` / `marginal` / `not_capable`. Severidad `success` / `warning` / `danger` / `neutral`.

### 🛠️ Protocolo de cada fix

1. 📖 Leer los archivos involucrados (`grep` + `cat`).
2. 🔍 Diagnosticar causa raíz.
3. 🔎 `grep -rn "string_viejo" src/ dashboard/ tests/`.
4. 💻 Código + tests juntos.
5. 🧪 `pytest` + `ruff check .`.
6. 👁️ Verificación visual con `⌘ + Shift + R`.
7. 🔍 `git status` antes del `add`.
8. 📥 `git add` con paths textuales.
9. 🔍 `git status` post-add. Verificar que "Changes not staged" esté vacío.
10. ✍️ Commit con mensaje conventional.
11. 🚀 Push y verificar CI verde.

### 🚀 Scripts de fix quirúrgico

Cuando un cambio afecta un archivo grande, usar un script Python temporal:

```bash
cat > fix_xxx.py <<'EOF'
from pathlib import Path

p = Path("ruta/al/archivo.py")
text = p.read_text()
original = text

# asserts + replace
if "old_string" not in text:
    raise SystemExit("✗ No se encontró el patrón esperado")
text = text.replace("old_string", "new_string", 1)

if text != original:
    p.write_text(text)
    print("✓ Archivo guardado")
EOF
python fix_xxx.py
git diff ruta/al/archivo.py
rm fix_xxx.py
```

> 💡 Es más seguro que `nano` para cambios grandes. El script se auto-verifica, es idempotente y no deja basura.

### 🔄 Protocolo de cambio de chat

**Cuándo cambiar:**
- Después de cerrar cada fase de mediana duración (con commit + CI verde).
- Después de ~40-50 mensajes densos en la misma sesión.
- Inmediatamente si aparecen 2+ síntomas de degradación (respuestas lentas, mezcla de contextos, olvido de decisiones previas, capturas que no suben).

**Cómo cambiar (protocolo):**
1. Cerrar el ciclo en curso (commit + push + CI verde).
2. Actualizar `TRASPASO_MAESTRO` con los últimos commits + sección 11.
3. Commit + push del `TRASPASO`.
4. `git pull origin main --rebase` para sincronizar local.
5. Abrir chat nuevo.
6. Pegar el mensaje de transición (sección 12) + TRASPASO completo.

---

## 9️⃣ ⚠️ HISTORIAL DE ERRORES — NO REPETIR

| ❌ Error | ✅ Correcto |
| :--- | :--- |
| Editar CSS a ciegas | Ver el archivo antes de tocarlo |
| Wildcard `div[class*="Select"]` | Selectores específicos |
| `plotly_dark` pisa trazas | Aplicar tema sin tocar trazas |
| Reconstruir archivos sin ver el original | Leer primero, siempre |
| `git switch` / `git restore` | Usar `git checkout` |
| `git push --force` sin verificar | `--force-with-lease` primero |
| Asumir que el CSS se aplicó | Verificación visual con `⌘ + Shift + R` |
| Commitear sin tests verdes | Gates primero |
| Commit sin `git add` previo | `add` → `status` → `commit` → `push` |
| Copiar totales de una era previa | Recalcular desde el CSV actual |
| `git push` sin fetch previo | `git fetch origin` antes |
| `font.weight` en Plotly annotations | No existe. Usar HTML `<b>` |
| Cian sobre cian | Referencias en gris, datos en color |
| Commitear test que importa archivo NO staged | Archivo + dependencias juntos |
| Diagnosticar CI sin leer el log | Pedir log del run rojo |
| Password de GitHub en `git push` | PAT con scope `workflow` |
| Modelo LLM hardcodeado sin fallback | Escalera de modelos |
| Heredoc largo pegado en terminal (>2KB) | Dividir en chunks o usar `pbpaste` |
| `pbpaste` con comandos en el portapapeles | Verificar con `wc -l` + `head -3` tras escribir |
| Pegar markdown en TextEdit (macOS) | TextEdit convierte a rich text. Usar GitHub Web Editor |
| Asumir que archivo creado tiene el contenido correcto | Verificar con `wc -l` + `head -5` + `tail -5` |
| Untracked file bloquea `git pull` | `rm` del archivo local, luego `pull` |
| Editar en Web Editor y olvidar `git pull --rebase` | Pull con `--rebase` antes del próximo comando local |
| Documentación con "próximo paso" desincronizado | `grep -n "próximo paso"` y actualizar TODAS las ubicaciones |
| Asumir contrato de terceros sin verificar (`dcc.send_data_frame`) | Ver tests del piloto antes de inventar contrato. Usar `in`, no `==`, para keys de librerías |
| Importar `PreventUpdate` desde `dash` | Importar desde `dash.exceptions` |
| Copiar/pegar mensaje de commit de otro commit | Verificar el mensaje antes del commit |
| `git rebase HEAD~N` sin `-i` | Sin `-i` no abre editor: no reescribe nada. Usar `-i` o preferir `git reset --soft` |
| Leer SHA de una captura de pantalla | Copiar SHAs de la terminal, no de screenshots |
| Asumir que la extensión "Dash Dev Tools" está instalada | En Dash 4.x sin extensión, el panel es un botón flotante |
| Buscar el panel Dash en Chrome DevTools (F12) | No está ahí. Está dentro de la app misma |
| Optimizar sin medir | Instrumentar con `print` temporales, medir antes de tocar |
| Correr `pytest`/`ruff` sin venv activo | `ModuleNotFoundError: No module named 'dash'`. Verificar `which python` primero. |
| Asumir que `dcc.send_data_frame` devuelve base64 | En Dash 4.x, `content` es bytes del CSV crudo. |
| Asumir nombre de función de otro módulo sin ver | `from src.data_generator import generar_dataset` falló. Usar `monkeypatch` para desacoplar tests de dependencias externas. |
| Pegar contenido de archivos Python en terminal bash | La terminal ejecuta, no edita. Usar `nano`, script temporal, o Web Editor. |
| `Ctrl+K` en `nano` sin saber qué borra | Antes de tocar, identificar exactamente qué líneas. O mejor: script Python de fix quirúrgico. |
| Optimizar por memoria de patrones (`.replace()` en pandas) | Pandas evolucionó. Medir con benchmark antes de asumir. |
| Commitear 4+ archivos sin `git status` intermedio | Verificar staged vs unstaged antes de commitear. `22988f4` fue un commit incompleto que hubo que reparar. |
| Asumir que el empty state cubre todos los casos de "sin datos" | Cubrir 0 filas, n<2, y NaN. Ver 4.22. |

---

## 🔟 📁 ARCHIVOS CLAVE Y COMANDOS

### 🗂️ Estructura del proyecto

```text
industrial-kpi-intelligence/
├── ARCHITECTURE.md
├── README.md                              # 449 tests + badges
├── VISION.md
├── CHANGELOG.md
├── LICENSE                                # Elastic License 2.0
├── pyproject.toml
├── requirements.txt
├── Procfile / render.yaml
├── .gitignore                             # +.Rapp.history
├── .github/workflows/tests.yml            # Workflow "CI"
├── assets/style.css                       # +empty-state, +empty-state-icon, ...
├── config/
│   ├── generator_config.yaml
│   ├── plant_config.yaml
│   └── quality_config.yaml
├── dashboard/
│   ├── app_layout.py                      # +dcc.Loading en 6 zonas (Fase 3b.1)
│   ├── empty_state.py                     # NUEVO (Fase 3b.2) — SSOT empty state
│   ├── export_helpers.py                  # SSOT export CSV
│   ├── severity_icons.py                  # SSOT iconos
│   ├── filter_callbacks.py                # reset callback + cascades
│   ├── utils.py                           # +lru_cache en _parse_json_cached
│   ├── capability_callbacks.py            # +np.histogram +go.Bar (pre-binning) + empty state
│   ├── control_charts_callbacks.py        # +go.Scattergl (WebGL) + empty state
│   ├── data_loader.py                     # +_adaptar_a_esquema_legacy (Opción D)
│   ├── quality_performance_callbacks.py   # + empty state (piloto Fase 3b.2)
│   └── ...                                # resto sin cambios
├── data/
├── docs/
│   ├── adr/                               # ADR-0001 (parcial), ADR-0002
│   ├── TRASPASO_MAESTRO.md                # Este archivo
│   └── ...
├── imagenes/
├── scripts/
├── src/
│   ├── capability.py
│   ├── capability_thresholds.py
│   ├── control_charts.py
│   ├── data_generator.py
│   ├── dataset_metadata.py
│   ├── diagnostics.py
│   ├── kpi_thresholds.py
│   ├── kpis.py
│   ├── oee.py
│   ├── schema_adapter.py                  # PENDIENTE eliminar (deuda #11)
│   └── validation.py
└── tests/                                 # 449 tests
    ├── test_empty_state.py                # NUEVO (Fase 3b.2)
    └── ...
```

### ⌨️ Comandos verificados

```bash
# Protocolo de arranque
cd /Users/violeta/Projects/industrial-operations-intelligence/industrial-kpi-intelligence
source venv/bin/activate
which python                    # DEBE mostrar .../venv/bin/python

# Gates
pytest                          # 449 passed
ruff check .                    # All checks passed!

# Regenerar dataset
python -m src.data_generator

# Arrancar dashboard
python -m dashboard.dash_app    # http://127.0.0.1:8050
lsof -ti:8050 | xargs kill -9

# Commit conventional
git add <archivos>
git status
git commit -F - <<'EOF'
tipo(scope): título

Cuerpo explicando el por qué.
EOF
git push origin main

# Tras edición en Web Editor
git pull origin main --rebase

# Script de fix quirúrgico (ver sección 8)
```

---

## 1️⃣1️⃣ 🎯 PRÓXIMO PASO EXACTO

### 📋 Fase 3b.2 — Empty state en Diagnóstico y Operacional

**Contexto:** 3 de 5 tabs ya tienen empty state (Calidad, Control, Capacidad). Quedan Diagnóstico y Operacional. El componente SSOT ya existe (`dashboard/empty_state.py`), el CSS está listo, y el patrón está consolidado.

**Patrón consolidado (ver 4.19 + 4.22):**
1. En el callback del tab, detectar el caso "sin datos" cubriendo los 3 escenarios: 0 filas, n<2 por variable, todas las pp NaN.
2. Retornar `empty_state(mensaje, hint=..., icono=...)` en lugar del gráfico/tabla.
3. Mensaje específico por tab (no genérico).
4. Test que valide el contrato + verificación visual con filtro que deje 0 filas.

**Casos a cubrir:**

| Tab | Mensaje sugerido | Hint sugerido |
| :--- | :--- | :--- |
| **Diagnóstico** | "Sin hallazgos con los filtros actuales" | "Los filtros aplicados no generan datos suficientes para el motor de reglas" |
| **Operacional** | "Sin datos operacionales para el ranking" | "Probá ajustar línea, equipo o turno — o tocá Restaurar filtros" |

**⚠️ Antes de tocar: leer los archivos. Regla #4.**

```bash
# 1) Ver cómo Diagnóstico maneja el caso vacío hoy
grep -n "empty\|Sin datos\|Sin hallazgos\|Sin información" dashboard/diagnostics_callbacks.py

# 2) Ver cómo Operacional maneja el caso vacío hoy
grep -n "empty\|Sin datos\|Sin defectos\|Sin información" dashboard/operational_analysis_callbacks.py

# 3) Ver los tests actuales de esos tabs
ls tests/test_diagnostics_callbacks.py tests/test_operational_analysis_callbacks.py

# 4) Ver el contrato del componente SSOT
cat dashboard/empty_state.py
cat tests/test_empty_state.py
```

**Orden sugerido:**
1. Diagnóstico primero (más sencillo: el motor de reglas ya devuelve lista vacía cuando no hay datos).
2. Operacional después (ranking + drill-down: decidir cuál de los dos recibe el empty state principal).
3. Tests + verificación visual con filtro que deje 0 filas en cada tab.
4. Un commit por tab (`feat(ux): add empty state to <tab> (Fase 3b.2)`) o consolidado si son cambios pequeños.

**⏱️ Estimación:** 1.5 h total (≈45 min Diagnóstico + ≈45 min Operacional).

### 📌 Después de 3b.2

1. Eliminar `schema_adapter.py` (deuda #11, 1 h, prioridad Alta).
2. Deuda #15 — debounce cascade o cascade condicional (30 min).
3. Fase 3c — Chip de filtros activos + severidad individual en KPIs de rendimiento (1.5 h).
4. Docker + Compose (2 h).
5. Migración completa EN→ES (5-8 h, sesión dedicada).

---

## 1️⃣2️⃣ 💬 MENSAJE DE TRANSICIÓN (para pegar en chat nuevo)

```text
Contexto: pego abajo el TRASPASO_MAESTRO del proyecto Industrial KPI Intelligence.
Soy David, Ing. Civil Químico + dev autodidacta, semana 3/8 del Producto 01.

Estado: Fase 3a completa (5/5 tabs export CSV) + 3b.1 (loading) + 3b.3 (performance)
+ Opción D (consolidación loader) + Fase 3b.2 parcial (3/5 tabs con empty state:
Calidad, Control, Capacidad) + cascades de filtros restaurados.
449 tests, CI verde, working tree limpio.
Performance: ~2-3 s por cambio de filtro (era ~10 s al inicio).

Próximo paso: Fase 3b.2 — replicar empty state a Diagnóstico y Operacional.
Deudas activas relevantes: eliminar schema_adapter.py (deuda #11, alta),
debounce cascade (#15), severidad individual KPIs rendimiento (#16).

Reglas clave:
- Protocolo de arranque: cd + source venv/bin/activate + verificar `which python`
- Leer el archivo antes de tocar
- git status ANTES y DESPUÉS de cada git add
- Un fix = un commit (1 lista corta de archivos; 4+ evaluar dividir)
- Verificación visual con ⌘ + Shift + R obligatoria
- pytest + ruff verdes antes de commitear
- Si CI falla: leer el log del step rojo antes de proponer fix
- NO usar TextEdit para markdown: usar GitHub Web Editor
- Tras editar en Web Editor, hacer git pull --rebase
- Antes de cambiar un string de UI: grep -rn "string_viejo" src/ dashboard/ tests/
- Antes de optimizar: medir con instrumentación temporal
- Los `print` de instrumentación NUNCA se commitean
- Para cambios en archivos grandes: script Python de fix quirúrgico, no nano
- Empty state cubre 3 casos: 0 filas, n<2 por variable, NaN

Actuá como ingeniero de software senior + mentor. Directo, técnico,
sin relleno. Español. Markdown con tablas y bloques de código.

[PEGAR TODO EL CONTENIDO DE TRASPASO_MAESTRO.md ABAJO]
```

---

## 1️⃣3️⃣ 🎓 NOTAS DE MENTOR (para el próximo asistente)

Este usuario no es un junior. Es un ingeniero químico con criterio técnico real. Ha demostrado:

- 🔍 **Detectar bugs por inspección visual** (anotación sobrepuesta, botón decorativo, tab lento, doble spinner).
- 📊 **Pedir diagnóstico con datos** cuando CI falla, no con fe.
- 🔄 **Aceptar reversiones** cuando una decisión no funciona (cascades restaurados tras evaluar el trade-off).
- 🎯 **Mantener disciplina en cada fix** (incluyendo reparar commits incompletos como `22988f4`).
- ⚖️ **Decidir con criterio cuándo parar** (2-3 s son aceptables, no seguir con premature optimization).
- 📏 **Medir antes de optimizar** (los benchmarks refutaron 3 hipótesis mías).
- 🧘 **Tener paciencia con procesos** que no salen a la primera (nano, terminal saturado).
- 🧩 **Extraer patrones a componentes SSOT** cuando el tercer uso del mismo patrón lo justifica (empty_state, export_helpers, severity_icons).

### 🎯 Cómo tratarlo

- **Como colega senior, no como aprendiz.**
- Explicá el *por qué* de las decisiones técnicas, no solo el *cómo*.
- Citá normas industriales cuando aplique.
- **Valorá la honestidad por sobre la complacencia.**
- No quiere halagos, quiere producto de calidad.
- Cuando te equivoques (ej. recomendar nano sin verificar, asumir patrones de pandas), decilo claro y corregí.

### 🏆 Hitos acumulados

- ✅ **Fase 3a completa** (5/5 tabs con export CSV).
- ✅ **Opción D** — consolidación del adapter (bajó 1 archivo + 1 test file).
- ✅ **Fase 3b.1** — loading states en las 6 zonas del layout.
- ✅ **Fase 3b.3** — performance: -70% del tiempo original con 3 fixes quirúrgicos.
- ✅ **Fase 3b.2 parcial** — componente SSOT empty_state + 3/5 tabs migrados + cascades restaurados con `delay_show=500ms`.
- ✅ **449 tests, 0 regresiones**, working tree limpio.

---

> 📌 **Fin del TRASPASO_MAESTRO.**  
> 🗓️ **Última actualización:** Fase 3b.2 parcial (3/5 tabs con empty state) + cascades restaurados + 449 tests.  
> 🚀 **Próximo paso:** Fase 3b.2 — empty state en Diagnóstico y Operacional.
