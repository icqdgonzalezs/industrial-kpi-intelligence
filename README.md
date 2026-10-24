# 📊 Industrial KPI Intelligence

## 🚀 Industrial Production & Quality Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLModel](https://img.shields.io/badge/SQLModel-0.0.46-FF6F00?logo=python&logoColor=white)](https://sqlmodel.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Jinja2](https://img.shields.io/badge/Jinja2-3.1.6-B41717?logo=jinja&logoColor=white)](https://jinja.palletsprojects.com/)
[![HTMX](https://img.shields.io/badge/HTMX-2.0.4-3D72D7?logo=htmx&logoColor=white)](https://htmx.org/)
[![Groq](https://img.shields.io/badge/Groq-LLM-F55036?logo=groq&logoColor=white)](https://groq.com/)
[![Tests](https://img.shields.io/badge/Tests-546%20passing-brightgreen)](tests/)
[![CI](https://github.com/icqdgonzalezs/industrial-kpi-intelligence/actions/workflows/tests.yml/badge.svg)](https://github.com/icqdgonzalezs/industrial-kpi-intelligence/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/License-Elastic_License_2.0-blue)](LICENSE)

**API REST y panel de control de KPIs de calidad industrial con IA integrada.** Cálculo real de FPY, tasas de scrap/reproceso, diagrama de Pareto, comparación operacional (línea/turno/máquina), análisis de capacidad de proceso (**Pp/Ppk**, NIST 6.1.3) y motor OEE (**Availability × Performance × Quality**, ISA-95/TPM). Incluye chat conversacional, diagnósticos automáticos, reportes ejecutivos narrados y detección de anomalías estadísticas.

---

## 🧠 Capacidades de IA (Groq LLM)

El proyecto integra el modelo **`openai/gpt-oss-120b`** (configurable vía `GROQ_MODEL`) para potenciar la toma de decisiones:

| Funcionalidad | Endpoint | Descripción |
| :--- | :--- | :--- |
| **Chat con KPIs** | `POST /chat/` | Preguntá en lenguaje natural sobre el estado de la planta. |
| **Diagnóstico asistido** | `GET /diagnostics/ai` | Analiza hallazgos (hotspots, capacidad, Pareto) y narra las causas raíz. |
| **Reporte ejecutivo** | `GET /reports/executive` | Resumen de una página con tono CFO/COO para gerencia. |
| **Detección de anomalías** | `GET /anomalies/` | Identifica valores atípicos mediante z-score e IQR (determinista, sin ML pesado). |

> 🔐 **Seguridad:** Todos los endpoints de IA están protegidos con **JWT** y **rate limiting** (30 req/min por IP).

---

## 📌 Problema industrial abordado

Una planta de envasado con **múltiples líneas, 23 equipos y 3 turnos** necesita monitorear su desempeño de calidad para identificar dónde se concentran los defectos, comparar desempeño entre máquinas/turnos, verificar si el proceso es estadísticamente capaz de cumplir especificaciones y calcular el **OEE** real de sus equipos críticos.

## 🎯 Objetivos

1. Calcular KPIs descriptivos de calidad (FPY, tasa de defectos, scrap, reproceso).
2. Identificar concentración de causas de defecto (Pareto 80/20).
3. Comparar desempeño por línea, máquina, turno y operador.
4. Evaluar capacidad de proceso (**Pp/Ppk**, Six Sigma) de variables críticas.
5. Calcular **OEE** de equipos críticos bajo estándar ISA-95/TPM.
6. Exponer todos los KPIs a través de una **API REST** (FastAPI) para integración con ERP, MES o PLCs.
7. Visualizar los KPIs en un **dashboard web** (Jinja2 + HTMX) para toma de decisiones.
8. **Generar diagnósticos y reportes narrados por IA** para acelerar la interpretación.

---

## 📊 Datos y metodología

**Los datos son 100% simulados**, generados por `src/data_generator.py` con semilla fija (`random_seed=42`) para reproducibilidad total. **18,078 registros** correspondientes a un año de operación.

Supuestos documentados en `config/generator_config.yaml`:

- **23 equipos** distribuidos en 4 líneas de producción (L1-L4).
- **3 turnos** con efectos diferenciados. Turno Noche tiene mayor tasa de defectos (fatiga/menor supervisión), documentado en la literatura de calidad.
- **Variables continuas de calidad**: peso y longitud, con especificaciones LSL/USL en `config/quality_config.yaml`.
- **Columnas OEE**: `planned_time_min`, `planned_downtime_min`, `unplanned_downtime_min`, `ideal_cycle_time_sec` — necesarias para el motor OEE.

---

Fórmulas (ver `src/kpis.py`, `src/capability.py`, `src/oee.py`):

```text
FPY = (producidas - defectuosas) / producidas

Pp = (USL - LSL) / (6 * sigma_overall)                    # sigma con ddof=1
Ppk = min[(USL - media)/(3sigma), (media - LSL)/(3sigma)]

OEE = Availability × Performance × Quality
Availability = Run Time / Planned Production Time
Performance = (Ideal Cycle Time × Units Produced) / Run Time    # capeado a 1.0
Quality = Good Units / Total Units Produced                     # = FPY
```

> **Nota NIST 6.1.3 / ISO 22514**: lo que históricamente se etiquetó como Cp/Cpk en este proyecto usa **sigma overall** (`ddof=1`), por lo que corresponde técnicamente a **Pp/Ppk**. El rename se aplicó en Semana 2 con tests actualizados. Los Cp/Cpk reales (sigma within, `MRbar/d2`) se agregan en una iteración futura junto con la carta X-bar/R.

---

## 📈 Resultados clave (reproducibles — se recalculan al correr el dashboard)

- **OEE promedio de planta: 0.8733** — coherente con benchmarks TPM de manufactura discreta (85-92%).
- **Performance con variabilidad realista**: mean 0.8733, std 0.0584 (dataset de 18k registros, seed fija).
- **FPY global: 95.7%** | Tasa de scrap: 1.29% | Tasa de reproceso: 2.97%.
- **Diagnóstico priorizado** por severidad (PRIORITY / WATCH / INFO) sobre hotspots de equipo/turno, capacidad de proceso y concentración de Pareto.
- **Pp/Ppk calculados** para variables continuas críticas, con clasificación Six Sigma (Capaz / Marginal / No capaz).

---

## 📸 Capturas del panel

**Panel principal — KPIs críticos y evolución de la tasa de defectos**

![Panel principal](imagenes/panel_vista_previa1.png)

**Análisis de causa raíz, comparación operacional y capacidad de proceso (Pp/Ppk)**

![Análisis y capacidad](imagenes/panel_vista_previa2.png)

---

## 🛠️ Stack tecnológico

| Herramienta | Uso |
|---|---|
| Python 3.11 | Lenguaje base (compatibilidad con pyarrow en macOS antiguos) |
| **FastAPI** | Framework web para la API REST y el dashboard |
| **SQLModel** | ORM (SQLAlchemy + Pydantic) para modelar la base de datos |
| **SQLite / PostgreSQL** | Base de datos relacional (SQLite en local, PostgreSQL en producción) |
| **Jinja2** | Motor de plantillas para el dashboard HTML |
| **HTMX** | Interactividad sin SPA (partials renderizados en servidor) |
| **Groq SDK** | Cliente para el modelo LLM (`openai/gpt-oss-120b`) |
| Pandas / NumPy | Procesamiento de datos |
| PyYAML | Configuración externalizada |
| PyJWT / bcrypt | Autenticación y hashing de contraseñas |
| Pytest | Suite de **546 tests** (460 legacy + 86 app/) |
| Ruff | Linter (pin `ruff==0.16.6` en CI para reproducibilidad) |
| GitHub Actions | CI: `ruff check` + `pytest --cov` en cada push |
| Railway | Deploy en producción (PaaS + PostgreSQL) |

---

## ⚙️ Instalación y ejecución rápida

```bash
# Clonar repositorio
git clone https://github.com/icqdgonzalezs/industrial-kpi-intelligence.git
cd industrial-kpi-intelligence

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Migrar datos desde CSV a SQLite (solo la primera vez)
python3 migrate_csv.py

# Levantar el servidor FastAPI (API + Dashboard)
uvicorn app.main:app --reload
```

**URLs disponibles:**

- API (Swagger UI): http://127.0.0.1:8000/docs
- Dashboard HTML: http://127.0.0.1:8000/
- Documentación OpenAPI: http://127.0.0.1:8000/openapi.json

> ⚠️ **Nota de compatibilidad (macOS 10.14 Mojave o anterior):** este proyecto requiere Python 3.11, no 3.13+. `pyarrow` (dependencia del stack de datos) no publica binarios precompilados para Python 3.13 en macOS antiguos. Instalar Python 3.11 desde [python.org](https://www.python.org/) si es necesario.

```bash
# Opciones avanzadas
# Regenerar el dataset sintético (18,078 registros, semilla fija reproducible)
python -m src.data_generator

# Correr la suite de tests completa (546 tests)
pytest tests/ -v

# Correr la suite con cobertura
pytest tests/ -v --cov=src --cov=dashboard --cov=app

# Verificar lint
ruff check .

# Evidencia numérica del motor OEE (mean/std/min/max + histograma)
python scripts/check_oee_distribution.py
```

---

## 🌐 API REST — Endpoints

| Método | Endpoint | Descripción | Auth |
| :--- | :--- | :--- | :--- |
| GET | `/kpis/` | Lista todos los KPIs registrados | Público |
| POST | `/kpis/` | Crea un nuevo KPI | JWT |
| GET | `/` | Dashboard HTML con tabla de KPIs | Redirige a `/login` si no hay sesión |
| GET | `/docs` | Documentación interactiva (Swagger UI) | Público |
| POST | `/auth/login` | Inicia sesión y devuelve JWT + cookie HttpOnly | Público |
| GET | `/auth/me` | Información del usuario autenticado | JWT |
| POST | `/auth/logout` | Cierra sesión (borra cookie) | Público |
| POST | `/chat/` | Chat con IA sobre los KPIs | JWT + Rate Limit |
| GET | `/diagnostics/ai` | Diagnóstico narrado por IA | JWT + Rate Limit |
| GET | `/reports/executive` | Reporte ejecutivo narrado por IA | JWT + Rate Limit |
| GET | `/anomalies/` | Detección de anomalías (z-score/IQR) | JWT + Rate Limit |

**Ejemplo con curl (KPIs):**

```bash
# Listar todos los KPIs
curl http://127.0.0.1:8000/kpis/

# Crear un nuevo KPI (requiere token JWT)
curl -X POST http://127.0.0.1:8000/kpis/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "nombre": "Disponibilidad",
    "valor": 95.2,
    "unidad": "%",
    "timestamp": "2026-09-23T10:00:00",
    "linea_produccion": "Linea 3"
  }'
```

---

## 📁 Estructura del proyecto

```text
industrial-kpi-intelligence/
├── app/                               # CAPA FASTAPI
│   ├── main.py                        # FastAPI + CORS + lifespan + routers
│   ├── models.py                      # SQLModel KPI + User (con tenant_id)
│   ├── schemas.py                     # Pydantic (KPICreate, UserLogin, Token, Anomalia)
│   ├── db.py                          # Configuración de SQLite/Postgres
│   ├── auth.py                        # JWT + bcrypt + get_current_user
│   ├── limiter.py                     # Rate limiter propio (deque de timestamps)
│   ├── routers/
│   │   ├── auth.py                    # Login, logout, /auth/me
│   │   ├── chat.py                    # POST /chat/ (IA)
│   │   ├── diagnostics.py             # GET /diagnostics/ai (IA)
│   │   ├── reports.py                 # GET /reports/executive (IA)
│   │   └── anomalies.py               # GET /anomalies/ (IA.4)
│   ├── services/
│   │   ├── llm_chat.py                # Groq + MODELO_DEFAULT (env var)
│   │   ├── llm_diagnostics.py         # Prompt para diagnóstico
│   │   ├── llm_reports.py             # Prompt para reportes ejecutivos
│   │   ├── executive_kpis.py          # Agregación de KPIs para reportes
│   │   ├── dataset_loader.py          # Wrapper de src/
│   │   └── anomaly_detector.py        # Lógica z-score/IQR
│   └── templates/                     # Jinja2 + HTMX (partials)
├── config/                            # YAMLs (quality, plant, generator)
├── data/                              # Dataset sintético
├── dashboard/                         # (Legacy) Dash — en retirada
├── src/                               # Lógica de dominio (kpis, oee, capability)
├── tests/                             # 546 tests (app/ + legacy)
├── docs/                              # ADRs, learning journal, TRASPASO
├── scripts/                           # Utilidades (seed_admin, check_oee)
├── static/                            # HTMX, CSS
├── .github/workflows/tests.yml        # CI (ruff + pytest --cov)
├── migrate_csv.py                     # Migración CSV → SQLite
├── requirements.txt                   # Dependencias
├── pyproject.toml                     # Configuración de Ruff y pytest
├── Procfile                           # Railway (uvicorn)
├── LICENSE                            # Elastic License 2.0
└── README.md
```

---

## 🔎 Conclusiones y líneas de mejora futuras

- **Motor de diagnóstico** prioriza automáticamente los hallazgos por severidad (PRIORITY/WATCH/INFO), combinando hotspots de equipo/turno, capacidad de proceso y concentración de Pareto.
- **El Ppk marginal** en variables continuas sugiere que el proceso no tiene margen de seguridad ante variabilidad adicional — se recomienda reducir sigma antes de ampliar límites de especificación.
- **OEE en 0.8733** de planta con Performance limitado por pérdidas de ritmo (micro-paradas, ajustes, variabilidad de turno) — coherente con benchmarks industriales.
- **Líneas futuras:** migración completa de Dash a FastAPI, incorporación de datos reales de planta vía OPC-UA, y RBAC (roles) para usuarios.

---

## 📚 Documentación

| Documento | Propósito |
| :--- | :--- |
| `docs/learning-journal/` | Bitácora de aprendizaje semana a semana (qué, por qué, cómo) |
| `docs/adr/` | Architecture Decision Records (decisiones arquitectónicas) |
| `docs/industrial-kpi-intelligence-master-plan.md` | Especificación completa del producto |
| `docs/nist_references/` | Referencias NIST (SPC, capability) |
| `TECHNICAL_DOCUMENTATION.md` | Referencia técnica por módulo |
| `CHANGELOG.md` | Historial de cambios reales |

---

## 📄 Licencia y Uso

Este proyecto está licenciado bajo **Elastic License 2.0 (ELv2)**, no MIT/Apache.

La diferencia práctica:

| Perfil | ¿Qué puedes hacer? |
| :--- | :--- |
| **Evaluador técnico / reclutador / portafolio** | Clonar, leer, ejecutar localmente, modificar para tu propio aprendizaje o evaluación, usar como referencia en una entrevista técnica. Sin restricciones. |
| **Empresa que quiere usarlo internamente** | Desplegarlo en tu propia infraestructura (on-premise o tu propia nube) para tu propia operación, con las mismas libertades de copia/modificación. |
| **Empresa que quiere revenderlo como servicio hosted a terceros** | **No permitido** bajo esta licencia. Ese uso requiere un acuerdo comercial conmigo — es exactamente la actividad que la licencia protege. |
| **Cliente pagando (Starter/Professional/Enterprise)** | Recibe una licencia de uso comercial explícita como parte del contrato de suscripción, con SLA, soporte y actualizaciones — independiente de los términos de este repositorio público. |

**En una frase:** puedes leer, correr y aprender de todo el código libremente. Lo único que no puedes hacer es tomarlo y ofrecerlo como tu propio SaaS competidor. Si tu empresa quiere usarlo como producto (no solo evaluarlo), hablemos de una licencia comercial.

Ver [LICENSE](LICENSE) para el texto legal completo.

---

## 👤 Autor

**David González** — Ingeniero Civil Químico | Data Analytics | Mejora Continua

[![LinkedIn](https://img.shields.io/badge/LinkedIn-David_Gonz%C3%A1lez-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/davidgonzalezsz)
[![GitHub](https://img.shields.io/badge/GitHub-icqdgonzalezs-181717?style=flat&logo=github&logoColor=white)](https://github.com/icqdgonzalezs)
[![Email](https://img.shields.io/badge/Email-icq.dgonzalezs%40gmail.com-EA4335?style=flat&logo=gmail&logoColor=white)](mailto:icq.dgonzalezs@gmail.com)

*Proyecto desarrollado como parte del portafolio profesional en análisis de datos industriales.*
