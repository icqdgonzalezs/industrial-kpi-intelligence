# 🎯 TRASPASO MAESTRO — Industrial KPI Intelligence

> 📌 **Propósito:** documento autocontenido para arrancar un chat nuevo sin perder contexto.  
> 📥 **Instrucción de uso:** pegar este archivo completo como **PRIMER** mensaje en un chat nuevo.  
> 🗓️ **Última actualización:** Ciclos 1.B.4 + 1.B.6 + schema-first cerrados. Commit `8ab15be`. **514 tests verdes, CI verde verificado (run #132).** Auth + rate limit (custom) + multi-tenant readiness en producción.  
> 🚀 **Próximo paso:** IA.2 — Diagnóstico asistido por LLM (2 h). Alternativa: migración tab por tab Dash → FastAPI. Ver sección 11.

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
| 13 | 🚫 **Nunca usar `passlib`.** Reemplazado por `bcrypt` directo (passlib 1.7.4 incompatible con bcrypt 5.x). |
| 14 | 🚫 **Nunca usar `python-jose[cryptography]` en este Mac.** Mojave Intel no tiene wheel de `cryptography` ≥50. Usar `PyJWT`. |
| 15 | 🚫 **Nunca pegar bloques >50 líneas en la Terminal ni en Railway Console.** Corrompe caracteres. Usar `pbpaste` o TextEdit. |
| 16 | 🚫 **Nunca tipear secretos con `input()`.** Usar `getpass.getpass()` (no ecoa). |
| 17 | 🚫 **Nunca reutilizar un valor como password y como SECRET_KEY.** Valores distintos por propósito. |
| 18 | 🚫 **Nunca usar slowapi para rate limiting.** Falla en silencio en este entorno. Usar `@rate_limit(max_requests, window_seconds)` de `app.limiter`. |
| 19 | 🗄️ **Migración de schema: DB primero, código después.** ALTER en Railway → recién después el deploy del código nuevo. |
| 20 | 🖱️ **Después de `open -e archivo`, hacer click en la ventana BLANCA de TextEdit antes de pegar.** El foco no cambia automáticamente en macOS. |

> 🚀 **Próximo paso concreto del proyecto:** IA.2 — Diagnóstico asistido por LLM. Alternativa: migración tab por tab Dash → FastAPI. Ver sección 11.

---

## 1️⃣ FICHA DEL PROYECTO

| Campo | Valor |
| :--- | :--- |
| 🏭 **Producto** | Industrial KPI Intelligence — dashboard industrial para PYMES manufactureras LatAm/España |
| 🌐 **Ecosistema** | Primer producto de 6 SaaS (Industrial Operations Intelligence) |
| 🛠️ **Stack legacy (dashboard)** | Python 3.11.9 · Plotly Dash 4.4.1 · Plotly · pandas · numpy |
| 🛠️ **Stack nuevo (API REST)** | FastAPI 0.141.1 · SQLModel 0.0.46 · SQLAlchemy 2.0.54 · Pydantic 2.13.5 · SQLite/Postgres · Jinja2 3.1.6 · Uvicorn 0.53.0 · python-multipart 0.0.32 · psycopg[binary] 3.3.6 |
| 🛠️ **Stack IA (operativo)** | Groq SDK 1.7.0 · Modelo `openai/gpt-oss-120b` · python-dotenv 1.2.3 · HTMX 2.0.4 |
| 🔐 **Stack Seguridad** | PyJWT 2.15.1 · bcrypt 5.0.0 · email-validator 2.3.0 · **rate limiter propio** (slowapi descartado, ver 4.54) |
| ☁️ **Stack Deploy** | Railway (PaaS) · Nixpacks (build automático) · Postgres addon · US West |
| 🧪 **Testing** | pytest 9.1.1 · pytest-cov 7.1.0 · ruff 0.16.6 · httpx2 2.13.1 · GitHub Actions CI/CD |
| 📏 **Estándares aplicables** | ISA-95 · TPM (OEE) · NIST 6.1.3 / ISO 22514 (Pp/Ppk) · AIAG SPC · OWASP · ISA-101 (HMI) · WCAG 2.1 · OpenAPI 3.1 · RFC 7518 (JWT) |
| ⚖️ **Licencia** | Elastic License 2.0 (nunca MIT) |
| 👤 **Usuario** | David González Santibáñez — Ing. Civil Químico + dev autodidacta |
| 📅 **Semana** | 5 de 8 |
| ✅ **Tests actuales** | **514 passed** (460 legacy + 54 app/) |
| 🟢 **CI** | Verde **verificado** (run #132, commit `8ab15be`) |
| 🧹 **Working tree** | Limpio, rama `main` sincronizada con `origin/main`. HEAD: `8ab15be`. |
| 🌐 **URL pública (Railway)** | `https://web-production-bb6a7.up.railway.app/` |
| 📊 **Producto 1 (MVP)** | ~99% (dashboard Dash + API FastAPI + IA + Auth + Rate limit + Multi-tenant readiness + Deploy Railway). Falta IA.2-4 + migración tabs. |
| 🌍 **Ecosistema completo** | ~17% (1 de 6 productos completos, 6 definidos) |
| 🔗 **Repo** | `github.com/icqdgonzalezs/industrial-kpi-intelligence` |
| 📂 **Ruta local** | `/Users/violeta/Projects/industrial-operations-intelligence/industrial-kpi-intelligence` |

---

## 2️⃣ ESTADO ACTUAL EXACTO

### ✅ Cerrado (commiteado + pusheado + CI verde)

**Dashboard Dash legacy (Fase 3b.2 completa):**

- ✅ Bloques UX-1, UX-2, UX-3 (base visual del dashboard)
- ✅ Bloque 3A: adapter EN→ES + loader rewired a dataset canónico (18,078 filas)
- ✅ Refactor thresholds a YAML (SSOT), tipografía ISA-101, iconografía WCAG 2.1 §1.4.1
- ✅ **Fase 3a** (`35d12c4` a `c9a2efb`): Export CSV — 5/5 tabs
- ✅ **Fase 3b.1** (`c91ae39`): loading states
- ✅ **Fase 3b.2 completa** (5 tabs con empty state + cascades)
- ✅ **Perf pre-binning** (`ce2c03f`): histograma Capacidad
- ✅ **Perf WebGL Control** (`e7e5d49`): `go.Scattergl`
- ✅ **Opción D** (`ba0e962`): consolidar `schema_adapter.py` dentro de `data_loader.py`

**Capa API REST (migración CSV → FastAPI):**

- ✅ **Migración CSV → FastAPI + SQLModel + SQLite** (`a162f15`): 7 archivos, +139/-29.
- ✅ **Dashboard Jinja2** (`724f4ac`) + 17 tests iniciales (`0c59acc`).

**Ciclo IA.1 (chat con KPIs — Groq + HTMX):**

- ✅ **`03f74a7`** — `feat(ai): add Groq LLM service for KPI chat`.
- ✅ **`ed806ea`** — `feat(ai): add chat UI with HTMX for KPI queries` (**deuda #27 cerrada**).

**Ciclo Deploy Railway:**

- ✅ **`86845ac`** — `feat(deploy): prepare FastAPI app for Railway deployment`.
- ✅ **`c68d139`** — `fix(db): force psycopg v3 driver in Postgres URL`.
- ✅ **Deploy Railway exitoso**: proyecto `easygoing-caring`, servicio `web` `Online`, Postgres addon vinculado, URL pública operativa.

**Ciclo Auth 1.A (JWT backend):**

- ✅ **`f00ea1e`** — `feat(auth): add JWT authentication with bcrypt password hashing`. PyJWT + bcrypt directo + `get_current_user`.

**Ciclo Auth 1.B.1-2 (endpoints POST + Login UI):**

- ✅ **`f6ac313`** — `feat(auth): protect POST endpoints with JWT dependency`. **Deuda #32 cerrada.**
- ✅ **`4314764`** — `feat(auth): add login UI with HttpOnly cookie + dual auth`. **Deuda #34 cerrada.**

**Ciclo Auth 1.B.3-7 (cierre auth en producción):**

- ✅ **`4ba0cd9`** — `feat(auth): add seed_admin script for first production user`. **Deuda #35 cerrada.**
- ✅ **`SECRET_KEY` + `COOKIE_SECURE=true` en Railway**. **Deudas #37 y #38 cerradas.**
- ✅ **Login end-to-end verificado** en URL pública. Admin `dcgscolchagua@gmail.com` en Postgres prod.

**Ciclo 1.B.4 (tests formales de auth):**

- ✅ **`025aa7e`** — `test(auth): add formal auth test suite (15 tests)`. Cobertura: login (éxito/fallo/422), `/auth/me` (válido/sin token/inválido/expirado), endpoints protegidos (POST /kpis/, POST /chat/), logout (borra cookie, idempotente, sin auth). **Deuda #36 cerrada.**

**Ciclo 1.B.6 (rate limiting custom):**

- ✅ **`d4308ec`** — `feat(chat): add rate limiting (30/min per IP) with custom sliding window`.
  - ✅ **`app/limiter.py`** (nuevo): `@rate_limit(max_requests, window_seconds)` con `deque` de timestamps, ventana deslizante por IP + endpoint.
  - ✅ **`app/routers/chat.py`**: `@rate_limit(30, 60)` en POST /chat/. Alineado con tier gratis de Groq (30 RPM).
  - ✅ **`app/main.py`**: eliminado registro de slowapi + middleware.
  - ✅ **`tests/app/conftest.py`**: fixture autouse que resetea contadores entre tests.
  - ✅ **`tests/app/test_chat.py`**: +2 tests (bajo límite → 200; supera → 429).
  - ✅ **Deuda #30 cerrada.** Slowapi descartado por falla silenciosa (ver 4.54).

**Ciclo Schema-first multi-tenant (tenant_id):**

- ✅ **`8ab15be`** — `feat(models): add tenant_id for multi-tenant readiness`.
  - ✅ **`app/models.py`**: `tenant_id: str = Field(default="default", index=True)` en `User` y `KPI`.
  - ✅ **ALTER TABLE en Postgres prod** (Railway) ejecutado ANTES del deploy. `IF NOT EXISTS` para idempotencia.
  - ✅ **`tests/app/test_models.py`**: +2 tests (KPI y User con default `"default"`).
  - ✅ **Schema-first**: la columna existe ya, el filtrado se activa cuando llegue cliente #2.

### 🟡 En curso

- *Nada.* Working tree limpio. CI #132 verde verificado.

### ⏳ Pendiente inmediato

- ⏳ **IA.2** — Diagnóstico asistido por LLM (2 h). **PRÓXIMO**.
- ⏳ **IA.3** — Reportes ejecutivos narrados (2 h).
- ⏳ **IA.4** — Detección de anomalías ML (3 h).
- ⏳ **Migración tab por tab** Dash → FastAPI (decisión 4.32).

---

## 3️⃣ LÍNEA TEMPORAL DE COMMITS

| Commit | Descripción | Tests |
| :--- | :--- | :---: |
| `8ab15be` | **feat(models): add tenant_id for multi-tenant readiness** | 514 |
| `d4308ec` | **feat(chat): add rate limiting (30/min per IP) with custom sliding window** | 512 |
| `025aa7e` | **test(auth): add formal auth test suite (15 tests)** | 510 |
| `c92cbf` | docs(handoff): close Auth 1.B in production + fix §8 code fence | 495 |
| `4ba0cd9` | **feat(auth): add seed_admin script for first production user** | 495 |
| `25b3652` | Docs(handoff): update TRASPASO with Auth 1.B.2 closed | 495 |
| `4314764` | **feat(auth): add login UI with HttpOnly cookie + dual auth** | 495 |
| `f6ac313` | **feat(auth): protect POST endpoints with JWT dependency** | 494 |
| `f00ea1e` | **feat(auth): add JWT authentication with bcrypt password hashing** | 490 |
| `c68d139` | **fix(db): force psycopg v3 driver in Postgres URL** | 490 |
| `86845ac` | **feat(deploy): prepare FastAPI app for Railway deployment** | 487 |
| `ed11c36` | Fix(deps): remove literal '+' from python-multipart line | 487 |
| `ab72a9e` | Fix(deps): add python-multipart for FastAPI Form parsing | 487 |
| `ed806ea` | **feat(ai): add chat UI with HTMX for KPI queries** | 487 |
| `03f74a7` | **feat(ai): add Groq LLM service for KPI chat** | 477 |
| `0c59acc` | Test(app): add unit + integration tests for FastAPI layer | 477 |
| `724f4ac` | Feat(fastapi): add Jinja2 dashboard for KPI visualization | 460 |
| `a561fff` | Fix(lint): resolve ruff findings in FastAPI layer | 460 |
| `785b0c4` | Fix(ci): restore requirements.txt for both stacks | 460 |
| `54ac5ed` | Chore(gitignore): ignore testing artifacts | 460 |
| `a162f15` | feat: migrar de CSV a FastAPI + SQLModel + SQLite | 460 |
| `85dd7fe` | docs: migrar de CSV a FastAPI + SQLModel + SQLite en README | 460 |
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

> 📈 **Evolución de tests:** 263 → ... → 490 → 494 → 495 → 510 → 512 → **514** (460 legacy + 54 app/).  
> ✅ **CI verde real verificado** (runs #112, #114, #117, #121, #122, #123, #125, #126, #128, #129, #130, #131, #132).

---

## 4️⃣ DECISIONES TÉCNICAS CLAVE

### 4.1 a 4.24 — Dashboard Dash legacy
*(Sin cambios: patrón strangler ADR-0001, SSOT YAML, SPC contextualizado, ISA-101, escala AIAG SPC, empty_state, cascades, perf cache, WebGL, etc.)*

### 4.25 🚀 Coexistencia Dash legacy + FastAPI nuevo
- **Decisión:** la capa FastAPI se construye **en paralelo**, sin tocar el dashboard Dash existente.
- **Estrategia:** `app/` convive con `dashboard/`, `src/`, `tests/`. Migración gradual.
- **Lección:** patrón *strangler* aplicado a nivel de arquitectura completa.

### 4.26 🧩 Separación modelo DB ↔ schema API
- **Solución:** `KPI` (tabla) ≠ `KPICreate` (schema Pydantic).
- **Lección:** arquitectura estándar de FastAPI en producción.

### 4.27 ⏰ Tratamiento del `timestamp` naive en SQLModel 0.0.46
- **Solución adoptada:** `sa_column=Column(DateTime(timezone=False))`.

### 4.28 🔄 Flujo de trabajo con `git clone` en vez de `git init`

### 4.29 🧹 Limpieza del `requirements.txt` post-`pip freeze`

### 4.30 🔒 .gitignore ampliado

### 4.31 🌐 URLs del proyecto
| Servicio | URL |
| :--- | :--- |
| Dashboard Dash (legacy) | `http://127.0.0.1:8050` |
| API FastAPI local + Swagger UI | `http://127.0.0.1:8000/docs` |
| Dashboard Jinja2 + chat IA local | `http://127.0.0.1:8000/` |
| **Producción (Railway)** | **`https://web-production-bb6a7.up.railway.app/`** |
| Swagger producción | `https://web-production-bb6a7.up.railway.app/docs` |

### 4.32 🎯 Migración completa Dash → FastAPI (decisión estratégica)
- **Decisión:** retirar progresivamente `dashboard/` y consolidar toda la presentación en `app/`.
- **Stack elegido:** Jinja2 + HTMX + Plotly.js.
- **Progreso:** Chat IA ✅, auth backend ✅, login UI ✅, seed admin ✅, rate limit ✅, multi-tenant readiness ✅. Falta: migración de tabs, retiro de `dashboard/`.

### 4.33 🔗 `httpx2` reemplaza `httpx` (Starlette 1.6.0)

### 4.34 🧪 SQLModel `table=True` NO valida en construcción

### 4.35 🤖 Groq + `openai/gpt-oss-120b` para el chat IA
- **IDs de modelos LLM son efímeros.** Groq deprecó `llama-3.3-70b-versatile` el 2026-08-16. Usar `openai/gpt-oss-120b`.

### 4.36 🧩 Arquitectura en 4 capas del chat IA
- **Servicio** (`app/services/llm_chat.py`), **Router** (`app/routers/chat.py`), **Contrato** (`Form(...)`), **Presentación** (HTMX + Jinja2).

### 4.37 📦 `python-multipart` es obligatorio para `Form(...)`

### 4.38 🎨 HTMX como reemplazo de callbacks Dash

### 4.39 ☁️ Railway como PaaS (sin Docker local)

### 4.40 🐘 Normalización de URL Postgres (`postgresql://` → `postgresql+psycopg://`)

### 4.41 🔑 bcrypt directo (sin passlib)

### 4.42 🔐 PyJWT en vez de python-jose (Mojave sin wheels de cryptography)

### 4.43 ⏱️ Timing-safe login (previene user enumeration)

### 4.44 🔒 SECRET_KEY de dev con >32 bytes (RFC 7518)

### 4.45 🎫 HS256 explícito (evita alg=none attack)

### 4.46 🍪 Cookie HttpOnly + SameSite=Lax + dual auth (Login UI)

### 4.47 🧭 `HX-Redirect` para navegación server-driven (HTMX)

### 4.48 🔀 Detección `HX-Request` para respuesta polimórfica

### 4.49 🚪 Redirect 302 para `GET /` sin sesión

### 4.50 🍪 Cookie `Secure` condicional por env var (cierre auth prod)

### 4.51 🔑 Seed admin idempotente con env vars (deuda #35)

### 4.52 🔐 Railway aplica env vars vía redeploy, no en caliente

### 4.53 🧪 Rotación de password con write-verify

### 4.54 🚦 Rate limiter propio (descartando slowapi por falla silenciosa)
- **Problema:** `slowapi 0.1.10` con `@limiter.limit("30/minute")` **no enforzaba el límite** en este entorno. El 31° request devolvía 200 en lugar de 429. Sin error, sin warning, sin log. Falla silenciosa.
- **Causa:** slowapi depende de detectar el parámetro `request: Request` en la firma del endpoint. Con `SlowAPIMiddleware` + decorador combinados, ninguno aplica el chequeo. Aun quitando el middleware, el decorador no enforzaba.
- **Solución:** implementación propia en `app/limiter.py` (~40 líneas):
  - `@rate_limit(max_requests, window_seconds)` decorador con `deque` de timestamps.
  - Ventana deslizante por clave `{ip}:{func.__qualname__}`.
  - `HTTPException 429` si se supera el límite.
  - `reset_all()` para tests (fixture `autouse` en conftest).
- **Ventajas:** sin dependencia externa, auditable, testeable, comportamiento determinista.
- **Trade-off:** estado en memoria (no compartido entre workers). Con uvicorn single-worker (Railway default) es suficiente. Si se escala a múltiples workers → migrar a Redis o rate limit en el reverse proxy.
- **Lección:** en seguridad, **fail closed** es el patrón correcto. Una dependencia que falla en silencio es peor que un bug explícito. Cuando una librería no funciona y no avisa, se reemplaza con código propio.

### 4.55 🗂️ Schema-first multi-tenant (`tenant_id`)
- **Decisión:** agregar `tenant_id: str = Field(default="default", index=True)` a `User` y `KPI` **ya**, sin activar el filtrado todavía.
- **Motivo:** multi-tenant prematuro (con un solo cliente) es la causa #1 de reescritura en SaaS. Schema-first, filtering-later.
- **Migración:** ALTER TABLE en Postgres prod **antes** del deploy del código nuevo (si el código corre contra tabla sin la columna → todas las `SELECT` fallan con `column does not exist` → 500 en producción).
- **Idempotencia:** `ADD COLUMN IF NOT EXISTS` + `CREATE INDEX IF NOT EXISTS` en Postgres. Correr la migración dos veces no rompe.
- **Qué NO implementar todavía:** filtrado en queries, endpoint de creación de tenants, dependency `get_current_tenant`. YAGNI hasta que haya cliente #2.
- **Lección:** agregar la columna con la tabla vacía cuesta 5 min. Agregarla con 3 clientes y datos vivos cuesta días (backfill, doble escritura, migración nocturna, plan de rollback, downtime).

### 4.56 🐍 `collections.abc` para ABCs (Python 3.11+)
- **Problema:** ruff UP035 detecta `from typing import Awaitable, Callable, Iterable, Iterator, Mapping, Sequence`.
- **Solución:** en Python 3.11+, importar esos ABCs desde `collections.abc`, no desde `typing`.
- **Excepción:** `Any` sigue viniendo de `typing` (no existe en `collections.abc`).
- **Lección:** los stubs de `typing` para esos símbolos están deprecados. Ruff lo enforce con la regla UP035.

---

## 5️⃣ ESTADO DE TESTS Y CALIDAD

### Tests legacy (460)

| Archivo | Tests |
| :--- | :---: |
| `test_app_layout.py` | 4 |
| `test_capability.py` | 40 |
| `test_capability_callbacks.py` | 25 |
| `test_capability_thresholds.py` | 28 |
| `test_control_charts.py` | 10 |
| `test_control_charts_callbacks.py` | 14 |
| `test_dash_app.py` | 11 |
| `test_data_generator.py` | 15 |
| `test_data_loader.py` | 17 |
| `test_dataset_metadata.py` | 21 |
| `test_diagnostics.py` | 13 |
| `test_diagnostics_callbacks.py` | 14 |
| `test_empty_state.py` | 7 |
| `test_export_helpers.py` | 16 |
| `test_filter_callbacks.py` | 4 |
| `test_filter_engine.py` | 11 |
| `test_kpi_callbacks.py` | 4 |
| `test_kpi_presenter.py` | 4 |
| `test_kpi_thresholds.py` | 19 |
| `test_kpis.py` | 32 |
| `test_oee.py` | 25 |
| `test_oee_presenter.py` | 6 |
| `test_operational_analysis_callbacks.py` | 42 |
| `test_plant_overview.py` | 6 |
| `test_plant_overview_components.py` | 5 |
| `test_quality_performance_callbacks.py` | 15 |
| `test_quality_performance_components.py` | 7 |
| `test_quality_performance_spec.py` | 6 |
| `test_severity_icons.py` | 9 |
| `test_utils.py` | 7 |
| `test_validation.py` | 22 |
| **Subtotal legacy** | **460** |

### Tests de `app/` (54)

| Archivo | Tests | Cobertura |
| :--- | :---: | :--- |
| `tests/app/test_models.py` | 8 | `KPI` SQLModel + `_normalizar_url_db` (3) + `tenant_id` default (2) |
| `tests/app/test_schemas.py` | 5 | `KPICreate`: parseo ISO, coacción, rechazo |
| `tests/app/test_endpoints.py` | 12 | `GET /`, `GET /kpis/`, `POST /kpis/` con `TestClient` |
| `tests/app/test_chat.py` | 12 | `POST /chat/` con mock + 2 de rate limiting |
| `tests/app/test_auth.py` | 15 | Login (5), /auth/me (4), endpoints protegidos (3), logout (3) |
| Tests auth integrados en endpoints | 2 | 401 sin token en POST |
| **Subtotal app/** | **54** | ✅ |

### Fixtures críticas

- `session` → SQLite en memoria (`StaticPool`, `check_same_thread=False`). Aislada por test.
- `client` → `TestClient` con `app.dependency_overrides[get_session]`.
- `mock_llm_ok` → `monkeypatch.setattr` sobre `app.routers.chat.consultar_llm`.
- `auth_headers` → crea user `test@example.com` + JWT válido.
- `_reset_rate_limiter` → **autouse**, resetea contadores del limiter antes/después de cada test.

### Total

> **514 tests passed** (460 legacy + 54 app/). **0 regresiones.**  
> Tiempo: ~80 s suite completa.

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
| **23** | `kpi_database.db` se migra manualmente | Automatización | 🟢 Baja |
| **24** | Doble stack de dashboards (Dash + FastAPI) | Mantenibilidad | 🟡 Media (transitoria) |
| **25** | Pandas 2.1.4 → 3.x | Reproducibilidad | 🟢 Baja |
| **26** | CI no mide cobertura de `app/` | Testing infra | 🟡 Media |
| ~~**27**~~ | ~~Fase IA pendiente~~ | ✅ **CERRADA** (`ed806ea`) | — |
| ~~**28**~~ | ~~Sin Dockerfile~~ | ✅ **CERRADA** (Railway) | — |
| ~~**29**~~ | ~~SQLite en producción~~ | ✅ **CERRADA** (Postgres Railway) | — |
| ~~**30**~~ | ~~Rate limit en `/chat/`~~ | ✅ **CERRADA** (`d4308ec` + `4.54`) | — |
| **31** | `GROQ_MODEL` hardcodeado | Mantenibilidad | 🟢 Baja |
| ~~**32**~~ | ~~POST sin proteger~~ | ✅ **CERRADA** (`f6ac313`) | — |
| **33** | IA.2, IA.3, IA.4 | Features | 🟡 Media |
| ~~**34**~~ | ~~Sin template login~~ | ✅ **CERRADA** (`4314764`) | — |
| ~~**35**~~ | ~~Sin seed admin~~ | ✅ **CERRADA** (`4ba0cd9`) | — |
| ~~**36**~~ | ~~Sin tests formales de auth~~ | ✅ **CERRADA** (`025aa7e`) | — |
| ~~**37**~~ | ~~`SECRET_KEY` no seteada en Railway~~ | ✅ **CERRADA** (Railway Variables) | — |
| ~~**38**~~ | ~~`COOKIE_SECURE=true` no seteado~~ | ✅ **CERRADA** (Railway Variables) | — |
| **39 🆕** | `slowapi` sigue en `requirements.txt` aunque ya no se usa | Limpieza | 🟢 Baja |
| **40 🆕** | Rate limiter propio: en memoria (no distribuido) | Escalabilidad | 🟢 Baja (1 worker) |
| **41 🆕** | `tests/app/test_models.py` importa `User` pero no lo usa directamente en tests previos | Cosmético | 🟢 Baja |

### 📌 Detalle de deudas activas

**Deuda 11 — `schema_adapter.py`:** `grep -rn "schema_adapter" src/ dashboard/ tests/ app/ --include="*.py"` → confirmar que nada lo importa → `git rm` → tests + ruff → commit `chore(cleanup)`.

**Deuda 15 — Doble spinner:** Cascade equipo + reset → 2 fires del store. Fix candidato: `debounce` 200ms.

**Deuda 16 — Semántica color KPIs rendimiento:** 4 KPIs heredan severidad del PPM total. Fix: severidad individual por KPI.

**Deuda 19 — Callback 2104 ms:** Dash Dev Tools. Fix: identificar callback, instrumentar, medir, optimizar.

**Deuda 24 — Doble stack de dashboards:** Transitoria. Retiro cuando Jinja2 cubra funcionalidad.

**Deuda 25 — Pandas 2 → 3:** `requirements.txt` fija `pandas>=2.1,<3`.

**Deuda 26 — Cobertura `app/` en CI:** Agregar `--cov=app`.

**Deuda 31 — `GROQ_MODEL` configurable:** Mover a `os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")`.

**Deuda 39 🆕 — Quitar slowapi de requirements:** `pip uninstall slowapi` → actualizar `requirements.txt` → commit `chore(deps)`. Sin impacto funcional.

**Deuda 40 🆕 — Rate limiter en memoria:** Con uvicorn single-worker (Railway default) es suficiente. Escalar a Redis si se pasa a múltiples workers.

**Deuda 41 🆕 — `User` import en test_models:** El import `from app.models import KPI, User` es ahora necesario por los 2 tests nuevos. No es deuda real, se documenta por transparencia.

---

## 7️⃣ ROADMAP PENDIENTE

| Fase | Fix / Feature | Estimación | Prioridad |
| :--- | :--- | :---: | :---: |
| **IA.2** | **Diagnóstico asistido por LLM** | 2 h | 🟡 Media — **PRÓXIMO** |
| **IA.3** | Reportes ejecutivos narrados | 2 h | 🟡 Media |
| **IA.4** | Detección de anomalías ML | 3 h | 🟡 Media |
| Seg.3 | CORS configurado | 30 min | 🟡 Media |
| Auto | APScheduler (ingesta CSV programada) | 2 h | 🟡 Media |
| Integración | Webhook `POST /webhooks/ingest` + API key | 2 h | 🟡 Media |
| Caso real | 3-5 entrevistas con usuario de planta + video demo | 4 h | 🟡 Media |
| Migración | Tab Diagnóstico (sin gráficos) | 4 h | 🟠 Media |
| Migración | Tab Calidad (Pareto + KPIs) | 6 h | 🟠 Media |
| Migración | Tab Capacidad (histograma + Pp/Ppk) | 8 h | 🟠 Media |
| Migración | Tab Control (I-MR + Western Electric) | 8 h | 🟠 Media |
| Migración | Tab Operacional (ranking + drill-down) | 8 h | 🟠 Media |
| Migración | Eliminar `dashboard/` legacy + ajustar CI | 4 h | 🟠 Media |
| Deuda | Eliminar `schema_adapter.py` (#11) | 1 h | 🔴 Alta |
| Deuda | Debounce cascade (#15) | 30 min | 🟡 Media |
| Deuda | Severidad KPIs rendimiento (#16) | 1.5 h | 🟡 Media |
| Deuda | Callback 2104 ms Calidad (#19) | 1-2 h | 🟡 Media |
| Deuda | `GROQ_MODEL` configurable (#31) | 15 min | 🟢 Baja |
| Deuda | Quitar `slowapi` de requirements (#39) | 10 min | 🟢 Baja |

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
| PAT con scope `repo` + `workflow`. | Nunca password en texto plano. |
| `git pull origin main --rebase` tras Web Editor. | Nunca `git pull` sin `--rebase`. |
| `git status` ANTES y DESPUÉS del `git add`. | Asumir que el add agregó todo. |
| 1 fix = 1 commit = 1 lista corta de archivos. | Commit con 6+ archivos mezclados. |
| **`git clone` en vez de `git init`** cuando ya hay historial. | `git init` + `remote add` + push. |
| **Quitar el `+` inicial** al pegar un diff en editor. | Pegar el `+` literal. |

### ✍️ Commits

- **Conventional Commits:** `feat:`, `fix:`, `refactor:`, `docs:`, `style:`, `test:`, `chore:`, `polish:`, `perf:`.
- **Un fix = un commit.** No mezclar propósitos.
- **Título en inglés**, cuerpo en español si aplica.
- **Antes de cambiar un string de UI:** `grep -rn "string_viejo" src/ dashboard/ app/ tests/`.

### 🤖 CI/CD

- **2/2 checks verdes antes de mergear.** Sin excepción.
- **Ningún push sin verificar el run CI anterior.**
- **Verificar con `curl`:**

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
- **Arquitectura nueva:** `app/` (FastAPI + SQLModel + Jinja2 + HTMX).
  - `app/routers/`: orquestación HTTP.
  - `app/services/`: lógica pura, sin HTTP.
  - `app/templates/`: Jinja2 (render server-side).
  - `app/auth.py`: JWT + bcrypt + `get_current_user(+_optional)`.
  - `app/limiter.py`: rate limiter propio (deque de timestamps).
- **Nomenclatura:** capacidad `world_class` / `capable` / `marginal` / `not_capable`.

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
- Después de ~40-50 mensajes densos.
- Inmediatamente si aparecen 2+ síntomas de degradación.

**Cómo cambiar (protocolo):**
1. Cerrar el ciclo en curso (commit + push + CI verde).
2. Actualizar `TRASPASO_MAESTRO` con los últimos commits + sección 11.
3. Commit + push del `TRASPASO`.
4. `git pull origin main --rebase` para sincronizar local.
5. Abrir chat nuevo.
6. Pegar el mensaje de transición (sección 12) + TRASPASO completo.

### 🆕 Reglas nuevas (ciclo IA.1 + Deploy + Auth + Rate limit + Tenant)

- **Nunca pegar el `+` inicial de un diff en un archivo de config.**
- **`python-multipart` es obligatorio para `Form(...)`, `File(...)`, `UploadFile(...)`.**
- **Los IDs de modelos LLM son efímeros.** Configurable desde env.
- **Nunca exponer secrets con `cat .env`.** Verificar con `grep -c` o `python -c`.
- **`passlib` está obsoleto.** Usar `bcrypt` directo.
- **`python-jose[cryptography]` no tiene wheels para Mojave Intel.** Usar `PyJWT`.
- **SQLAlchemy no adivina el driver Postgres.** URL explícita: `postgresql+psycopg://`.
- **Timing-safe check en login.** bcrypt corre siempre.
- **`algorithms=["HS256"]` explícito en PyJWT.**
- **SECRET_KEY de dev >32 bytes** (RFC 7518).
- **Cookie HttpOnly + SameSite=Lax para navegador; Bearer para API.**
- **Cookie `Secure` condicional por env var.** Nunca hardcodear.
- **HTMX necesita `hx-ext="json-enc"`** cuando el endpoint espera JSON.
- **`HX-Redirect` para navegación server-driven.**
- **`GET /` protegido con redirect 302 a `/login`.**
- **`GET /` protegido con redirect 302 a `/login`.**
- **Nunca pegar bloques >50 líneas en la Terminal ni en Railway Console.** Usar `pbpaste` o TextEdit.
- **Nunca tipear secretos con `input()`.** Usar `getpass.getpass()`.
- **Nunca reutilizar el mismo valor como password y como SECRET_KEY.**
- **Railway aplica env vars vía redeploy, no en caliente.**
- **Write-verify en operaciones sobre credenciales.**
- **Seed admin idempotente.**
- **🆕 Slowapi falla en silencio en este entorno.** Usar `@rate_limit` de `app.limiter`.
- **🆕 En Python 3.11+: `Awaitable`, `Callable`, `Iterable`, `Iterator`, `Mapping`, `Sequence` se importan desde `collections.abc`, no desde `typing`.**
- **🆕 Después de `open -e archivo`, hacer click en la ventana BLANCA de TextEdit antes de `Cmd+A` / `Cmd+V`.**
- **🆕 Si bash escupe errores de sintaxis durante un paste grande, verificar con `grep` si el archivo destino quedó bien.**
- **🆕 Migración de schema: DB primero, código después.**
- **🆕 Rate limiter propio en `app/limiter.py` (deque de timestamps), no slowapi.**

---

## 9️⃣ ⚠️ HISTORIAL DE ERRORES — NO REPETIR

| ❌ Error | ✅ Correcto |
| :--- | :--- |
| **Pegar `+python-multipart>=0.0.20,<1` en `requirements.txt`.** | Quitar el `+` inicial. |
| **Usar `llama-3.3-70b-versatile` (deprecado 2026-08-16).** | Usar `openai/gpt-oss-120b`. |
| **`cat .env` para verificar la key.** | `python -c "from dotenv import load_dotenv; import os; ..."`. |
| **Pegar la API key completa en el chat.** | Enmascararla. Si se expone, rotarla. |
| **Escribir "CI verde" sin verificar Actions.** | `curl` a la API ANTES. |
| **Confundir "tests verdes locales" con "CI verde".** | Local usa venv ya poblado; CI arranca de cero. |
| **Usar `python-jose[cryptography]` en Mojave Intel.** | Usar `PyJWT`. |
| **Usar `passlib` con bcrypt 5.x.** | Usar `bcrypt` directo. |
| **Usar `datetime.now(timezone.utc)` (ruff UP017).** | Usar `datetime.now(UTC)`. |
| **Dejar `algorithms=None` en PyJWT.** | `algorithms=[ALGORITHM]` con `ALGORITHM="HS256"` fijo. |
| **URL Postgres sin driver explícito.** | `postgresql+psycopg://...`. |
| **Mismo tiempo de respuesta para email existe/no existe.** | bcrypt siempre corre (dummy hash). |
| **SECRET_KEY de dev <32 bytes.** | >32 bytes (RFC 7518). |
| **Poner `hx-post` sin `hx-ext="json-enc"`.** | Agregar `hx-ext="json-enc"` al form. |
| **Esperar que `hx-post` navegue el browser.** | Devolver `HX-Redirect: /`. |
| **Dejar `GET /` público.** | Redirect 302 a `/login`. |
| **`mkdir -p ~/...` sin verificar dónde está el proyecto.** | `git remote -v` + `ls ~/Projects/`. |
| **`pip3 freeze > requirements.txt` en Python global.** | Escribir a mano. |
| **`git init` + `git remote add` cuando ya hay historial.** | `git clone` + `cp -R`. |
| **Asumir que `NaiveDatetime` es importable desde `sqlmodel`.** | `sa_column=Column(DateTime(timezone=False))`. |
| **Asumir que `KPI(nombre=None)` levanta `ValidationError`.** | SQLModel `table=True` NO valida. |
| **Enviar `"id": 0` en POST a FastAPI.** | `id` es autoincremental. |
| **`git push` sin PAT.** | PAT con scope `repo` + `workflow`. |
| **`rm -rf` sin backup.** | Backup con `mv` a `.bak`. |
| **`sed -i ''` con `\n` en macOS.** | Usar `perl -i -pe` o heredoc. |
| **Pegar bloques >50 líneas en la Terminal con `Cmd+V`.** | `pbpaste > archivo` o TextEdit. |
| **Usar `input()` para password en consola no interactiva.** | `getpass.getpass()` no ecoa. |
| **Pegar password/SECRET_KEY en el chat.** | Rotar inmediatamente. |
| **Reutilizar el mismo valor como password y SECRET_KEY.** | Valores distintos por propósito. |
| **Correr `curl` desde dentro del contenedor Railway.** | `curl` desde tu Mac. |
| **Setear env vars de Railway desde la consola del contenedor.** | Railway UI → Variables → Deploy. |
| **Verificar `SECRET_KEY set` en la consola del deployment viejo.** | Confirmar hash del deployment nuevo + `Online` sin `Building`. |
| **Rotar password a ciegas sin verificar el round-trip.** | `assert verify_password(pw, hash_password(pw))` antes y después del commit. |
| **Confundir 401 con 422 en login.** | Leer el código. Cada código HTTP apunta a una capa distinta. |
| **Tipear la password en `read -s` sin prompt visible.** | `read -rs -p "prompt: " VAR`. |
| **Copiar de MacPass y pegar en `read -s`: agregar `\r` (33 chars en vez de 32).** | Limpiar con `tr -d '[:space:]'`. |
| **Pegar un JWT completo en el chat.** | Redactar como `<TOKEN>`. |
| **Heredoc (`cat > file << EOF`) con >100 líneas desde el chat.** | TextEdit o `pbpaste`. |
| **🆕 Usar slowapi para rate limiting.** | Usar `@rate_limit` de `app.limiter`. |
| **🆕 Combinar `@limiter.limit` con `SlowAPIMiddleware`.** | Elegir uno solo. Combinar = silencio. |
| **🆕 Pegar Python en la Terminal pensando que es TextEdit.** | Verificar barra de título antes de pegar. |
| **🆕 Deployar código que usa una columna nueva sin haberla creado en DB.** | ALTER primero, deploy después. |
| **🆕 Importar `Awaitable`/`Callable` desde `typing`.** | Importar desde `collections.abc`. |
| **🆕 Asumir que un paste falló porque bash ladró.** | Verificar con `grep`/`cat` el archivo destino. |

---

## 🔟 📁 ARCHIVOS CLAVE Y COMANDOS

### 🗂️ Estructura del proyecto (post schema-first)

```text
industrial-kpi-intelligence/
├── README.md                              # 514 tests + badges
├── VISION.md
├── ARCHITECTURE.md
├── CHANGELOG.md
├── LICENSE                                # Elastic License 2.0
├── pyproject.toml
├── requirements.txt
├── Procfile                               # uvicorn app.main:app --host 0.0.0.0 --port $PORT
├── .env                                   # GROQ_API_KEY (gitignored)
├── .gitignore
├── .github/workflows/tests.yml            # Workflow "CI"
├── assets/style.css
│
├── app/                                   # CAPA FASTAPI
│   ├── main.py                            # FastAPI + lifespan + routers + GET / (302 si no auth)
│   ├── models.py                          # SQLModel KPI + User (con tenant_id)
│   ├── schemas.py                         # Pydantic KPICreate + UserLogin + UserCreate + UserPublic + Token
│   ├── db.py                              # DATABASE_URL + _normalizar_url_db + create_db_and_tables + get_session
│   ├── auth.py                            # JWT (PyJWT) + bcrypt + get_current_user(+_optional)
│   ├── limiter.py                         # 🆕 Rate limiter propio (deque de timestamps)
│   ├── templates_config.py
│   ├── routers/
│   │   ├── auth.py                        # POST /auth/login + POST /auth/logout + GET /auth/me
│   │   └── chat.py                        # POST /chat/ (con @rate_limit(30, 60))
│   ├── services/
│   │   └── llm_chat.py                    # Groq + construir_contexto + consultar_llm
│   └── templates/
│       ├── index.html
│       ├── login.html
│       └── partials/
│           ├── _chat.html
│           └── _chat_response.html
│
├── static/js/htmx.min.js                  # HTMX 2.0.4
├── config/
├── dashboard/                             # Legacy Dash (EN RETIRADA)
├── data/
├── docs/
│   ├── adr/
│   └── TRASPASO_MAESTRO.md
├── imagenes/
├── scripts/
│   └── seed_admin.py                      # Crea primer admin desde env vars
├── src/                                   # Lógica legacy
│   ├── capability.py
│   ├── control_charts.py
│   ├── kpis.py
│   ├── oee.py
│   ├── diagnostics.py
│   └── schema_adapter.py                  # PENDIENTE eliminar (deuda #11)
├── migrate_csv.py
├── kpi_database.db                        # Local, gitignored
│
└── tests/
    ├── app/
    │   ├── conftest.py                    # + auth_headers + _reset_rate_limiter
    │   ├── test_models.py                 # 8
    │   ├── test_schemas.py                # 5
    │   ├── test_endpoints.py              # 12
    │   ├── test_chat.py                   # 12
    │   └── test_auth.py                   # 15
    └── ... (460 legacy)
```

### ⌨️ Comandos verificados

```bash
# Protocolo de arranque
cd /Users/violeta/Projects/industrial-operations-intelligence/industrial-kpi-intelligence
source venv/bin/activate
which python                    # DEBE mostrar .../venv/bin/python

# Gates
pytest                          # 514 passed (~80 s)
pytest tests/app/ -v            # 54 passed (~1 s)
ruff check .                    # All checks passed!

# Arrancar API FastAPI + dashboard + chat local
uvicorn app.main:app --reload   # http://127.0.0.1:8000/login
lsof -ti:8000 | xargs kill -9

# Arrancar dashboard Dash (legacy)
python -m dashboard.dash_app    # http://127.0.0.1:8050
lsof -ti:8050 | xargs kill -9

# Verificar URL pública
curl -s -o /dev/null -w "GET /      → %{http_code}\n" https://web-production-bb6a7.up.railway.app/
curl -s -o /dev/null -w "GET /login → %{http_code}\n" https://web-production-bb6a7.up.railway.app/login
curl -s -o /dev/null -w "GET /docs  → %{http_code}\n" https://web-production-bb6a7.up.railway.app/docs

# Test login en producción
read -rs -p "pw: " PW && PW=$(printf '%s' "$PW" | tr -d '[:space:]') && \
  curl -si -X POST "https://web-production-bb6a7.up.railway.app/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"dcgscolchagua@gmail.com\",\"password\":\"$PW\"}" \
  | grep -iE "^(HTTP|set-cookie)"; unset PW

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

### 📋 IA.2 — Diagnóstico asistido por LLM (2 h)

**Contexto:** el ciclo Auth 1.B + rate limit + schema-first está cerrado. El proyecto tiene:
- Auth completo en producción (login + cookie HttpOnly + rate limit + admin).
- Chat IA operativo con Groq.
- Multi-tenant readiness (columna `tenant_id` en `User` y `KPI`).
- 514 tests verdes. CI #132 verde.

**Qué es IA.2:**

Un endpoint nuevo `GET /diagnostics/ai` (o similar) que:
1. Carga los KPIs recientes + reglas de diagnóstico del dominio (R1-R4 de `src/diagnostics.py`).
2. Arma un prompt industrial con el contexto (qué está fuera de control, qué es capacidad marginal, qué defecto subió).
3. Llama a Groq con system prompt específico de "ingeniero de procesos senior".
4. Devuelve un diagnóstico narrado en lenguaje natural: *"La línea L1 tiene Cp=1.15 con Ppk=0.92. El proceso está descentrado hacia el límite superior, no disperso. Recomiendo ajustar la media…"*.
5. Se renderiza en el dashboard Jinja2 (tab Diagnóstico, nuevo) o como partial HTMX.

**Cambios:**

| # | Archivo | Acción |
|:---:|:---|:---|
| 1 | `app/services/llm_diagnostics.py` | **Nuevo** — prompt + llamada a Groq + parseo |
| 2 | `app/routers/diagnostics.py` | **Nuevo** — endpoint `GET /diagnostics/ai` |
| 3 | `app/templates/partials/_diagnostics_ai.html` | **Nuevo** — render del diagnóstico |
| 4 | `app/templates/index.html` | Agregar sección o tab |
| 5 | `app/main.py` | `include_router(diagnostics_router)` |
| 6 | `tests/app/test_diagnostics.py` | **Nuevo** — 5-8 tests con mock del LLM |

**Reutilización:**
- `app/services/llm_chat.py` como referencia (mismo Groq client, mismos mocks).
- Reglas de `src/diagnostics.py` (ya existen y están testeadas).
- Fixture `mock_llm_ok` (ya existe, extender a diagnostics).
- Rate limit (`@rate_limit`) — aplicarlo también al nuevo endpoint.

**Estimación:** 2 h.

---

### 📋 Alternativa — Migración tab por tab Dash → FastAPI

Si preferís avanzar en la retirada del Dash legacy (decisión 4.32), el orden propuesto es:

| Fase | Tab | Estimación |
|:---:|:---|:---:|
| 1 | Tab Diagnóstico (sin gráficos) | 4 h |
| 2 | Tab Calidad (Pareto + KPIs) | 6 h |
| 3 | Tab Capacidad (histograma + Pp/Ppk) | 8 h |
| 4 | Tab Control (I-MR + Western Electric) | 8 h |
| 5 | Tab Operacional (ranking + drill-down) | 8 h |
| 6 | Eliminar `dashboard/` legacy + ajustar CI | 4 h |

**Ventaja:** producto vendible single-stack.
**Desventaja:** 5-6 ciclos largos, con mucho riesgo de regresión visual.

**Recomendación:** IA.2 primero. El Dashboard Dash sigue funcional como fallback. Migrarlo puede esperar a tener 1-2 clientes que justifiquen el ROI.

---

⏱️ **Después de IA.2:**

1. **IA.3** — Reportes ejecutivos narrados (2 h).
2. **IA.4** — Detección de anomalías ML (3 h).
3. **Caso real** — 3-5 entrevistas con usuario de planta + video demo (4 h).
4. **Migración tab por tab** (decisión 4.32).

---

## 1️⃣2️⃣ 💬 MENSAJE DE TRANSICIÓN (para pegar en chat nuevo)

```text
Contexto: pego abajo el TRASPASO_MAESTRO del proyecto Industrial KPI Intelligence.
Soy David, Ing. Civil Químico + dev autodidacta, semana 5/8.

Estado: Ciclos 1.B.4 (tests formales de auth), 1.B.6 (rate limit custom),
y schema-first multi-tenant (tenant_id) cerrados. HEAD 8ab15be.
CI #132 verde. 514 tests passed (460 legacy + 54 app/).
URL pública: https://web-production-bb6a7.up.railway.app/

Cerrado en las últimas 5 sesiones:
- Test suite formal de auth (15 tests): commit 025aa7e
- Rate limiter propio (slowapi descartado por falla silenciosa): commit d4308ec
- tenant_id en User + KPI + ALTER Postgres: commit 8ab15be

Estado del deploy:
- URL pública operativa (Railway + Postgres).
- Auth completo end-to-end verificado en prod.
- Rate limit funcional (429 al 31° request en la misma ventana).
- Columna tenant_id en Postgres prod.

Próximo paso: IA.2 — Diagnóstico asistido por LLM.
Alternativa: migración tab por tab Dash → FastAPI.
Estimación total: ~2h. Ver sección 11 del TRASPASO.

Deudas activas relevantes:
- #11 eliminar schema_adapter.py (alta, legacy)
- #15 debounce cascade (media, legacy)
- #16 severidad individual KPIs (media, legacy)
- #19 callback 2104 ms (media, legacy)
- #26 CI no mide cobertura app/ (media)
- #25 pandas 2→3 (baja, diferida)
- #31 GROQ_MODEL configurable (baja)
- #39 quitar slowapi de requirements (baja)
- #40 rate limiter en memoria (baja, 1 worker)
- #41 import User en test_models (cosmético)

Reglas clave (ver sección 8 completa):
- Protocolo de arranque: cd + source venv/bin/activate + which python
- Leer el archivo antes de tocar
- git status ANTES y DESPUÉS de cada git add
- Un fix = un commit
- Verificación visual ⌘ + Shift + R obligatoria
- pytest + ruff verdes antes de commitear
- NINGÚN push sin verificar el run CI anterior con curl a la API
- requirements.txt debe reproducir el venv real (--dry-run)
- Nunca pegar el '+' inicial de un diff en config
- python-multipart obligatorio para Form/File en FastAPI
- Los IDs de modelos LLM son efímeros
- NUNCA exponer secrets con cat .env
- PyJWT, NO python-jose
- bcrypt directo, NO passlib
- SQLAlchemy no adivina driver Postgres: postgresql+psycopg://
- Timing-safe login: bcrypt corre siempre
- algorithms=["HS256"] explícito
- SECRET_KEY dev >32 bytes (RFC 7518)
- Cookie HttpOnly + SameSite=Lax para navegador; Bearer para API
- Cookie Secure condicional (env var COOKIE_SECURE)
- HTMX con hx-ext="json-enc" si el endpoint espera JSON
- HX-Redirect para navegación server-driven
- GET / protegido con redirect 302 a /login
- SQLModel table=True NO valida; usar schemas.py
- FastAPI TestClient usa httpx2
- Nunca pegar bloques >50 líneas en la Terminal ni en Railway Console
- Nunca tipear secretos con input(); usar getpass
- Nunca reutilizar password como SECRET_KEY
- Railway aplica env vars vía redeploy, no en caliente
- Write-verify en operaciones sobre credenciales
- Seed admin idempotente
- Slowapi falla en silencio: usar @rate_limit de app.limiter
- En Python 3.11+: Awaitable/Callable desde collections.abc
- Después de open -e archivo, click en TextEdit antes de pegar
- Si bash ladra durante un paste, verificar con grep el archivo destino
- Migración de schema: DB primero, código después

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
- Cuando te equivoques, decilo claro y corregí.

### 🏆 Hitos acumulados

- ✅ **Fase 3a completa** (5/5 tabs con export CSV).
- ✅ **Migración a FastAPI + SQLModel** (`a162f15`).
- ✅ **Dashboard Jinja2 operativo** (`724f4ac`).
- ✅ **Chat IA con Groq operativo** (`ed806ea`).
- ✅ **Deploy exitoso en Railway** con Postgres.
- ✅ **Auth JWT backend operativo** (`f00ea1e`).
- ✅ **Endpoints POST protegidos** (`f6ac313`).
- ✅ **Login UI con cookie HttpOnly + dual auth + logout** (`4314764`).
- ✅ **Seed admin script** (`4ba0cd9`).
- ✅ **`SECRET_KEY` real + `COOKIE_SECURE=true` en Railway.**
- ✅ **Login verificado end-to-end en producción.**
- ✅ **Test suite formal de auth** (15 tests, `025aa7e`).
- ✅ **Rate limiter propio** (slowapi descartado, `d4308ec`).
- ✅ **Multi-tenant readiness** (`tenant_id` en User + KPI, `8ab15be`).
- ✅ **514 tests, 0 regresiones.**

### 🔬 Lecciones metodológicas del ciclo 1.B.4 + 1.B.6 + Schema

- **Los tests atrapan los bugs que en producción son carísimos.** El test de rate limit detectó que slowapi no enforzaba. Sin él, hubieras descubierto el problema cuando Groq bloqueara tu API por abuso.
- **Dependencias que fallan en silencio son peores que bugs explícitos.** Slowapi no avisó, no logueó, solo no hizo. Reemplazarlo con 40 líneas de código propio fue la decisión correcta.
- **Fail closed > fail open.** En seguridad, si no podés verificar, rechazá. Nunca "pasar porque no hay error".
- **Migración DB primero, código después.** ALTER en Railway → deploy. Si el deploy va primero, todas las `SELECT` fallan con `column does not exist`.
- **Schema-first es barato hoy, carísimo mañana.** Agregar la columna con la tabla casi vacía cuesta 5 min. Con 3 clientes y datos vivos cuesta días.
- **Un test que "pasa por la razón equivocada" es peor que no tenerlo.** `<token-forjado>` literal no prueba nada. Los tests deben reproducir la condición real.
- **El foco en macOS no cambia automáticamente al abrir una ventana.** `open -e archivo` abre TextEdit pero deja el foco en la Terminal si no clickeás.
- **Si bash ladra durante un paste, no asumas que el archivo quedó mal.** Verificá con `grep`/`cat`. A veces el paste llegó al destino correcto y bash procesó pedazos sueltos.
- **`collections.abc` > `typing` para ABCs en Python 3.11+.** Ruff UP035 lo enforce.
- **La regla del "un paste chico por vez" aplica a Railway Console también.** Los heredocs largos se corrompen igual.

### 📊 Métricas del ciclo 1.B.4 + 1.B.6 + Schema

- **Commits:** 4 (`c92cbf`, `025aa7e`, `d4308ec`, `8ab15be`).
- **Archivos nuevos:** `app/limiter.py`, `tests/app/test_auth.py`.
- **Archivos modificados:** `app/main.py`, `app/models.py`, `app/routers/chat.py`, `tests/app/conftest.py`, `tests/app/test_chat.py`, `tests/app/test_models.py`.
- **Tests:** 495 → 510 → 512 → **514**.
- **Deudas cerradas:** #30 (rate limit), #36 (tests auth).
- **Deudas nuevas:** #39 (quitar slowapi de requirements), #40 (rate limiter no distribuido), #41 (import cosmético).
- **Scorecard:** Seguridad subió de 9.0 → **9.3**.

### 📈 Scorecard de la oferta (Full Stack VI Región)

| Categoría | Peso | Estado proyecto | Aporta |
|:---|:---:|:---:|:---:|
| Backend / APIs / DB | 20% | 9.0 | 1.80 |
| Frontend / Dashboards | 15% | 8.5 | 1.28 |
| Dominio industrial | 15% | 10 | 1.50 |
| Tests / Calidad / Git | 10% | 9.5 | 0.95 |
| **IA / Automatización IA** | **25%** | **7.5** | **1.88** |
| **Cloud / Deployment** | **10%** | **8.0** | **0.80** |
| Seguridad | 5% | 9.3 | 0.47 |
| **TOTAL** | 100% | — | **8.68** |

**Subió de 8.41 → ~8.68.** El bloque Seguridad subió de 8.0 → 9.0 (auth prod) → 9.3 (rate limit custom + tests formales + multi-tenant readiness).

**Siguiente salto:** cerrar IA.2-4 → **~9.2**. Con caso real + video demo → **~9.4**.

**Techo alcanzable en 2 semanas:** 9.4.

---

> 📌 **Fin del TRASPASO_MAESTRO.**  
> 🗓️ **Última actualización:** Ciclos 1.B.4 + 1.B.6 + schema-first cerrados. Commit `8ab15be`. 514 tests verdes. CI verde verificado (run #132).  
> 🚀 **Próximo paso:** IA.2 — Diagnóstico asistido por LLM. Ver sección 11.
