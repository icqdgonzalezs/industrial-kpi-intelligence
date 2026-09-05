# 🏭 Industrial KPI Intelligence

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-Plotly-00CC96?logo=plotly&logoColor=white)](https://dash.plotly.com/)
[![Tests](https://img.shields.io/badge/Tests-195%20passing-brightgreen)](tests/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**Plataforma de inteligencia operacional industrial** — convierte datos crudos de planta en KPIs, diagnóstico priorizado y análisis de capacidad de proceso (Six Sigma), con un motor de reglas que responde la pregunta que realmente importa: **¿qué amerita atención primero?**

**🚀 [Ver demo en vivo](TODO-pegar-aquí-el-link-de-Render)** — actualizar tras desplegar (ver sección Deploy)

---

## 📌 El problema que resuelve

Una planta de envasado con múltiples líneas, equipos, turnos y operadores genera datos de calidad todos los días — pero un dashboard de gráficos no le dice a un supervisor **dónde intervenir primero**. Este proyecto va un paso más allá de "mostrar números": cruza KPIs por dimensión, capacidad de proceso (Cp/Cpk) y concentración de defectos (Pareto) en un **motor de diagnóstico** que prioriza hallazgos como lo haría un ingeniero de calidad senior revisando el turno.

## 🎯 Qué hace

1. **KPIs de calidad** — FPY, tasa de defectos, scrap, reproceso, calculados sobre unidades totales (no promedio de tasas, evita sesgo).
2. **Diagnóstico priorizado** (motor de reglas) — combina hotspots de equipo/turno, Cp/Cpk y Pareto en hallazgos rankeados por severidad (`PRIORITY` / `WATCH` / `INFO`), con umbrales documentados y calibrados contra el dataset.
3. **Operational Analysis** — ranking comparativo por línea/máquina/turno/operador, con drill-down interactivo: clic en una barra y ves el detalle de ese grupo.
4. **Capacidad de proceso (Cp/Cpk)** — evaluación Six Sigma por variable crítica, contra límites de especificación configurables.
5. **Pareto de defectos** — identifica qué causa concentra la mayor parte del problema.

## 🧠 Por qué esto no es "otro dashboard de portafolio"

La mayoría de proyectos similares muestran gráficos. Este además **decide qué mostrar primero**: el motor de diagnóstico (`src/diagnostics.py`) es lógica pura, 100% testeada, con cada umbral documentado y justificado contra los datos reales del proyecto — no números elegidos "porque se ven bien".

---

## 📊 Datos y metodología

Los datos son sintéticos, generados por `src/data_generator.py` con semilla fija (`random_seed=42`) para reproducibilidad total. El dataset actual (`data/calidad_muestra.csv`) cubre 2 líneas × 4 máquinas (8 equipos), 3 turnos, 250 lotes.

**Hallazgos reales que produce el motor de diagnóstico sobre este dataset** (reproducibles corriendo la app):

| Severidad | Categoría | Hallazgo |
|---|---|---|
| 🔴 PRIORITY | Pareto de defectos | "Mancha" concentra 38.5% de las unidades defectuosas |
| 🟡 WATCH | Equipo | L1-M04: tasa de defectos 5.7% (1.22x el promedio de planta) |
| 🟡 WATCH | Equipo | L2-M04: tasa de defectos 5.4% (1.17x el promedio de planta) |
| 🟡 WATCH | Capacidad de proceso | Peso — Cpk 1.05 (Marginal) |
| 🟡 WATCH | Capacidad de proceso | Longitud — Cpk 1.05 (Marginal) |

Fórmulas (ver `src/kpis.py` y `src/capability.py`):
FPY = (producidas - defectuosas) / producidas
Cp = (USL - LSL) / (6 * sigma)
Cpk = min[(USL - media)/(3sigma), (media - LSL)/(3sigma)]---

## 🏗️ Arquitectura

Separación estricta entre lógica analítica y presentación — regla de oro del proyecto: **`src/` nunca importa Dash, y los callbacks nunca calculan estadística.**

industrial-kpi-intelligence/
├── src/ # Lógica pura, 100% testeada, sin Dash
│ ├── kpis.py # FPY, scrap, reproceso, Pareto, KPIs por dimensión
│ ├── capability.py # Cp/Cpk (Six Sigma)
│ ├── diagnostics.py # Motor de diagnóstico priorizado (el diferenciador)
│ ├── validation.py # Data quality gate
│ └── data_generator.py # Generador sintético (supuestos documentados)
│
├── dashboard/ # Capa Dash — callbacks delgados, sin lógica estadística
│ ├── dash_app.py # Punto de entrada
│ ├── app_layout.py # Composición del layout
│ ├── data_loader.py # Carga dataset + config
│ ├── utils.py # Deserialización de stores + tema Plotly compartido
│ ├── filter_.py # Control Center (filtros)
│ ├── kpi_.py # Grilla de KPIs
│ ├── quality_performance_.py # FPY/scrap/reproceso + Pareto
│ ├── capability_.py # Cp/Cpk
│ ├── diagnostics_.py # Panel de hallazgos priorizados
│ ├── operational_analysis_.py # Ranking comparativo + drill-down
│ └── plant_overview*.py # Vista general de planta
│
├── assets/style.css # Tema visual (servido automáticamente por Dash)
├── config/ # LSL/USL, umbrales Cpk, parámetros del generador
├── data/calidad_muestra.csv # Dataset sintético
├── tests/ # 195 tests — un archivo por módulo de src/ y dashboard/
├── .github/workflows/tests.yml # CI: ruff + pytest en cada push
├── Procfile / render.yaml # Deploy en Render (gunicorn)
└── requirements.txt


---

## ⚙️ Instalación y ejecución local

```bash
git clone https://github.com/icqdgonzalezs/industrial-kpi-intelligence.git
cd industrial-kpi-intelligence

python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Ejecutar el dashboard (desarrollo) — como módulo, desde la raíz del proyecto
python -m dashboard.dash_app
# Abre http://127.0.0.1:8050

# Ejecutar como en producción (gunicorn, el mismo comando que usa Render)
gunicorn dashboard.dash_app:server

# Regenerar el dataset sintético
python3 -m src.data_generator

# Correr la suite de tests (195 casos)
pytest tests/ -v --cov=src --cov=dashboard
```

## ☁️ Deploy

Este repo incluye `Procfile` y `render.yaml` listos para [Render](https://render.com) (plan gratuito, sin tarjeta):

1. Conectar el repo en Render → "New Web Service"
2. Render detecta `render.yaml` automáticamente
3. Deploy — la URL pública queda lista en ~3 minutos

---

## 🔎 Próximas líneas de mejora

- Carta de control estadístico (X-barra/R) para detectar causas asignables en tiempo real
- Incorporar datos reales de planta cuando estén disponibles
- Exportar el panel de diagnóstico a PDF/reporte ejecutivo

---

## 👤 Autor

**David González** – Ingeniero Civil Químico | Data Analytics | Mejora Continua

[![LinkedIn](https://img.shields.io/badge/LinkedIn-David_González-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/davidgonzalezsz)
[![GitHub](https://img.shields.io/badge/GitHub-icqdgonzalezs-181717?style=flat&logo=github&logoColor=white)](https://github.com/icqdgonzalezs)
[![Email](https://img.shields.io/badge/Email-icq.dgonzalezs%40gmail.com-EA4335?style=flat&logo=gmail&logoColor=white)](mailto:icq.dgonzalezs@gmail.com)

---

*Parte de **Industrial Operations Intelligence** — mi portafolio de soluciones digitales para operaciones industriales (Analyze → Simulate → Predict → Optimize → Decide).*
