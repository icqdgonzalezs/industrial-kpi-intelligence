# 🏛️ Architecture — Industrial KPI Intelligence

> 📌 **Propósito:** describir la arquitectura técnica del Producto 01 del ecosistema.
> 📥 **Audiencia:** desarrolladores, revisores técnicos, futuros colaboradores.
> 🗓️ **Última actualización:** Semana 3/8, Fase 4a + Doc + σ cerradas.
> 🔗 **Referencias:** [`VISION.md`](VISION.md) · [`docs/adr/`](docs/adr/) · [`docs/TECHNICAL_DOCUMENTATION.md`](docs/TECHNICAL_DOCUMENTATION.md)

---

## 🎯 1. Visión general

**Industrial KPI Intelligence** es un dashboard industrial de soporte de decisiones para plantas manufactureras. Calcula KPIs de calidad, capacidad de proceso (Pp/Ppk), control estadístico (SPC) y OEE, con alineación a estándares industriales (ISA-95, AIAG SPC, NIST 6.1.3, ISA-101, WCAG 2.1).

**Rol arquitectónico:** *Decision Support System*. No es un SCADA, MES ni PLC. Lee datos, los analiza, y presenta hallazgos accionables.

**Producto 01** del ecosistema `Industrial Operations Intelligence` (ver [`VISION.md`](VISION.md)).

---

## 🗂️ 2. Estructura del repositorio

```text
industrial-kpi-intelligence/
├── assets/          → CSS del tema oscuro (ISA-101)
├── config/          → YAMLs de configuración (SSOT)
├── dashboard/       → Presentación (Plotly Dash)
├── data/            → Dataset sintético canónico
├── docs/            → Documentación extendida + ADRs
├── imagenes/        → Capturas del README
├── scripts/         → Utilidades puntuales (verificación, migración)
├── src/             → Lógica de negocio pura (sin UI)
├── tests/           → 390 tests (unitarios + integración)
├── pyproject.toml   → Config pytest + ruff
└── requirements.txt → Dependencias
```

**Separación de concerns (3 capas):**

| Capa | Carpeta | Responsabilidad |
|---|---|---|
| **Lógica de negocio** | `src/` | Cálculos puros, sin dependencias de UI. 100% testeable. |
| **Presentación** | `dashboard/` | Dash, callbacks, componentes visuales, formateo. |
| **Configuración** | `config/` | YAMLs como SSOT (Single Source of Truth). |

**Regla:** `src/` **no importa** de `dashboard/`. La dependencia va **en un solo sentido** (`dashboard/` → `src/`). Esto garantiza que la lógica de negocio sea portable (CLI, API REST, notebooks, otros frontends).

---

## 🏗️ 3. Diagrama de capas

```text
┌──────────────────────────────────────────────────────────────────┐
│  CAPA 1 — PRESENTACIÓN (dashboard/)                              │
│                                                                  │
│  Módulos por pestaña (patrón *_callbacks.py + *_components.py):  │
│   • kpi_callbacks.py         + kpi_components.py                 │
│   • capability_callbacks.py  + capability_components.py          │
│   • control_charts_*.py                                          │
│   • diagnostics_*.py                                             │
│   • quality_performance_*.py                                     │
│   • operational_analysis_*.py                                    │
│   • plant_overview.py                                            │
│                                                                  │
│  Presenters (traducción + i18n):                                 │
│   • kpi_presenter.py     (delega a src/kpi_thresholds)           │
│   • oee_presenter.py     (keys EN → labels ES)                   │
│   • severity_icons.py    (SSOT: ✓ / ⚠ / ✕ / vacío)              │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│  CAPA 2 — LÓGICA DE NEGOCIO (src/)                                │
│                                                                  │
│  Análisis:                                                       │
│   • kpis.py            → FPY, scrap, reproceso, Pareto           │
│   • capability.py      → Pp/Ppk (NIST 6.1.3 / ISO 22514)         │
│   • control_charts.py  → Cartas I-MR (Western Electric)          │
│   • oee.py             → OEE = A × P × Q (ISA-95 / TPM)          │
│   • diagnostics.py     → Motor de diagnóstico priorizado         │
│                                                                  │
│  SSOT de umbrales (leen YAML):                                   │
│   • kpi_thresholds.py         → umbrales KPI (success/warning)   │
│   • capability_thresholds.py  → umbrales Ppk + PPM               │
│                                                                  │
│  Infraestructura:                                                │
│   • data_generator.py     → Generador determinista (seed=42)     │
│   • schema_adapter.py     → EN → ES (deuda activa, ver §7)       │
│   • dataset_metadata.py   → Frescura del dataset                 │
│   • validation.py         → Data quality gate                    │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│  CAPA 3 — CONFIGURACIÓN (config/)                                │
│                                                                  │
│   • generator_config.yaml   → Parámetros del dataset sintético   │
│   • plant_config.yaml       → Líneas, equipos, turnos, operarios │
│   • quality_config.yaml     → SSOT unificado:                    │
│        ├─ ppk_thresholds       (1.67 / 1.33 / 1.00)              │
│        ├─ ppm_thresholds       (100 / 1000)                      │
│        ├─ kpi_thresholds       (FPY, defectos, scrap)            │
│        ├─ variables_criticas   (LSL / USL por variable)          │
│        └─ variables[FILL|SEAM|CHECK|CAPPER|FFS|SEAL|PACK]        │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🎯 4. Patrón SSOT (Single Source of Truth)

El proyecto usa **SSOT en YAML + wrapper Python** para todos los umbrales. El principio es: **nunca hardcodear un umbral en el código de negocio**.

### Ejemplo 1 — Umbrales KPI (`kpi_thresholds`)

```python
# src/kpi_thresholds.py
def clasificar_kpi_por_nombre(nombre: str, valor: float) -> StatusType:
    config = cargar_umbrales_kpi()  # Lee YAML, cacheado con @lru_cache
    kpi = config.get(nombre)
    return clasificar_kpi(valor, kpi["thresholds"], kpi["direction"])
