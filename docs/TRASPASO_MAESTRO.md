# 🎯 TRASPASO MAESTRO — Industrial KPI Intelligence

> 📌 **Propósito:** documento autocontenido para arrancar un chat nuevo sin perder contexto.
> 📥 **Instrucción de uso:** pegar este archivo completo como PRIMER mensaje en un chat nuevo.
> 🗓️ **Última actualización:** Fase 4a + Doc + σ + **Fase 3a completa (5/5 tabs con export CSV)** + fixes UX/perf.

---

## 🔴 INSTRUCCIONES PARA EL ASISTENTE (leer primero)

Estás retomando un proyecto en curso. Antes de responder:

| # | Regla |
|---|---|
| 1 | **Leer completo este archivo.** No asumir nada que no esté acá. |
| 2 | **Actuar como ingeniero de software + mentor.** El usuario es autodidacta y valora explicaciones pedagógicas breves. |
| 3 | **Respetar reglas no negociables** (sección 8). No proponer alternativas que las violen. |
| 4 | **Antes de tocar código: leer el archivo.** Regla absoluta del proyecto. |
| 5 | **Verificar con `git status` antes de cada `git add`.** No confiar en la memoria. |
| 6 | **Un fix = un commit.** No mezclar propósitos. |
| 7 | **No commitear sin: pytest verde + ruff limpio + verificación visual.** |
| 8 | **Si algo falla, pedir datos crudos** (salida de terminal, log de CI), no proponer fixes por especulación. |
| 9 | **Estilo de respuesta:** directo, técnico, sin relleno. Markdown con tablas y bloques de código. Español. |
| 10 | **No repetir contexto que ya está acá.** El usuario ya lo sabe; solo aportar valor nuevo. |

> 🎯 **Próximo paso concreto del proyecto:** decidir el próximo frente — 3 opciones en sección 11 (schema_adapter vs Fase 3b vs Fase 3c). Recomendación: schema_adapter (deuda activa 🔴 Alta).

---

## 1️⃣ FICHA DEL PROYECTO

| Campo | Valor |
|---|---|
| 🏭 **Producto** | Industrial KPI Intelligence — dashboard industrial para PYMES manufactureras LatAm/España |
| 🌐 **Ecosistema** | Primer producto de 6 SaaS (Industrial Operations Intelligence) |
| 🛠️ **Stack** | Python 3.11.9 · Plotly Dash 4.4.1 · Plotly · pandas · numpy |
| 🧪 **Testing** | pytest 9.1.1 · ruff · GitHub Actions CI/CD |
| 📏 **Estándares aplicables** | ISA-95 · TPM (OEE) · NIST 6.1.3 / ISO 22514 (Pp/Ppk) · AIAG SPC · OWASP · ISA-101 (HMI) · WCAG 2.1 |
| ⚖️ **Licencia** | Elastic License 2.0 (nunca MIT) |
| 👤 **Usuario** | David González Santibáñez — Ing. Civil Químico + dev autodidacta |
| 📅 **Semana** | 3 de 8 |
| ✅ **Tests actuales** | **434 passed** |
| 🟢 **CI** | 2/2 verde (workflow CI, renombrado desde "Tests") |
| 🧹 **Working tree** | Limpio, rama `main` sincronizada con `origin/main` |
| 📊 **Producto 1 (MVP)** | ~85% |
| 🌍 **Ecosistema completo** | ~17% (1 de 6 productos completos, 6 definidos) |
| 🔗 **Repo** | github.com/icqdgonzalezs/industrial-kpi-intelligence |
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
- ✅ **Doc** (`c2ab9ed` + `f3eb79c` + `5be2e6b`): README actualizado, workflow renombrado a `CI`, VISION.md, ARCHITECTURE.md
- ✅ **Repo hygiene** (`e58151b`): docs movidos a `docs/`, basura eliminada, .gitignore completado
- ✅ **Fase 3a-α** (`35d12c4`): Export CSV — piloto Capacidad (patrón original con `store-capacidad`)
- ✅ **Fase 3a-β** (`7e744e8`): Export CSV — Calidad (variante sin store, recomputa Pareto)
- ✅ **Fase 3a-γ** (`b0082ff`): Export CSV — Control (variante sin store, tabla I+MR unificada)
- ✅ **Fase 3a-δ** (`ae7a54b`): Export CSV — Diagnóstico (variante sin store, tabla de hallazgos)
- ✅ **Fase 3a-ε** (`c9a2efb`): Export CSV — Operacional (variante sin store, ranking por dimensión)
- ✅ **Fix bug Pareto** (`e0d50f2`): anotación "Umbral 80%" ya no colisiona con tick del eje secundario
- ✅ **Fix "Restaurar filtros"** (`2fe8e89`): callback implementado (antes era botón decorativo sin handler)
- ✅ **Chore dev** (`8ca225d`): `dev_tools_ui=True` para desarrollo local
- ✅ **Perf parseo JSON** (`6efd967`): `lru_cache` reduce reset de filtros de ~10 s a ~4-6 s

