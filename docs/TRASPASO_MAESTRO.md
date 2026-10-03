# 🎯 TRASPASO MAESTRO — Industrial KPI Intelligence

> 📌 **Propósito:** documento autocontenido para arrancar un chat nuevo sin perder contexto.  
> 📥 **Instrucción de uso:** pegar este archivo completo como **PRIMER** mensaje en un chat nuevo.  
> 🗓️ **Última actualización:** Bloque 1.B.1 + 1.B.2 (Auth endpoints + Login UI) cerrados. Commit `4314764` pusheado. **495 tests verdes, CI 2/2 verde verificado (run #126).**  
> 🚀 **Próximo paso:** Bloque 1.B.3-6 — Cerrar auth en producción (seed admin + SECRET_KEY + tests + rate limit). Ver sección 11.

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

> 🚀 **Próximo paso concreto del proyecto:** Bloque 1.B.3 — `scripts/seed_admin.py` (crear admin en Railway). Ver sección 11.

---

## 1️⃣ FICHA DEL PROYECTO

| Campo | Valor |
| :--- | :--- |
| 🏭 **Producto** | Industrial KPI Intelligence — dashboard industrial para PYMES manufactureras LatAm/España |
| 🌐 **Ecosistema** | Primer producto de 6 SaaS (Industrial Operations Intelligence) |
| 🛠️ **Stack legacy (dashboard)** | Python 3.11.9 · Plotly Dash 4.4.1 · Plotly · pandas · numpy |
| 🛠️ **Stack nuevo (API REST)** | FastAPI 0.141.1 · SQLModel 0.0.46 · SQLAlchemy 2.0.54 · Pydantic 2.13.5 · SQLite/Postgres · Jinja2 3.1.6 · Uvicorn 0.53.0 · python-multipart 0.0.32 · psycopg[binary] 3.3.6 |
| 🛠️ **Stack IA (operativo)** | Groq SDK 1.7.0 · Modelo `openai/gpt-oss-120b` · python-dotenv 1.2.3 · HTMX 2.0.4 |
| 🔐 **Stack Seguridad** | PyJWT 2.15.1 · bcrypt 5.0.0 · slowapi 0.1.10 · email-validator 2.3.0 |
| ☁️ **Stack Deploy** | Railway (PaaS) · Nixpacks (build automático) · Postgres addon · US West |
| 🧪 **Testing** | pytest 9.1.1 · pytest-cov 7.1.0 · ruff 0.16.6 · httpx2 2.13.1 · GitHub Actions CI/CD |
| 📏 **Estándares aplicables** | ISA-95 · TPM (OEE) · NIST 6.1.3 / ISO 22514 (Pp/Ppk) · AIAG SPC · OWASP · ISA-101 (HMI) · WCAG 2.1 · OpenAPI 3.1 · RFC 7518 (JWT) |
| ⚖️ **Licencia** | Elastic License 2.0 (nunca MIT) |
| 👤 **Usuario** | David González Santibáñez — Ing. Civil Químico + dev autodidacta |
| 📅 **Semana** | 4 de 8 |
| ✅ **Tests actuales** | **495 passed** (460 legacy + 35 app/) |
| 🟢 **CI** | 2/2 verde **verificado** (run #126, commit `4314764`) |
| 🧹 **Working tree** | Limpio, rama `main` sincronizada con `origin/main`. HEAD: `4314764`. |
| 🌐 **URL pública (Railway)** | `https://web-production-bb6a7.up.railway.app/` |
| 📊 **Producto 1 (MVP)** | ~97% (dashboard Dash + API FastAPI + IA + Auth UI + Deploy Railway). Falta seed admin + SECRET_KEY real + rate limit. |
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
- ✅ **Fase 3b.1** (`c91ae39`): loading states
- ✅ **Perf pre-binning** (`ce2c03f`): histograma Capacidad
- ✅ **Perf WebGL Control** (`e7e5d49`): `go.Scattergl`
- ✅ **Componente empty_state** (`6a0547e`)
- ✅ **Fase 3b.2 completa** (5 tabs con empty state + cascades)
- ✅ **Opción D** (`ba0e962`): consolidar `schema_adapter.py` dentro de `data_loader.py`

**Capa API REST (migración CSV → FastAPI):**

- ✅ **Migración CSV → FastAPI + SQLModel + SQLite** (`a162f15`): 7 archivos, +139/-29.
  - ✅ `app/models.py` — Modelo `KPI` con `sa_column=Column(DateTime(timezone=False))`.
  - ✅ `app/schemas.py` — Schema `KPICreate` (BaseModel puro).
  - ✅ `app/db.py` — SQLite + `create_db_and_tables()` + `get_session()`.
  - ✅ `app/main.py` — FastAPI con `lifespan`, `GET /kpis/` y `POST /kpis/`.
  - ✅ `migrate_csv.py` — Script de migración CSV → SQLite.

**Ciclo #21 + #22 (dashboard Jinja2 + tests app/):**

- ✅ **`54ac5ed`** — `chore(gitignore): ignore testing artifacts`.
- ✅ **`785b0c4`** — `fix(ci): restore requirements.txt for both stacks`.
- ✅ **`a561fff`** — `fix(lint): resolve ruff findings in FastAPI layer`.
- ✅ **`724f4ac`** — `feat(fastapi): add Jinja2 dashboard for KPI visualization` (**deuda #21 cerrada**).
- ✅ **`0c59acc`** — `test(app): add unit + integration tests for FastAPI layer` (**deuda #22 cerrada**). 17 tests con `TestClient` + SQLite en memoria.

**Ciclo IA.1 (chat con KPIs — Groq + HTMX):**

- ✅ **`03f74a7`** — `feat(ai): add Groq LLM service for KPI chat`. Cliente Groq async singleton + constructor de contexto + system prompt industrial.
- ✅ **`ed806ea`** — `feat(ai): add chat UI with HTMX for KPI queries` (**deuda #27 cerrada**). Router `POST /chat/` + templates `_chat.html` / `_chat_response.html` + HTMX 2.0.4 + CSS.
- ✅ **`ab72a9e`** — `fix(deps): add python-multipart for FastAPI Form parsing` (histórico).
- ✅ **`ed11c36`** — `fix(deps): remove literal '+' from python-multipart line`. CI #117 verde.

**Ciclo Deploy Railway:**

- ✅ **`86845ac`** — `feat(deploy): prepare FastAPI app for Railway deployment`. 3 archivos: `Procfile` (uvicorn en vez de gunicorn Dash), `app/db.py` (DATABASE_URL desde env + `pool_pre_ping=True`), `requirements.txt` (+psycopg[binary]). CI #121 verde.
- ✅ **`c68d139`** — `fix(db): force psycopg v3 driver in Postgres URL`. Agrega `_normalizar_url_db()` (convierte `postgresql://` → `postgresql+psycopg://`) + 3 tests. CI #122 verde.
- ✅ **Deploy Railway exitoso**: proyecto `easygoing-caring`, servicio `web` `Online`, Postgres addon vinculado, URL pública `https://web-production-bb6a7.up.railway.app/`.
- ✅ **Variables en Railway**: `DATABASE_URL` (auto por addon), `GROQ_API_KEY` (manual).
- ✅ **4 endpoints verificados en producción**: `GET /` 200, `GET /docs` 200, `GET /kpis/` 200, `POST /chat/` 200 + respuesta del LLM.

**Ciclo Auth 1.A (JWT backend):**

- ✅ **`f00ea1e`** — `feat(auth): add JWT authentication with bcrypt password hashing`. 6 archivos, +68/-3. CI #123 verde.
  - ✅ `app/auth.py` (196 líneas): PyJWT + bcrypt directo + `get_current_user`.
  - ✅ `app/routers/auth.py` (100 líneas): `POST /auth/login` + `GET /auth/me`.
  - ✅ `app/models.py`: modelo `User` (email único + hashed_password + is_active + created_at).
  - ✅ `app/schemas.py`: `UserLogin`, `UserCreate`, `UserPublic`, `Token`.
  - ✅ `app/main.py`: registrar `auth_router`.
  - ✅ `requirements.txt`: PyJWT, bcrypt, slowapi, email-validator (sin passlib, sin python-jose).
- ✅ **7 tests end-to-end con `TestClient`**: login OK (200), password incorrecta (401), email inexistente (401), `/auth/me` con token (200), sin token (401), token inválido (401), password <8 chars → 422.

**Ciclo Auth 1.B.1 (endpoints POST protegidos — este ciclo):**

- ✅ **`f6ac313`** — `feat(auth): protect POST endpoints with JWT dependency`. `POST /kpis/` y `POST /chat/` ahora requieren `Depends(get_current_user)`. 401 sin token válido.
- ✅ **CI verde** (run #125).

**Ciclo Auth 1.B.2 (Login UI + cookie HttpOnly — este ciclo):**

- ✅ **`4314764`** — `feat(auth): add login UI with HttpOnly cookie + dual auth`.
  - ✅ `app/templates/login.html`: form con `hx-post="/auth/login"` + `hx-ext="json-enc"`.
  - ✅ `POST /auth/login` setea cookie HttpOnly (`SameSite=Lax`) además de devolver JSON.
  - ✅ Dual auth: `OAuth2PasswordBearer(auto_error=False)` + lectura de cookie + `get_current_user_optional`.
  - ✅ `GET /` con `get_current_user_optional` → redirect 302 a `/login` si no hay sesión.
  - ✅ Navbar con logout (`POST /auth/logout` idempotente + borra cookie).
  - ✅ Detección de `HX-Request` para responder HTML (partial) o JSON (API) según cliente.
- ✅ **CI verde** (run #126). **495 tests passed** (460 legacy + 35 app/).

### 🟡 En curso

- *Nada.* Working tree limpio. CI #126 verde verificado.

### ⏳ Pendiente inmediato (Bloque 1.B — cerrar auth en producción)

- ⏳ **1.B.3** — `scripts/seed_admin.py` para crear primer user admin en Railway.
- ⏳ **1.B.5** — `SECRET_KEY` + `COOKIE_SECURE=true` en Railway.
- ⏳ **1.B.7** — Verificar login end-to-end en URL pública.
- ⏳ **1.B.4** — `tests/app/test_auth.py` formales (12-15 tests en CI).
- ⏳ **1.B.6** — Rate limit en `/chat/` con `slowapi` (instalado, sin aplicar — deuda #30).

---

## 3️⃣ LÍNEA TEMPORAL DE COMMITS

| Commit | Descripción | Tests |
| :--- | :--- | :---: |
| `4314764` | **feat(auth): add login UI with HttpOnly cookie + dual auth** | 495 |
| `f6ac313` | **feat(auth): protect POST endpoints with JWT dependency** | 494 |
| `f00ea1e` | **feat(auth): add JWT authentication with bcrypt password hashing** (6 files, +68/-3) | 490 |
| `c68d139` | **fix(db): force psycopg v3 driver in Postgres URL** (2 files) | 490 |
| `86845ac` | **feat(deploy): prepare FastAPI app for Railway deployment** (3 files) | 487 |
| `ed11c36` | Fix(deps): remove literal '+' from python-multipart line | 487 |
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

> 📈 **Evolución de tests:** 263 → ... → 450 → 453 → 460 → 477 → 487 → 490 → 494 → **495** (460 legacy + 35 app/).  
> ✅ **CI verde real verificado** (runs #112, #114, #117, #121, #122, #123, #125, #126). Los runs rojos #107, #108, #109, #115, #116 quedan como histórico.

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
| API FastAPI local + Swagger UI | `http://127.0.0.1:8000/docs` | `uvicorn app.main:app --reload` |
| Dashboard Jinja2 + chat IA local | `http://127.0.0.1:8000/` | (mismo servidor) |
| **Producción (Railway)** | **`https://web-production-bb6a7.up.railway.app/`** | (auto-deploy desde main) |
| Swagger producción | `https://web-production-bb6a7.up.railway.app/docs` | (mismo servidor) |
| OpenAPI JSON | `https://web-production-bb6a7.up.railway.app/openapi.json` | (mismo servidor) |

### 4.32 🎯 Migración completa Dash → FastAPI (decisión estratégica)
- **Decisión:** retirar progresivamente `dashboard/` y consolidar toda la presentación en `app/` (FastAPI + Jinja2 + HTMX + Plotly.js).
- **Motivo:** producto vendible single-stack, código limpio, sin dependencia del framework Dash.
- **Estrategia:** strangler tab por tab. Cada tab migrado reemplaza al equivalente Dash.
- **Stack elegido:** Jinja2 (server-side render) + HTMX (interactividad sin SPA) + Plotly.js (mismos gráficos que Dash).
- **Timeline:** ~5 semanas (fases 0-10).
- **Gate bloqueante:** tests para `app/` (#22) ✅ cerrada.
- **Progreso:** Chat IA integrado ✅, auth backend ✅, login UI ✅. Falta: seed admin, migración de tabs, retiro de `dashboard/`.

### 4.33 🔗 `httpx2` reemplaza `httpx` (Starlette 1.6.0)
- **Problema:** Starlette 1.6.0 deprecó `httpx` en `TestClient` (`StarletteDeprecationWarning`).
- **Solución:** instalar `httpx2>=2.13,<3`. Starlette lo detecta automáticamente.
- **Lección:** leer los `DeprecationWarning` temprano; migrar antes de que sea bloqueante.

### 4.34 🧪 SQLModel `table=True` NO valida en construcción
- **Problema:** `KPI(nombre=None)` no levanta `ValidationError` (contrato real de SQLModel).
- **Solución:** la validación de entrada es responsabilidad de `KPICreate` (Pydantic `BaseModel`).
- **Lección:** los tests prueban el contrato real del código, no el deseado.

### 4.35 🤖 Groq + `openai/gpt-oss-120b` para el chat IA
- **Decisión:** usar **Groq** como proveedor LLM (gratis, rápido, OpenAI-compatible) con modelo **`openai/gpt-oss-120b`** (producción).
- **Motivo:** Groq tiene tier gratuito generoso (30 RPM, 14.4k RPD), latencia ~1s para ~700 tokens, SDK idéntico al de OpenAI.
- **Histórico:** los modelos `llama-3.3-70b-versatile` y `llama-3.1-8b-instant` fueron **deprecados el 2026-08-16**. El reemplazo oficial es `openai/gpt-oss-120b`.
- **Lección:** los IDs de modelos LLM son efímeros. Diseñar el ID como configurable (`os.getenv("GROQ_MODEL", ...)`).

### 4.36 🧩 Arquitectura en 4 capas del chat IA
- **Decisión:** separar el chat en 4 capas claras.
  - **Servicio** (`app/services/llm_chat.py`): habla con Groq. No sabe HTTP.
  - **Router** (`app/routers/chat.py`): orquesta DB + service + template.
  - **Contrato** (`Form(min_length=1, max_length=500)`): validación en el borde.
  - **Presentación** (`partials/_chat.html` + `_chat_response.html`): HTML + HTMX.
- **Lección:** los servicios deben ser agnósticos del transporte.

### 4.37 📦 `python-multipart` es obligatorio para `Form(...)`
- **Problema:** FastAPI valida `python-multipart` en import-time del módulo (decorador `@router.post` evalúa `Form(...)`).
- **Error típico:** `RuntimeError: Form data requires "python-multipart" to be installed.`
- **Lección:** endpoints con `Form`, `File`, `UploadFile` o `OAuth2PasswordRequestForm` requieren `python-multipart` explícito en `requirements.txt`.

### 4.38 🎨 HTMX como reemplazo de callbacks Dash
- **Decisión:** **HTMX 2.0.4** (51 KB, single-file) en vez de React/Vue.
- **Motivo:** server-side render + HTML declarativo. Cero estado JS, cero build step, cero npm.
- **Lección:** para dashboards internos, HTMX + Jinja2 es 10x más simple que una SPA.

### 4.39 ☁️ Railway como PaaS (sin Docker local)
- **Problema:** Mac con macOS Mojave 10.14 no soporta Docker Desktop moderno. Sin Docker local no se puede buildear la imagen.
- **Solución:** usar Railway (PaaS) que detecta el stack por `requirements.txt` + `Procfile` y buildea en su infraestructura con Nixpacks.
- **Ventajas:** cero instalación local, cero RAM consumida, auto-deploy desde GitHub, Postgres addon con un click.
- **Trade-off:** no se aprende Docker en esta ruta. Aprendizaje diferido a cuando se tenga Mac moderno o Linux.
- **Lección:** la herramienta correcta depende del contexto. No forzar Docker cuando el hardware no lo soporta.

### 4.40 🐘 Normalización de URL Postgres (`postgresql://` → `postgresql+psycopg://`)
- **Problema:** Railway y otros PaaS generan URLs `postgresql://...`. SQLAlchemy las interpreta como driver `psycopg2` (legacy). El proyecto usa `psycopg` v3.
- **Error en producción:** `ModuleNotFoundError: No module named 'psycopg2'` + crash al arrancar.
- **Solución:** `_normalizar_url_db()` en `app/db.py` que convierte `postgresql://` → `postgresql+psycopg://` antes de `create_engine`. Idempotente: si ya tiene `+psycopg`, no toca. Si es `sqlite://`, no toca.
- **Test:** 3 tests unitarios en `test_models.py` (`test_normalizar_url_postgres`, `test_normalizar_url_ya_normalizada`, `test_normalizar_url_sqlite_no_se_toca`).
- **Lección:** SQLAlchemy no adivina el driver. La URL debe especificarlo explícitamente cuando hay múltiples opciones.

### 4.41 🔑 bcrypt directo (sin passlib)
- **Problema:** `passlib 1.7.4` (de 2020) es incompatible con `bcrypt 5.x` (2024). Falla con `AttributeError: module 'bcrypt' has no attribute '__about__'` + `ValueError: password cannot be longer than 72 bytes`.
- **Solución:** usar `bcrypt` directo (`bcrypt.gensalt()` + `bcrypt.hashpw()` + `bcrypt.checkpw()`). Sin abstracción de passlib.
- **Ventajas:** 1 dependencia en vez de 2, mantenimiento activo, compatible con Python 3.11+.
- **Lección:** passlib está en su ocaso. La comunidad migró a bcrypt directo o argon2-cffi.

### 4.42 🔐 PyJWT en vez de python-jose (Mojave sin wheels de cryptography)
- **Problema:** `python-jose[cryptography]` requiere `cryptography>=50` que no tiene wheel para macOS Mojave Intel. Compilar desde fuente falla por falta de Rust/OpenSSL.
- **Solución:** usar **PyJWT** (Python puro para HS256). No requiere `cryptography`.
- **Cambio API:** `from jose import jwt` → `import jwt`, `JWTError` → `InvalidTokenError`. Casi idéntico.
- **Lección:** antes de agregar una dep, verificar que tenga wheel precompilado para tu plataforma. Para Mojave Intel, preferir librerías Python puras.

### 4.43 ⏱️ Timing-safe login (previene user enumeration)
- **Problema:** si el login devuelve distinto tiempo cuando el email existe vs no existe (~250ms por bcrypt vs ~0ms), un atacante puede medir la latencia para enumerar emails.
- **Solución:** ejecutar `verify_password()` **siempre**, incluso si el user no existe. Se usa un `_DUMMY_HASH` (hash bcrypt válido de password desconocido) para forzar la ejecución de bcrypt.
- **Consecuencia:** tiempo de respuesta constante (~250ms) para ambos casos.
- **Lección:** la seguridad no es solo "no filtrar strings". Los tiempos también filtran información.

### 4.44 🔒 SECRET_KEY de dev con >32 bytes (RFC 7518)
- **Problema:** PyJWT emite `InsecureKeyLengthWarning` cuando el HMAC key es <32 bytes para SHA256.
- **Solución:** fallback de dev = `"dev-insecure-secret-change-me-and-over-32-bytes-please"` (54 bytes).
- **Lección:** el fallback de dev debe simular las condiciones de producción. Si en prod usarás 32+ bytes, el fallback también.

### 4.45 🎫 HS256 explícito (evita alg=none attack)
- **Decisión:** `decode_access_token()` usa `algorithms=[ALGORITHM]` con `ALGORITHM = "HS256"` fijo.
- **Motivo:** sin esto, PyJWT acepta cualquier algoritmo del header, incluyendo `alg=none` → bypass de firma.
- **Lección:** nunca dejar que el cliente dicte el algoritmo. Siempre fijo, siempre explícito.

### 4.46 🍪 Cookie HttpOnly + SameSite=Lax + dual auth (Login UI)
- **Decisión:** `POST /auth/login` setea cookie `HttpOnly` con `SameSite=Lax` además de devolver el JWT en el body. Los endpoints protegidos aceptan **header `Authorization: Bearer` o cookie**.
- **Motivo:** doble cliente: (a) navegador con HTMX (usa cookie, más seguro contra XSS porque JS no puede leerla), (b) API/Swagger/curl (usa header). `SameSite=Lax` mitiga CSRF en navegación cruzada.
- **Implementación:** `OAuth2PasswordBearer(auto_error=False)` para que no exija header; la dependency `get_current_user` busca primero el header, después la cookie.
- **Consecuencia:** `get_current_user` (401 si no hay sesión) y `get_current_user_optional` (devuelve `None`) conviven.
- **Lección:** para apps híbridas HTML+API, la cookie HttpOnly es la ruta segura para el navegador; el header Bearer queda para integraciones programáticas.

### 4.47 🧭 `HX-Redirect` para navegación server-driven (HTMX)
- **Decisión:** el server responde con header `HX-Redirect: /` en éxito de login; HTMX navega el navegador hacia `/`.
- **Motivo:** con HTMX, un form con `hx-post` no hace navegación por defecto. Si devolvés un 200 con HTML, HTMX lo inyecta en el target. Si querés navegación, `HX-Redirect`.
- **Extensión necesaria:** `hx-ext="json-enc"` en el form para que HTMX serialice como JSON en vez de `application/x-www-form-urlencoded`. Requerido porque `POST /auth/login` recibe `UserLogin` (Pydantic) como JSON.
- **Lección:** HTMX permite dos tipos de respuesta para el mismo endpoint: partial (render in-place) o navegación completa (`HX-Redirect`). Elegir según UX.

### 4.48 🔀 Detección `HX-Request` para respuesta polimórfica
- **Decisión:** el endpoint detecta el header `HX-Request: true`. Si presente → devuelve HTML parcial + `HX-Redirect`. Si ausente (curl, Swagger, JS) → devuelve JSON normal.
- **Motivo:** mismo endpoint sirve a HTMX (form del navegador) y a API (`curl -X POST`). Sin duplicar rutas.
- **Lección:** FastAPI puede responder distinto según el cliente. Es un patrón útil para backends híbridos sin duplicar contratos.

### 4.49 🚪 Redirect 302 para `GET /` sin sesión
- **Decisión:** `GET /` con `get_current_user_optional` → si es `None`, retorna `RedirectResponse(url="/login", status_code=302)`. `GET /login` es la única ruta pública HTML.
- **Motivo:** sin esto, un usuario anónimo veía el dashboard (con chat IA roto por 401). Mejor UX: redirigir antes de mostrar.
- **Consecuencia:** `GET /` deja de ser público. Se documenta en el TRASPASO que el "entrypoint" del navegador es `/login`.
- **Lección:** proteger endpoints POST no alcanza si el entrypoint HTML queda abierto. El navegador debe arrancar en login.

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

### Tests de `app/` (35)

| Archivo | Tests | Cobertura conceptual |
| :--- | :---: | :--- |
| `tests/app/test_models.py` | 6 | `KPI` SQLModel (creación, timestamp naive, contrato real) + 3 de `_normalizar_url_db` |
| `tests/app/test_schemas.py` | 5 | `KPICreate`: parseo ISO, coacción numérica, rechazo inválido |
| `tests/app/test_endpoints.py` | 9 | `GET /`, `GET /kpis/`, `POST /kpis/` con `TestClient` |
| `tests/app/test_chat.py` | 10 | `POST /chat/` con mock del LLM |
| Tests de auth (integrados en endpoints existentes) | 5 | 401 sin token en POST protegidos, redirect 302 en `GET /` sin cookie, login OK + cookie, logout idempotente |
| **Subtotal app/** | **35** | ✅ |

### Fixtures críticas (conftest.py)

- `session` → SQLite en memoria (`StaticPool`, `check_same_thread=False`). Aislada por test. **No toca `kpi_database.db`.**
- `client` → `TestClient` con `app.dependency_overrides[get_session]`. Cero contaminación entre tests.
- `mock_llm_ok` → `monkeypatch.setattr` sobre `app.routers.chat.consultar_llm`. Evita pegarle a Groq real.
- `auth_headers` → genera token válido para tests de endpoints protegidos (reutilizar en `test_auth.py` de 1.B.4).

### Total

> **495 tests passed** (460 legacy + 35 app/). **0 regresiones. 0 warnings críticos.**  
> Tiempo: ~62 s suite completa. Tests de `app/` corren en ~0.6 s.

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
| **25** | Pandas 2.1.4 → 3.x | Reproducibilidad | 🟢 Baja |
| **26** | CI no mide cobertura de `app/` | Testing infra | 🟡 Media |
| ~~**27**~~ | ~~Fase IA pendiente~~ | ✅ **CERRADA** (`ed806ea`) | — |
| ~~**28**~~ | ~~Sin Dockerfile ni docker-compose~~ | ✅ **CERRADA** (Railway sin Docker, decisión 4.39) | — |
| ~~**29**~~ | ~~SQLite en producción~~ | ✅ **CERRADA** (Postgres addon en Railway) | — |
| **30 🆕** | Rate limit en `/chat/` no aplicado (slowapi instalado) | Seguridad/Costos | 🔴 **Alta (próximo)** |
| **31 🆕** | `GROQ_MODEL` hardcodeado (debería leerse de `.env`) | Mantenibilidad | 🟢 Baja |
| ~~**32**~~ | ~~`POST /kpis/` y `POST /chat/` sin proteger~~ | ✅ **CERRADA** (`f6ac313`) | — |
| **33 🆕** | IA.2, IA.3, IA.4 (diagnóstico/reportes/anomalías con LLM) | Features | 🟡 Media |
| ~~**34**~~ | ~~Sin template login~~ | ✅ **CERRADA** (`4314764`) | — |
| **35 🆕** | Sin seed admin (no hay forma de crear primer usuario en prod) | Operaciones | 🔴 **Alta (próximo)** |
| **36 🆕** | Sin tests formales de auth (cobertura parcial dentro de endpoints) | Testing infra | 🟡 Media |
| **37 🆕** | `SECRET_KEY` no seteada en Railway (usa fallback de dev en prod) | Seguridad | 🔴 **Alta (próximo)** |
| **38 🆕** | `COOKIE_SECURE=true` no seteado en Railway | Seguridad | 🔴 **Alta (próximo)** |

### 📌 Detalle de deudas activas

**Deuda 11 — Eliminación de `schema_adapter.py`:** `grep -rn "schema_adapter" src/ dashboard/ tests/ app/ --include="*.py"` → confirmar que nada lo importa → `git rm` → tests + ruff → commit `chore(cleanup)`.

**Deuda 15 — Doble spinner residual:** Cascade equipo + reset → 2 fires del store. Fix candidato: `debounce` 200ms o cascade condicional.

**Deuda 16 — Semántica color KPIs rendimiento:** Los 4 KPIs heredan severidad agregada del PPM total. Fix: severidad individual por KPI (Fase 3c).

**Deuda 19 — Callback de 2104 ms:** Detectado en Dash Dev Tools. Fix: identificar callback exacto, instrumentar, medir, optimizar.

**Deuda 24 — Doble stack de dashboards:** Transitoria. Una vez el dashboard Jinja2 cubra todas las funcionalidades del Dash, se retira el Dash.

**Deuda 25 — Pandas 2 → 3:** `requirements.txt` fija `pandas>=2.1,<3`. Migrar a pandas 3 es su propio ciclo.

**Deuda 26 — Cobertura de `app/` en CI:** El workflow corre `pytest tests/ -v --cov=src --cov=dashboard`. Fix candidato: agregar `--cov=app`.

**Deuda 30 🆕 — Rate limiting en `/chat/`:** slowapi 0.1.10 está instalado. Falta: `SlowAPIMiddleware` en `main.py` + `@limiter.limit("30/minute")` en el router de chat. Groq tier gratis tiene 30 RPM.

**Deuda 31 🆕 — `GROQ_MODEL` configurable:** Mover de constante a `os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")`. Facilita migrar modelos sin tocar código.

**Deuda 35 🆕 — Seed admin:** No hay forma de crear el primer usuario en producción. Fix: `scripts/seed_admin.py` que lea `ADMIN_EMAIL` + `ADMIN_PASSWORD` de env y cree el user.

**Deuda 36 🆕 — Tests formales de auth:** Cubrimos 401 en POST y redirect 302 en `GET /` dentro de tests existentes, pero falta un `tests/app/test_auth.py` (12-15 tests) que cubra login OK/fallo, `/auth/me`, `/auth/logout`, tokens expirados. Correrlo en CI.

**Deuda 37 🆕 — `SECRET_KEY` en Railway:** No seteada. Usa el fallback de dev. Fix: `openssl rand -hex 32` → agregar como variable de entorno en Railway → redeploy.

**Deuda 38 🆕 — `COOKIE_SECURE=true` en Railway:** Sin esta var, la cookie se envía en HTTP. En prod (HTTPS) debe ir `Secure`. Fix: agregar var → redeploy.

---

## 7️⃣ ROADMAP PENDIENTE

| Fase | Fix / Feature | Estimación | Prioridad |
| :--- | :--- | :---: | :---: |
| **Auth.1.B.3** | **`scripts/seed_admin.py` (crear admin en Railway)** | 15 min | 🔴 **Alta — PRÓXIMO PASO** |
| **Auth.1.B.5** | **SECRET_KEY + COOKIE_SECURE=true en Railway** | 5 min | 🔴 Alta |
| **Auth.1.B.7** | **Verificar login en URL pública** | 20 min | 🔴 Alta |
| **Auth.1.B.4** | **`tests/app/test_auth.py` formales (12-15 tests)** | 45 min | 🟡 Media |
| **Auth.1.B.6** | **Rate limit `/chat/` con slowapi (deuda #30)** | 30 min | 🟡 Media |
| Seg.3 | CORS configurado | 30 min | 🟡 Media |
| IA.2 | Diagnóstico asistido por LLM | 2 h | 🟡 Media |
| IA.3 | Reportes ejecutivos narrados | 2 h | 🟡 Media |
| IA.4 | Detección de anomalías ML | 3 h | 🟡 Media |
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
| **`git clone` en vez de `git init`** cuando ya hay historial remoto. | `git init` + `remote add` + push. |
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
- **Ningún push sin verificar el estado del run CI inmediatamente anterior.**
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
  - `app/routers/`: orquestación HTTP.
  - `app/services/`: lógica pura, sin HTTP.
  - `app/templates/`: Jinja2 (render server-side).
  - `app/auth.py`: JWT + bcrypt + `get_current_user` + `get_current_user_optional`.
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

### 🆕 Reglas nuevas (ciclo IA.1 + Deploy + Auth)

- **Nunca pegar el `+` inicial de un diff en un archivo de config.** El `+` significa "línea agregada", no es parte del contenido.
- **`python-multipart` es obligatorio para `Form(...)`, `File(...)`, `UploadFile(...)` en FastAPI.** FastAPI lo valida en import-time.
- **Los IDs de modelos LLM son efímeros.** Groq deprecó `llama-3.3-70b-versatile` el 2026-08-16. Usar `openai/gpt-oss-120b`. Configurable desde env.
- **Nunca exponer secrets con `cat .env`.** Verificar con `grep -c` o `python -c`.
- **`passlib` está obsoleto.** Usar `bcrypt` directo.
- **`python-jose[cryptography]` no tiene wheels para Mojave Intel.** Usar `PyJWT`.
- **SQLAlchemy no adivina el driver Postgres.** URL explícita: `postgresql+psycopg://`.
- **Timing-safe check en login.** bcrypt corre siempre, incluso si el user no existe.
- **`algorithms=["HS256"]` explícito en PyJWT.** Nunca dejar que el cliente dicte el algoritmo.
- **SECRET_KEY de dev >32 bytes** (RFC 7518).
- **Cookie HttpOnly + SameSite=Lax para sesión de navegador.** El header Bearer queda para API/curl/Swagger.
- **HTMX necesita `hx-ext="json-enc"`** cuando el endpoint espera JSON (Pydantic body). Sin esto, HTMX manda `application/x-www-form-urlencoded`.
- **`HX-Redirect` para navegación server-driven.** Un 200 con HTML NO navega el browser.
- **`GET /` protegido con redirect 302 a `/login`.** Sin esto, anónimos ven el dashboard roto.

---

## 9️⃣ ⚠️ HISTORIAL DE ERRORES — NO REPETIR

| ❌ Error | ✅ Correcto |
| :--- | :--- |
| **Pegar `+python-multipart>=0.0.20,<1` en `requirements.txt`.** | Quitar el `+` inicial. |
| **Asumir que `python-multipart` está instalado porque algo lo arrastra.** | Declararlo explícito en `requirements.txt`. |
| **Usar `llama-3.3-70b-versatile` (deprecado 2026-08-16).** | Usar `openai/gpt-oss-120b`. |
| **`cat .env` para verificar la key.** | `python -c "from dotenv import load_dotenv; import os; ..."`. |
| **Pegar la API key completa en el chat.** | Enmascararla. Si se expone, rotarla. |
| **Escribir "CI verde" sin verificar Actions.** | `curl` a la API ANTES. |
| **Asumir que `requirements.txt` refleja el venv real.** | `pip install --dry-run` en venv limpio. |
| **Confundir "tests verdes locales" con "CI verde".** | Local usa venv ya poblado; CI arranca de cero. |
| **Usar `python-jose[cryptography]` en Mojave Intel.** | **Falló.** Usar `PyJWT` (Python puro). |
| **Usar `passlib` con bcrypt 5.x.** | **Falló.** Usar `bcrypt` directo. |
| **Usar `datetime.now(timezone.utc)` (ruff UP017).** | Usar `datetime.now(UTC)`. |
| **Dejar `algorithms=None` en PyJWT.** | `algorithms=[ALGORITHM]` con `ALGORITHM="HS256"` fijo. |
| **URL Postgres sin driver explícito.** | `postgresql+psycopg://...` (SQLAlchemy no adivina). |
| **Mismo tiempo de respuesta para email existe/no existe.** | bcrypt siempre corre (dummy hash). |
| **SECRET_KEY de dev <32 bytes.** | >32 bytes (RFC 7518). PyJWT lo advierte. |
| **Poner `hx-post` sin `hx-ext="json-enc"` a un endpoint que espera JSON.** | Agregar `hx-ext="json-enc"` al form. |
| **Esperar que `hx-post` navegue el browser.** | Devolver header `HX-Redirect: /` en éxito. |
| **Dejar `GET /` público pensando que "el POST está protegido".** | Proteger el entrypoint HTML con redirect 302 a `/login`. |
| **`mkdir -p ~/industrial-kpi-intelligence/app/...`** sin preguntar dónde está el proyecto. | `git remote -v` + `ls ~/Projects/`. |
| **Asumir que una carpeta nueva es el proyecto activo.** | `git status` para verificar. |
| **`pip3 freeze > requirements.txt` en Python global.** | Escribir a mano. |
| **`git init` + `git remote add`** cuando ya hay historial. | `git clone` + `cp -R`. |
| **Asumir que `NaiveDatetime` es importable desde `sqlmodel`.** | **NO existe.** Usar `sa_column=Column(DateTime(timezone=False))`. |
| **Asumir que `KPI(nombre=None)` levanta `ValidationError`.** | SQLModel `table=True` NO valida. |
| **Enviar `"id": 0` en POST a FastAPI.** | El `id` es autoincremental. |
| **Confundir "example value" de Swagger con datos reales.** | "Try it out" → "Execute". |
| **`git push` sin PAT.** | PAT con scope `repo` + `workflow`. |
| **`rm -rf` de carpetas duplicadas sin verificar.** | Backup primero (`mv` a `.bak`). |
| **`sed -i ''` con `\n` en macOS.** | No funciona. Usar `perl -i -pe` o heredoc. |

---

## 🔟 📁 ARCHIVOS CLAVE Y COMANDOS

### 🗂️ Estructura del proyecto (post Auth 1.B.2)

```text
industrial-kpi-intelligence/
├── ARCHITECTURE.md
├── README.md                              # 495 tests + badges
├── VISION.md
├── CHANGELOG.md
├── LICENSE                                # Elastic License 2.0
├── pyproject.toml                         # ruff + pytest
├── requirements.txt                       # ~25 deps (FastAPI + Dash + IA + Auth + tooling)
├── Procfile                               # uvicorn app.main:app --host 0.0.0.0 --port $PORT
├── render.yaml                            # (histórico, no aplica a Railway)
├── .env                                   # GROQ_API_KEY (gitignored)
├── .gitignore
├── .github/workflows/tests.yml            # Workflow "CI"
├── assets/style.css
│
├── app/                                   # CAPA FASTAPI
│   ├── __init__.py
│   ├── main.py                            # FastAPI app + lifespan + mount /static + include_router(auth, chat) + GET / (302 si no auth) + GET/POST /kpis/
│   ├── models.py                          # SQLModel KPI + User
│   ├── schemas.py                         # Pydantic KPICreate + UserLogin + UserCreate + UserPublic + Token
│   ├── db.py                              # DATABASE_URL desde env + _normalizar_url_db + create_db_and_tables + get_session
│   ├── auth.py                            # JWT (PyJWT) + bcrypt + get_current_user + get_current_user_optional
│   ├── templates_config.py                # Jinja2Templates compartido
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py                        # POST /auth/login (cookie HttpOnly + HX-Redirect) + POST /auth/logout + GET /auth/me
│   │   └── chat.py                        # POST /chat/ (HTML parcial, protegido)
│   ├── services/
│   │   ├── __init__.py
│   │   └── llm_chat.py                    # Groq + construir_contexto + consultar_llm
│   └── templates/
│       ├── index.html                     # Dashboard + navbar con logout + chat
│       ├── login.html                     # 🆕 form HTMX con hx-ext="json-enc"
│       └── partials/
│           ├── _chat.html
│           └── _chat_response.html
│
├── static/
│   └── js/
│       └── htmx.min.js                    # HTMX 2.0.4
│
├── config/
├── dashboard/                             # Legacy Dash (EN RETIRADA)
├── data/
├── docs/
│   ├── adr/
│   └── TRASPASO_MAESTRO.md
├── imagenes/
├── scripts/                               # (pendiente: seed_admin.py)
│
├── src/                                   # Lógica legacy
│   ├── capability.py
│   ├── control_charts.py
│   ├── kpis.py
│   ├── oee.py
│   ├── diagnostics.py
│   └── schema_adapter.py                  # PENDIENTE eliminar (deuda #11)
│
├── migrate_csv.py
├── kpi_database.db                        # Local, gitignored
│
└── tests/
    ├── app/                               # 35 tests del stack FastAPI
    │   ├── conftest.py                    # + fixture auth_headers
    │   ├── test_models.py                 # 6 tests (KPI + normalizar URL)
    │   ├── test_schemas.py                # 5 tests
    │   ├── test_endpoints.py              # 9 tests (+ 401 sin token)
    │   ├── test_chat.py                   # 10 tests
    │   └── test_auth.py                   # PENDIENTE 1.B.4 (12-15 tests formales)
    └── ... (460 legacy)
```

### ⌨️ Comandos verificados

```bash
# Protocolo de arranque
cd /Users/violeta/Projects/industrial-operations-intelligence/industrial-kpi-intelligence
source venv/bin/activate
which python                    # DEBE mostrar .../venv/bin/python

# Gates
pytest                          # 495 passed (~62 s)
pytest tests/app/ -v            # 35 passed (~0.6 s)
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

# Test login en producción (después de seed admin)
curl -s -X POST "https://web-production-bb6a7.up.railway.app/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "..."}'

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

### 📋 Bloque 1.B.3-6 — Cerrar auth en producción

**Contexto:** Bloques 1.B.1 y 1.B.2 cerrados. Auth completo backend + UI.
- 1.B.1 (commit `f6ac313`): `POST /kpis/` y `POST /chat/` protegidos con JWT.
- 1.B.2 (commit `4314764`): login UI con cookie HttpOnly, dual auth (header + cookie), navbar con logout, `GET /` con redirect 302 a `/login`.
- 495 tests verdes. CI #126 verde. HEAD: `4314764`.

**Estado del deploy:** URL pública operativa en Railway con Postgres, pero
usa el fallback de dev para `SECRET_KEY` y no tiene `COOKIE_SECURE=true`.
Además no hay user admin creado en la DB de producción.

**Pendientes de Bloque 1.B:**

| # | Sub-fase | Duración | Prioridad |
|:---:|:---|:---:|:---:|
| **1.B.3** | `scripts/seed_admin.py` (crear admin en Railway) | 15 min | 🔴 Alta |
| **1.B.5** | SECRET_KEY + COOKIE_SECURE=true en Railway | 5 min | 🔴 Alta |
| **1.B.7** | Verificar login en URL pública | 20 min | 🔴 Alta |
| **1.B.4** | `tests/app/test_auth.py` formales (12-15 tests) | 45 min | 🟡 Media |
| **1.B.6** | Rate limit `/chat/` con slowapi | 30 min | 🟡 Media |

**Orden recomendado:** primero funcional en producción (1.B.3 → 1.B.5 → 1.B.7),
después cobertura (1.B.4 → 1.B.6).

---

#### 1.B.3 — Script `seed_admin.py` (15 min)

**Crear `scripts/seed_admin.py`:**

```python
# scripts/seed_admin.py
"""Crea el primer user admin leyendo credenciales de env vars.

Uso local:
    ADMIN_EMAIL=admin@example.com ADMIN_PASSWORD=xxx python scripts/seed_admin.py

Uso en Railway (via Console del dashboard o `railway run`):
    Mismas env vars + ejecutar el mismo comando.
"""
import os
from sqlmodel import Session, select
from app.db import engine, create_db_and_tables
from app.models import User
from app.auth import hash_password


def main() -> None:
    create_db_and_tables()
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    if not email or not password:
        raise SystemExit(
            "ADMIN_EMAIL y ADMIN_PASSWORD son requeridos como env vars."
        )
    with Session(engine) as s:
        existing = s.exec(select(User).where(User.email == email)).first()
        if existing:
            print(f"User {email} ya existe, skip")
            return
        s.add(User(email=email, hashed_password=hash_password(password)))
        s.commit()
        print(f"✅ User {email} creado")


if __name__ == "__main__":
    main()
```

Ejecutar en Railway desde Console del bloque web con las env vars seteadas.

#### 1.B.5 — SECRET_KEY + COOKIE_SECURE en Railway (5 min)

```bash
# Generar secret de 64 chars hex (32 bytes)
openssl rand -hex 32
```

En Railway → bloque web → Variables → + New Variable:

| Variable | Valor |
|:---|:---|
| `SECRET_KEY` | resultado de `openssl rand -hex 32` |
| `COOKIE_SECURE` | `true` |

Después: click en **Deploy** (arriba a la izquierda del canvas) para aplicar.

#### 1.B.7 — Verificar login en URL pública (20 min)

```bash
URL="https://web-production-bb6a7.up.railway.app"

# 1. Seed del admin en Railway (via Console del dashboard web)
#    Ver 1.B.3.

# 2. Test login desde curl
curl -s -X POST "$URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@...", "password": "..."}' | python3 -m json.tool

# 3. Verificar POST /chat/ sin token → 401
curl -s -o /dev/null -w "POST /chat/ sin auth → %{http_code}\n" \
  -X POST "$URL/chat/" --data-urlencode "query=test"

# 4. Verificar GET / sin cookie → 302 redirect a /login
curl -s -o /dev/null -w "GET / sin auth → %{http_code}\n" "$URL/"

# 5. Verificación visual en navegador:
#    - Abrir $URL → redirect a /login
#    - Login con admin creado
#    - Ver dashboard con navbar + tabla KPIs + chat IA
#    - Chat IA funciona end-to-end
#    - Logout → vuelve a /login
```

#### 1.B.4 — `tests/app/test_auth.py` formales (45 min)

12-15 tests en CI:

- **5 de login:** OK (200 + cookie), password incorrecta (401), email inexistente (401), password <8 chars (422), email inválido (422).
- **4 de `/auth/me`:** con token (200), sin token (401), token inválido (401), token expirado (401).
- **3 de endpoints protegidos:** `POST /kpis/` sin auth (401), `POST /chat/` sin auth (401), con auth (200/201).
- **3 de `POST /auth/logout`:** idempotente, borra cookie, no requiere auth.

Fixture `auth_headers` ya existe en `conftest.py`. Reutilizarla.

#### 1.B.6 — Rate limit `/chat/` con slowapi (30 min)

- `SlowAPIMiddleware` en `main.py`.
- `@limiter.limit("30/minute")` en `POST /chat/`.
- Exception handler para `RateLimitExceeded` → 429.
- 1-2 tests con `TestClient` verificando el 429.

---

⏱️ **Después de Bloque 1.B:**

1. **IA.2** — Diagnóstico asistido por LLM (2 h).
2. **Migración tab por tab Dash → FastAPI** (decisión 4.32).
3. **Primer contacto con 5-10 prospectos** (validación comercial).

---

## 1️⃣2️⃣ 💬 MENSAJE DE TRANSICIÓN (para pegar en chat nuevo)

```text
Contexto: pego abajo el TRASPASO_MAESTRO del proyecto Industrial KPI Intelligence.
Soy David, Ing. Civil Químico + dev autodidacta, semana 4/8.

Estado: Bloques 1.B.1 (endpoints POST protegidos) y 1.B.2 (Login UI + cookie
HttpOnly) cerrados. HEAD 4314764. CI #126 verde. 495 tests passed
(460 legacy + 35 app/).
URL pública: https://web-production-bb6a7.up.railway.app/

Cerrado en las últimas 3 sesiones:
- Auth backend JWT (PyJWT + bcrypt directo): commit f00ea1e
- Protección de POST /kpis/ y /chat/ con JWT: commit f6ac313
- Login UI con cookie HttpOnly + dual auth + logout: commit 4314764

Estado del deploy:
- URL pública operativa (Railway + Postgres).
- Login UI verificada en localhost (login → dashboard → logout).
- Pendiente en prod: seed admin + SECRET_KEY real + COOKIE_SECURE=true.

Próximo paso: Bloque 1.B.3-6 — Cerrar auth en producción.
Orden: 1.B.3 (seed_admin) → 1.B.5 (SECRET_KEY) → 1.B.7 (verificar)
→ 1.B.4 (tests formales) → 1.B.6 (rate limit).
Estimación total: ~2 h. Ver sección 11 del TRASPASO.

Deudas activas relevantes:
- #30 rate limit /chat/ (alta, próximo)
- #35 seed admin (alta, próximo)
- #36 tests formales auth (media, próximo)
- #37 SECRET_KEY en Railway (alta, próximo)
- #38 COOKIE_SECURE=true (alta, próximo)
- #11 eliminar schema_adapter.py (alta, legacy)
- #15 debounce cascade (media, legacy)
- #16 severidad individual KPIs (media, legacy)
- #19 callback 2104 ms (media, legacy)
- #26 CI no mide cobertura app/ (media)
- #25 pandas 2→3 (baja, diferida)
- #31 GROQ_MODEL configurable (baja)

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
- Los IDs de modelos LLM son efímeros (Groq deprecó llama-3.3-70b)
- NUNCA exponer secrets con cat .env
- PyJWT, NO python-jose
- bcrypt directo, NO passlib
- SQLAlchemy no adivina driver Postgres: postgresql+psycopg://
- Timing-safe login: bcrypt corre siempre
- algorithms=["HS256"] explícito
- SECRET_KEY dev >32 bytes (RFC 7518)
- Cookie HttpOnly + SameSite=Lax para navegador; Bearer para API
- HTMX con hx-ext="json-enc" si el endpoint espera JSON
- HX-Redirect para navegación server-driven
- GET / protegido con redirect 302 a /login
- SQLModel table=True NO valida; usar schemas.py
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
- ✅ **Fase 3b.1, 3b.2, 3b.3 completas**.
- ✅ **Migración a FastAPI + SQLModel + SQLite** (`a162f15`).
- ✅ **Dashboard Jinja2 operativo** (`724f4ac`).
- ✅ **17 tests iniciales para `app/`** (`0c59acc`).
- ✅ **CI verde real verificado** (runs #112, #114, #117, #121, #122, #123, #125, #126).
- ✅ **Decisión estratégica de migración completa Dash → FastAPI** (4.32).
- ✅ **Chat IA con Groq operativo** (`ed806ea`).
- ✅ **HTMX integrado** (interactividad sin SPA).
- ✅ **Deploy exitoso en Railway** con Postgres (URL pública operativa).
- ✅ **Auth JWT backend operativo** (`f00ea1e`).
- ✅ **Endpoints POST protegidos** (`f6ac313`).
- ✅ **Login UI con cookie HttpOnly + dual auth + logout** (`4314764`).
- ✅ **495 tests, 0 regresiones.**

### 🔬 Lecciones metodológicas del ciclo Auth 1.B

- **Proteger POST no alcanza si el entrypoint HTML queda público.** `GET /` debía redirigir a `/login`. Sin esto, anónimos veían un dashboard roto por 401 en el chat.
- **Cookie HttpOnly es la ruta segura para navegadores.** JS no puede leerla, XSS no la roba. `SameSite=Lax` mitiga CSRF sin necesitar tokens adicionales.
- **Dual auth (header + cookie) evita duplicar endpoints.** Mismo `get_current_user`, distinto transporte. `OAuth2PasswordBearer(auto_error=False)` es la clave.
- **HTMX exige `hx-ext="json-enc"` para mandar JSON.** Por defecto serializa como `application/x-www-form-urlencoded`. Si el endpoint recibe Pydantic, hay que activarlo.
- **HTMX no navega el browser con un 200.** Para navegación server-driven, devolver header `HX-Redirect`.
- **El header `HX-Request` habilita respuestas polimórficas.** Mismo endpoint → HTML parcial para HTMX, JSON para curl/Swagger.
- **Timing-safe login no es paranoia.** Los tiempos de respuesta filtran información. `_DUMMY_HASH` normaliza.
- **Un "verde" en el TRASPASO es foto histórica.** Verificar CI con `curl` antes de cada push.

### 📊 Métricas del ciclo Auth 1.B (f6ac313 + 4314764)

- **Commits:** 2 (`f6ac313`, `4314764`).
- **Archivos nuevos:** `app/templates/login.html`.
- **Archivos modificados:** `app/main.py`, `app/routers/auth.py`, `app/routers/chat.py`, `app/auth.py`, `app/templates/index.html`, `tests/app/conftest.py`.
- **Tests:** 490 → 494 → **495**.
- **Deudas cerradas:** #32 (endpoints sin proteger), #34 (sin template login).
- **Deudas nuevas:** #38 (`COOKIE_SECURE=true` en Railway).
- **Scorecard:** Seguridad subió de 6.0 → 8.0.

### 📈 Scorecard de la oferta (Full Stack VI Región)

| Categoría | Peso | Estado proyecto | Aporta |
|:---|:---:|:---:|:---:|
| Backend / APIs / DB | 20% | 9.0 | 1.80 |
| Frontend / Dashboards | 15% | 8.5 | 1.28 |
| Dominio industrial | 15% | 10 | 1.50 |
| Tests / Calidad / Git | 10% | 9.5 | 0.95 |
| **IA / Automatización IA** | **25%** | **7.5** | **1.88** |
| **Cloud / Deployment** | **10%** | **8.0** | **0.80** |
| Seguridad | 5% | 8.0 | 0.40 |
| **TOTAL** | 100% | — | **8.61** |

**Subió de 8.41 → ~8.6.** El bloque Seguridad pasó de 6 a 8 (login UI + cookie HttpOnly + dual auth + logout + entrypoint protegido). El bloque Cloud subió ligeramente (8.0) por la URL pública con login operativa.

**Siguiente salto:** cerrar 1.B.3-6 (seed admin + SECRET_KEY + COOKIE_SECURE + rate limit + tests formales) → **~9.0**.

**Techo alcanzable en 2 semanas:** 9.3 (con IA.2-4 + caso real + video demo).

---

> 📌 **Fin del TRASPASO_MAESTRO.**  
> 🗓️ **Última actualización:** Bloque 1.B.1 + 1.B.2 cerrados (commit `4314764`). 495 tests verdes. CI 2/2 verde verificado (run #126).  
> 🚀 **Próximo paso:** Bloque 1.B.3-6 — Cerrar auth en producción. Ver sección 11.
