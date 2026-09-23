# 📊 Industrial KPI Intelligence

## 🚀 Industrial Production & Quality Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLModel](https://img.shields.io/badge/SQLModel-0.0.46-FF6F00?logo=python&logoColor=white)](https://sqlmodel.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Jinja2](https://img.shields.io/badge/Jinja2-3.1.6-B41717?logo=jinja&logoColor=white)](https://jinja.palletsprojects.com/)
[![Tests](https://img.shields.io/badge/Tests-390%20passing-brightgreen)](tests/)
[![CI](https://github.com/icqdgonzalezs/industrial-kpi-intelligence/actions/workflows/tests.yml/badge.svg)](https://github.com/icqdgonzalezs/industrial-kpi-intelligence/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/License-Elastic_License_2.0-blue)](LICENSE)

**API REST y panel de control de KPIs de calidad industrial** con cálculo real de FPY, tasas de scrap/reproceso, diagrama de Pareto, comparación operacional (línea/turno/máquina), análisis de capacidad de proceso (**Pp/Ppk**, NIST 6.1.3) y motor OEE (**Availability × Performance × Quality**, ISA-95/TPM).

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
7. Visualizar los KPIs en un **dashboard web** (Jinja2) para toma de decisiones.
8. Generar conclusiones accionables, no solo gráficos.

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
```
FPY = (producidas - defectuosas) / producidas

Pp = (USL - LSL) / (6 * sigma_overall) # sigma con ddof=1
Ppk = min[(USL - media)/(3sigma), (media - LSL)/(3sigma)]

OEE = Availability × Performance × Quality
Availability = Run Time / Planned Production Time
Performance = (Ideal Cycle Time × Units Produced) / Run Time # capeado a 1.0
Quality = Good Units / Total Units Produced # = FPY
```

---


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
| **SQLite** | Base de datos relacional ligera (sin servidor) |
| **Jinja2** | Motor de plantillas para el dashboard HTML |
| Pandas / NumPy | Procesamiento de datos |
| PyYAML | Configuración externalizada |
| Pytest | Suite de **390 tests** unitarios |
| Ruff | Linter (pin `ruff==0.16.6` en CI para reproducibilidad) |
| GitHub Actions | CI: `ruff check` + `pytest --cov` en cada push |

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
- **API (Swagger UI):** http://127.0.0.1:8000/docs
- **Dashboard HTML:** http://127.0.0.1:8000/
- **Documentación OpenAPI:** http://127.0.0.1:8000/openapi.json

⚠️ **Nota de compatibilidad (macOS 10.14 Mojave o anterior):** este proyecto requiere **Python 3.11**, no 3.13+. pyarrow (dependencia del stack de datos) no publica binarios precompilados para Python 3.13 en macOS antiguos. Instalar Python 3.11 desde python.org si es necesario.

---

```bash
# Opciones avanzadas
# Regenerar el dataset sintético (18,078 registros, semilla fija reproducible)
python -m src.data_generator

# Correr la suite de tests completa (390 tests)
pytest tests/ -v

# Correr la suite con cobertura
pytest tests/ -v --cov=src --cov=dashboard

# Verificar lint
ruff check .

# Evidencia numérica del motor OEE (mean/std/min/max + histograma)
python scripts/check_oee_distribution.py
```

---

## 🌐 API REST — Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/kpis/` | Lista todos los KPIs registrados |
| `POST` | `/kpis/` | Crea un nuevo KPI |
| `GET` | `/` | Dashboard HTML con tabla de KPIs |
| `GET` | `/docs` | Documentación interactiva (Swagger UI) |

**Ejemplo con `curl`:**

```bash
# Listar todos los KPIs
curl http://127.0.0.1:8000/kpis/

# Crear un nuevo KPI
curl -X POST http://127.0.0.1:8000/kpis/ \
  -H "Content-Type: application/json" \
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

```
industrial-kpi-intelligence/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Aplicación FastAPI (endpoints + dashboard)
│   ├── models.py                  # Modelo SQLModel (tabla KPI)
│   ├── schemas.py                 # Schema Pydantic para validación de entrada
│   ├── db.py                      # Configuración de SQLite y sesión
│   └── templates/
│       └── index.html             # Dashboard HTML con Jinja2
├── config/
│   ├── quality_config.yaml        # LSL/USL, umbrales Ppk (Six Sigma)
│   ├── plant_config.yaml          # Definición de líneas, equipos, turnos, operadores
│   └── generator_config.yaml      # Parámetros del generador sintético + supuestos OEE
├── data/
│   ├── raw/                       # Dataset sintético canónico (18k registros, EN)
│   └── legacy/                    # Dataset histórico retirado (documentado en ADR-0001)
├── dashboard/
│   ├── dash_app.py                # (Legacy) Aplicación Dash previa
│   ├── app_layout.py              # (Legacy) Composición + navegación por pestañas
│   └── ...                        # (Legacy) Componentes y callbacks
├── src/
│   ├── data_generator.py          # Generador de datos (supuestos documentados)
│   ├── schema_adapter.py          # Adapter EN → ES (Camino A, ADR-0001)
│   ├── kpis.py                    # FPY, scrap, reproceso, Pareto
│   ├── capability.py              # Pp/Ppk (NIST 6.1.3 / ISO 22514)
│   ├── control_charts.py          # Carta I-MR (control estadístico)
│   ├── oee.py                     # Motor OEE (ISA-95/TPM)
│   ├── diagnostics.py             # Motor de diagnóstico priorizado
│   └── validation.py              # Data quality gate
├── tests/                         # 390 tests (por módulo)
├── scripts/
│   └── check_oee_distribution.py  # Evidencia numérica del motor OEE
├── docs/
│   ├── adr/                       # Architecture Decision Records
│   ├── learning-journal/          # Bitácora de aprendizaje por semana
│   ├── nist_references/           # Referencias NIST (dominio público)
│   └── industrial-kpi-intelligence-master-plan.md
├── assets/
│   └── style.css                  # Tema oscuro "sala de control"
├── imagenes/                      # Capturas del dashboard para el README
├── .github/workflows/tests.yml    # CI: ruff + pytest en cada push
├── migrate_csv.py                 # Script de migración de CSV a SQLite
├── requirements.txt               # Dependencias con versiones fijadas
├── pyproject.toml                 # Configuración de Ruff y pytest
├── Procfile / render.yaml         # Deploy en Render (gunicorn)
├── TECHNICAL_DOCUMENTATION.md     # Referencia técnica por módulo
├── CHANGELOG.md                   # Historial real de cambios
├── LICENSE                        # Elastic License 2.0
└── README.md
```

---

## 🔎 Conclusiones y líneas de mejora futuras

1. **Motor de diagnóstico** prioriza automáticamente los hallazgos por severidad (PRIORITY/WATCH/INFO), combinando hotspots de equipo/turno, capacidad de proceso y concentración de Pareto.

2. El **Ppk marginal** en variables continuas sugiere que el proceso no tiene margen de seguridad ante variabilidad adicional — se recomienda reducir sigma antes de ampliar límites de especificación.

3. **OEE en 0.8733 de planta** con Performance limitado por pérdidas de ritmo (micro-paradas, ajustes, variabilidad de turno) — coherente con benchmarks industriales.

4. **Líneas futuras**: carta de control X-bar/R multivariante, incorporación de datos reales de planta vía OPC-UA, autenticación JWT + RBAC, y despliegue productivo con PostgreSQL.

---


## 📚 Documentación

| Documento | Propósito |
|---|---|
| [`docs/learning-journal/`](docs/learning-journal/) | Bitácora de aprendizaje semana a semana (qué, por qué, cómo) |
| [`docs/adr/`](docs/adr/) | Architecture Decision Records (decisiones arquitectónicas) |
| [`docs/industrial-kpi-intelligence-master-plan.md`](docs/industrial-kpi-intelligence-master-plan.md) | Especificación completa del producto |
| [`docs/nist_references/`](docs/nist_references/) | Referencias NIST (SPC, capability) |
| [`TECHNICAL_DOCUMENTATION.md`](TECHNICAL_DOCUMENTATION.md) | Referencia técnica por módulo |
| [`CHANGELOG.md`](CHANGELOG.md) | Historial de cambios reales |

---

## 📄 Licencia y Uso

Este proyecto está licenciado bajo **Elastic License 2.0 (ELv2)**, no MIT/Apache.

La diferencia práctica:

| Perfil | ¿Qué puedes hacer? |
|---|---|
| **Evaluador técnico / reclutador / portafolio** | Clonar, leer, ejecutar localmente, modificar para tu propio aprendizaje o evaluación, usar como referencia en una entrevista técnica. Sin restricciones. |
| **Empresa que quiere usarlo internamente** | Desplegarlo en tu propia infraestructura (on-premise o tu propia nube) para tu propia operación, con las mismas libertades de copia/modificación. |
| **Empresa que quiere revenderlo como servicio hosted a terceros** | **No permitido** bajo esta licencia. Ese uso requiere un acuerdo comercial conmigo — es exactamente la actividad que la licencia protege. |
| **Cliente pagando (Starter/Professional/Enterprise)** | Recibe una licencia de uso comercial explícita como parte del contrato de suscripción, con SLA, soporte y actualizaciones — independiente de los términos de este repositorio público. |

**En una frase:** puedes leer, correr y aprender de todo el código libremente. Lo único que no puedes hacer es tomarlo y ofrecerlo como tu propio SaaS competidor. Si tu empresa quiere usarlo como producto (no solo evaluarlo), hablemos de una licencia comercial.

Ver [`LICENSE`](LICENSE) para el texto legal completo.

---

## 👤 Autor

**David González** — Ingeniero Civil Químico | Data Analytics | Mejora Continua

[![LinkedIn](https://img.shields.io/badge/LinkedIn-David_González-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/davidgonzalezsz)
[![GitHub](https://img.shields.io/badge/GitHub-icqdgonzalezs-181717?style=flat&logo=github&logoColor=white)](https://github.com/icqdgonzalezs)
[![Email](https://img.shields.io/badge/Email-icq.dgonzalezs%40gmail.com-EA4335?style=flat&logo=gmail&logoColor=white)](mailto:icq.dgonzalezs@gmail.com)

---

*Proyecto desarrollado como parte del portafolio profesional en análisis de datos industriales.*