### 🟡 En curso

> **Nada.** Sesión cerrada. Working tree limpio.

### ⏳ Pendiente (roadmap en sección 7)

- ⏳ **Eliminar `schema_adapter.py`** (deuda activa, condición de muerte cumplida) **(PRÓXIMO PASO RECOMENDADO)**
- ⏳ **Fase 3b** — Loading + empty states + optimización cálculos (KDE, webgl cartas control)
- ⏳ **Fase 3c** — Chip de filtros activos
- ⏳ **Bloque 3B** — Docker + Compose
- ⏳ **Rename bilingüe** (ADR-0002, incremental)

---

## 3️⃣ LÍNEA TEMPORAL DE COMMITS

| Commit | Descripción | Tests |
|---|---|---|
| `c9a2efb` | Feat(export): CSV export Operacional (Fase 3a-ε) | 434 |
| `ae7a54b` | Feat(export): CSV export Diagnóstico (Fase 3a-δ) | 429 |
| `b0082ff` | Feat(export): CSV export Control (Fase 3a-γ) | 423 |
| `6efd967` | Perf(utils): cache JSON parse (Fase 3b anticipada) | 416 |
| `c0f2977` | Docs(handoff): update TRASPASO after Fase 3a-beta + perf fixes | 416 |
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
| `b78d1ce` | Docs: VISION.md (renombre 06→00) — superseded | 390 |
| `1ab8246` | Docs: VISION.md (truncado) — superseded | 390 |
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

📈 **Evolución de tests:** `263` → `270` → `274` → `279` → `284` → `290` → `295` → `316` → `335` → `343` → `359` → `390` → `408` → `411` → `414` → `416` → `423` → `429` → **`434`**

---

## 4️⃣ DECISIONES TÉCNICAS CLAVE

### 4.1 🔄 Patrón strangler para migración EN→ES

- **Solución:** `src/schema_adapter.py` traduce EN→ES.
- **Estado:** deuda activa (ver ADR-0001). Condición de muerte cumplida. **Próximo paso recomendado.**

### 4.2 🗃️ SSOT en YAML para umbrales

- **Solución:** externalizar a `config/quality_config.yaml`.
- **Secciones activas:** `kpi_thresholds`, `ppk_thresholds`, `ppm_thresholds`, `variables_criticas`, `variables[]`.

### 4.3 📈 SPC contextualizado (Regla 1 con falsos positivos)

- **Solución:** `resumen_control_estadistico()` calcula esperados = n × 0.0027.
- **Lección:** en SPC con muestras grandes, siempre observados vs esperados.

### 4.4 🏭 Rendimiento vs Capacidad (Fix #4)

- **Solución:** 4 KPIs nuevos: % dentro, % bajo LSL, % sobre USL, PPM total.
- **Hallazgo:** Peso PPM=55 (✓ verde) vs Longitud PPM=221 (⚠ ámbar), ambos con Ppk=1.33.
- **Lección:** Ppk solo oculta diferencias de rendimiento real.

### 4.5 🖥️ ISA-101 para HMI industrial

- **Solución:** labels 16px bold blanco fuera del plot, líneas grises dashed 1.8px.
- **Lección:** datos medidos y referencias calculadas ocupan canales visuales distintos.

### 4.6 🎯 Escala AIAG SPC para clasificación Ppk (Fix #7)

Escala de 4 niveles: `Ppk ≥ 1.67` → Clase mundial · `1.33 ≤ Ppk < 1.67` → Capaz · `1.00 ≤ Ppk < 1.33` → Marginal · `Ppk < 1.00` → No capaz.

### 4.7 🏷️ SSOT de labels visibles (Fix #5.6)

