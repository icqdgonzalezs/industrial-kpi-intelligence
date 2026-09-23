# 🎯 TRASPASO MAESTRO — Industrial KPI Intelligence

> 📌 **Propósito:** documento autocontenido para arrancar un chat nuevo sin perder contexto.  
> 📥 **Instrucción de uso:** pegar este archivo completo como **PRIMER** mensaje en un chat nuevo.  
> 🗓️ **Última actualización:** Ciclo #21 + #22 cerrado (dashboard Jinja2 + tests para `app/`). Commit `0c59acc` pusheado. **477 tests verdes, CI 2/2 verde verificado (run #112).**  
> 🚀 **Próximo paso:** Fase IA — chat con KPIs (RAG + LLM). Ver sección 11.

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
| 11 | 🔍 **Ningún push sin verificar el run CI anterior.** El "verde" del TRASPASO es foto histórica, no estado vivo. |

> 🚀 **Próximo paso concreto del proyecto:** Fase IA.1 — chat con KPIs (RAG + LLM, proveedor Groq). Ver sección 11.

---

## 1️⃣ FICHA DEL PROYECTO

| Campo | Valor |
| :--- | :--- |
| 🏭 **Producto** | Industrial KPI Intelligence — dashboard industrial para PYMES manufactureras LatAm/España |
| 🌐 **Ecosistema** | Primer producto de 6 SaaS (Industrial Operations Intelligence) |
| 🛠️ **Stack legacy (dashboard)** | Python 3.11.9 · Plotly Dash 4.4.1 · Plotly · pandas · numpy |
| 🛠️ **Stack nuevo (API REST)** | FastAPI 0.141.1 · SQLModel 0.0.46 · SQLAlchemy 2.0.54 · Pydantic 2.13.5 · SQLite · Jinja2 3.1.6 · Uvicorn 0.53.0 |
| 🛠️ **Stack IA (próximo)** | Groq API (Llama 3.3 70B) · SDK OpenAI-compatible · python-dotenv |
| 🧪 **Testing** | pytest 9.1.1 · pytest-cov 7.1.0 · ruff 0.16.6 · httpx2 2.13.1 · GitHub Actions CI/CD |
| 📏 **Estándares aplicables** | ISA-95 · TPM (OEE) · NIST 6.1.3 / ISO 22514 (Pp/Ppk) · AIAG SPC · OWASP · ISA-101 (HMI) · WCAG 2.1 · OpenAPI 3.1 |
| ⚖️ **Licencia** | Elastic License 2.0 (nunca MIT) |
| 👤 **Usuario** | David González Santibáñez — Ing. Civil Químico + dev autodidacta |
| 📅 **Semana** | 3 de 8 |
| ✅ **Tests actuales** | **477 passed** (460 legacy + 17 app/) |
| 🟢 **CI** | 2/2 verde **verificado** (run #112, commit `0c59acc`) |
| 🧹 **Working tree** | Limpio, rama `main` sincronizada con `origin/main`. HEAD: `0c59acc`. |
| 📊 **Producto 1 (MVP)** | ~92% (dashboard Dash) + capa API al 90% (dashboard Jinja2 + tests OK). **Migración completa Dash → FastAPI en curso.** |
| 🌍 **Ecosistema completo** | ~17% (1 de 6 productos completos, 6 definidos) |
| 🔗 **Repo** | `github.com/icqdgonzalezs/industrial-kpi-intelligence` |
| 📂 **Ruta local** | `/Users/violeta/Projects/industrial-operations-intelligence/industrial-kpi-intelligence` |

---

## 2️⃣ ESTADO ACTUAL EXACTO

### ✅ Cerrado (commiteado + pusheado + CI verde)

**Dashboard Dash legacy (Fase 3b.2 completa):**

- ✅ Bloques UX-1, UX-2, UX-3 (base visual del dashboard)
- ✅ Bloque 3A: adapter EN→ES + loader rewired a dataset canónico (18,078 filas)
- ✅ Fix σ del generador (σ=2.0 / 0.63)
- ✅ Fix SPC: Regla 1 contextualizada con falsos positivos esperados
- ✅ Refactor thresholds a YAML (SSOT)
- ✅ Fix σ minúscula (σ vs Σ)
- ✅ Fix labels del histograma
- ✅ Fix tipografía ISA-101
- ✅ Fix color de líneas
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
- ✅ **Fase 3a** (`35d12c4` a `c9a2efb`): Export CSV — 5/5 tabs
- ✅ **Fix bug Pareto** (`e0d50f2`)
- ✅ **Fix "Restaurar filtros"** (`2fe8e89`)
- ✅ **Chore dev** (`8ca225d`): `dev_tools_ui=True`
- ✅ **Perf cache JSON** (`6efd967`): `lru_cache`
- ✅ **Opción D** (`ba0e962`): consolidar `schema_adapter.py` dentro de `data_loader.py`
- ✅ **Fase 3b.1** (`c91ae39`): loading states
- ✅ **Perf pre-binning** (`ce2c03f`): histograma Capacidad
- ✅ **Perf WebGL Control** (`e7e5d49`): `go.Scattergl`
- ✅ **Componente empty_state** (`6a0547e`)
- ✅ **Piloto Calidad** (`529d83f`)
- ✅ **Fix doble spinner Capacidad** (`b9514ed`)
- ✅ **Fase 3b.2 Control + cascades** (`d5542e2` + `22988f4`)
- ✅ **.Rapp.history gitignored** (`47e3bd9`)
- ✅ **Fase 3b.2 Capacidad** (`722297f`)
- ✅ **Fix test Capacidad** (`4516129`)
- ✅ **Fase 3b.2 Diagnóstico** (`d23af82`)
- ✅ **Fase 3b.2 Operacional** (`9c780d8`)

**Capa API REST (migración CSV → FastAPI):**

- ✅ **Doc README** (`85dd7fe` — Web Editor): badges separados (Dash legacy + FastAPI nuevo).
- ✅ **Migración CSV → FastAPI + SQLModel + SQLite** (`a162f15`): 7 archivos, +139/-29.
  - ✅ `app/models.py` — Modelo `KPI` con `sa_column=Column(DateTime(timezone=False))`.
  - ✅ `app/schemas.py` — Schema `KPICreate` (BaseModel puro, separación DB ↔ API).
  - ✅ `app/db.py` — SQLite + `create_db_and_tables()` + `get_session()`.
  - ✅ `app/main.py` — FastAPI con `lifespan`, `GET /kpis/` y `POST /kpis/`.
  - ✅ `migrate_csv.py` — Script de migración CSV → SQLite.
  - ✅ `requirements.txt` — limpieza inicial.
  - ✅ `.gitignore` — ampliado.

**Ciclo #21 + #22 (nuevo — este bloque):**

- ✅ **`54ac5ed`** — `chore(gitignore): ignore testing artifacts` (`.coverage`, `htmlcov/`, `.pytest_cache/`).
- ✅ **`785b0c4`** — `fix(ci): restore requirements.txt for both stacks` (job `test` del CI).
- ✅ **`a561fff`** — `fix(lint): resolve ruff findings in FastAPI layer` (job `lint` + per-file-ignores B008).
- ✅ **`724f4ac`** — `feat(fastapi): add Jinja2 dashboard for KPI visualization` (**deuda #21 cerrada**). `app/templates/index.html` + endpoint `GET /`.
- ✅ **`0c59acc`** — `test(app): add unit + integration tests for FastAPI layer` (**deuda #22 cerrada**). 17 tests con `TestClient` + SQLite en memoria.

### 🟡 En curso

- *Nada.* Working tree limpio. CI #112 verde verificado.

### ⏳ Pendiente inmediato (Fase IA)

- ⏳ **Fase IA.1** — Chat con KPIs (RAG + LLM, Groq). Ver sección 11.
- ⏳ **Deuda #11** — eliminar `schema_adapter.py` legacy.
- ⏳ **Deuda #15** — debounce cascade.
- ⏳ **Deuda #16** — severidad individual en KPIs de rendimiento.
- ⏳ **Deuda #19** — optimizar callback de 2104 ms en Calidad.
- ⏳ **Migración completa Dash → FastAPI** (ver decisión 4.32).

---

## 3️⃣ LÍNEA TEMPORAL DE COMMITS

| Commit | Descripción | Tests |
| :--- | :--- | :---: |
| `0c59acc` | **test(app): add unit + integration tests for FastAPI layer** (7 files, +310/-2) | 477 |
| `724f4ac` | **feat(fastapi): add Jinja2 dashboard for KPI visualization** | 460 |
| `a561fff` | Fix(lint): resolve ruff findings in FastAPI layer | 460 |
| `785b0c4` | Fix(ci): restore requirements.txt for both stacks | 460 |
| `54ac5ed` | Chore(gitignore): ignore testing artifacts | 460 |
| `a162f15` | feat: migrar de CSV a FastAPI + SQLModel + SQLite (7 files, +139/-29) | 460 |
| `85dd7fe` | docs: migrar de CSV a FastAPI + SQLModel + SQLite en README (Web Editor) | 460 |
| `9c780d8` | Feat(ux): add empty state to Operacional (Fase 3b.2) | 460 |
| `d23af82` | Feat(ux): add empty state to Diagnóstico (Fase 3b.2) | 453 |
| `db0bd52` | Docs(handoff): update TRASPASO to Fase 3b.2 partial state | 450 |
| `4516129` | Fix(test): update Capacidad empty state test after message change | 450 |
| `722297f` | Feat(ux): add empty state to Capacidad tab (Fase 3b.2) | 450 |
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

> 📈 **Evolución de tests:** 263 → ... → 450 → 453 → 460 → **477** (460 legacy + 17 app/).  
> ✅ **CI verde real verificado** (run #112). Los runs rojos #107, #108, #109 quedan como histórico.

---

## 4️⃣ DECISIONES TÉCNICAS CLAVE

### 4.1 a 4.24 — Dashboard Dash legacy
*(Sin cambios: patrón strangler ADR-0001, SSOT YAML, SPC contextualizado, ISA-101, escala AIAG SPC, empty_state, cascades, perf cache, WebGL, etc.)*

### 4.25 🚀 Coexistencia Dash legacy + FastAPI nuevo
- **Decisión:** la capa FastAPI se construye **en paralelo**, sin tocar el dashboard Dash existente.
- **Motivo:** el dashboard Dash funciona al 92% del MVP con 460 tests verdes.
- **Estrategia:** `app/` convive con `dashboard/`, `src/`, `tests/`. Migración gradual.
- **Consecuencia:** dos puntos de entrada:
  - `python -m dashboard.dash_app` → Dash (puerto 8050).
  - `uvicorn app.main:app --reload` → FastAPI (puerto 8000).
- **Lección:** patrón *strangler* aplicado a nivel de arquitectura completa.

### 4.26 🧩 Separación modelo DB ↔ schema API
- **Problema:** SQLModel `table=True` no ejecuta validadores de Pydantic.
- **Solución:** `KPI` (tabla) ≠ `KPICreate` (schema Pydantic).
- **Flujo:** endpoint recibe `KPICreate` → convierte con `KPI(**kpi_data.model_dump())` → inserta.
- **Lección:** arquitectura estándar de FastAPI en producción.

### 4.27 ⏰ Tratamiento del `timestamp` naive en SQLModel 0.0.46
- **Problema:** SQLModel exige por defecto `timezone-aware` datetimes.
- **Solución adoptada:** `sa_column=Column(DateTime(timezone=False))`.
- **Lección:** `sa_column` es la vía de escape cuando SQLModel impone un default restrictivo.

### 4.28 🔄 Flujo de trabajo con `git clone` en vez de `git init`
- **Solución:** `git clone` + `cp -R` del trabajo nuevo. Evita merges raros.

### 4.29 🧹 Limpieza del `requirements.txt` post-`pip freeze`
- **Lección:** `pip freeze` es peligroso en entornos sin venv. Escribir dependencias top-level + transitivas críticas a mano.

### 4.30 🔒 .gitignore ampliado
- **Añadido:** `*.db`, `*.sqlite`, `*.sqlite3`, `.env`, `*.log`, `*.alerts`, `kpis.csv`, y (ciclo actual) `.coverage`, `.coverage.*`, `htmlcov/`, `.pytest_cache/`.

### 4.31 🌐 URLs del proyecto
| Servicio | URL | Comando |
| :--- | :--- | :--- |
| Dashboard Dash (legacy) | `http://127.0.0.1:8050` | `python -m dashboard.dash_app` |
| API FastAPI + Swagger UI | `http://127.0.0.1:8000/docs` | `uvicorn app.main:app --reload` |
| Dashboard Jinja2 | `http://127.0.0.1:8000/` | (mismo servidor) |
| OpenAPI JSON | `http://127.0.0.1:8000/openapi.json` | (mismo servidor) |

### 4.32 🎯 Migración completa Dash → FastAPI (decisión estratégica)
- **Decisión:** retirar progresivamente `dashboard/` y consolidar toda la presentación en `app/` (FastAPI + Jinja2 + HTMX + Plotly.js).
- **Motivo:** producto vendible single-stack, código limpio, sin dependencia del framework Dash.
- **Estrategia:** strangler tab por tab. Cada tab migrado reemplaza al equivalente Dash y se elimina el código legacy.
- **Stack elegido:** Jinja2 (server-side render) + HTMX (interactividad sin SPA) + Plotly.js (mismos gráficos que Dash).
- **Timeline:** ~5 semanas (fases 0-10).
- **Riesgo aceptado:** deadline del MVP. Mitigación: fases atómicas, gates por fase.
- **Gate bloqueante:** tests para `app/` (#22) ✅ ya cerrada.

### 4.33 🔗 `httpx2` reemplaza `httpx` (Starlette 1.6.0)
- **Problema:** Starlette 1.6.0 deprecó `httpx` en `TestClient` (`StarletteDeprecationWarning`).
- **Solución:** instalar `httpx2>=2.13,<3`. Starlette lo detecta automáticamente.
- **Lección:** leer los `DeprecationWarning` temprano; migrar antes de que sea bloqueante.

### 4.34 🧪 SQLModel `table=True` NO valida en construcción
- **Problema:** `KPI(nombre=None)` no levanta `ValidationError` (contrato real de SQLModel).
- **Solución:** la validación de entrada es responsabilidad de `KPICreate` (Pydantic `BaseModel`).
- **Consecuencia en tests:** los tests del modelo documentan el contrato real (`test_kpi_no_valida_en_construccion`), no uno imaginario.
- **Lección:** los tests prueban el contrato real del código, no el deseado.

---

## 5️⃣ ESTADO DE TESTS Y CALIDAD

### Tests legacy (460)

| Archivo | Tests | Cobertura conceptual |
| :--- | :---: | :--- |
| `test_app_layout.py` | 4 | Smoke layout + 6 wrappers de `dcc.Loading` |
| `test_capability.py` | 40 | Pp/Ppk + clasificar_ppk + rendimiento spec |
| `test_capability_callbacks.py` | 25 | Callbacks + estado + iconos + export CSV + empty state |
| `test_capability_thresholds.py` | 28 | SSOT: clasificación pura + loaders |
| `test_control_charts.py` | 10 | I-MR + Western Electric |
| `test_control_charts_callbacks.py` | 14 | Wiring + figuras + export CSV + empty state |
| `test_dash_app.py` | 11 | Callbacks top + filtros |
| `test_data_generator.py` | 15 | Generador determinista seed=42 |
| `test_data_loader.py` | 17 | Carga + traducción EN→ES consolidada |
| `test_dataset_metadata.py` | 21 | Frescura del dataset |
| `test_diagnostics.py` | 13 | Reglas de diagnóstico |
| `test_diagnostics_callbacks.py` | 14 | Resumen + export CSV |
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
| `test_operational_analysis_callbacks.py` | 42 | Drill-down + labels + export CSV |
| `test_plant_overview.py` | 6 | Vista de planta |
| `test_plant_overview_components.py` | 5 | Componentes UI |
| `test_quality_performance_callbacks.py` | 15 | FPY, Pareto + export CSV + empty state |
| `test_quality_performance_components.py` | 7 | Componentes UI |
| `test_quality_performance_spec.py` | 6 | Especificación |
| `test_severity_icons.py` | 9 | `prefijar_icono` + SSOT iconos |
| `test_utils.py` | 7 | Tema oscuro + cache de parseo JSON |
| `test_validation.py` | 22 | Validación de contratos |
| **Subtotal legacy** | **460** | ✅ |

### Tests de `app/` (17) — nuevo

| Archivo | Tests | Cobertura conceptual |
| :--- | :---: | :--- |
| `tests/app/test_models.py` | 3 | `KPI` SQLModel: creación, timestamp naive, contrato real (no valida en construcción) |
| `tests/app/test_schemas.py` | 5 | `KPICreate`: parseo ISO, coacción numérica, rechazo inválido |
| `tests/app/test_endpoints.py` | 9 | `GET /`, `GET /kpis/`, `POST /kpis/` con `TestClient` |
| **Subtotal app/** | **17** | ✅ |

### Fixtures críticas (conftest.py)

- `session` → SQLite en memoria (`StaticPool`, `check_same_thread=False`). Aislada por test. **No toca `kpi_database.db`.**
- `client` → `TestClient` con `app.dependency_overrides[get_session]`. Cero contaminación entre tests.

### Total

> **477 tests passed** (460 legacy + 17 app/). **0 regresiones. 0 warnings.**  
> Tiempo: ~60 s suite completa + ~0.20 s tests de `app/` (SQLite en memoria, gratis).

---

## 6️⃣ DEUDA TÉCNICA CONOCIDA

| # | Deuda | Impacto | Prioridad |
| :---: | :--- | :--- | :---: |
| **11** | `schema_adapter.py` (archivo físico pendiente de eliminar) | Arquitectura | 🔴 **Alta** |
| **12** | Doble convención bilingüe (ADR-0002) | Mantenibilidad | 🟡 Media |
| **15** | Doble spinner al cambiar Línea | UX | 🟡 Media |
| **16** | KPIs de rendimiento heredan severidad agregada | UX | 🟡 Media |
| **17** | Dataset sintético homogéneo inter-línea | Validación | 🟢 Baja |
| **19** | Callback de 2104 ms en zona Calidad | Performance | 🟡 Media |
| **20** | Verificación UI de empty states no automatizable | Testing infra | 🟢 Baja |
| ~~**21**~~ | ~~Falta dashboard Jinja2~~ | ✅ **CERRADA** (`724f4ac`) | — |
| ~~**22**~~ | ~~Sin tests para `app/`~~ | ✅ **CERRADA** (`0c59acc`) | — |
| **23** | `kpi_database.db` se migra manualmente (no automatizado en CI) | Automatización | 🟢 Baja |
| **24** | Doble stack de dashboards (Dash 8050 + FastAPI 8000) | Mantenibilidad | 🟡 Media (transitoria) |
| **25 🆕** | Pandas 2.1.4 → 3.x (requirements actualizado a `>=2.1,<3`) | Reproducibilidad | 🟢 Baja |
| **26 🆕** | CI no mide cobertura de `app/` (solo `--cov=src --cov=dashboard`) | Testing infra | 🟡 Media |
| **27 🆕** | Fase IA pendiente (chat con KPIs, RAG, LLM) | **Feature** | 🔴 **Alta (próximo)** |

### 📌 Detalle de deudas activas

**Deuda 11 — Eliminación de `schema_adapter.py`:**
- `grep -rn "schema_adapter" src/ dashboard/ tests/ app/ --include="*.py"` → confirmar que nada lo importa.
- `git rm src/schema_adapter.py` → `pytest` + `ruff check .` → commit `chore(cleanup): remove legacy schema_adapter.py`.

**Deuda 15 — Doble spinner residual:**
- Cascade equipo + reset → 2 fires del store.
- **Fix candidato:** `debounce` 200ms o cascade condicional.

**Deuda 16 — Semántica color KPIs rendimiento:**
- Los 4 KPIs heredan severidad agregada del PPM total.
- **Fix:** severidad individual por KPI (Fase 3c).

**Deuda 19 — Callback de 2104 ms:**
- Detectado en Dash Dev Tools: nodo con timing de **2104 ms** en zona de Calidad.
- **Fix propuesto:** identificar callback exacto, instrumentar, medir, optimizar.

**Deuda 24 — Doble stack de dashboards:**
- Dash legacy (8050) + FastAPI/Jinja2 (8000).
- **Transitoria.** Una vez el dashboard Jinja2 cubra todas las funcionalidades del Dash, se retira el Dash.
- **Estrategia:** strangler a nivel de dashboard, tab por tab. Ver decisión 4.32.

**Deuda 25 🆕 — Pandas 2 → 3:**
- `requirements.txt` fija `pandas>=2.1,<3`. El venv tiene 2.1.4.
- Migrar a pandas 3 es su propio ciclo (rama, validación, commit dedicado). No mezclar con otras features.

**Deuda 26 🆕 — Cobertura de `app/` en CI:**
- El workflow corre `pytest tests/ -v --cov=src --cov=dashboard`. No incluye `--cov=app`.
- **Fix candidato:** agregar `--cov=app` al comando del workflow.

**Deuda 27 🆕 — Fase IA:**
- Endpoint `POST /chat/` con RAG + LLM (Groq). Ver sección 11.

---

## 7️⃣ ROADMAP PENDIENTE

| Fase | Fix / Feature | Estimación | Prioridad |
| :--- | :--- | :---: | :---: |
| **IA.1** | **Chat con KPIs (RAG + LLM, Groq)** | 3-4 h | 🔴 **Alta — PRÓXIMO PASO** |
| IA.2 | Diagnóstico asistido por LLM | 2 h | 🟡 Media |
| IA.3 | Generación de reportes ejecutivos (LLM narra KPIs) | 2 h | 🟡 Media |
| IA.4 | Detección de anomalías ML (Isolation Forest sobre I-MR) | 3 h | 🟡 Media |
| Docker | Dockerfile + docker-compose (Postgres) | 3 h | 🟠 Media |
| Deploy | Railway o Fly.io + dominio | 1 h | 🔴 Alta (portafolio) |
| Seguridad | JWT + rate limit + CORS | 4 h | 🔴 Alta |
| Automatización | APScheduler (ingesta CSV → SQLite cada N min) | 2 h | 🟡 Media |
| Integración | Webhook `POST /webhooks/ingest` + API key | 2 h | 🟡 Media |
| Caso real | 3-5 entrevistas con usuario de planta + video demo | 4 h | 🟡 Media |
| Migración | Tab Diagnóstico (sin gráficos) | 4 h | 🟠 Media |
| Migración | Tab Calidad (Pareto + KPIs) | 6 h | 🟠 Media |
| Migración | Tab Capacidad (histograma + Pp/Ppk) | 8 h | 🟠 Media |
| Migración | Tab Control (I-MR + Western Electric) | 8 h | 🟠 Media |
| Migración | Tab Operacional (ranking + drill-down) | 8 h | 🟠 Media |
| Migración | Eliminar `dashboard/` legacy + ajustar CI | 4 h | 🟠 Media |
| σ legacy | Eliminar `schema_adapter.py` (deuda #11) | 1 h | 🔴 Alta |
| 3b.3 legacy | Deuda #15: debounce cascade | 30 min | 🟡 Media |
| 3c legacy | Deuda #16 (severidad KPIs) + Chip filtros activos | 1.5 h | 🟡 Media |
| perf legacy | Deuda #19: callback 2104 ms Calidad | 1-2 h | 🟡 Media |

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
| `git status` ANTES y DESPUÉS del `git add`. | Asumir que el add agregó todo. |
| 1 fix = 1 commit = 1 lista corta de archivos. | Commit con 6+ archivos mezclando propósitos. |
| **`git clone` en vez de `git init`** cuando ya hay historial remoto. | `git init` + `remote add` + push (puede causar merge raro). |
| **`cp -R` desde backup a clon fresco** tras migraciones grandes. | Trabajar en carpeta `mkdir` sin repo git. |

### ✍️ Commits

- **Conventional Commits:** `feat:`, `fix:`, `refactor:`, `docs:`, `style:`, `test:`, `chore:`, `polish:`, `perf:`.
- **Un fix = un commit.** No mezclar propósitos.
- **Título en inglés**, cuerpo en español si aplica.
- **Antes de cambiar un string de UI:** `grep -rn "string_viejo" src/ dashboard/ app/ tests/`.

### 🤖 CI/CD

- **2/2 checks verdes antes de mergear.** Sin excepción.
- Cualquier push dispara el workflow CI (~60-90 s).
- **Si CI falla:** leer el log del step rojo antes de proponer fixes.
- **Ningún push sin verificar el estado del run CI inmediatamente anterior.** Un "verde" en el TRASPASO es foto histórica, no estado vivo.
- **Verificar con `gh run list`** (si está instalado) **o `curl` a la API de GitHub:**
  ```bash
  curl -s "https://api.github.com/repos/icqdgonzalezs/industrial-kpi-intelligence/actions/runs?per_page=1" | python3 -c "
  import json, sys
  r = json.load(sys.stdin)['workflow_runs'][0]
  print(f\"Run #{r['run_number']} | {r['conclusion']} | {r['head_commit']['message'].splitlines()[0]}\")
  "
  ```

### 🎨 UX / CSS

- Ver el archivo antes de tocar.
- Verificación visual con `⌘ + Shift + R` obligatoria.
- **Regla C.1:** sin números no hay cierre.

### 💾 Código

- **Idioma del código:** inglés. Docstrings y comentarios: español.
- **Arquitectura legacy:** `src/` (lógica) / `dashboard/` (presentación Dash).
- **Arquitectura nueva:** `app/` (FastAPI + SQLModel + Jinja2 + templates).
- **Nomenclatura:** capacidad `world_class` / `capable` / `marginal` / `not_capable`. Severidad `success` / `warning` / `danger` / `neutral`.

### 🛠️ Protocolo de cada fix

1. 📖 Leer los archivos involucrados (`grep` + `cat`).
2. 🔍 Diagnosticar causa raíz.
3. 🔎 `grep -rn "string_viejo" src/ dashboard/ app/ tests/`.
4. 💻 Código + tests juntos.
5. 🧪 `pytest` + `ruff check .`.
6. 👁️ Verificación visual con `⌘ + Shift + R`.
7. 🔍 `git status` antes del `add`.
8. 📥 `git add` con paths textuales.
9. 🔍 `git status` post-add. Verificar que "Changes not staged" esté vacío.
10. ✍️ Commit con mensaje conventional.
11. 🚀 Push + **verificar CI verde con `curl` a la API**.

### 🚀 Scripts de fix quirúrgico

```bash
cat > fix_xxx.py <<'EOF'
from pathlib import Path
p = Path("ruta/al/archivo.py")
text = p.read_text()
original = text
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

### 🔄 Protocolo de cambio de chat

**Cuándo cambiar:**
- Después de cerrar cada fase de mediana duración (con commit + CI verde).
- Después de ~40-50 mensajes densos en la misma sesión.
- Inmediatamente si aparecen 2+ síntomas de degradación.

**Cómo cambiar (protocolo):**
1. Cerrar el ciclo en curso (commit + push + CI verde).
2. Actualizar `TRASPASO_MAESTRO` con los últimos commits + sección 11.
3. Commit + push del `TRASPASO`.
4. `git pull origin main --rebase` para sincronizar local.
5. Abrir chat nuevo.
6. Pegar el mensaje de transición (sección 12) + TRASPASO completo.

### 🆕 Reglas nuevas (ciclo #21 + #22)

- **Ningún push sin verificar el estado del run CI inmediatamente anterior.** Un "verde" en el TRASPASO es foto histórica, no estado vivo. Verificar con `curl` a la API de GitHub ANTES de documentar o pushear.
- **`requirements.txt` debe reproducir el venv real, no el ideal.** Validar con `pip install --dry-run -r requirements.txt` en venv limpio antes de commitear.
- **Los tests prueban el contrato real del código, no el deseado.** Si SQLModel `table=True` no valida en construcción (limitación conocida), el test debe probar que NO valida (o no existir).
- **FastAPI con `TestClient`:** usar `httpx2` (Starlette 1.6.0 deprecó `httpx`). Fixtures con SQLite en memoria (`StaticPool`) + `dependency_overrides` para aislar tests de la DB real.
- **Antes de `pip freeze > requirements.txt`:** verificar que estás en un venv.
- **Al añadir un servicio nuevo (FastAPI):** usar puerto distinto al existente (8000 vs 8050).
- **Al migrar de una tecnología a otra:** empezar con capa aditiva (nuevo `app/` sin tocar `src/`).
- **Antes de crear un nuevo directorio del proyecto:** verificar dónde está el proyecto original con `git remote -v` y `ls`. Nunca `mkdir` a ciegas en `$HOME`.

---

## 9️⃣ ⚠️ HISTORIAL DE ERRORES — NO REPETIR

| ❌ Error | ✅ Correcto |
| :--- | :--- |
| **Escribir "CI verde" en el TRASPASO sin verificar Actions.** | Verificar con `gh run list` o `curl` a la API ANTES de documentar. |
| **Asumir que `requirements.txt` refleja el venv real.** | Validar con `pip install --dry-run -r requirements.txt` en venv limpio. |
| **Confundir "460 tests verdes locales" con "CI verde".** | Local usa venv ya poblado; CI arranca de cero en cada run. |
| **`mkdir -p ~/industrial-kpi-intelligence/app/...`** sin preguntar dónde está el proyecto. | Preguntar primero: `git remote -v` + `ls ~/Projects/`. Trabajar en el proyecto existente. |
| **Asumir que una carpeta nueva es el proyecto activo.** | Verificar con `git status` si es repo git y con `ls` si tiene los archivos originales. |
| **`pip3 freeze > requirements.txt` en Python global.** | Escribir el `requirements.txt` a mano con las dependencias top-level + transitivas críticas. |
| **`git init` + `git remote add`** cuando ya hay historial remoto. | `git clone` fresco + `cp -R` del trabajo nuevo. |
| **Asumir que `NaiveDatetime` es importable desde `sqlmodel`.** | **NO existe.** Usar `sa_column=Column(DateTime(timezone=False))`. |
| **Confiar en `field_validator` en modelo SQLModel `table=True`.** | Pydantic no ejecuta validadores en modelos de tabla. Separar en `schemas.py`. |
| **Asumir que `KPI(nombre=None)` levanta `ValidationError`.** | SQLModel `table=True` NO valida en construcción. La validación la hace `KPICreate`. |
| **Enviar `"id": 0` en POST a FastAPI.** | El `id` es autoincremental. **Nunca** enviarlo en el body de un POST de creación. |
| **Confundir el "example value" de Swagger UI con datos reales.** | El ejemplo se muestra por defecto. Para ver datos reales: **"Try it out"** → **"Execute"**. |
| **`git push` sin PAT** → `Invalid username or token`. | Usar el PAT con scope `repo` + `workflow` como contraseña. |
| **`rm -rf` de carpetas duplicadas sin verificar.** | Backup primero (`mv` a `.bak`), verificar en el proyecto original, luego borrar. |

---

## 🔟 📁 ARCHIVOS CLAVE Y COMANDOS

### 🗂️ Estructura del proyecto (post ciclo #21 + #22)

```text
industrial-kpi-intelligence/
├── ARCHITECTURE.md
├── README.md                              # 477 tests + badges (Dash + FastAPI)
├── VISION.md
├── CHANGELOG.md
├── LICENSE                                # Elastic License 2.0
├── pyproject.toml                         # ruff + pytest (testpaths = ["tests", "tests/app"])
├── requirements.txt                       # 17 deps (ambos stacks + tooling CI)
├── Procfile / render.yaml
├── .gitignore                             # +*.db, *.sqlite, kpis.csv, .env, .coverage, .pytest_cache/
├── .github/workflows/tests.yml            # Workflow "CI" (lint + test)
├── assets/style.css
│
├── app/                                   # 🆕 CAPA FASTAPI
│   ├── __init__.py
│   ├── main.py                            # FastAPI app + lifespan + GET / + GET/POST /kpis/
│   ├── models.py                          # SQLModel KPI (sa_column=DateTime(timezone=False))
│   ├── schemas.py                         # Pydantic KPICreate (BaseModel)
│   ├── db.py                              # SQLite + create_db_and_tables + get_session
│   └── templates/
│       └── index.html                     # ✅ Jinja2 (tabla KPIs con empty state)
│
├── config/
│   ├── generator_config.yaml
│   ├── plant_config.yaml
│   └── quality_config.yaml
│
├── dashboard/                             # Legacy Dash (puerto 8050) — EN RETIRADA
│   └── ...
│
├── data/
├── docs/
│   ├── adr/
│   ├── TRASPASO_MAESTRO.md                # Este archivo
│   └── ...
├── imagenes/
├── scripts/
│
├── src/                                   # Lógica legacy (intacta)
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
│
├── migrate_csv.py                         # 🆕 CSV → SQLite
├── kpi_database.db                        # 🆕 Local, NO en git (gitignored)
│
└── tests/
    ├── app/                               # 🆕 17 tests del stack FastAPI
    │   ├── __init__.py
    │   ├── conftest.py                    # Fixtures: session + client (SQLite en memoria)
    │   ├── test_models.py                 # 3 tests
    │   ├── test_schemas.py                # 5 tests
    │   └── test_endpoints.py              # 9 tests
    ├── test_empty_state.py
    └── ... (460 tests legacy)
```

### ⌨️ Comandos verificados

```bash
# Protocolo de arranque
cd /Users/violeta/Projects/industrial-operations-intelligence/industrial-kpi-intelligence
source venv/bin/activate
which python                    # DEBE mostrar .../venv/bin/python

# Gates
pytest                          # 477 passed (~60 s)
pytest tests/app/ -v            # 17 passed (~0.20 s)
ruff check .                    # All checks passed!

# Arrancar dashboard Dash (legacy)
python -m dashboard.dash_app    # http://127.0.0.1:8050
lsof -ti:8050 | xargs kill -9

# Arrancar API FastAPI (nuevo)
uvicorn app.main:app --reload   # http://127.0.0.1:8000/docs
lsof -ti:8000 | xargs kill -9

# Migrar CSV → SQLite
python3 migrate_csv.py          # Crea kpi_database.db

# Verificar datos en SQLite
python3 -c "
from sqlmodel import Session, select
from app.db import engine
from app.models import KPI
with Session(engine) as session:
    for k in session.exec(select(KPI)).all():
        print(f'{k.id} | {k.nombre} | {k.valor} {k.unidad}')
"

# Verificar estado del último run de CI
curl -s "https://api.github.com/repos/icqdgonzalezs/industrial-kpi-intelligence/actions/runs?per_page=1" | python3 -c "
import json, sys
r = json.load(sys.stdin)['workflow_runs'][0]
print(f\"Run #{r['run_number']} | {r['conclusion']} | {r['head_commit']['message'].splitlines()[0]}\")
"

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
```

---

## 1️⃣1️⃣ 🎯 PRÓXIMO PASO EXACTO

### 📋 Fase IA.1 — Chat con KPIs (RAG + LLM)

**Objetivo:** endpoint `POST /chat/` que responde preguntas en lenguaje natural sobre los KPIs almacenados en SQLite.

**Stack elegido:** Groq API (Llama 3.3 70B) — gratis, rápido (~500 ms), compatible con el SDK de OpenAI.

**Motivación estratégica:** la oferta de Full Stack (VI Región) menciona IA 7 veces (25% del peso). Sin IA, el proyecto puntúa 6.5/10 para la oferta. Con IA funcionando: 8.5/10.

**Decisiones técnicas:**

| # | Decisión | Elección |
| :---: | :--- | :--- |
| 1 | Proveedor LLM | **Groq** (Llama 3.3 70B). Gratis, rápido, migrable a OpenAI después. |
| 2 | Arquitectura | Sin RAG complejo todavía (4-50 KPIs caben enteros en el contexto). YAGNI. |
| 3 | Seguridad | API key en `.env` (gitignored). Nunca en el frontend. |
| 4 | UX | Formulario HTMX (`hx-post="/chat/"`), sin recargar página. |
| 5 | Testing | Mock del cliente LLM (`unittest.mock.AsyncMock`). Tests sin pegarle a Groq. |

**Plan de ejecución:**

1. **Crear cuenta Groq + obtener API key:** `https://console.groq.com`. Guardarla en `.env`:
   ```bash
   echo 'GROQ_API_KEY=gsk_...' > .env
   ```
2. **Instalar deps:**
   ```bash
   pip install groq python-dotenv
   ```
   Agregar a `requirements.txt` en sección IA.
3. **Crear `app/services/llm_chat.py`:** cliente Groq async + construcción de contexto desde la DB.
4. **Crear `app/routers/chat.py`:** endpoint `POST /chat/` con body `{query: str}`.
5. **Registrar router en `app/main.py`:** `app.include_router(chat_router)`.
6. **Template `app/templates/partials/_chat.html`:** formulario HTMX + área de respuesta.
7. **Integrar en `index.html`:** incluir `_chat.html`.
8. **Crear `tests/app/test_chat.py`:** 4-5 tests con mock del LLM (validación input, mock respuesta, error controlado).
9. **Verificación visual:** `uvicorn app.main:app --reload` → `http://127.0.0.1:8000/` → probar chat.
10. **Commit + push + verificar CI verde con `curl`.**

**Estructura de archivos a crear:**

```text
app/
├── routers/                    # 🆕
│   ├── __init__.py
│   └── chat.py                 # POST /chat/
├── services/                   # 🆕
│   ├── __init__.py
│   └── llm_chat.py             # Cliente Groq + construcción de contexto
├── templates/
│   ├── index.html              # modificar: incluir _chat.html
│   └── partials/               # 🆕
│       └── _chat.html
└── main.py                     # modificar: include_router(chat_router)

tests/app/
└── test_chat.py                # 🆕 4-5 tests con mock
```

**Estimación:** 3-4 h.

**⏱️ Después de IA.1:**

1. **IA.2** — Diagnóstico asistido por LLM (2 h).
2. **Docker + Deploy Railway** (4 h).
3. **Seguridad JWT + rate limit** (4 h).
4. **Migración tab por tab Dash → FastAPI** (ver decisión 4.32).

---

## 1️⃣2️⃣ 💬 MENSAJE DE TRANSICIÓN (para pegar en chat nuevo)

```text
Contexto: pego abajo el TRASPASO_MAESTRO del proyecto Industrial KPI Intelligence.
Soy David, Ing. Civil Químico + dev autodidacta, semana 3/8 del Producto 01.

Estado: ciclo #21 + #22 cerrado (commit 0c59acc). 477 tests verdes (460 legacy + 17 app/).
CI 2/2 verde VERIFICADO (run #112). Working tree limpio.

Cerrado en el último ciclo:
- Dashboard Jinja2 (app/templates/index.html + endpoint GET /) — commit 724f4ac
- 17 tests para app/ (TestClient + SQLite en memoria) — commit 0c59acc
- requirements.txt restaurado para ambos stacks — commit 785b0c4
- ruff fixes en app/ (per-file-ignores B008) — commit a561fff
- httpx2 reemplaza httpx (Starlette 1.6.0) — sin warnings

Decisión estratégica en curso: MIGRACIÓN COMPLETA Dash → FastAPI
(ver decisión 4.32 del TRASPASO). Stack elegido: Jinja2 + HTMX + Plotly.js.
Timeline: ~5 semanas, strangler tab por tab.

Próximo paso: Fase IA.1 — chat con KPIs (RAG + LLM, Groq).
Estimación 3-4 h. Ver sección 11 del TRASPASO.
Motivación: la oferta de Full Stack (VI Región) menciona IA 7 veces (25% del peso).

Deudas activas relevantes:
- #27 fase IA (alta, próximo paso)
- #11 eliminar schema_adapter.py (alta, legacy)
- #15 debounce cascade (media, legacy)
- #16 severidad individual KPIs rendimiento (media, legacy)
- #19 callback 2104 ms en Calidad (media, legacy)
- #26 CI no mide cobertura de app/ (media)
- #25 pandas 2→3 (baja, diferida)

Reglas clave (ver sección 8 completa):
- Protocolo de arranque: cd + source venv/bin/activate + verificar `which python`
- Leer el archivo antes de tocar
- git status ANTES y DESPUÉS de cada git add
- Un fix = un commit
- Verificación visual con ⌘ + Shift + R obligatoria
- pytest + ruff verdes antes de commitear
- NINGÚN push sin verificar el run CI anterior con curl a la API
- requirements.txt debe reproducir el venv real (validar con --dry-run)
- NO usar TextEdit para markdown: usar GitHub Web Editor
- Tras editar en Web Editor: git pull --rebase
- NUNCA enviar "id": 0 en POST a FastAPI
- NUNCA confundir el "example value" de Swagger UI con datos reales
- SQLModel table=True NO valida en construcción; usar schemas.py con BaseModel
- Al añadir un servicio nuevo: puerto distinto (8000 FastAPI vs 8050 Dash)
- FastAPI TestClient usa httpx2 (Starlette 1.6.0)

Actuá como ingeniero de software senior + mentor. Directo, técnico,
sin relleno. Español. Markdown con tablas y bloques de código.

[PEGAR TODO EL CONTENIDO DE TRASPASO_MAESTRO.md ABAJO]
```

---

## 1️⃣3️⃣ 🎓 NOTAS DE MENTOR (para el próximo asistente)

### 🎯 Cómo tratarlo

- **Como colega senior, no como aprendiz.**
- Explicá el *por qué* de las decisiones técnicas, no solo el *cómo*.
- Citá normas industriales cuando aplique (ISA-95, NIST, AIAG, ISO).
- **Valorá la honestidad por sobre la complacencia.**
- No quiere halagos, quiere producto de calidad.
- Cuando te equivoques, decilo claro y corregí.

### 🏆 Hitos acumulados

- ✅ **Fase 3a completa** (5/5 tabs con export CSV).
- ✅ **Opción D** — consolidación del adapter.
- ✅ **Fase 3b.1** — loading states.
- ✅ **Fase 3b.3** — performance: -70% del tiempo original.
- ✅ **Fase 3b.2 completa** — empty states en 5/5 tabs + cascades.
- ✅ **Migración a FastAPI + SQLModel + SQLite** (`a162f15`).
- ✅ **Dashboard Jinja2 operativo** (`724f4ac`).
- ✅ **17 tests para `app/`** (`0c59acc`) — deuda #22 cerrada.
- ✅ **CI verde real verificado** (run #112) — no "verde de foto".
- ✅ **477 tests, 0 regresiones, 0 warnings.**
- ✅ **`requirements.txt` reproducible** (validado en venv limpio).
- ✅ **Decisión estratégica de migración completa Dash → FastAPI** (4.32).

### 🔬 Lecciones metodológicas de este ciclo

- **Un "verde" en el TRASPASO es foto histórica, no estado vivo.** Verificar CI con `curl` a la API antes de cada push. El caso `a162f15` (verde en doc, rojo en realidad) costó 2 h de diagnóstico.
- **`requirements.txt` es contrato de reproducibilidad, no lista de deseos.** Validar con `pip install --dry-run` en venv limpio. Los pines "aspiracionales" (pandas 3.0.5 cuando el venv tiene 2.1.4) rompen CI.
- **Los tests prueban el contrato real del código, no el deseado.** SQLModel `table=True` no valida en construcción. Los tests documentan ese contrato real, no lo imaginan.
- **Un test rojo puede significar dos cosas:** el código tiene bug (fix código) o el test está mal escrito (fix test). Diagnosticar antes de tocar.
- **`httpx2` reemplaza a `httpx` en Starlette 1.6.0.** Leer los DeprecationWarnings temprano.
- **FastAPI TestClient:** SQLite en memoria (`StaticPool`) + `dependency_overrides` para aislar tests de la DB real.
- **Un fix = un commit.** 5 commits en este ciclo, cada uno con propósito claro. Nada mezclado.
- **La documentación es parte del trabajo, no un extra.** Actualizar TRASPASO al cerrar cada fase.

### 📊 Métricas del ciclo

- **Commits:** 5 (`54ac5ed`, `785b0c4`, `a561fff`, `724f4ac`, `0c59acc`).
- **Archivos tocados:** 12 (5 nuevos en `tests/app/`, 2 nuevos en `app/`, 5 modificados).
- **Líneas:** +310/-2 (solo tests) + Jinja2 dashboard + requirements + pyproject.
- **Tests:** 460 → **477** (+17).
- **Deudas cerradas:** #21, #22.
- **Deudas nuevas:** #25 (pandas 2→3), #26 (coverage de `app/`), #27 (fase IA).
- **Tiempo total:** ~4 h de sesión distribuida.

---

> 📌 **Fin del TRASPASO_MAESTRO.**  
> 🗓️ **Última actualización:** Ciclo #21 + #22 cerrado (commit `0c59acc`). 477 tests verdes. CI 2/2 verde verificado (run #112).  
> 🚀 **Próximo paso:** Fase IA.1 — chat con KPIs (RAG + LLM, Groq). Ver sección 11.