```

```yaml
# config/quality_config.yaml
kpi_thresholds:
  fpy:
    direction: higher_is_better
    success: 0.95
    warning: 0.90
  tasa_defectos:
    direction: lower_is_better
    success: 0.03
    warning: 0.05
```

### Ejemplo 2 — Umbrales Ppk + PPM (`capability_thresholds`)

```python
# src/capability_thresholds.py
def cargar_umbrales_ppk() -> dict:
    return _leer_seccion_cacheados(str(QUALITY_CONFIG_PATH), "ppk_thresholds")

def clasificar_ppk_puro(ppk: float, umbrales: dict | None) -> str:
    t = umbrales or DEFAULT_PPK_THRESHOLDS
    if ppk >= t["clase_mundial"]: return "Clase mundial"
    if ppk >= t["capaz"]:        return "Capaz"
    if ppk >= t["marginal"]:     return "Marginal"
    return "No capaz"
```

### Ventajas del patrón

| Aspecto | Beneficio |
|---|---|
| **Multi-cliente SaaS** | Cada cliente puede tener su propio `quality_config.yaml`. |
| **Tests sin I/O** | Los umbrales se pueden inyectar como parámetro. |
| **Fallback seguro** | Si el YAML falta, se usan `DEFAULT_*` en el módulo. Nunca crash. |
| **Cero duplicación** | Un cambio en el YAML se propaga a todo el sistema. |

---

## 🔄 5. Flujo de datos

```text
[data/raw/synthetic_production_data.csv]   ← 18,078 filas, esquema EN
            │
            │ ①  dashboard/data_loader.py lee el CSV
            ▼
[DataFrame EN]
            │
            │ ②  src/schema_adapter.py traduce EN → ES
            ▼
[DataFrame ES]   ← contrato interno del motor analítico
            │
            │ ③  Filtros: filter_engine.py (línea, equipo, turno, operador)
            ▼
[DataFrame ES filtrado]   ← almacenado en dcc.Store (store-datos-filtrados)
            │
            ├── ④a  src/kpis.py         → FPY, defectos, scrap, Pareto
            ├── ④b  src/capability.py   → Pp/Ppk + rendimiento spec
            ├── ④c  src/control_charts.py → Cartas I-MR
            ├── ④d  src/oee.py          → OEE (A×P×Q)
            └── ④e  src/diagnostics.py  → Hallazgos priorizados
            │
            ▼
[Resultados dict + clasificación semántica]
            │
            │ ⑤  Presenters: kpi_presenter.py, oee_presenter.py, severity_icons.py
            ▼
[Componentes Dash: html.Span con className + icono Unicode]
            │
            │ ⑥  Render en el browser (assets/style.css)
            ▼