- **Solución:** `LABELS_EJES_DIMENSION = {value: label}` derivado de `DIMENSIONES_DISPONIBLES`.
- **Lección:** cada string visible al usuario debe venir de un único lugar.

### 4.8 ♿ Iconografía no cromática en semáforos (Fase 4a — WCAG 2.1 §1.4.1)

- **Solución:** SSOT `dashboard/severity_icons.py` con `prefijar_icono()`.
- **Lección:** la accesibilidad no es "nice to have". Es funcionalidad industrial.

### 4.9 🎯 Migración de umbrales Ppk + PPM a YAML SSOT (Fase σ)

- **Problema:** umbrales Ppk y PPM hardcodeados en `src/capability.py`, más una sección YAML muerta que los contradecía.
- **Solución:** nuevo módulo `src/capability_thresholds.py` (clasificación pura + loaders cacheados). YAML unificado.
- **API pública intacta:** `clasificar_ppk(ppk)` sigue con firma previa (umbrales opcionales con default = leer del YAML).
- **Lección:** un YAML que no se lee es peor que no tener YAML. Da falsa ilusión de configurabilidad.
- **Tests:** 359 → 390 (+31) sin modificar tests existentes.

### 4.10 📥 Patrón de Export CSV (Fase 3a — piloto Capacidad)

- **Problema:** los datos de cada tab no se podían exportar. El usuario debía copiar de la pantalla.
- **Solución:** módulo SSOT `dashboard/export_helpers.py` con:
  - `nombre_csv(tab)`: genera nombre con timestamp.
  - `boton_export(tab)`: botón estándar con ID uniforme.
  - `crear_descarga_csv(json_data, tab)`: función pura (testeable).
- **Patrón replicable:** cada tab necesita 3 cambios (component + callback + tests).
- **Lección:** el primer caso define el patrón. Los siguientes son su aplicación.

### 4.11 📥 Variante del patrón Export CSV (Fase 3a-β a 3a-ε)

- **Contexto:** 4 de los 5 tabs (Calidad, Control, Diagnóstico, Operacional) **no tienen `store-<tab>` propio**.
- **Variante adoptada:** el callback de export lee de `store-datos-filtrados` (y `store-capacidad` para Diagnóstico) y **recomputa** el análisis en el momento (cálculo trivial).
- **Por qué no crear stores artificiales:** solo existirían para servir al export. Sería estado mantenido por callbacks de display que ya tienen muchos outputs.
- **Lección de ingeniería:** un Store que existe solo para alimentar a un consumidor puede reemplazarse por una función pura del estado ya disponible. *Derive, don't store*.
- **Regla derivada:** si el tab tiene store propio → patrón original del piloto. Si no → variante con `store-datos-filtrados` + recomputo.
- **Resultado:** 5/5 tabs cerrados. 4 con variante, 1 (Capacidad) con patrón original.

### 4.12 📥 Decisiones de formato por tab (Fase 3a)

| Tab | Formato del CSV | Razón |
|---|---|---|
| **Capacidad** | Tabla Pp/Ppk completa | Salida analítica natural (ya calculada en `store-capacidad`) |
| **Calidad** | Pareto de defectos | Concentración de causas — análisis clásico del Quality Manager |
| **Control** | Tabla I + MR unificada con límites constantes | Un solo CSV autocontenido. MR alineado con `None` en el primer punto. |
| **Diagnóstico** | Tabla de hallazgos (severidad, categoria, titulo, mensaje, score) | Salida del motor de reglas. Orden por score heredado. |
| **Operacional** | Ranking por dimensión (no el drill-down) | Ranking es determinístico, drill-down es efímero. *Exportá el dato, no la vista*. |

**Regla general derivada:** cada tab exporta su **salida analítica natural**. Ni más ni menos.

### 4.13 🔧 Implementación de "Restaurar filtros" (Fase 3a — bug fix)

- **Problema:** el botón existía en el layout (`components_dash.py:101`) pero nunca tuvo callback. Era decorativo.
- **Diagnóstico:** 4 puntos de fallo posibles (layout, registro, callback, lógica). Se resolvió con `grep` sistemático, no por especulación.
- **Solución:**
  - Función pura `valores_default_filtros(fecha_min, fecha_max)`: retorna tupla de 6 valores.
  - Callback reset que escribe los 6 Outputs con `allow_duplicate=True` + `prevent_initial_call=True`.
  - **`allow_duplicate=True`** requerido en el reset y en los 4 callbacks de cascade (Dash 2.9+ prohíbe dos callbacks escribiendo el mismo Output sin este flag).
  - **`prevent_initial_call=True`** en los 4 cascades: evitan que se disparen al montar la app.
