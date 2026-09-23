# 🎯 TRASPASO MAESTRO — Industrial KPI Intelligence

> 📌 **Propósito:** documento autocontenido para arrancar un chat nuevo sin perder contexto.  
> 📥 **Instrucción de uso:** pegar este archivo completo como **PRIMER** mensaje en un chat nuevo.  
> 🗓️ **Última actualización:** Migración a FastAPI + SQLModel + SQLite completada (capa API paralela al dashboard Dash legacy). Commit `a162f15` pusheado. 460 tests verdes, CI verde.  
> 🚀 **Próximo paso:** Fase 4 de FastAPI — dashboard Jinja2 (`app/templates/index.html` + endpoint `/`).

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

> 🚀 **Próximo paso concreto del proyecto:** Fase 4 de FastAPI — crear `app/templates/index.html` + endpoint `/` para el dashboard Jinja2. Ver sección 11.

---

## 1️⃣ FICHA DEL PROYECTO

| Campo | Valor |
| :--- | :--- |
| 🏭 **Producto** | Industrial KPI Intelligence — dashboard industrial para PYMES manufactureras LatAm/España |
| 🌐 **Ecosistema** | Primer producto de 6 SaaS (Industrial Operations Intelligence) |
| 🛠️ **Stack legacy (dashboard)** | Python 3.11.9 · Plotly Dash 4.4.1 · Plotly · pandas · numpy |
| 🛠️ **Stack nuevo (API REST)** | FastAPI 0.141.1 · SQLModel 0.0.46 · SQLAlchemy 2.0.54 · Pydantic 2.13.5 · SQLite · Jinja2 3.1.6 · Uvicorn 0.53.0 |
| 🧪 **Testing** | pytest 9.1.1 · ruff · GitHub Actions CI/CD |
| 📏 **Estándares aplicables** | ISA-95 · TPM (OEE) · NIST 6.1.3 / ISO 22514 (Pp/Ppk) · AIAG SPC · OWASP · ISA-101 (HMI) · WCAG 2.1 · OpenAPI 3.1 |
| ⚖️ **Licencia** | Elastic License 2.0 (nunca MIT) |
| 👤 **Usuario** | David González Santibáñez — Ing. Civil Químico + dev autodidacta |
| 📅 **Semana** | 3 de 8 |
| ✅ **Tests actuales** | **460 passed** (sin cambios tras la migración FastAPI) |
| 🟢 **CI** | 2/2 verde (workflow CI) |
| 🧹 **Working tree** | Limpio, rama `main` sincronizada con `origin/main`. HEAD: `a162f15`. |
| 📊 **Producto 1 (MVP)** | ~92% (dashboard Dash) + capa API nueva al 80% (falta dashboard Jinja2) |
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

**Capa API REST (migración CSV → FastAPI — nueva en esta sesión):**

- ✅ **Doc README** (`85dd7fe` — vía Web Editor): README actualizado para mencionar FastAPI + SQLModel + SQLite. Se separaron las insignias (Dash legacy + FastAPI nuevo).
- ✅ **Migración completa** (`a162f15`): 7 archivos, 139 inserciones, 29 deleciones.
  - ✅ `app/models.py` — Modelo SQLModel `KPI` con `sa_column=Column(DateTime(timezone=False))` (resuelve el problema de naive datetime).
  - ✅ `app/schemas.py` — Schema Pydantic `KPICreate` (separación modelo DB ↔ schema API).
  - ✅ `app/db.py` — Configuración de SQLite (`kpi_database.db`) + `create_db_and_tables()` + `get_session()`.
  - ✅ `app/main.py` — FastAPI con `lifespan` moderno, `GET /kpis/` y `POST /kpis/`. Endpoints probados: 200 OK y 201 Created (este último generó `id: 4`).
  - ✅ `migrate_csv.py` — Script de migración CSV → SQLite vía pandas + SQLModel. Migra 3 KPIs de prueba (OEE, Tasa de defectos, MTTR).
  - ✅ `requirements.txt` — Limpiado de 74 paquetes a 8 (se quitó todo el ruido: matplotlib, jupyter, plotly, etc.).
  - ✅ `.gitignore` — Ampliado con `*.db`, `*.sqlite`, `*.sqlite3`, `kpis.csv`, `.env`, logs y `.DS_Store`.