[Dashboard interactivo: KPIs con color + icono, gráficos Plotly]
```

**Convención de keys de datos:** inglés (`world_class`, `availability`, `performance`) → permite i18n real. Los presenters traducen a español según contexto (ver [ADR-0002](docs/adr/0002-naming-convention.md)).

---

## 🧪 6. Estrategia de testing

**390 tests, todos verdes, organizados por módulo.**

| Tipo | Ubicación | Ejemplos |
|---|---|---|
| **Unitarios puros** | `tests/test_<modulo>.py` | `test_kpis.py`, `test_capability.py` |
| **Wiring de callbacks** | `tests/test_<modulo>_callbacks.py` | `test_kpi_callbacks.py` |
| **Integración** | `tests/test_dash_app.py` | Carga completa + filtros |
| **Contratos** | `tests/test_validation.py` | Data quality gate |
| **Golden tests** | `tests/test_severity_icons.py` | Iconografía WCAG 2.1 |

**Reglas de testing (no negociables):**

1. **Código + tests juntos** en el mismo commit.
2. **Función pura** → test parametrizado (ej. `clasificar_ppk` con 15 casos).
3. **I/O** → test con `tmp_path` (fixtures de pytest).
4. **Nunca mockear** la lógica de negocio. Solo I/O externo.
5. **CI verde 2/2** (ruff + pytest) antes de mergear.

---

## 🛠️ 7. Deuda arquitectónica conocida

### 7.1 ⚠️ `schema_adapter.py` — Adapter transitorio (ver ADR-0001)

- **Qué es:** capa que traduce el dataset canónico EN → contrato interno ES.
- **Por qué existe:** migración incremental sin big-bang (patrón strangler).
- **Condición de muerte:** cuando `validation.py` consuma directamente el esquema EN.
- **Plazo original:** Semanas 3-4 del plan de 8 semanas.
- **Estado actual:** Semana 3, **criterios cumplidos** (390 tests > 225, CI verde, ADRs Semana 2 mergeados).
- **Acción pendiente:** eliminar en commit `refactor: remove schema_adapter after validation.py migrated to canonical schema`.

### 7.2 ⚠️ Doble convención de nombres (ver ADR-0002)

- **Qué es:** API analítica legacy en español, módulos nuevos en inglés.
- **Por qué existe:** rename global rompería ~225 tests en un solo commit.
- **Plan:** rename incremental por módulo, respetando ventana de 2 semanas entre cada uno.
- **Dato clave:** keys de datos **siempre en inglés**, labels visibles al usuario **siempre en español**.

### 7.3 ℹ️ Umbrales hardcodeados residuales

- `PPM_WORLD_CLASS` / `PPM_ACCEPTABLE` → **migrados a YAML** (Fase σ, commit `8138498`).
- `UMBRAL_PPK_*` → **migrados a YAML** (Fase σ, commit `8138498`).

---

## 🚀 8. Cómo escalar (referencia a VISION.md)

Este repositorio es el **Producto 01** del ecosistema `Industrial Operations Intelligence`. Los otros 5 productos (ver [`VISION.md`](VISION.md)) siguen arquitecturas similares:

| Producto | Stack | Patrón reutilizable |
|:---:|---|---|
| **00** Traceability | FastAPI + SQLModel + Jinja2 | SSOT en YAML + tests + CI |
| **02** Digital Twin | Python + SimPy | Lógica pura en `src/` + presentación separada |
| **03** Predictive Maintenance | Python + Scikit-learn | Pipeline sklearn → API → dashboard |
| **04** Process Optimizer | Python + SciPy + OR-Tools | Solvers en `src/` + restricciones en YAML |
| **05** AI Copilot | LLM + RAG | Índice vectorial + prompt templates en `src/` |

**Patrones que se replican:**
- Separación `src/` (lógica) vs presentación.
- SSOT en YAML para configuración.
- Tests + CI antes de mergear.
- Conventional Commits.
- Documentación versionada en `docs/`.

---

## 📏 9. Convenciones

### Código

- **Idioma:** inglés (nombres de función, clases, variables).
- **Docstrings:** español (para el equipo).
- **Mensajes de error:** inglés (facilita debugging + i18n futuro).

### Estructura

- **`src/`** solo lógica de negocio. Sin dependencias de Dash.
- **`dashboard/`** solo presentación. Importa de `src/`, nunca al revés.
- **`tests/`** espeja la estructura de `src/` + `dashboard/`.
- **`docs/`** documentación extendida (ADRs, bitácoras, master plan).

### Commits

- **Conventional Commits:** `feat:`, `fix:`, `refactor:`, `docs:`, `style:`, `test:`, `chore:`, `polish:`.
- **Un fix = un commit.** No mezclar propósitos.
- **Título en inglés**, cuerpo en español si aplica.

### Branching

- `main` → rama estable, siempre verde.
- `feature/<nombre>`, `fix/<nombre>`, `refactor/<nombre>` → ramas de trabajo.
- **Un PR por feature/fix.** CI verde obligatorio antes de merge.

---

## 🎓 10. Principios de diseño

| Principio | Aplicación en este proyecto |
|---|---|
| **SRP** (Single Responsibility) | Cada módulo hace una cosa. `kpi_thresholds.py` solo clasifica. |
| **DRY** (Don't Repeat Yourself) | SSOT en YAML. Un umbral, un lugar. |
| **YAGNI** (You Aren't Gonna Need It) | No extraer abstracciones hasta tener 3 casos de uso. |
| **Fail-safe** | Si el YAML falta, se usan defaults. Nunca crash. |
| **Testeable por diseño** | Funciones puras + I/O aislado + inyección de dependencias. |
| **Estándares industriales** | Cada métrica cita su norma (ISA-95, AIAG SPC, NIST 6.1.3). |
| **Accesibilidad por diseño** | WCAG 2.1 desde el inicio. Iconografía no cromática. |

---

> 📌 **Fin del ARCHITECTURE.md.**
> Próxima actualización: cuando se elimine el `schema_adapter.py` (ver §7.1) o se cierre el renombrado bilingüe (ver §7.2).