- **Lección:** en Dash, un botón sin callback **no falla silenciosamente** — simplemente no hace nada. Es un modo de fallo traicionero que requiere verificación visual.
- **Nota sobre import:** `PreventUpdate` vive en `dash.exceptions`, no en `dash` raíz.

### 4.14 ⚡ Caché de parseo JSON (Fase 3b anticipada)

- **Problema:** los ~10 callbacks consumidores de `store-datos-filtrados` deserializaban el mismo JSON (18,078 filas) en cada cambio de filtro.
- **Medición con `print` temporal:** 10 parseos × ~650 ms promedio = **~6.5 s de los 10 s totales**.
- **Solución:** `@lru_cache(maxsize=2)` sobre `_parse_json_cached(json_data)` en `dashboard/utils.py`.
  - Primer consumidor parsea (~650 ms).
  - Resto recibe cache hit (~5-15 ms) + copia defensiva `.copy()`.
- **Decisiones clave:**
  - **`maxsize=2`, no 128:** mantiene el JSON actual + el previo. Memoria acotada (~60 MB), sin crecer con el tiempo. Un maxsize grande sería un memory leak silencioso en producción.
  - **`.copy()` defensivo:** el DataFrame cacheado es compartido entre los 10 callbacks. Si uno lo muta, los otros 9 verían la mutación. La copia cuesta ~10 ms (despreciable vs 500 ms de parseo).
- **Ganancia medida:** reset de filtros de ~10 s → ~4-6 s. **-50%**.
- **Lección:** la causa raíz era **arquitectónica** (10 consumidores del mismo JSON), no algorítmica (los cálculos de Pp/Ppk están bien).
- **Deuda residual:** los 10 callbacks **siguen ejecutándose**. El parseo ya no cuesta, pero los cálculos individuales (KDE en capability, reglas en diagnostics) son la siguiente capa (~1-2 s + ~1-1.5 s respectivamente). Diferido a Fase 3b o Fase 5.

---

## 5️⃣ ESTADO DE TESTS Y CALIDAD

| Archivo | Tests | Cobertura conceptual |
|---|:---:|---|
| `test_capability.py` | 40 | Pp/Ppk + clasificar_ppk + rendimiento spec + inyección SSOT |
| `test_capability_callbacks.py` | 22 | Callbacks + `_estado_capacidad` + iconos + export CSV |
| `test_capability_thresholds.py` | 28 | SSOT: clasificación pura + loaders |
| `test_control_charts.py` | 10 | I-MR + Western Electric |
| `test_control_charts_callbacks.py` | 9 | Wiring + figuras + export CSV Control |
| `test_dash_app.py` | 11 | Callbacks top + filtros |
| `test_data_generator.py` | 15 | Generador determinista seed=42 |
| `test_data_loader.py` | 13 | Adapter + manejo de errores |
| `test_dataset_metadata.py` | 21 | Frescura del dataset |
| `test_diagnostics.py` / `_callbacks` | 13 + 11 | Findings + Pareto + export CSV Diagnóstico |
| `test_export_helpers.py` | 16 | nombre_csv + boton_export + crear_descarga_csv |
| `test_filter_callbacks.py` | 3 | `valores_default_filtros` + smoke de registro (reset) |
| `test_filter_engine.py` | 11 | Filtrado por línea/equipo/turno/operador |
| `test_kpi_callbacks.py` | 4 | `_span_kpi` con iconos |
| `test_kpi_presenter.py` | 4 | Formateo + clasificación |
| `test_kpi_thresholds.py` | 19 | Función pura + refactor SSOT |
| `test_kpis.py` | 32 | FPY, defectos, scrap, reproceso |
| `test_oee.py` / `_presenter` | 25 + 6 | OEE (A×P×Q) ISA-95 |
| `test_operational_analysis_callbacks.py` | 35 | Drill-down + `_label_dimension` + export CSV Operacional |
| `test_plant_overview.py` / `_components` | 6 + 5 | Vista de planta |
| `test_quality_performance_callbacks.py` | 13 | FPY, Pareto + export CSV Calidad |
| `test_quality_performance_components.py` | 7 | Componentes UI |
| `test_quality_performance_spec.py` | 6 | Especificación |
| `test_schema_adapter.py` | 11 | Adapter EN→ES (se elimina con el adapter) |
| `test_severity_icons.py` | 9 | `prefijar_icono` + SSOT iconos |
| `test_utils.py` | 7 | Tema oscuro + cache de parseo JSON |
| `test_validation.py` | 22 | Validación de contratos |
| **TOTAL** | **434** | ✅ Todos verdes |

