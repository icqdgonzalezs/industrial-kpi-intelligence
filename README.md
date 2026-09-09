# 🏭 Industrial KPI Intelligence

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-Plotly-00CC96?logo=plotly&logoColor=white)](https://dash.plotly.com/)
[![Tests](https://img.shields.io/badge/Tests-194%20passing-brightgreen)](tests/)
[![License](https://img.shields.io/badge/License-Elastic_License_2.0-blue)](LICENSE)

**Plataforma de inteligencia operacional industrial** — convierte datos crudos de planta en KPIs, control estadístico de proceso, capacidad Six Sigma y un motor de diagnóstico que prioriza qué amerita atención primero.

**🚀 [Ver demo en vivo](TODO-pegar-aquí-el-link-de-Render)**

---

## 📌 El problema que resuelve

Una planta con múltiples líneas, equipos y turnos genera datos de calidad todos los días — pero un dashboard de gráficos no le dice a un supervisor **dónde intervenir primero**. Este proyecto cruza KPIs, capacidad de proceso, control estadístico y Pareto en un motor de reglas que prioriza hallazgos como lo haría un ingeniero de calidad senior.

## 🎯 Qué hace

| Pestaña | Responde a | Técnica |
|---|---|---|
| **Diagnóstico** | ¿Qué requiere atención primero? | Motor de reglas priorizado (PRIORITY/WATCH/INFO) |
| **Calidad** | ¿Cómo va el desempeño global? | FPY, scrap, reproceso, Pareto de defectos |
| **Capacidad** | ¿El proceso cumple especificación? | Cp/Cpk (Six Sigma) |
| **Control** | ¿El proceso está estadísticamente estable? | Carta I-MR, límites de control, Western Electric |
| **Operacional** | ¿Qué línea/turno/operador destaca? | Ranking comparativo con drill-down interactivo |

## 🧠 El diferenciador: motor de diagnóstico

La mayoría de dashboards de portafolio muestran gráficos. Este además **decide qué mostrar primero**: `src/diagnostics.py` es lógica pura, 100% testeada, con cada umbral documentado y calibrado contra los datos reales — no números elegidos "porque se ven bien". Ejemplo real que produce sobre el dataset del proyecto:

> 🔴 **PRIORITY** — Pareto: "Mancha" concentra 38.5% de las unidades defectuosas
> 🟡 **WATCH** — Equipo L1-M04: tasa de defectos 1.22x el promedio de planta
> 🟡 **WATCH** — Capacidad: Peso, Cpk 1.05 (Marginal)

## 🏗️ Arquitectura

Regla de oro: **`src/` nunca importa Dash, los callbacks nunca calculan estadística.**
industrial-kpi-intelligence/
├── src/ # Lógica pura, 100% testeada, sin Dash
│ ├── kpis.py # FPY, scrap, reproceso, Pareto, KPIs por dimensión
│ ├── capability.py # Cp/Cpk (Six Sigma)
│ ├── control_charts.py # Carta I-MR (control estadístico)
│ ├── diagnostics.py # Motor de diagnóstico priorizado
│ ├── validation.py # Data quality gate
│ └── data_generator.py # Generador sintético (supuestos documentados)
│
├── dashboard/ # Capa Dash — callbacks delgados
│ ├── dash_app.py # Punto de entrada
│ ├── app_layout.py # Composición + navegación por pestañas
│ ├── utils.py # Deserialización de stores + tema Plotly compartido
│ └── <módulo>_components.py / <módulo>_callbacks.py # Un par por pestaña
│
├── assets/style.css # Tema oscuro "sala de control"
├── config/ # LSL/USL, umbrales Cpk, parámetros del generador
├── tests/ # 194 tests
├── .github/workflows/tests.yml # CI: ruff + pytest en cada push
├── Procfile / render.yaml # Deploy en Render (gunicorn)
└── CHANGELOG.md # Historial real de cambios, verificado

## ⚙️ Instalación y ejecución local

```bash
git clone https://github.com/icqdgonzalezs/industrial-kpi-intelligence.git
cd industrial-kpi-intelligence
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

python -m dashboard.dash_app          # desarrollo — abre http://127.0.0.1:8050
gunicorn dashboard.dash_app:server    # producción (mismo comando que usa Render)

pytest tests/ -v --cov=src --cov=dashboard   # 194 tests
```

## ☁️ Deploy

`Procfile` y `render.yaml` listos para [Render](https://render.com) (plan gratuito): conectar el repo → Render detecta la config automáticamente → deploy en ~3 minutos.

## 📄 Historial de cambios

Ver [`CHANGELOG.md`](CHANGELOG.md) — cada entrada corresponde a un commit real, validado con tests y, en los bugs más delicados, con peticiones HTTP reales contra el servidor.

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

---

*Parte de **Industrial Operations Intelligence** — portafolio de soluciones digitales para operaciones industriales (Analyze → Simulate → Predict → Optimize → Decide).*