### 🟡 En curso

- *Nada.* Sesión cerrada. Working tree limpio.

### ⏳ Pendiente inmediato (Fase 4 de FastAPI)

- ⏳ **Dashboard Jinja2** (`app/templates/index.html` + endpoint `GET /`) — pendiente de creación en esta sesión.
- ⏳ **Eliminar `schema_adapter.py`** (deuda #11 legacy del dashboard Dash).
- ⏳ **Deuda #15** — debounce cascade o cascade condicional.
- ⏳ **Fase 3c** — Chip de filtros activos + severidad individual en KPIs de rendimiento (deuda #16).
- ⏳ **Bloque 3B** — Docker + Compose.
- ⏳ **Deuda #19** — optimizar callback de 2104 ms en Calidad.
- ⏳ **Tests para la capa FastAPI** — actualmente no hay tests unitarios para `app/`.

---

## 3️⃣ LÍNEA TEMPORAL DE COMMITS

| Commit | Descripción | Tests |
| :--- | :--- | :---: |
| `a162f15` | **feat: migrar de CSV a FastAPI + SQLModel + SQLite** (7 files, +139/-29) | 460 |
| `85dd7fe` | docs: migrar de CSV a FastAPI + SQLModel + SQLite en README (vía Web Editor) | 460 |
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

> 📈 **Evolución de tests:** 263 → ... → 450 → **453** → **460** → **460** (estable).  
> La migración FastAPI **no añadió tests** todavía. Deuda nueva: cubrir `app/` con pytest.

---

## 4️⃣ DECISIONES TÉCNICAS CLAVE

### 4.1 a 4.24 — Dashboard Dash legacy
*(Sin cambios: ver versión anterior del TRASPASO. Se mantienen vigentes: patrón strangler ADR-0001, SSOT YAML, SPC contextualizado, ISA-101, escala AIAG SPC, empty_state, cascades, perf cache, WebGL, etc.)*

### 4.25 🚀 Coexistencia Dash legacy + FastAPI nuevo
- **Decisión:** la capa FastAPI se construye **en paralelo**, sin tocar el dashboard Dash existente.
- **Motivo:** el dashboard Dash funciona al 92% del MVP con 460 tests verdes y CI verde. Reescribirlo todo a FastAPI sería un riesgo innecesario en esta fase.
- **Estrategia:** la carpeta `app/` y `migrate_csv.py` conviven con `dashboard/`, `src/`, `tests/` originales. Migración gradual.
- **Consecuencia:** el repo tiene dos puntos de entrada:
  - `python -m dashboard.dash_app` → dashboard Dash (puerto 8050).
  - `uvicorn app.main:app --reload` → API FastAPI (puerto 8000).
- **Lección:** el patrón *strangler* aplica también a nivel de arquitectura completa, no solo de módulos. La migración de Dash a FastAPI se hará módulo a módulo.

### 4.26 🧩 Separación modelo DB ↔ schema API (FastAPI)
- **Problema:** SQLModel con `table=True` no ejecuta los validadores de Pydantic correctamente. Un `field_validator` en el modelo de tabla no convierte `"2026-09-23T10:00:00"` (string) a `datetime` antes de llegar a SQLite.
- **Solución:** separar en dos modelos:
  - `KPI` (en `app/models.py`): modelo de tabla (`table=True`), sin validadores.
  - `KPICreate` (en `app/schemas.py`): schema Pydantic puro (`BaseModel`), con validación automática de `datetime`.
- **Flujo:** el endpoint recibe `KPICreate`, convierte a `KPI` con `KPI(**kpi_data.model_dump())`, e inserta. En ese punto el `timestamp` ya es un `datetime` nativo.
- **Lección:** es la arquitectura estándar de FastAPI en producción. Separar entrada (Pydantic) de persistencia (SQLModel/SQLAlchemy).

### 4.27 ⏰ Tratamiento del `timestamp` naive en SQLModel 0.0.46
- **Problema:** SQLModel 0.0.46 exige por defecto que los `datetime` tengan timezone (`timezone-aware`). Las fechas del CSV son naive (sin zona horaria, hora local de planta).
- **Error:** `ValueError: Datetime values must have timezone information. Use datetime.now(timezone.utc), or annotate the field with NaiveDatetime for naive storage.`
- **Soluciones evaluadas:**
  - `NaiveDatetime` de Pydantic → **NO existe** como tipo importable en SQLModel 0.0.46.
  - `field_validator` en modelo `table=True` → **NO se ejecuta** correctamente.
  - **✅ Adoptada:** `sa_column=Column(DateTime(timezone=False))`.
- **Código final:**
  ```python
  from sqlalchemy import Column, DateTime
  from sqlmodel import Field, SQLModel

  class KPI(SQLModel, table=True):
      id: Optional[int] = Field(default=None, primary_key=True)
      nombre: str
      valor: float
      unidad: str
      timestamp: datetime = Field(sa_column=Column(DateTime(timezone=False)))
      linea_produccion: str
  ```
- **Lección:** cuando SQLModel impone un default restrictivo, `sa_column` es la vía de escape a SQLAlchemy crudo sin romper el modelo.

### 4.28 🔄 Flujo de trabajo con `git clone` en vez de `git init`
- **Problema:** la carpeta local `~/industrial-kpi-intelligence/` creada con `mkdir` no era un repo git. `git status` daba `fatal: not a git repository`.
- **Solución adoptada:** en vez de `git init` + `git remote add` (que puede causar conflictos con el historial remoto), se hizo:
  1. Backup de la carpeta actual: `mv industrial-kpi-intelligence industrial-kpi-intelligence-local`.
  2. Clonar limpio: `git clone <repo>`.
  3. Copiar los archivos nuevos al clon: `cp -R ~/.../app .` etc.
  4. Commit + push normal.
- **Lección:** `git clone` es más seguro que `git init` + `remote add` cuando ya existe historial en el remoto. Evita merges raros y conflictos de historial.

### 4.29 🧹 Limpieza del `requirements.txt` post-`pip freeze`
- **Problema:** `pip3 freeze > requirements.txt` capturó **74 paquetes** instalados en el Python global del usuario (matplotlib, jupyter, plotly, pytest, etc.). Solo 8 son del proyecto.
- **Solución:** escribir manualmente las 8 dependencias reales:
  ```
  fastapi==0.141.1
  uvicorn==0.53.0
  sqlmodel==0.0.46
  SQLAlchemy==2.0.54
  pydantic==2.13.5
  Jinja2==3.1.6
  pandas==3.0.5
  python-dateutil==2.9.0.post0
  ```
- **Lección:** `pip freeze` es peligroso en entornos sin venv. **Nunca** usar el output crudo como `requirements.txt` de un proyecto. Mejor: escribir las dependencias top-level + las transitivas críticas a mano.

### 4.30 🔒 .gitignore ampliado
- **Añadido:**
  ```
  # Base de datos (NO subir a GitHub)
  *.db
  *.sqlite
  *.sqlite3

  # Entorno
  .env

  # Logs y alertas
  *.log
  *.alerts

  # Datos de prueba (CSV)
  kpis.csv
  ```
- **Motivo:** `kpi_database.db` no debe subirse a GitHub. Contiene datos locales. `kpis.csv` es dato de prueba.
- **Verificación post-commit:** `git status` **NO** muestra `kpi_database.db` como untracked. ✅ Confirmado en el commit `a162f15`.

### 4.31 🌐 URLs del proyecto (post-migración)
| Servicio | URL | Comando |
| :--- | :--- | :--- |
| Dashboard Dash (legacy) | `http://127.0.0.1:8050` | `python -m dashboard.dash_app` |
| API FastAPI + Swagger UI | `http://127.0.0.1:8000/docs` | `uvicorn app.main:app --reload` |
| OpenAPI JSON | `http://127.0.0.1:8000/openapi.json` | (mismo servidor) |
| Dashboard Jinja2 (pendiente) | `http://127.0.0.1:8000/` | (mismo servidor) |

---

## 5️⃣ ESTADO DE TESTS Y CALIDAD

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
| `test_diagnostics_callbacks.py` | 14 | Resumen + export CSV + 3 tests de `construir_outputs_diagnostico` |
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
| `test_operational_analysis_callbacks.py` | 42 | Drill-down + labels + export CSV + 7 tests de `construir_outputs_ranking/_detalle` |
| `test_plant_overview.py` | 6 | Vista de planta |
| `test_plant_overview_components.py` | 5 | Componentes UI |
| `test_quality_performance_callbacks.py` | 15 | FPY, Pareto + export CSV + empty state |
| `test_quality_performance_components.py` | 7 | Componentes UI |
| `test_quality_performance_spec.py` | 6 | Especificación |
| `test_severity_icons.py` | 9 | `prefijar_icono` + SSOT iconos |
| `test_utils.py` | 7 | Tema oscuro + cache de parseo JSON |
| `test_validation.py` | 22 | Validación de contratos |
| **TOTAL** | **460** | ✅ **Todos verdes** |

> ⚠️ **Deuda nueva:** `app/`, `migrate_csv.py` **no tienen tests todavía**. Se ha de añadir:
> - `tests/test_app_models.py` — validación del modelo `KPI`.
> - `tests/test_app_schemas.py` — validación de `KPICreate` (datetime parse).
> - `tests/test_app_endpoints.py` — tests de `GET /kpis/` y `POST /kpis/` con `TestClient` de FastAPI.
> - `tests/test_migrate_csv.py` — test de migración de un CSV temporal.
> Estimación: 1.5 h, +25 tests aprox.

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
| **21 🆕** | **Falta dashboard Jinja2** (`app/templates/index.html` + endpoint `/`) | Feature | 🔴 **Alta (próximo paso)** |
| **22 🆕** | **Sin tests para `app/`** (FastAPI + SQLModel + migrate_csv) | Testing | 🟡 Media |
| **23 🆕** | **`kpi_database.db` se migra manualmente** (no automatizado en CI) | Automatización | 🟢 Baja |
| **24 🆕** | **Doble stack de dashboards** (Dash legacy 8050 + Jinja2 nuevo 8000) | Mantenibilidad | 🟡 Media (transitoria) |

### 📌 Detalle de deudas activas

**Deuda 11 — Eliminación de `schema_adapter.py`:** ⚠️ **Pendiente (era el próximo paso antes de la migración FastAPI)**
- `grep -rn "schema_adapter" src/ dashboard/ tests/ --include="*.py"` → confirmar que nada lo importa.
- `git rm src/schema_adapter.py` → `pytest` + `ruff check .` → commit `chore(cleanup): remove legacy schema_adapter.py`.

**Deuda 15 — Doble spinner residual:**
- Cascade equipo + reset → 2 fires del store.
- **Fix candidato:** `debounce` 200ms o cascade condicional.

**Deuda 16 — Semántica color KPIs rendimiento:**
- Los 4 KPIs heredan severidad agregada del PPM total.
- **Fix:** severidad individual por KPI (Fase 3c).

**Deuda 19 — Callback de 2104 ms (nueva):**
- Detectado en Dash Dev Tools: nodo con timing de **2104 ms** en zona de Calidad.
- **Fix propuesto:** identificar callback exacto, instrumentar, medir, aplicar optimización.

**Deuda 21 🆕 — Dashboard Jinja2 pendiente:**
- Crear `app/templates/index.html` + endpoint `GET /` en `app/main.py`.
- `Jinja2Templates(directory="app/templates")`.
- Tabla HTML con `{{ kpis }}` iterando.
- **Estimación:** 30 min.

**Deuda 22 🆕 — Sin tests para `app/`:**
- `test_app_models.py`, `test_app_schemas.py`, `test_app_endpoints.py` (con `TestClient`), `test_migrate_csv.py`.
- **Estimación:** 1.5 h, +25 tests.

**Deuda 24 🆕 — Doble stack de dashboards:**
- Dash legacy (puerto 8050) + FastAPI/Jinja2 (puerto 8000).
- **Transitoria.** Una vez el dashboard Jinja2 cubra todas las funcionalidades del Dash, se retira el Dash.
- **Estrategia:** strangler a nivel de dashboard, tab por tab.

---

## 7️⃣ ROADMAP PENDIENTE

| Fase | Fix / Feature | Estimación | Prioridad |
| :--- | :--- | :---: | :---: |
| **4.FastAPI.1** | **Dashboard Jinja2 (`app/templates/index.html` + endpoint `/`)** | 30 min | 🔴 **Alta — PRÓXIMO PASO** |
| **4.FastAPI.2** | **Tests para `app/`** (`test_app_*.py`) | 1.5 h | 🟡 Media |
| **4.FastAPI.3** | Commit + push del dashboard Jinja2 | 10 min | 🔴 Alta |
| σ legacy | Eliminar `schema_adapter.py` (deuda #11) | 1 h | 🔴 Alta |
| 3b.3 legacy | Deuda #15: debounce cascade | 30 min | 🟡 Media |
| 3c legacy | Deuda #16 (severidad KPIs) + Chip filtros activos | 1.5 h | 🟡 Media |
| perf legacy | Deuda #19: callback 2104 ms Calidad | 1-2 h | 🟡 Media |
| 5 legacy | Docker + Compose (Bloque 3B) | 2 h | 🟠 Media |
| σ legacy | Migración completa EN→ES (Opción A') | 5-8 h | 🔴 Alta (diferida) |
| σ legacy | Rename bilingüe incremental (ADR-0002) | Semanas 5-6 | 🟡 Media |
| — | `ServersideOutput` (si el uso lo justifica) | 2-3 h | 🟢 Baja |

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
| 1 fix = 1 commit = 1 lista corta de archivos. | Commit con 6+ archivos mezclando propósitos. |
| **`git clone` en vez de `git init`** cuando ya hay historial remoto. | `git init` + `remote add` + push (puede causar merge raro). |
| **`cp -R` desde backup a clon fresco** tras migraciones grandes. | Trabajar en carpeta `mkdir` sin repo git. |

### ✍️ Commits

- **Conventional Commits:** `feat:`, `fix:`, `refactor:`, `docs:`, `style:`, `test:`, `chore:`, `polish:`, `perf:`.
- **Un fix = un commit.** No mezclar propósitos.
- **Título en inglés**, cuerpo en español si aplica.
- **Verificar el mensaje antes de commitear.**
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
- **Arquitectura legacy:** `src/` (lógica) / `dashboard/` (presentación) / `tests/`.
- **Arquitectura nueva:** `app/` (FastAPI + SQLModel + templates).
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

### 🆕 Reglas nuevas (esta sesión)

- **Antes de `pip freeze > requirements.txt`:** verificar que estás en un venv. Si no, escribir el requirements a mano.
- **Al añadir un servicio nuevo (FastAPI):** usar puerto distinto al existente (8000 vs 8050) para coexistencia.
- **Al migrar de una tecnología a otra:** empezar con capa aditiva (nuevo `app/` sin tocar `src/`). No romper el legacy.
- **Antes de crear un nuevo directorio del proyecto:** verificar dónde está el proyecto original con `git remote -v` y `ls`. Nunca `mkdir` a ciegas en `$HOME`.

---

## 9️⃣ ⚠️ HISTORIAL DE ERRORES — NO REPETIR

*(Se mantienen los errores previos. Nuevos de esta sesión:)*

| ❌ Error | ✅ Correcto |
| :--- | :--- |
| **`mkdir -p ~/industrial-kpi-intelligence/app/...`** sin preguntar dónde está el proyecto. | Preguntar primero: `git remote -v` + `ls ~/Projects/`. Trabajar en el proyecto existente. |
| **Asumir que una carpeta nueva es el proyecto activo.** | Verificar con `git status` si es repo git y con `ls` si tiene los archivos originales. |
| **`pip3 freeze > requirements.txt` en Python global.** | Escribir el `requirements.txt` a mano con las dependencias top-level + transitivas críticas. |
| **`git init` + `git remote add`** cuando ya hay historial remoto. | `git clone` fresco + `cp -R` del trabajo nuevo. Evita merges de historial. |
| **Asumir que `NaiveDatetime` es importable desde `sqlmodel`.** | **NO existe.** Usar `sa_column=Column(DateTime(timezone=False))`. |
| **Confiar en `field_validator` en modelo SQLModel `table=True`.** | Pydantic no ejecuta validadores en modelos de tabla. Separar en `schemas.py` (`BaseModel`). |
| **Enviar `"id": 0` en POST a FastAPI.** | El `id` es autoincremental. **Nunca** enviarlo en el body de un POST de creación. |
| **Confundir el "example value" de Swagger UI con datos reales.** | El ejemplo se muestra por defecto. Para ver datos reales: clic en **"Try it out"** → **"Execute"**. |
| **`git push` sin PAT** → `Invalid username or token`. | Usar el PAT con scope `repo` + `workflow` como contraseña. Nunca la contraseña de GitHub. |
| **`rm -rf` de carpetas duplicadas sin verificar.** | Backup primero (`mv` a `.bak`), verificar en el proyecto original, luego borrar. |

---

## 🔟 📁 ARCHIVOS CLAVE Y COMANDOS

### 🗂️ Estructura del proyecto (post-migración)

```text
industrial-kpi-intelligence/
├── ARCHITECTURE.md
├── README.md                              # 460 tests + badges (Dash + FastAPI)
├── VISION.md
├── CHANGELOG.md
├── LICENSE                                # Elastic License 2.0
├── pyproject.toml
├── requirements.txt                       # 8 deps (FastAPI stack)
├── Procfile / render.yaml
├── .gitignore                             # +*.db, *.sqlite, kpis.csv, .env
├── .github/workflows/tests.yml            # Workflow "CI"
├── assets/style.css
│
├── app/                                   # 🆕 CAPA FASTAPI
│   ├── __init__.py
│   ├── main.py                            # FastAPI app + lifespan + GET/POST /kpis/
│   ├── models.py                          # SQLModel KPI (sa_column=DateTime(timezone=False))
│   ├── schemas.py                         # Pydantic KPICreate
│   ├── db.py                              # SQLite + create_db_and_tables + get_session
│   └── templates/                         # 🚧 PENDIENTE: index.html (Jinja2)
│
├── config/
│   ├── generator_config.yaml
│   ├── plant_config.yaml
│   └── quality_config.yaml
│
├── dashboard/                             # Legacy Dash (puerto 8050)
│   ├── app_layout.py
│   ├── empty_state.py
│   ├── export_helpers.py
│   ├── severity_icons.py
│   ├── filter_callbacks.py
│   ├── utils.py
│   ├── capability_callbacks.py
│   ├── control_charts_callbacks.py
│   ├── data_loader.py
│   ├── diagnostics_callbacks.py
│   ├── operational_analysis_callbacks.py
│   ├── quality_performance_callbacks.py
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
├── src/                                   # Lógica legacy
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
└── tests/                                 # 460 tests
    ├── test_empty_state.py
    └── ...
```

### ⌨️ Comandos verificados

```bash
# Protocolo de arranque
cd /Users/violeta/Projects/industrial-operations-intelligence/industrial-kpi-intelligence
source venv/bin/activate
which python                    # DEBE mostrar .../venv/bin/python

# Gates legacy
pytest                          # 460 passed
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

### 📋 Deuda #21 — Crear dashboard Jinja2 (Fase 4 FastAPI)

**Contexto:** la API FastAPI funciona (GET + POST verificados), pero aún no hay dashboard HTML. Falta el endpoint `GET /` y el template `app/templates/index.html`.

**Verificación previa (regla #4 — antes de tocar):**

```bash
cd /Users/violeta/Projects/industrial-operations-intelligence/industrial-kpi-intelligence
source venv/bin/activate

# 1) ¿Existe la carpeta templates?
ls -la app/templates/ 2>/dev/null || echo "No existe, hay que crearla"

# 2) ¿Existe el endpoint / en main.py?
grep -n "def dashboard\|TemplateResponse\|Jinja2Templates" app/main.py

# 3) ¿Está Jinja2 instalado?
python -c "import jinja2; print(jinja2.__version__)"
```

**Plan de ejecución:**

1. **Crear carpeta:** `mkdir -p app/templates`
2. **Crear template HTML:** `app/templates/index.html` con tabla `{{ kpis }}`.
3. **Añadir imports en `app/main.py`:**
   ```python
   from fastapi import Request
   from fastapi.responses import HTMLResponse
   from fastapi.templating import Jinja2Templates

   templates = Jinja2Templates(directory="app/templates")
   ```
4. **Añadir endpoint al final de `app/main.py`:**
   ```python
   @app.get("/", response_class=HTMLResponse)
   def dashboard(request: Request, session: Session = Depends(get_session)):
       kpis = session.exec(select(KPI)).all()
       return templates.TemplateResponse("index.html", {"request": request, "kpis": kpis})
   ```
5. **Verificación visual:** `uvicorn app.main:app --reload` → abrir `http://127.0.0.1:8000/`.
6. **Gates:** `pytest` + `ruff check .` (sin cambios esperados).
7. **`git status`** → `app/templates/index.html` + `app/main.py` modificados.
8. **Commit:**
   ```bash
   git commit -F - <<'EOF'
   feat(fastapi): add Jinja2 dashboard for KPI visualization

   Añade endpoint GET / que renderiza tabla HTML con todos los KPIs.
   Completa la capa de presentación del stack FastAPI + SQLModel.
   EOF
   git push origin main
   ```
9. **Verificar CI 2/2 verde.**

**⏱️ Estimación:** 30 min.

### 📌 Después del dashboard Jinja2

1. **Tests para `app/`** (deuda #22, 1.5 h, +25 tests).
2. **Eliminar `schema_adapter.py`** (deuda #11 legacy, 1 h).
3. **Deuda #15** — debounce cascade (30 min).
4. **Fase 3c** — Chip de filtros activos + severidad individual en KPIs (1.5 h).
5. **Deuda #19** — investigar callback 2104 ms de Calidad (1-2 h).
6. **Docker + Compose** (2 h).

---

## 1️⃣2️⃣ 💬 MENSAJE DE TRANSICIÓN (para pegar en chat nuevo)

```text
Contexto: pego abajo el TRASPASO_MAESTRO del proyecto Industrial KPI Intelligence.
Soy David, Ing. Civil Químico + dev autodidacta, semana 3/8 del Producto 01.

Estado: Fase 3b.2 completa (5/5 tabs con empty state) + cascades restaurados + 460 tests verdes.
Además, MIGRACIÓN A FASTAPI + SQLMODEL + SQLITE COMPLETADA (commit a162f15):
- app/models.py, app/schemas.py, app/db.py, app/main.py
- migrate_csv.py (CSV → SQLite)
- requirements.txt limpiado (8 deps)
- .gitignore ampliado (*.db, *.sqlite, kpis.csv)
- GET /kpis/ y POST /kpis/ verificados en Swagger UI (200 y 201)
Performance: ~2-3 s por cambio de filtro en el dashboard Dash legacy.

Próximo paso: Deuda #21 — crear dashboard Jinja2 (app/templates/index.html + endpoint /).
Estimación 30 min. Ver sección 11 del TRASPASO.

Deudas activas relevantes:
- #21 dashboard Jinja2 (alta, próximo paso)
- #22 sin tests para app/ (media)
- #11 eliminar schema_adapter.py (alta, legacy)
- #15 debounce cascade (media, legacy)
- #16 severidad individual KPIs rendimiento (media, legacy)
- #19 callback 2104 ms en Calidad (media, legacy)

Reglas clave:
- Protocolo de arranque: cd + source venv/bin/activate + verificar `which python`
- Leer el archivo antes de tocar
- git status ANTES y DESPUÉS de cada git add
- Un fix = un commit
- Verificación visual con ⌘ + Shift + R obligatoria
- pytest + ruff verdes antes de commitear
- NO usar TextEdit para markdown: usar GitHub Web Editor
- Tras editar en Web Editor: git pull --rebase
- Antes de crear un nuevo directorio del proyecto: verificar dónde está el proyecto original
- NUNCA enviar "id": 0 en POST a FastAPI
- NUNCA confundir el "example value" de Swagger UI con datos reales
- Al separar modelo DB vs schema API: usar schemas.py con BaseModel puro
- Al añadir un servicio nuevo: puerto distinto (8000 FastAPI vs 8050 Dash)
- Al migrar de tecnología: capa aditiva, no romper el legacy

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
- Cuando te equivoques (ej. recomendar `NaiveDatetime` sin verificar, `mkdir` a ciegas en `$HOME`, asumir que el "example value" de Swagger es el output real), decilo claro y corregí.

### 🏆 Hitos acumulados

- ✅ **Fase 3a completa** (5/5 tabs con export CSV).
- ✅ **Opción D** — consolidación del adapter.
- ✅ **Fase 3b.1** — loading states.
- ✅ **Fase 3b.3** — performance: -70% del tiempo original.
- ✅ **Fase 3b.2 completa** — empty states en 5/5 tabs + cascades.
- ✅ **460 tests, 0 regresiones.**
- ✅ **Migración a FastAPI + SQLModel + SQLite** (commit `a162f15`).
- ✅ **Persistencia real con SQLite** + modelo `KPI` funcional.
- ✅ **Doble stack coexistente:** Dash legacy (8050) + FastAPI (8000).
- ✅ **Comprensión del patrón de seguridad `sa_column`** para sobreescribir defaults restrictivos de SQLModel.

### 🔬 Lecciones metodológicas de este ciclo

- **Capa aditiva primero, refactor después.** Cuando se migra de una tecnología a otra, empezar con una carpeta nueva (`app/`) que coexiste con la legacy. No romper el legacy. El patrón strangler aplica a nivel de arquitectura completa.
- **Preguntar antes de crear.** Antes de `mkdir -p ~/proyecto/app`, preguntar dónde está el proyecto original con `git remote -v` y `ls`. Evita carpetas duplicadas en `$HOME`.
- **Separar modelo DB ↔ schema API es no negociable en FastAPI.** `KPI` (tabla) ≠ `KPICreate` (schema). Sin esta separación, Pydantic no convierte strings a `datetime` en modelos de tabla.
- **Swagger UI muestra ejemplos, no datos reales.** Para ver la respuesta del endpoint, siempre clic en "Try it out" → "Execute". Confundir uno con otro genera horas de depuración fantasma.
- **`sa_column` es la vía de escape.** Cuando SQLModel impone un default demasiado estricto (timezone-aware datetime), `sa_column=Column(...)` permite volver a SQLAlchemy crudo sin romper el modelo.
- **`pip freeze` no es `requirements.txt`.** Un `requirements.txt` limpio se escribe a mano con las dependencias top-level + transitivas críticas. `pip freeze` captura todo el entorno, no el proyecto.
- **`git clone` > `git init` cuando ya hay historial remoto.** El segundo puede causar merges de historial raros. El primero es limpio y predecible.
- **Los modelos de IA gratuitos en terminal a veces se desvían.** Cuando `dsf` (fixer) recibe un script, a veces lo reescribe entero en vez de corregirlo. Revisar siempre el output con `cat` + `git diff`.

### 📊 Métricas del ciclo

- **Commits:** 2 (1 web + 1 local).
- **Archivos tocados:** 7 (5 nuevos, 2 modificados).
- **Líneas:** +139 / -29.
- **Tests:** 460 → 460 (sin cambios).
- **Tiempo total:** ~3 h de sesión distribuida.

---

> 📌 **Fin del TRASPASO_MAESTRO.**  
> 🗓️ **Última actualización:** Migración FastAPI + SQLModel + SQLite completada (commit `a162f15`).  
> 🚀 **Próximo paso:** Deuda #21 — crear dashboard Jinja2 (`app/templates/index.html` + endpoint `GET /`).
