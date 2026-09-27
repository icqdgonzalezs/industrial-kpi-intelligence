# 🎯 TRASPASO MAESTRO — Industrial KPI Intelligence

> 📌 **Propósito:** documento autocontenido para arrancar un chat nuevo sin perder contexto.  
> 📥 **Instrucción de uso:** pegar este archivo completo como **PRIMER** mensaje en un chat nuevo.  
> 🗓️ **Última actualización:** Ciclo IA.1 cerrado (chat con KPIs + Groq LLM + HTMX). Commit `ed11c36` pusheado. **487 tests verdes, CI 2/2 verde verificado (run #117).**  
> 🚀 **Próximo paso:** Deploy Railway (Docker + Postgres + variables de entorno). Ver sección 11.

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
| 12 | 🚫 **Nunca pegar `+` de un diff en un archivo real.** El prefijo `+` significa "línea agregada", no es parte del contenido. |

> 🚀 **Próximo paso concreto del proyecto:** Deploy Railway — Dockerfile + docker-compose + migrar SQLite → Postgres. Ver sección 11.

---

## 1️⃣ FICHA DEL PROYECTO

| Campo | Valor |
| :--- | :--- |
| 🏭 **Producto** | Industrial KPI Intelligence — dashboard industrial para PYMES manufactureras LatAm/España |
| 🌐 **Ecosistema** | Primer producto de 6 SaaS (Industrial Operations Intelligence) |
| 🛠️ **Stack legacy (dashboard)** | Python 3.11.9 · Plotly Dash 4.4.1 · Plotly · pandas · numpy |
| 🛠️ **Stack nuevo (API REST)** | FastAPI 0.141.1 · SQLModel 0.0.46 · SQLAlchemy 2.0.54 · Pydantic 2.13.5 · SQLite · Jinja2 3.1.6 · Uvicorn 0.53.0 · python-multipart 0.0.32 |
| 🛠️ **Stack IA (operativo)** | Groq SDK 1.7.0 · Modelo `openai/gpt-oss-120b` · python-dotenv 1.2.3 · HTMX 2.0.4 |
| 🧪 **Testing** | pytest 9.1.1 · pytest-cov 7.1.0 · ruff 0.16.6 · httpx2 2.13.1 · GitHub Actions CI/CD |
| 📏 **Estándares aplicables** | ISA-95 · TPM (OEE) · NIST 6.1.3 / ISO 22514 (Pp/Ppk) · AIAG SPC · OWASP · ISA-101 (HMI) · WCAG 2.1 · OpenAPI 3.1 |
| ⚖️ **Licencia** | Elastic License 2.0 (nunca MIT) |
| 👤 **Usuario** | David González Santibáñez — Ing. Civil Químico + dev autodidacta |
| 📅 **Semana** | 3 de 8 |
| ✅ **Tests actuales** | **487 passed** (460 legacy + 17 app/ + 10 chat) |
| 🟢 **CI** | 2/2 verde **verificado** (run #117, commit `ed11c36`) |
| 🧹 **Working tree** | Limpio, rama `main` sincronizada con `origin/main`. HEAD: `ed11c36`. |
| 📊 **Producto 1 (MVP)** | ~95% (dashboard Dash + API FastAPI con IA operativa). Deploy público pendiente. |
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

**Ciclo #21 + #22 (dashboard Jinja2 + tests app/):**

- ✅ **`54ac5ed`** — `chore(gitignore): ignore testing artifacts` (`.coverage`, `htmlcov/`, `.pytest_cache/`).
- ✅ **`785b0c4`** — `fix(ci): restore requirements.txt for both stacks` (job `test` del CI).
- ✅ **`a561fff`** — `fix(lint): resolve ruff findings in FastAPI layer` (job `lint` + per-file-ignores B008).
- ✅ **`724f4ac`** — `feat(fastapi): add Jinja2 dashboard for KPI visualization` (**deuda #21 cerrada**). `app/templates/index.html` + endpoint `GET /`.
- ✅ **`0c59acc`** — `test(app): add unit + integration tests for FastAPI layer` (**deuda #22 cerrada**). 17 tests con `TestClient` + SQLite en memoria.

**Ciclo IA.1 (chat con KPIs — Groq + HTMX):**

- ✅ **`03f74a7`** — `feat(ai): add Groq LLM service for KPI chat`. Cliente Groq async singleton + constructor de contexto + system prompt industrial.
- ✅ **`ed806ea`** — `feat(ai): add chat UI with HTMX for KPI queries` (**deuda #27 cerrada**). Router `POST /chat/` + templates `_chat.html` / `_chat_response.html` + HTMX 2.0.4 + CSS.
- ✅ **`ab72a9e`** — `fix(deps): add python-multipart for FastAPI Form parsing` (falló CI por prefijo `+` literal — histórico).
- ✅ **`ed11c36`** — `fix(deps): remove literal '+' from python-multipart line`. CI #117 verde.

### 🟡 En curso

- *Nada.* Working tree limpio. CI #117 verde verificado.

### ⏳ Pendiente inmediato (Deploy)

- ⏳ **Fase Deploy** — Dockerfile + docker-compose + migrar SQLite → Postgres + Railway.
- ⏳ **Deuda #11** — eliminar `schema_adapter.py` legacy.
- ⏳ **Deuda #15** — debounce cascade.
- ⏳ **Deuda #16** — severidad individual en KPIs de rendimiento.
- ⏳ **Deuda #19** — optimizar callback de 2104 ms en Calidad.
- ⏳ **Migración completa Dash → FastAPI** (ver decisión 4.32).

---

## 3️⃣ LÍNEA TEMPORAL DE COMMITS

| Commit | Descripción | Tests |
| :--- | :--- | :---: |
| `ed11c36` | **fix(deps): remove literal '+' from python-multipart line** | 487 |
| `ab72a9e` | Fix(deps): add python-multipart for FastAPI Form parsing | 487 |
| `ed806ea` | **feat(ai): add chat UI with HTMX for KPI queries** (9 files, +321/-2) | 487 |
| `03f74a7` | **feat(ai): add Groq LLM service for KPI chat** | 477 |
| `0c59acc` | Test(app): add unit + integration tests for FastAPI layer (7 files, +310/-2) | 477 |
| `724f4ac` | Feat(fastapi): add Jinja2 dashboard for KPI visualization | 460 |
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

> 📈 **Evolución de tests:** 263 → ... → 450 → 453 → 460 → 477 → **487** (460 legacy + 17 app/ + 10 chat).  
> ✅ **CI verde real verificado** (runs #112, #114, #117). Los runs rojos #107, #108, #109, #115, #116 quedan como histórico.

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
- **Añadido:** `*.db`, `*.sqlite`, `*.sqlite3`, `.env`, `*.log`, `*.alerts`, `kpis.csv`, `.coverage`, `.coverage.*`, `htmlcov/`, `.pytest_cache/`.

### 4.31 🌐 URLs del proyecto
| Servicio | URL | Comando |
| :--- | :--- | :--- |
| Dashboard Dash (legacy) | `http://127.0.0.1:8050` | `python -m dashboard.dash_app` |
| API FastAPI + Swagger UI | `http://127.0.0.1:8000/docs` | `uvicorn app.main:app --reload` |
| Dashboard Jinja2 + chat IA | `http://127.0.0.1:8000/` | (mismo servidor) |
| Chat endpoint | `POST http://127.0.0.1:8000/chat/` | (mismo servidor) |
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

### 4.35 🤖 Groq + `openai/gpt-oss-120b` para el chat IA
- **Decisión:** usar **Groq** como proveedor LLM (gratis, rápido, OpenAI-compatible) con modelo **`openai/gpt-oss-120b`** (producción).
- **Motivo:** Groq tiene tier gratuito generoso (30 RPM, 14.4k RPD), latencia ~1.5s para ~700 tokens, SDK idéntico al de OpenAI (migración trivial).
- **Histórico:** los modelos `llama-3.3-70b-versatile` y `llama-3.1-8b-instant` fueron **deprecados el 2026-08-16**. El reemplazo oficial es `openai/gpt-oss-120b`.
- **Arquitectura:** sin RAG vectorial todavía. Los 4-50 KPIs caben enteros en el contexto del prompt. YAGNI.
- **Lección:** los IDs de modelos LLM son efímeros. Diseñar el ID como configurable (idealmente desde `.env` con fallback).

### 4.36 🧩 Arquitectura en 4 capas del chat IA
- **Decisión:** separar el chat en 4 capas claras.
  - **Servicio** (`app/services/llm_chat.py`): habla con Groq. No sabe HTTP.
  - **Router** (`app/routers/chat.py`): orquesta DB + service + template.
  - **Contrato** (`Form(min_length=1, max_length=500)`): validación en el borde.
  - **Presentación** (`partials/_chat.html` + `_chat_response.html`): HTML + HTMX.
- **Motivo:** testeable en cada capa sin acoplar. Cambiar de proveedor LLM toca 1 archivo.
- **Lección:** los servicios deben ser agnósticos del transporte. Los routers orquestan, no calculan.

### 4.37 📦 `python-multipart` es obligatorio para `Form(...)`
- **Problema:** FastAPI valida la presencia de `python-multipart` **en import-time** del módulo (cuando el decorador `@router.post` evalúa `Form(...)`), no en runtime.
- **Error típico:** `RuntimeError: Form data requires "python-multipart" to be installed.`
- **Solución:** declarar `python-multipart>=0.0.20,<1` en `requirements.txt`.
- **Lección:** cualquier endpoint con `Form`, `File`, `UploadFile` u `OAuth2PasswordRequestForm` requiere `python-multipart`. **Nunca confiar en dependencias transitivas.**

### 4.38 🎨 HTMX como reemplazo de callbacks Dash
- **Decisión:** usar **HTMX 2.0.4** (51 KB, single-file) en vez de React/Vue para la interactividad del dashboard.
- **Motivo:** server-side render (Jinja2) + HTML declarativo. Cero estado JS, cero build step, cero npm.
- **Cómo funciona:** `hx-post="/chat/"` en el `<form>` → HTMX hace el POST → server devuelve HTML parcial → HTMX lo inyecta con `hx-target` + `hx-swap`.
- **Reemplaza:** callbacks de Dash (Python + estado en JS) con requests HTTP puros.
- **Lección:** para dashboards internos, HTMX + Jinja2 es 10x más simple que una SPA. La complejidad se justifica solo si se necesita estado rico en cliente.

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

### Tests de `app/` (17) — ciclo #22

| Archivo | Tests | Cobertura conceptual |
| :--- | :---: | :--- |
| `tests/app/test_models.py` | 3 | `KPI` SQLModel: creación, timestamp naive, contrato real (no valida en construcción) |
| `tests/app/test_schemas.py` | 5 | `KPICreate`: parseo ISO, coacción numérica, rechazo inválido |
| `tests/app/test_endpoints.py` | 9 | `GET /`, `GET /kpis/`, `POST /kpis/` con `TestClient` |
| **Subtotal app/** | **17** | ✅ |

### Tests del chat IA (10) — ciclo IA.1

| Archivo | Tests | Cobertura conceptual |
| :--- | :---: | :--- |
| `tests/app/test_chat.py` | 10 | POST `/chat/` con mock del LLM |
| **Subtotal chat** | **10** | ✅ |

**Detalle de los 10 tests del chat:**
- 4 happy path (200 + HTML + respuesta mock + métricas + query preservada).
- 3 validación (query vacío → 422, query > 500 chars → 422, sin query → 422).
- 2 manejo de errores (TimeoutError → mensaje de timeout, Exception → mensaje genérico).
- 1 dashboard incluye chat (`Asistente de planta` + `hx-post="/chat/"` + `htmx.min.js` en HTML).

### Fixtures críticas (conftest.py)

- `session` → SQLite en memoria (`StaticPool`, `check_same_thread=False`). Aislada por test. **No toca `kpi_database.db`.**
- `client` → `TestClient` con `app.dependency_overrides[get_session]`. Cero contaminación entre tests.
- `mock_llm_ok` → `monkeypatch.setattr` sobre `app.routers.chat.consultar_llm`. Evita pegarle a Groq real.

### Total

> **487 tests passed** (460 legacy + 17 app/ + 10 chat). **0 regresiones. 0 warnings.**  
> Tiempo: ~60 s suite completa. Tests de `app/` corren en ~0.20 s (SQLite en memoria, gratis).

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
| **25** | Pandas 2.1.4 → 3.x (requirements actualizado a `>=2.1,<3`) | Reproducibilidad | 🟢 Baja |
| **26** | CI no mide cobertura de `app/` (solo `--cov=src --cov=dashboard`) | Testing infra | 🟡 Media |
| ~~**27**~~ | ~~Fase IA pendiente~~ | ✅ **CERRADA** (`ed806ea`) | — |
| **28 🆕** | Sin Dockerfile ni docker-compose | Deploy | 🔴 **Alta (próximo)** |
| **29 🆕** | SQLite en producción (debería ser Postgres) | Escalabilidad | 🔴 **Alta (con deploy)** |
| **30 🆕** | Sin rate limiting en `/chat/` (Groq tier gratis: 30 RPM) | Seguridad/Costos | 🟡 Media |
| **31 🆕** | `GROQ_MODEL` hardcodeado (debería leerse de `.env` con fallback) | Mantenibilidad | 🟢 Baja |
| **32 🆕** | Sin autenticación (chat accesible sin login) | Seguridad | 🔴 Alta (con deploy público) |
| **33 🆕** | IA.2, IA.3, IA.4 (diagnóstico/reportes/anomalías con LLM) | Features | 🟡 Media |

### 📌 Detalle de deudas activas

**Deuda 11 — Eliminación de `schema_adapter.py`:**
- `grep -rn "schema_adapter" src/ dashboard/ tests/ app/ --include="*.py"` → confirmar que nada lo importa.
- `git rm src/schema_adapter.py` → `pytest` + `ruff check .` → commit `chore(cleanup): remove legacy schema_adapter.py`.

**Deuda 15 — Doble spinner residual:** Cascade equipo + reset → 2 fires del store. Fix candidato: `debounce` 200ms o cascade condicional.

**Deuda 16 — Semántica color KPIs rendimiento:** Los 4 KPIs heredan severidad agregada del PPM total. Fix: severidad individual por KPI (Fase 3c).

**Deuda 19 — Callback de 2104 ms:** Detectado en Dash Dev Tools. Fix: identificar callback exacto, instrumentar, medir, optimizar.

**Deuda 24 — Doble stack de dashboards:** Transitoria. Una vez el dashboard Jinja2 cubra todas las funcionalidades del Dash, se retira el Dash (ver decisión 4.32).

**Deuda 25 — Pandas 2 → 3:** `requirements.txt` fija `pandas>=2.1,<3`. Migrar a pandas 3 es su propio ciclo.

**Deuda 26 — Cobertura de `app/` en CI:** El workflow corre `pytest tests/ -v --cov=src --cov=dashboard`. Fix candidato: agregar `--cov=app` al comando del workflow.

**Deuda 28 🆕 — Dockerfile + docker-compose:** Necesario para deploy. Ver sección 11.

**Deuda 29 🆕 — Migrar SQLite → Postgres:** Railway provee Postgres como addon. Cambiar `DATABASE_URL` a variable de entorno.

**Deuda 30 🆕 — Rate limiting en `/chat/`:** Groq tier gratis tiene 30 RPM. Si varios usuarios consultan, se agota. Fix: `slowapi` o límite por IP en el router.

**Deuda 31 🆕 — `GROQ_MODEL` configurable:** Mover de constante a `os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")`. Facilita migrar modelos sin tocar código.

**Deuda 32 🆕 — Autenticación:** Sin JWT, cualquiera con la URL puede usar el chat y consumir la API key de Groq. Bloqueante para deploy público real.

**Deuda 33 🆕 — IA.2/IA.3/IA.4:** Diagnóstico asistido, reportes ejecutivos, detección de anomalías ML. Fases naturales después del deploy.

---

## 7️⃣ ROADMAP PENDIENTE

| Fase | Fix / Feature | Estimación | Prioridad |
| :--- | :--- | :---: | :---: |
| **Deploy.1** | **Dockerfile multi-stage** | 1 h | 🔴 **Alta — PRÓXIMO PASO** |
| **Deploy.2** | **docker-compose.yml (app + Postgres)** | 1 h | 🔴 Alta |
| **Deploy.3** | **Migrar SQLite → Postgres** (`DATABASE_URL` env) | 1 h | 🔴 Alta |
| **Deploy.4** | **Cuenta Railway + deploy** | 1 h | 🔴 Alta |
| **Deploy.5** | **Configurar `GROQ_API_KEY` como variable de entorno** | 15 min | 🔴 Alta |
| **Deploy.6** | **Verificar URL pública con chat IA funcionando** | 30 min | 🔴 Alta |
| **Seg.1** | **JWT auth básica** (antes de mostrar la URL) | 2 h | 🔴 Alta |
| Seg.2 | Rate limit en `/chat/` (slowapi) | 1 h | 🟡 Media |
| Seg.3 | CORS configurado | 30 min | 🟡 Media |
| IA.2 | Diagnóstico asistido por LLM (explica hallazgos de `src/diagnostics.py`) | 2 h | 🟡 Media |
| IA.3 | Generación de reportes ejecutivos (LLM narra KPIs + Pareto) | 2 h | 🟡 Media |
| IA.4 | Detección de anomalías ML (Isolation Forest sobre I-MR) | 3 h | 🟡 Media |
| Auto | APScheduler (ingesta CSV → SQLite cada N min) | 2 h | 🟡 Media |
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

> ⚠️ Si `which python` no muestra la ruta del venv, los comandos fallarán con `ModuleNotFoundError` o `ruff: command not found`. Verificar antes de correr gates.

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
| **Quitar el `+` inicial** al pegar un diff en editor. | Pegar el `+` literal (rompe archivos de config). |

### ✍️ Commits

- **Conventional Commits:** `feat:`, `fix:`, `refactor:`, `docs:`, `style:`, `test:`, `chore:`, `polish:`, `perf:`.
- **Un fix = un commit.** No mezclar propósitos.
- **Título en inglés**, cuerpo en español si aplica.
- **Antes de cambiar un string de UI:** `grep -rn "string_viejo" src/ dashboard/ app/ tests/`.

### 🤖 CI/CD

- **2/2 checks verdes antes de mergear.** Sin excepción.
- Cualquier push dispara el workflow CI (~60-90 s).
- **Si CI falla:** leer el log del step rojo ANTES de proponer fixes.
- **Ningún push sin verificar el estado del run CI inmediatamente anterior.** Un "verde" en el TRASPASO es foto histórica, no estado vivo.
- **Verificar con `curl` a la API de GitHub:**
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
- **Arquitectura nueva:** `app/` (FastAPI + SQLModel + Jinja2 + HTMX).
  - `app/routers/`: orquestación HTTP (reciben request, devuelven response).
  - `app/services/`: lógica pura, sin HTTP (hablan con APIs externas, construyen datos).
  - `app/templates/`: Jinja2 (render server-side).
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

### 🆕 Reglas nuevas (ciclo IA.1)

- **Nunca pegar el `+` inicial de un diff en un archivo de config.** El `+` significa "línea agregada", no es parte del contenido. Si se pega literal, pip falla con `Invalid requirement`.
- **`python-multipart` es obligatorio para `Form(...)`, `File(...)`, `UploadFile(...)` en FastAPI.** FastAPI lo valida en import-time del módulo, no en runtime. Declarar en `requirements.txt`.
- **Los IDs de modelos LLM son efímeros.** Groq deprecó `llama-3.3-70b-versatile` el 2026-08-16. Diseñar el ID como configurable (`os.getenv("GROQ_MODEL", ...)`).
- **Nunca exponer secrets con `cat .env`.** Verificar con `grep -c "GROQ_API_KEY" .env` (cuenta líneas) o `python -c "from dotenv import load_dotenv; ..."` (verifica existencia, no valor).
- **Regla heredada ciclo #21 + #22:** todo lo anterior se mantiene.

---

## 9️⃣ ⚠️ HISTORIAL DE ERRORES — NO REPETIR

| ❌ Error | ✅ Correcto |
| :--- | :--- |
| **Pegar `+python-multipart>=0.0.20,<1` en `requirements.txt`.** | Quitar el `+` inicial. Ese prefijo indica "línea agregada" en un diff, no es parte del contenido. |
| **Asumir que `python-multipart` está instalado porque algo lo arrastra.** | Declararlo explícitamente en `requirements.txt`. FastAPI lo valida en import-time. |
| **Usar `llama-3.3-70b-versatile` (deprecado 2026-08-16).** | Usar `openai/gpt-oss-120b` (producción en Groq). |
| **`cat .env` para verificar la key.** | `python -c "from dotenv import load_dotenv; import os; ..."` (verifica existencia, no valor). |
| **Pegar la API key completa en el chat.** | Pegarla enmascarada (`gsk_abc12...xyz`). Si se expone, rotarla inmediatamente en el panel del proveedor. |
| **Escribir "CI verde" en el TRASPASO sin verificar Actions.** | Verificar con `curl` a la API ANTES de documentar. |
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

### 🗂️ Estructura del proyecto (post ciclo IA.1)

```text
industrial-kpi-intelligence/
├── ARCHITECTURE.md
├── README.md                              # 487 tests + badges (Dash + FastAPI + IA)
├── VISION.md
├── CHANGELOG.md
├── LICENSE                                # Elastic License 2.0
├── pyproject.toml                         # ruff + pytest (testpaths = ["tests", "tests/app"])
├── requirements.txt                       # 21 deps (FastAPI + Dash + IA + tooling CI)
├── Procfile / render.yaml
├── .env                                   # GROQ_API_KEY (gitignored, NUNCA subir)
├── .gitignore                             # +*.db, *.sqlite, kpis.csv, .env, .coverage, .pytest_cache/
├── .github/workflows/tests.yml            # Workflow "CI" (lint + test)
├── assets/style.css
│
├── app/                                   # 🆕 CAPA FASTAPI (en crecimiento)
│   ├── __init__.py
│   ├── main.py                            # FastAPI app + lifespan + GET / + GET/POST /kpis/ + include_router(chat)
│   ├── models.py                          # SQLModel KPI (sa_column=DateTime(timezone=False))
│   ├── schemas.py                         # Pydantic KPICreate (BaseModel)
│   ├── db.py                              # SQLite + create_db_and_tables + get_session
│   ├── templates_config.py                # 🆕 Jinja2Templates compartido (main + routers)
│   ├── routers/                           # 🆕
│   │   ├── __init__.py
│   │   └── chat.py                        # POST /chat/ (HTML parcial)
│   ├── services/                          # 🆕
│   │   ├── __init__.py
│   │   └── llm_chat.py                    # Groq AsyncGroq + construir_contexto + consultar_llm
│   └── templates/
│       ├── index.html                     # Dashboard + formulario chat incluido
│       └── partials/                      # 🆕
│           ├── _chat.html                 # Formulario HTMX
│           └── _chat_response.html        # HTML parcial de respuesta/error
│
├── static/                                # 🆕
│   └── js/
│       └── htmx.min.js                    # HTMX 2.0.4 (51 KB)
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
├── migrate_csv.py                         # CSV → SQLite
├── kpi_database.db                        # Local, NO en git (gitignored)
│
└── tests/
    ├── app/                               # 27 tests del stack FastAPI
    │   ├── __init__.py
    │   ├── conftest.py                    # Fixtures: session + client (SQLite en memoria)
    │   ├── test_models.py                 # 3 tests
    │   ├── test_schemas.py                # 5 tests
    │   ├── test_endpoints.py              # 9 tests
    │   └── test_chat.py                   # 10 tests (chat con mock)
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
pytest                          # 487 passed (~60 s)
pytest tests/app/ -v            # 27 passed (~0.5 s)
ruff check .                    # All checks passed!

# Arrancar API FastAPI + dashboard + chat
uvicorn app.main:app --reload   # http://127.0.0.1:8000/
lsof -ti:8000 | xargs kill -9   # matar si quedó zombie

# Arrancar dashboard Dash (legacy)
python -m dashboard.dash_app    # http://127.0.0.1:8050
lsof -ti:8050 | xargs kill -9

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

# Test manual del chat (sin arrancar server)
python -c "
import asyncio
from datetime import datetime
from app.models import KPI
from app.services.llm_chat import consultar_llm

kpis = [
    KPI(id=1, nombre='OEE', valor=85.5, unidad='%',
        timestamp=datetime(2026, 9, 23, 8, 0), linea_produccion='L1'),
]
async def main():
    r = await consultar_llm('¿Cómo está el OEE?', kpis)
    print(r['respuesta'])
    print(f\"{r['elapsed_ms']} ms\")
asyncio.run(main())
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

### 📋 Fase Deploy.1 — Dockerfile + docker-compose

**Contexto:** el chat IA funciona en `localhost:8000`. Falta deployarlo a una URL pública para portafolio y demo. La oferta de Full Stack (VI Región) exige portafolio visible: *"nos interesa ver lo que eres capaz de construir"*.

**Objetivo:** `https://<nombre>.up.railway.app/` con el dashboard + chat IA funcionando en producción, con Postgres como DB y `GROQ_API_KEY` como variable de entorno.

**Plan de ejecución:**

1. **Crear `Dockerfile`** (multi-stage, Python 3.11-slim, ~20 líneas):
   ```dockerfile
   # Stage 1: builder
   FROM python:3.11-slim AS builder
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir --user -r requirements.txt

   # Stage 2: runtime
   FROM python:3.11-slim
   WORKDIR /app
   COPY --from=builder /root/.local /root/.local
   COPY . .
   ENV PATH=/root/.local/bin:$PATH
   EXPOSE 8000
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Crear `.dockerignore`** (excluir `.venv/`, `.git/`, `__pycache__/`, `*.db`, `.env`, etc.).

3. **Crear `docker-compose.yml`** para desarrollo local con Postgres:
   ```yaml
   services:
     db:
       image: postgres:16-alpine
       environment:
         POSTGRES_DB: kpi
         POSTGRES_USER: kpi
         POSTGRES_PASSWORD: dev
       ports:
         - "5432:5432"
     app:
       build: .
       ports:
         - "8000:8000"
       environment:
         DATABASE_URL: postgresql://kpi:dev@db:5432/kpi
         GROQ_API_KEY: ${GROQ_API_KEY}
       depends_on:
         - db
   ```

4. **Migrar `app/db.py` a variable de entorno:**
   ```python
   DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kpi_database.db")
   engine = create_engine(DATABASE_URL)
   ```
   Con fallback a SQLite para desarrollo local.

5. **Crear `railway.toml`** (configuración de deployment):
   ```toml
   [build]
   builder = "dockerfile"
   dockerfilePath = "Dockerfile"

   [deploy]
   startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
   healthcheckPath = "/docs"
   ```

6. **Crear cuenta Railway** (`railway.app`) → conectar con GitHub → crear proyecto → linkear repo.

7. **Agregar Postgres addon** desde el dashboard de Railway. Obtener `DATABASE_URL` automáticamente.

8. **Configurar variables de entorno en Railway:**
   - `GROQ_API_KEY` → la key real.
   - `GROQ_MODEL` → `openai/gpt-oss-120b` (o default).
   - `DATABASE_URL` → auto-generada por el addon.

9. **Deploy:** push a `main` → Railway buildea automáticamente.

10. **Verificar URL pública:** abrir `https://<proyecto>.up.railway.app/` + probar el chat.

**Estructura de archivos a crear:**

```text
industrial-kpi-intelligence/
├── Dockerfile                     # 🆕 multi-stage build
├── .dockerignore                  # 🆕 excluir .venv, .git, *.db, .env
├── docker-compose.yml             # 🆕 dev local con Postgres
├── railway.toml                   # 🆕 config deploy
└── app/db.py                      # modificar: DATABASE_URL desde env
```

**Estimación:** 3-4 h.

**⚠️ Bloqueante previo:** agregar JWT auth básica (deuda #32). Sin auth, la URL pública expone el consumo de Groq a cualquiera. Ver "Seg.1" en el roadmap.

**⏱️ Después de Deploy:**

1. **Seguridad** — JWT + rate limit + CORS (4 h).
2. **IA.2** — Diagnóstico asistido por LLM (2 h).
3. **IA.3** — Reportes ejecutivos narrados (2 h).
4. **Migración tab por tab Dash → FastAPI** (ver decisión 4.32).

---

## 1️⃣2️⃣ 💬 MENSAJE DE TRANSICIÓN (para pegar en chat nuevo)

```text
Contexto: pego abajo el TRASPASO_MAESTRO del proyecto Industrial KPI Intelligence.
Soy David, Ing. Civil Químico + dev autodidacta, semana 3/8 del Producto 01.

Estado: ciclo IA.1 cerrado (commit ed11c36). 487 tests verdes (460 legacy + 17 app/ + 10 chat).
CI 2/2 verde VERIFICADO (run #117). Working tree limpio.

Cerrado en el último ciclo (IA.1 — Chat con KPIs):
- Groq LLM service (app/services/llm_chat.py) — commit 03f74a7
- Chat UI con HTMX (app/routers/chat.py + templates partials) — commit ed806ea
- python-multipart agregado (fix import-time de FastAPI Form) — commit ab72a9e
- Fix del '+' literal en requirements.txt — commit ed11c36

Modelo IA: openai/gpt-oss-120b vía Groq (gratis, ~1.5s por consulta, ~700 tokens).
Los modelos llama-3.3-70b-versatile y llama-3.1-8b-instant fueron deprecados 2026-08-16.

Próximo paso: Fase Deploy.1 — Dockerfile + docker-compose + Railway.
Estimación 3-4 h. Ver sección 11 del TRASPASO.
Motivación: la oferta de Full Stack (VI Región) pide portafolio visible con URL.

Decisión estratégica en curso: MIGRACIÓN COMPLETA Dash → FastAPI
(ver decisión 4.32 del TRASPASO). Stack elegido: Jinja2 + HTMX + Plotly.js.

Deudas activas relevantes:
- #28 Dockerfile + docker-compose (alta, próximo paso)
- #29 SQLite → Postgres (alta, con deploy)
- #32 JWT auth (alta, bloqueante para URL pública)
- #30 rate limit en /chat/ (media)
- #31 GROQ_MODEL configurable (baja)
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
- Nunca pegar el '+' inicial de un diff en archivos de config
- python-multipart es obligatorio para Form/File/UploadFile en FastAPI
- Los IDs de modelos LLM son efímeros (Groq deprecó llama-3.3-70b en 2026-08-16)
- NUNCA exponer secrets con `cat .env` (usar `python -c` que verifica existencia)
- NO usar TextEdit para markdown: usar GitHub Web Editor
- Tras editar en Web Editor: git pull --rebase
- NUNCA enviar "id": 0 en POST a FastAPI
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
- ✅ **CI verde real verificado** (run #112).
- ✅ **477 tests, 0 regresiones, 0 warnings.**
- ✅ **`requirements.txt` reproducible** (validado en venv limpio).
- ✅ **Decisión estratégica de migración completa Dash → FastAPI** (4.32).
- ✅ **Chat IA con Groq operativo en dashboard** (`ed806ea`) — deuda #27 cerrada.
- ✅ **487 tests, CI verde verificado** (run #117).
- ✅ **Arquitectura 4 capas para IA** (service + router + contrato + presentación).
- ✅ **HTMX integrado** (interactividad sin SPA, sin build step).

### 🔬 Lecciones metodológicas de este ciclo

- **Los diffs tienen sintaxis propia.** El `+` inicial no es parte del contenido. Al pegar un diff en un editor, quitarlo siempre.
- **FastAPI valida `Form(...)` en import-time.** Sin `python-multipart`, el módulo no se importa. Falla en colección de tests, no en ejecución.
- **Los IDs de modelos LLM son efímeros.** Groq deprecó Llama 3.3 el 2026-08-16. Diseñar el ID como configurable desde el primer día.
- **Los secrets NUNCA se imprimen.** `cat .env` expone el valor. Usar `grep -c` o un script de Python que verifique existencia, no contenido.
- **HTMX reemplaza callbacks Dash con 51 KB.** Para dashboards internos, es 10x más simple que una SPA.
- **Arquitectura en capas para IA.** Service (habla con Groq) + Router (orquesta HTTP) + Contrato (Form) + Presentación (Jinja2). Cambiar de proveedor LLM toca 1 archivo.
- **Un test rojo puede significar dos cosas:** el código tiene bug (fix código) o el test está mal escrito (fix test). Diagnosticar antes de tocar.
- **TestClient con `httpx2`** (Starlette 1.6.0 deprecó `httpx`).
- **Mock del LLM en tests:** `monkeypatch.setattr("app.routers.chat.consultar_llm", fake)`. Tests deterministas, sin coste de API.
- **Un fix = un commit.** 4 commits en este ciclo IA.1, cada uno con propósito claro.

### 📊 Métricas del ciclo IA.1

- **Commits:** 4 (`03f74a7`, `ed806ea`, `ab72a9e`, `ed11c36`).
- **Archivos nuevos:** 11 (`services/llm_chat.py`, `routers/chat.py`, `templates_config.py`, 2 templates partials, `htmx.min.js`, `test_chat.py`, `__init__.py`s).
- **Líneas:** +321/-2 (chat UI) + 131 (llm_chat) + 10 (templates_config).
- **Tests:** 477 → **487** (+10 chat).
- **Deudas cerradas:** #27.
- **Deudas nuevas:** #28 (Docker), #29 (Postgres), #30 (rate limit), #31 (modelo configurable), #32 (JWT), #33 (IA.2-4).
- **Tiempo total:** ~6 h distribuidas.

### 📈 Scorecard de la oferta (Full Stack VI Región)

| Categoría | Peso | Estado proyecto | Aporta |
|:---|:---:|:---:|:---:|
| Backend / APIs / DB | 20% | 8.5 | 1.70 |
| Frontend / Dashboards | 15% | 8.5 | 1.28 |
| Dominio industrial | 15% | 10 | 1.50 |
| Tests / Calidad / Git | 10% | 9.5 | 0.95 |
| **IA / Automatización IA** | **25%** | **6.5** | **1.63** |
| Cloud / Deployment | 10% | 2 | 0.20 |
| Seguridad | 5% | 3 | 0.15 |
| **TOTAL** | 100% | — | **7.40** |

**Subió de 6.5 (inicio del ciclo) a 7.4.** El bloque IA pasó de 0 a 6.5.

**Siguiente salto:** Deploy Railway (+0.6 en Cloud) + JWT auth (+0.2 en Seguridad) → **~8.2**.

**Techo alcanzable en 2 semanas:** 9.0 (con IA.2-4 + caso real + video demo).

---

> 📌 **Fin del TRASPASO_MAESTRO.**  
> 🗓️ **Última actualización:** Ciclo IA.1 cerrado (commit `ed11c36`). 487 tests verdes. CI 2/2 verde verificado (run #117).  
> 🚀 **Próximo paso:** Fase Deploy.1 — Dockerfile + docker-compose + Railway. Ver sección 11.