---

## 6️⃣ DEUDA TÉCNICA CONOCIDA

| # | Deuda | Impacto | Prioridad |
|:---:|---|---|:---:|
| 1 | ~~README dice "263 passing"~~ | — | ✅ Resuelta |
| 2 | ~~Capacidad: dos verdades no explicadas~~ | — | ✅ Resuelta (Fix #7) |
| 3 | ~~Sin timestamp de datos en header~~ | — | ✅ Resuelta (Fix #6) |
| 4 | ~~Barras verticales con 17 labels ilegibles~~ | — | ✅ Resuelta (Fix #5) |
| 5 | ~~Export CSV por tab (5/5 completados ✅)~~ | — | ✅ Resuelta (Fase 3a) |
| 6 | Sin loading / empty states | Robustez | 🟡 Media |
| 7 | ~~Sin iconografía en semáforos (solo color)~~ | — | ✅ Resuelta (Fase 4a) |
| 8 | Docker + Compose pendiente | Deploy | 🟠 Media |
| 9 | ~~Umbrales Ppk hardcodeados~~ | — | ✅ Resuelta (Fase σ) |
| 10 | ~~Falta VISION.md y ARCHITECTURE.md~~ | — | ✅ Resuelta (Doc) |
| 11 | **`schema_adapter.py`** (adapter transitorio) | Deuda activa | 🔴 **Alta** |
| 12 | **Doble convención bilingüe** (ADR-0002) | Mantenibilidad | 🟡 Media |
| 13 | **Performance: cálculos individuales por callback** | UX | 🟠 Media |
| 14 | **Control: render cartas I-MR con SVG sobre 18k puntos** | UX | 🟢 Baja |

**Deuda 13 — Performance residual:**

- ✅ **Resuelto:** parseo redundante JSON cacheado con `lru_cache` (-50% tiempo total, de 10 s a 4-6 s).
- ⏳ **Residual:** los ~10 callbacks siguen ejecutándose. Costo estimado: KDE en `capability` (~1-2 s), reglas en `diagnostics` (~1-1.5 s), resto distribuido.
- **Fix candidato:** cache por variable en `capability`, vectorización de `diagnostics`.
- **Diferido a:** Fase 3b (junto a loading/empty states).

**Deuda 14 — Control rendering:**

- ⏳ `dcc.Graph` renderiza ~18k puntos por SVG en cartas I y MR.
- **Fix candidato:** `render_mode="webgl"` (~10-100× más rápido). Impacto UX en hover/export estático. Evaluar en Fase 3b.

---

## 7️⃣ ROADMAP PENDIENTE

| Fase | Fix/Feature | Estimación | Prioridad |
|:---:|---|:---:|:---:|
| **σ** | **Eliminar `schema_adapter.py`** (deuda activa, ADR-0001) **(PRÓXIMO PASO RECOMENDADO)** | 1 h | 🔴 **Alta** |
| 3b | Loading + empty states + optimización cálculos (KDE, diagnostics) + webgl cartas | 4 h | 🟡 Media |
| 3c | Chip de filtros activos | 1 h | 🟢 Baja |
| σ | Rename bilingüe incremental (ADR-0002) | Semanas 5-6 | 🟡 Media |
| 5 | Docker + Compose (Bloque 3B) | 2 h | 🟠 Media |

---

## 8️⃣ REGLAS OPERATIVAS NO NEGOCIABLES

### 💻 Terminal (protocolo de arranque)

**SIEMPRE al abrir terminal nueva:**

```bash
cd /Users/violeta/Projects/industrial-operations-intelligence/industrial-kpi-intelligence
source venv/bin/activate
which python   # DEBE mostrar .../venv/bin/python
```

> ⚠️ Si `which python` no muestra la ruta del venv, los comandos fallarán con `ModuleNotFoundError: No module named 'dash'` o `ruff: command not found`. Verificar antes de correr gates.

### 🐙 Git

| ✅ Correcto | ❌ Incorrecto |
|---|---|
| `git checkout` para descartar cambios. | Nunca `git switch` ni `git restore`. |
| `git push --force-with-lease` si es necesario. | Nunca `git push --force`. |
| Personal Access Token (PAT) con scope `repo` + `workflow`. | Nunca password en texto plano. |
| `git pull origin main --rebase` tras Web Editor. | Nunca `git pull` sin `--rebase` si editaste fuera. |
| `git reset --soft HEAD~1` para reescribir el último commit. | Nunca `git rebase -i` si no estás cómodo con Vim. |

### ✍️ Commits

- Conventional Commits: `feat:`, `fix:`, `refactor:`, `docs:`, `style:`, `test:`, `chore:`, `polish:`, `perf:`.
- Un fix = un commit. No mezclar propósitos.
- Título en inglés, cuerpo en español si aplica.
- **Verificar el mensaje antes de commitear. No copiar/pegar el mensaje de otro commit.**

### 🤖 CI/CD

- 2/2 checks verdes antes de mergear. Sin excepción.
- Cualquier push dispara el workflow CI (~50 s).

### 🎨 UX / CSS

- Ver el archivo antes de tocar.
- Verificación visual con `⌘ + Shift + R` obligatoria.
- **Regla C.1:** sin números no hay cierre.

### 💾 Código

- Idioma del código: inglés. Docstrings y comentarios: español.
- Arquitectura: `src/` (lógica) / `dashboard/` (presentación) / `tests/`.
- Nomenclatura: capacidad `world_class` / `capable` / `marginal` / `not_capable`. Severidad `success` / `warning` / `danger` / `neutral`.

### 🛠️ Protocolo de cada fix

1. Leer los archivos involucrados (`grep` + `cat`).
2. Diagnosticar causa raíz.
3. `grep -rn "string_viejo" src/ dashboard/ tests/`.
4. Código + tests juntos.
5. `pytest` + `ruff check .`.
6. Verificación visual con `⌘ + Shift + R`.
7. `git status` antes del add.
8. `git add` con paths textuales.
9. `git status` post-add.
10. Commit con mensaje conventional.
11. Push y verificar CI verde.

---

## 9️⃣ ⚠️ HISTORIAL DE ERRORES — NO REPETIR

| ❌ Error | ✅ Correcto |
|---|---|
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
| `git push` sin `fetch` previo | `git fetch origin` antes |
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
| Untracked file bloquea `git pull` | `rm` del archivo local, luego pull |
| Editar en Web Editor y olvidar `git pull --rebase` | Pull con `--rebase` antes del próximo comando local |
| Documentación con "próximo paso" desincronizado | `grep -n "próximo paso"` y actualizar TODAS las ubicaciones |
| Asumir contrato de terceros sin verificar (`dcc.send_data_frame`) | Ver tests del piloto antes de inventar contrato. Usar `in`, no `==`, para keys de librerías |
| Importar `PreventUpdate` desde `dash` | Importar desde `dash.exceptions` |
| Copiar/pegar mensaje de commit de otro commit | Verificar el mensaje antes del commit; cada commit describe su propio contenido |
| `git rebase HEAD~N` sin `-i` | Sin `-i` no abre editor: no reescribe nada. Usar `-i` o preferir `git reset --soft` |
| Leer SHA de una captura de pantalla | Copiar SHAs de la terminal, no de screenshots (confusión f/1, l/I) |
| Asumir que la extensión "Dash Dev Tools" está instalada | En Dash 4.x sin extensión, el panel es un botón flotante en la esquina inferior derecha de la app |
| Buscar el panel Dash en Chrome DevTools (F12) | No está ahí. Está dentro de la app misma |
| Optimizar sin medir | Instrumentar con `print` temporales o panel flotante, medir antes de tocar |
| Correr pytest/ruff sin venv activo | `ModuleNotFoundError: No module named 'dash'` / `ruff: command not found`. Verificar `which python` primero. |
| Asumir que `dcc.send_data_frame` devuelve base64 | En Dash 4.x, `content` es bytes del CSV crudo. Decodificar directo con `isinstance(contenido, bytes)`. |
| Asumir nombre de función de otro módulo sin ver | `from src.data_generator import generar_dataset` falló porque la función se llama distinto. Usar `monkeypatch` para desacoplar tests de dependencias externas. |

---

## 🔟 📁 ARCHIVOS CLAVE Y COMANDOS

### 🗂️ Estructura del proyecto

```text
industrial-kpi-intelligence/
├── ARCHITECTURE.md                        # Arquitectura técnica (313 líneas)
├── README.md                              # Actualizado: 434 tests + badges
├── VISION.md                              # Visión del ecosistema (188 líneas)
├── CHANGELOG.md
├── LICENSE                                # Elastic License 2.0
├── pyproject.toml                         # Config pytest + ruff
├── requirements.txt
├── Procfile / render.yaml                 # Deploy Render
├── .gitignore
├── .github/workflows/tests.yml            # Workflow "CI"
├── assets/                                # CSS tema oscuro
│   └── style.css
├── config/                                # YAMLs (SSOT)
│   ├── generator_config.yaml
│   ├── plant_config.yaml
│   └── quality_config.yaml
├── dashboard/                             # Presentación
│   ├── export_helpers.py                  # SSOT export CSV (Fase 3a)
│   ├── severity_icons.py                  # SSOT iconos (Fase 4a)
│   ├── filter_callbacks.py                # +valores_default_filtros + reset callback
│   ├── utils.py                           # +lru_cache en _parse_json_cached
│   ├── capability_components.py           # +botón export
│   ├── capability_callbacks.py            # +callback export
│   ├── quality_performance_components.py  # +botón export
│   ├── quality_performance_callbacks.py   # +exportar_pareto_calidad
│   ├── control_charts_components.py       # +botón export
│   ├── control_charts_callbacks.py        # +exportar_control_csv
│   ├── diagnostics_components.py          # +botón export
│   ├── diagnostics_callbacks.py           # +exportar_diagnostico_csv
│   ├── operational_analysis_components.py # +botón export
│   ├── operational_analysis_callbacks.py  # +exportar_operacional_csv
│   └── ...
├── data/                                  # Dataset canónico
├── docs/                                  # Documentación extendida
│   ├── adr/                               # ADR-0001, ADR-0002
│   ├── learning-journal/
│   ├── nist_references/
│   ├── industrial-kpi-intelligence-master-plan.md
│   ├── TECHNICAL_DOCUMENTATION.md
│   └── TRASPASO_MAESTRO.md                # Este archivo
├── imagenes/
├── scripts/
├── src/                                   # Lógica de negocio
│   ├── capability.py
│   ├── capability_thresholds.py
│   ├── control_charts.py
│   ├── data_generator.py
│   ├── dataset_metadata.py
│   ├── diagnostics.py
│   ├── kpi_thresholds.py
│   ├── kpis.py
│   ├── oee.py
│   ├── schema_adapter.py                  # ⚠️ Deuda activa (eliminar)
│   └── validation.py
└── tests/                                 # 434 tests
    ├── test_control_charts_callbacks.py
    ├── test_diagnostics_callbacks.py
    ├── test_operational_analysis_callbacks.py
    ├── test_quality_performance_callbacks.py
    ├── test_filter_callbacks.py
    ├── test_utils.py
    └── ...
```

### ⌨️ Comandos verificados

```bash
# Protocolo de arranque (SIEMPRE)
cd /Users/violeta/Projects/industrial-operations-intelligence/industrial-kpi-intelligence
source venv/bin/activate
which python                    # DEBE mostrar .../venv/bin/python

# Gates
pytest                          # 434 passed
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

# Reescribir último commit sin abrir editor
git reset --soft HEAD~1
git commit -F - <<'EOF'
nuevo mensaje
EOF
git push --force-with-lease origin main

# Crear archivos largos: USAR GITHUB WEB EDITOR
# https://github.com/<user>/<repo>/edit/main/<archivo>
```

---

## 1️⃣1️⃣ 🎯 PRÓXIMO PASO EXACTO

### Fase 3a completa ✅ — decidir próximo frente

Los 5 tabs exportan CSV. Los 4 pendientes del roadmap original están acá:

| Opción | Qué es | Estimación | Riesgo | Recomendación |
|:---:|---|:---:|:---:|:---:|
| **A** | Eliminar `schema_adapter.py` (deuda activa 🔴 Alta) | 1 h | Bajo | ✅ Recomendada |
| **B** | Fase 3b — Loading + empty states + perf (KDE, webgl) | 4 h | Medio | 🟡 |
| **C** | Fase 3c — Chip de filtros activos | 1 h | Bajo | 🟢 |

**Por qué A:**

1. Condición de muerte cumplida hace semanas (ADR-0001).
2. 11 tests se liberan (`test_schema_adapter.py`).
3. Menos código = menos superficie de bug.
4. Cierra una deuda activa (no solo "pendiente").
5. Antes de agregar features nuevas (Fase 3b), limpiar la base.
6. Es 1 h vs 4 h de Fase 3b.

**Cierre esperado de opción A:**

- 0 referencias a `schema_adapter` en `src/`, `dashboard/`, `tests/`.
- `tests/test_schema_adapter.py` eliminado.
- Tests bajan de 434 → ~423 (11 eliminados).
- README/ARCHITECTURE actualizados si mencionan el adapter.
- ADR-0001 marcado como "cumplido".

---

## 1️⃣2️⃣ 💬 MENSAJE DE TRANSICIÓN (para pegar en chat nuevo)

```text
Contexto: pego abajo el TRASPASO_MAESTRO del proyecto Industrial KPI Intelligence.
Soy David, Ing. Civil Químico + dev autodidacta, semana 3/8 del Producto 01.

Estado: Fase 4a + σ + Doc + Fase 3a COMPLETA (5/5 tabs con export CSV) + fixes UX/perf cerrados.
434 tests, CI verde, working tree limpio.
Próximo paso: decidir entre schema_adapter (recomendado) / Fase 3b / Fase 3c.

Reglas clave:
- Protocolo de arranque: cd + source venv/bin/activate + verificar `which python`
- Leer el archivo antes de tocar
- git status antes de cada git add
- Un fix = un commit
- Verificación visual con ⌘ + Shift + R obligatoria
- pytest + ruff verdes antes de commitear
- NO usar TextEdit para markdown: usar GitHub Web Editor
- Tras editar en Web Editor, hacer git pull --rebase
- Antes de optimizar: medir con instrumentación temporal
- Los `print` de instrumentación NUNCA se commitean

Actuá como ingeniero de software senior + mentor. Directo, técnico,
sin relleno. Español. Markdown con tablas y bloques de código.

[PEGAR TODO EL CONTENIDO DE TRASPASO_MAESTRO.md ABAJO]
```

---

## 1️⃣3️⃣ 🎓 NOTAS DE MENTOR (para el próximo asistente)

Este usuario no es un junior. Es un ingeniero químico con criterio técnico real. Ha demostrado en estas sesiones:

- 🔍 Detectar bugs por inspección visual (anotación sobrepuesta, botón decorativo).
- 📊 Pedir diagnóstico con datos cuando CI falla, no con fe.
- 🔄 Aceptar reversiones cuando una decisión no funciona.
- 🎯 Mantener disciplina en cada fix (un fix = un commit, verificación visual, gates verdes).
- ⚖️ Decidir con criterio cuándo parar (no persistir con herramientas que no aparecen; medir antes de optimizar).
- 📏 Instrumentar para medir (los `print` de performance dieron el dato clave).
- 📝 Documentar a medida que avanza.

### 🎯 Cómo tratarlo

- Como colega senior, no como aprendiz.
- Explicá el por qué de las decisiones técnicas, no solo el cómo.
- Citá normas industriales cuando aplique (ISA-101, AIAG SPC, NIST 6.1.3, WCAG 2.1).
- Valorá la honestidad por sobre la complacencia.
- No quiere halagos, quiere producto de calidad.
- Cuando te equivoques (ej. leer mal un SHA, asumir nombre de función), decilo claro y corregí. No eches la culpa ni inventes excusas.

### 🏆 Hito alcanzado en esta sesión

**Fase 3a completa (5/5 tabs con export CSV).** Se aplicó el patrón del piloto a 4 tabs más, con 2 variantes identificadas (con/sin store propio) y 3 decisiones de diseño específicas por tab (formato del CSV). Cada tab con tests dedicados, verificación visual, y CI verde. 434 tests, 0 regresiones, working tree limpio.

---

> 📌 **Fin del TRASPASO_MAESTRO.**
> Última actualización: Fase 4a + σ + Doc + Fase 3a completa + fixes UX/perf.
> Próximo paso: decidir entre schema_adapter (recomendado) / Fase 3b / Fase 3c.
