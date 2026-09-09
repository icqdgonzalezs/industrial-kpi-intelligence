# 📘 Industrial KPI Intelligence
## Master Build Plan — Plant Manufacturing Analytics, Quality Engineering & Process Control

> **Documento maestro de construcción, aprendizaje y evolución del proyecto.**
>
> Este archivo define la arquitectura, modelo industrial, alcance funcional, metodología estadística, estructura de software, estrategia de testing, workflow de terminal/Bash, roadmap y criterios de calidad que utilizaremos para construir **Industrial KPI Intelligence** desde su estado actual hasta una versión de portfolio de alto impacto.

---

# 0. Propósito de este documento

Este archivo será utilizado simultáneamente como:

1. Especificación funcional.
2. Especificación técnica.
3. Bitácora de construcción.
4. Guía de aprendizaje.
5. Guía de terminal/Bash y Python.
6. Guía de estadística industrial y Six Sigma.
7. Guía de testing y calidad de software.
8. Checklist de release para GitHub.
9. Material de preparación para entrevistas técnicas.

La regla general será:

> **No implementaremos una funcionalidad solamente porque se vea bien.**
>
> Cada componente deberá responder a un problema operacional o de calidad y deberá poder defenderse técnicamente.


# 1. 🎯 Visión definitiva del proyecto

## 1.1 Qué estamos construyendo

**Industrial KPI Intelligence** será una aplicación web interactiva para:

- monitorizar desempeño de una planta manufacturera;
- validar la calidad de los datos;
- analizar producción y calidad;
- comparar líneas, equipos, turnos y productos;
- detectar desviaciones;
- analizar capacidad de proceso;
- aplicar Statistical Process Control (SPC);
- detectar excepciones;
- priorizar investigaciones;
- estimar pérdidas operacionales;
- simular escenarios What-If;
- apoyar decisiones de mejora continua.

No será presentado como un sistema de control automático de planta.

No enviará comandos a PLC.

No reemplazará MES, SCADA, ERP, LIMS ni sistemas de calidad.

Su rol será:

> **Decision Support / Manufacturing Analytics**


# 2. 🏭 Dominio industrial elegido

## 2.1 Industria

El proyecto estará basado en una:

> **Planta ficticia de fabricación y packaging de productos alimentarios / consumer goods.**

La planta será sintética, pero inspirada en procesos de manufactura reales.

Importante:

- no diremos que es una planta de Nestlé;
- no utilizaremos datos internos de Nestlé;
- no afirmaremos que reproduce exactamente una planta real;
- usaremos maquinaria y problemas industriales plausibles;
- las reglas del dataset serán explícitamente documentadas.

La inspiración de dominio permite que el modelo responda preguntas que un ingeniero de producción, calidad o mejora continua podría realmente realizar.


# 3. 🏗️ Modelo físico de la planta

## 3.1 Estructura general

```text
PLANTA
│
├── LÍNEA 1 — Canning
│   │
│   ├── Depalletizer
│   ├── Can Feeder
│   ├── Filler
│   ├── Seamer
│   ├── Can Washer
│   ├── X-Ray / Inspection
│   ├── Checkweigher
│   ├── Labeler / Coder
│   └── Case Packer
│
├── LÍNEA 2 — Bottling
│   ├── Rinser
│   ├── Filler
│   ├── Capper
│   ├── Labeler
│   ├── Checkweigher
│   └── Case Packer
│
├── LÍNEA 3 — Pouch
│   ├── Form-Fill-Seal
│   ├── Seal Inspection
│   ├── Checkweigher
│   ├── Metal Detector
│   └── Cartoner
│
└── LÍNEA 4 — Secondary Packaging
    ├── Case Packer
    ├── Palletizer
    └── Stretch Wrapper
```

La planta no será perfectamente simétrica: una línea puede tener más equipos que otra. Esto es intencionalmente más realista que obligar a todas las líneas a tener la misma cantidad de máquinas.


# 4. 🔢 Cantidad de equipos

Modelo objetivo inicial:

- Línea 1 → 9 equipos
- Línea 2 → 6 equipos
- Línea 3 → 5 equipos
- Línea 4 → 3 equipos

**Total inicial: 23 equipos modelados.**

Dentro de ellos seleccionaremos aproximadamente **10 Critical Assets** para el dashboard principal.

Esto evita confundir:

```text
cantidad de equipos modelados
```

con:

```text
cantidad de equipos monitoreados con máxima profundidad
```

La aplicación deberá ser capaz de representar una planta mayor de lo que necesariamente muestra en el primer vistazo.


# 5. 🚨 Critical Assets

Los Critical Assets serán los equipos que concentran:

- monitoreo;
- SPC;
- capability;
- ranking;
- excepciones;
- pérdidas;
- diagnóstico.

Ejemplo conceptual:

```text
L1-FILL-01
L1-SEAM-01
L1-CHECK-01

L2-FILL-01
L2-CAPPER-01
L2-CHECK-01

L3-FFS-01
L3-SEAL-01
L3-CHECK-01

L4-PACK-01
```

La selección exacta se definirá al cerrar el modelo de datos.


# 6. 🆔 Identificación de equipos

No eliminaremos los IDs técnicos.

Utilizaremos varios atributos.

## Equipment ID

Ejemplo:

```text
L2-FILL-01
```

Interpretación:

```text
L2    → Línea 2
FILL  → Tipo de equipo
01    → Número secuencial
```

## Equipment Name

```text
Liquid Filler 01
```

## Equipment Type

```text
FILLER
```

## Ejemplo completo

```text
equipment_id   = L2-FILL-01
equipment_name = Liquid Filler 01
equipment_type = FILLER
line_id        = L2
```

Esto permite separar:

- identidad;
- descripción;
- clasificación;
- ubicación.


# 7. 🧱 Jerarquía industrial

La jerarquía conceptual será:

```text
PLANT
  ↓
AREA
  ↓
LINE
  ↓
EQUIPMENT
  ↓
PROCESS VARIABLE
```

Ejemplo:

```text
Plant 01
   ↓
Packaging
   ↓
Line 2
   ↓
L2-FILL-01
   ↓
Fill Weight
```

Esta jerarquía será la base para el *drill-down* del dashboard.


# 8. 📊 Modelo de producción

El dataset dejará de limitarse a 250 lotes.

Objetivo de simulación:

- 12 meses;
- 4 líneas;
- ~23 equipos;
- ~10 critical assets;
- 3 turnos;
- ~24 operadores;
- varios productos;
- miles de registros;
- múltiples lotes.

Objetivo orientativo:

```text
10.000 – 30.000 registros
```

El número exacto se definirá en función de rendimiento, utilidad y simplicidad.


# 9. 📅 Tiempo

Campos esperados:

```text
timestamp
date
year
month
week
shift
```

Para análisis temporal:

```python
df["timestamp"] = pd.to_datetime(df["timestamp"])
```

La validación de fechas será parte del Data Quality Gate.


# 10. 👥 Turnos y operadores

Turnos:

```text
Morning
Afternoon
Night
```

Operadores:

```text
OP001
OP002
...
OP024
```

Los operadores podrán relacionarse con turnos.

No agregaremos atributos personales innecesarios. La finalidad es estudiar desempeño operacional, no construir un sistema de RRHH.


# 11. 📦 Productos y lotes

Productos:

```text
PRD-A
PRD-B
PRD-C
PRD-D
PRD-E
PRD-F
```

Cada producto podrá tener:

- líneas compatibles;
- configuración;
- especificaciones;
- parámetros objetivo.

Lotes:

```text
LOT-000001
LOT-000002
...
```

El lote permitirá:

- trazabilidad;
- análisis de defectos;
- investigación;
- identificación de lotes críticos.


# 12. 🧪 Variables de proceso

Las variables serán específicas de cada tipo de equipo.

### Filler

```text
fill_weight
fill_volume
temperature
flow_rate
line_speed
```

### Seamer

```text
seam_height
seam_width
seam_thickness
internal_pressure
```

### Checkweigher

```text
weight
weight_deviation
reject_rate
```

### Metal Detector

```text
detection_rate
false_reject_rate
```

Esto evita el error de usar exactamente las mismas variables para todas las máquinas.


# 13. 🛠️ Calidad, defectos, scrap y reproceso

Campos generales:

```text
units_produced
units_defective
units_scrap
units_rework
defect_type
```

Ejemplos de defectos:

```text
Underweight
Overweight
Seal Defect
Label Defect
Contamination
Foreign Material
Package Integrity
Coding Error
```

La taxonomía podrá depender del proceso.

Cuando corresponda, deberá cumplirse:

```text
units_defective
=
units_scrap + units_rework
```


# 14. 🎲 Motor de datos sintéticos

`src/data_generator.py` deberá:

- generar registros;
- aplicar relaciones industriales;
- crear variabilidad;
- introducir eventos;
- mantener reproducibilidad;
- permitir modificar supuestos mediante configuración.

La generación no debe ser ruido aleatorio sin estructura.


# 15. 🌱 Reproducibilidad

Se mantendrá una semilla fija:

```python
RANDOM_SEED = 42
```

La idea:

```text
same seed
    ↓
same random stream
    ↓
same synthetic dataset
```

Esto permite reproducir:

- bugs;
- tests;
- análisis;
- comparaciones entre versiones.


# 16. 🎭 Eventos de proceso simulados

Ejemplos:

## Equipment drift

```text
L2-FILL-01
    ↓
fill weight slowly drifts
    ↓
Cpk decreases
    ↓
defect rate increases
```

## Shift effect

```text
Night
   ↓
slightly higher variability
```

## Equipment condition

```text
L1-SEAM-01
   ↓
seal variability increases
   ↓
seal defects increase
```

## Product/setup interaction

```text
Product B
   ↓
setup sensitivity
   ↓
higher process variability
```

Estas señales serán diseñadas para que la aplicación pueda descubrir patrones, pero serán explícitamente sintéticas.


# 17. 📋 Specification Limits

Cada variable crítica tendrá configuración.

Ejemplo:

```yaml
fill_weight:
  nominal: 500.0
  lsl: 492.0
  usl: 508.0
```

Los límites:

```text
LSL
USL
```

son **Specification Limits**.

No son lo mismo que los límites de control.


# 18. 📈 Control Limits

Los límites de control:

```text
LCL
CL
UCL
```

describen el comportamiento estadístico del proceso.

Regla fundamental:

```text
Specification Limits
≠
Control Limits
```

El dashboard deberá hacer visible esta diferencia.


# 19. 🧪 Statistical Process Control — SPC

SPC será uno de los pilares del proyecto.

La primera versión debe:

- calcular límites;
- construir cartas;
- identificar señales OOC;
- permitir filtrar por línea/equipo/variable;
- mostrar estado del proceso.


# 20. 📊 Selección de cartas

No elegiremos una carta por estética.

## Datos individuales

```text
I-MR
```

## Subgrupos

Si tenemos:

```text
Lot 001
  sample 1
  sample 2
  sample 3
  sample 4
  sample 5
```

entonces podremos utilizar:

```text
X-bar / R
```

La estructura de los datos determinará la metodología.


# 21. 🚨 OOC — Out of Control

Estados:

```text
IN CONTROL
WATCH
OUT OF CONTROL
```

Primera regla:

```text
point > UCL
or
point < LCL
```

Posteriormente podremos incorporar reglas adicionales si existe una necesidad demostrable y las cubrimos con tests.


# 22. 📐 Capability Analysis

El motor mantendrá:

```text
mean
sigma
Cp
Cpk
n
LSL
USL
classification
```

## Cp

```text
Cp = (USL - LSL) / (6 × sigma)
```

Cp pregunta esencialmente si la variación natural cabe dentro de la especificación suponiendo centrado perfecto.

## Cpk

```text
Cpk =
min(
    (USL - mean) / (3 × sigma),
    (mean - LSL) / (3 × sigma)
)
```

Cpk incorpora el centrado.


# 23. ⚠️ Interpretación de capacidad

Convención del proyecto:

```text
Cpk >= 1.33
→ Capable / Excellent

1.00 <= Cpk < 1.33
→ Marginal / Monitor

Cpk < 1.00
→ Not capable / Action required
```

Estas categorías serán una convención de reporting del proyecto y no deben presentarse como una ley universal.

Además:

> **Cp/Cpk no demuestra por sí solo que el proceso esté bajo control estadístico.**

La interpretación deberá considerar estabilidad, distribución, tamaño muestral y calidad de datos.


# 24. 📊 KPI Engine

KPIs generales:

```text
Production
FPY
Defect Rate
Scrap Rate
Rework Rate
```

Podrán incorporarse otros KPIs solamente cuando existan datos adecuados para calcularlos correctamente.

Por ejemplo, no calcularemos OEE si no tenemos los componentes necesarios.


# 25. 🧮 Agregación correcta

No promediaremos porcentajes sin analizar el volumen.

Ejemplo:

```text
Line 1 defect rate = 2%
Line 2 defect rate = 8%
```

El promedio simple de 5% puede ser engañoso si los volúmenes son distintos.

Para una agregación global:

```text
total defects
/
total production
```

Esto entrega una tasa ponderada por volumen.


# 26. 🔍 Pareto

Proceso:

```text
defect types
      ↓
frequency
      ↓
sort descending
      ↓
cumulative percentage
```

El gráfico mostrará:

- barras;
- porcentaje acumulado;
- causas prioritarias;
- contraste visual sobrio.

La visualización debe ayudar a identificar dónde investigar, no convertirse en decoración.


# 27. 🚨 Exception Center

Ejemplo:

```text
PRIORITY

L2-FILL-01
Defect Rate: 6.1%
Cpk: 0.96
OOC Events: 7
Night Shift: 7.1%
```

La excepción podrá combinar:

```text
defect rate
scrap
Cpk
OOC
equipment
shift
product
```

El ranking deberá explicar por qué algo aparece como prioridad.


# 28. 🧠 Diagnostic / Investigation Engine

El diagnóstico será de **apoyo a la investigación**, no de causalidad automática.

Ejemplo:

```text
Equipment
+
Shift
+
High defect rate
+
OOC signal
```

Resultado:

> Elevated performance deviation detected on L2-FILL-01 during Night Shift. Investigate equipment condition, setup, calibration and shift-specific operating conditions.

Nunca se deberá afirmar automáticamente:

```text
Root cause = Operator
```

sin evidencia causal.


# 29. 💰 Impact / Loss Analysis

Cadena:

```text
Defects
   ↓
Rework
   ↓
Scrap
   ↓
Economic Impact
```

Parámetros:

```text
scrap_units
rework_units
scrap_cost_per_unit
rework_cost_per_unit
estimated_loss
```

El resultado se presentará como estimación.


# 30. 💡 What-If Analysis

Ejemplo:

```text
Current defect rate = 6.1%
Target defect rate  = 4.0%
```

Cálculos:

```text
current_defects
=
production × current_defect_rate

target_defects
=
production × target_defect_rate

potential_reduction
=
current_defects - target_defects
```

Ahorro potencial:

```text
potential_scrap_saving
=
potential_scrap_reduction × scrap_cost_per_unit
```

Nunca se mostrará como ahorro garantizado.


# 31. 🕒 Data Freshness

La aplicación deberá mostrar la fecha/hora real de actualización:

```text
Last data update:
YYYY-MM-DD HH:MM
```

No se deberá inventar la última actualización.

La información deberá derivarse de la fuente o archivo utilizado.


# 32. 🛡️ Data Quality Gate

Flujo:

```text
DATA SOURCE
    ↓
VALIDATION
    ↓
PASS ───────────► ANALYSIS
    │
    └────────────► FAIL
                       ↓
                 STOP ANALYSIS
```

Validaciones:

- DataFrame;
- columnas;
- nulos;
- timestamps;
- producción;
- defectos;
- scrap;
- reproceso;
- reconciliación;
- variables continuas;
- línea;
- equipo;
- turno;
- producto;
- coherencia línea/equipo.


# 33. 🧠 Por qué el Data Quality Gate es obligatorio

Un KPI calculado sobre datos inválidos puede ser peor que no tener KPI.

Ejemplo:

```text
production = 0
defects = 20
```

No debemos permitir:

```text
20 / 0
```

En software industrial, la validación protege:

- decisiones;
- confianza;
- trazabilidad;
- interpretaciones;
- futuras integraciones.


# 34. 🖥️ Plataforma: Dash

La interfaz migrará de Streamlit a:

```text
Dash
Plotly
Dash DAQ
HTML/CSS
```

Razón de negocio:

> construir una identidad de aplicaciones analíticas interactivas industriales.

Dash no será utilizado solamente para “verse más profesional”. También permitirá una arquitectura explícita de componentes, callbacks y estado.


# 35. 🎨 Lenguaje visual

La interfaz será:

- dark;
- minimalista;
- industrial;
- compacta;
- de alta densidad informativa;
- con estados semánticos;
- inspirada en el patrón visual de industrial control room.

La referencia estética es el proyecto de SPC seleccionado como referencia, pero la implementación será propia.

Paleta conceptual:

```text
Dark background
Dark panels
Light text
Muted text
Teal/Cyan accent

NORMAL   → green / teal
WATCH    → yellow
PRIORITY → red
```

Regla:

> **Los colores representan estado operacional, no decoración.**


# 36. 🖥️ Dashboard principal

Layout conceptual:

```text
┌────────────────────────────────────────────────────────────┐
│ INDUSTRIAL KPI INTELLIGENCE                ● SYSTEM READY │
│ Process Control & Quality Analytics                        │
├────────────────────────────────────────────────────────────┤
│ CONTROL CENTER                                             │
│ Period | Line | Equipment | Shift | Operator | Product    │
├────────────────────────────────────────────────────────────┤
│ PROCESS HEALTH                                             │
│ FPY | DEFECT RATE | SCRAP | REWORK | CPK                  │
├────────────────────────────────────────────────────────────┤
│ KPI MONITORING                                             │
│ Parameter | N | Trend | OOC | Status                       │
├────────────────────────────────────────────────────────────┤
│ PROCESS CONTROL                                            │
│ SPC CHART                         EXCEPTION CENTER          │
├───────────────────────────────┬────────────────────────────┤
│ QUALITY ANALYSIS              │ CAPABILITY                 │
│ Pareto / distributions        │ Cp / Cpk / specs           │
├───────────────────────────────┴────────────────────────────┤
│ IMPACT / WHAT-IF                                           │
├────────────────────────────────────────────────────────────┤
│ Data Quality: PASS | Last Update: YYYY-MM-DD HH:MM        │
└────────────────────────────────────────────────────────────┘
```


# 37. 🎛️ Control Center

Filtros principales:

```text
Period
Line
Equipment
Shift
Operator
Product
Parameter
```

Los filtros serán dependientes.

Ejemplo:

```text
Line = L2
    ↓
Equipment choices
    ↓
only equipment from L2
```

Y:

```text
Equipment = L2-FILL-01
    ↓
Parameter choices
    ↓
only parameters relevant to FILLER
```


# 38. 🔄 Callbacks Dash

Patrón general:

```text
INPUT
  ↓
CALLBACK
  ↓
ANALYTICS
  ↓
OUTPUT
```

Ejemplos:

```text
Line dropdown
    ↓
callback
    ↓
update equipment dropdown
```

```text
Equipment selection
    ↓
callback
    ↓
update SPC chart
```

```text
Date + Line + Equipment
    ↓
callback
    ↓
update KPIs
```


# 39. 🗃️ Estado

Cuando corresponda se utilizará:

```text
dcc.Store
```

y separaremos:

```text
UI STATE
≠
RAW DATA
≠
ANALYTICAL RESULT
```

La finalidad es evitar acoplamiento innecesario.


# 40. 📁 Arquitectura objetivo

```text
industrial-kpi-intelligence/
│
├── app.py
│
├── config/
│   ├── quality_config.yaml
│   ├── plant_config.yaml
│   └── theme_config.yaml
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── src/
│   ├── __init__.py
│   ├── data_generator.py
│   ├── data_access.py
│   ├── validation.py
│   ├── kpis.py
│   ├── capability.py
│   ├── control_charts.py
│   ├── diagnostics.py
│   ├── impact.py
│   └── utils.py
│
├── dashboard/
│   ├── __init__.py
│   ├── layout.py
│   ├── components/
│   │   ├── header.py
│   │   ├── filters.py
│   │   ├── kpi_cards.py
│   │   ├── status.py
│   │   ├── charts.py
│   │   ├── alerts.py
│   │   └── tables.py
│   └── callbacks/
│       ├── filters.py
│       ├── kpis.py
│       ├── spc.py
│       ├── capability.py
│       ├── diagnostics.py
│       └── impact.py
│
├── assets/
│   ├── style.css
│   └── theme.css
│
├── tests/
│   ├── test_data_generator.py
│   ├── test_validation.py
│   ├── test_kpis.py
│   ├── test_capability.py
│   ├── test_control_charts.py
│   ├── test_diagnostics.py
│   └── test_impact.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE
```


# 41. 🧩 Responsabilidad de módulos

## `src/data_generator.py`

Genera datos sintéticos.

No contiene:

- HTML;
- callbacks;
- layout.

## `src/data_access.py`

Carga datos desde CSV y, en una evolución, SQL.

## `src/validation.py`

Valida datos.

## `src/kpis.py`

Calcula KPIs descriptivos.

## `src/capability.py`

Calcula Cp/Cpk.

## `src/control_charts.py`

Calcula límites y señales SPC.

No dibuja.

## `src/diagnostics.py`

Genera señales de investigación.

## `src/impact.py`

Calcula pérdidas y escenarios What-If.

## `dashboard/components/`

Construye piezas visuales reutilizables.

## `dashboard/callbacks/`

Conecta interacción y resultados.

## `app.py`

Orquesta la aplicación sin absorber toda la lógica.


# 42. 🧱 Separation of Concerns

Arquitectura conceptual:

```text
DATA
  ↓
VALIDATION
  ↓
ANALYTICS
  ↓
DECISION LOGIC
  ↓
VISUALIZATION
```

Evitar:

```text
app.py
  ├── carga datos
  ├── limpia
  ├── calcula Cpk
  ├── calcula SPC
  ├── HTML
  └── exportación
```

La separación permite testear cada capa.


# 43. 🧪 Testing Strategy

Objetivos:

```text
Correctness
+
Regression protection
+
Confidence
```

Se cubrirán:

- generator;
- validation;
- KPIs;
- capability;
- SPC;
- diagnostics;
- impact;
- integración básica.


# 44. 🧪 Edge Cases prioritarios

## Validation

- columna inexistente;
- nulos;
- producción negativa;
- defectos > producción;
- scrap > defectos;
- rework > defectos;
- reconciliación incorrecta;
- equipo inexistente.

## Capability

- n < 2;
- USL <= LSL;
- sigma = 0;
- datos idénticos;
- media cercana a USL;
- media cercana a LSL.

## SPC

- pocos datos;
- límites inválidos;
- punto sobre UCL;
- punto bajo LCL.

## Impact

- producción = 0;
- target >= current;
- costo negativo.


# 45. ✅ Quality Gates

Antes de cada release:

```text
pytest
↓
compileall
↓
lint
↓
dependency check
↓
manual smoke test
↓
Dash run
↓
git diff
↓
git status
```

La aplicación no se considera lista porque “abre”.


# 46. 💻 Terminal y Bash

El desarrollo será guiado desde terminal.

Comandos fundamentales:

```bash
cd ~/Projects/industrial-operations-intelligence/industrial-kpi-intelligence
pwd
ls -la
find . -maxdepth 3 -type f | sort
source venv/bin/activate
python --version
which python
pytest -q
python -m compileall -q src dashboard tests
```

Cada comando será enseñado con:

```text
¿Qué hace?
¿Por qué lo usamos?
¿Qué resultado esperamos?
¿Qué puede salir mal?
```


# 47. 🐍 Entorno virtual

Crear:

```bash
python -m venv venv
```

Activar:

```bash
source venv/bin/activate
```

Instalar:

```bash
pip install -r requirements.txt
```

El entorno virtual permite aislar las dependencias del proyecto.


# 48. 🚀 Ejecución Dash

El entry point final será:

```bash
python app.py
```

o la variante elegida por la arquitectura final.

La documentación se actualizará para reflejar el comando real, no uno hipotético.


# 49. 🔀 Git workflow

Antes de modificar:

```bash
git status
git diff
```

Después:

```bash
git add .
git commit -m "feat: ..."
git push origin main
```

Nunca se debe hacer commit de forma mecánica sin revisar qué archivos cambiaron.


# 50. 🧹 `.gitignore`

Debe excluir como mínimo:

```text
venv/
__pycache__/
*.pyc
.pytest_cache/
.DS_Store
.env
```

Nunca subir:

- credenciales;
- tokens;
- secretos;
- caches;
- entorno virtual.


# 51. 🔄 CI/CD

GitHub Actions deberá ejecutar:

```text
push / pull request
       ↓
install dependencies
       ↓
pytest
       ↓
compile / lint
       ↓
PASS / FAIL
```

El objetivo es proteger el proyecto contra regresiones.


# 52. 📦 Dependencias

Base prevista:

```text
pandas
numpy
plotly
dash
dash-bootstrap-components
pyyaml
pytest
```

Posibles dependencias adicionales, solamente si se justifican:

```text
scipy
openpyxl
ruff
```

`requirements.txt` deberá reflejar el entorno real.


# 53. 🧭 User Journey

La interfaz deberá responder en este orden:

```text
1. What am I analyzing?
2. What is the plant status?
3. Where is the deviation?
4. Is the process statistically stable?
5. Is the process capable?
6. Where should I investigate?
7. What is the potential impact?
```


# 54. 🏭 Uso empresarial del producto

El sistema se diseñará pensando en una adaptación futura a una empresa.

## Paso 1 — Fuente de datos

Posibles fuentes reales:

```text
MES
SCADA
PLC
LIMS
ERP
SQL
CSV
Excel
```

Primera implementación:

```text
CSV
```

Posteriormente:

```text
PostgreSQL / SQL
```

## Paso 2 — Calidad de datos

Los datos no pasan al dashboard sin validación.

## Paso 3 — Configuración

Calidad configura:

- productos;
- especificaciones;
- equipos;
- variables;
- targets.

## Paso 4 — Monitoreo

Supervisor revisa:

- estado general;
- KPIs;
- excepciones.

## Paso 5 — Investigación

Se hace drill-down:

```text
Plant
  ↓
Line
  ↓
Equipment
  ↓
Parameter
```

## Paso 6 — Decisión

El equipo utiliza:

- SPC;
- capability;
- Pareto;
- diagnóstico;
- impacto.

## Paso 7 — Mejora

Se investiga la causa raíz en terreno y se ejecutan acciones.

La herramienta prioriza, pero no sustituye Gemba, 5 Why, Ishikawa, mantenimiento, laboratorio ni proceso de decisión de la empresa.


# 55. 🗄️ Evolución del backend

Primera versión:

```text
CSV
```

Segunda:

```text
SQL / PostgreSQL
```

Futuras integraciones:

```text
MES
SCADA
LIMS
ERP
```

La capa analítica se mantendrá desacoplada de la fuente.

Objetivo:

> poder cambiar la fuente de datos sin reescribir la lógica de KPI, SPC y capability.


# 56. 🚧 Roadmap

## Phase 0 — Baseline

- auditoría;
- baseline Git;
- tests;
- documentación.

## Phase 1 — Industrial Data Model

- 4 líneas;
- ~23 equipos;
- 10 critical assets;
- productos;
- turnos;
- operadores;
- variables;
- especificaciones.

## Phase 2 — Synthetic Data Engine

- timestamps;
- eventos;
- defects;
- scrap;
- rework;
- process variables;
- reproducibility.

## Phase 3 — Data Quality Gate

- schema;
- nulls;
- ranges;
- reconciliation;
- equipment identity.

## Phase 4 — Analytics Layer

- KPIs;
- dimensional analysis;
- Pareto;
- critical lots.

## Phase 5 — Capability

- Cp;
- Cpk;
- classification;
- edge cases.

## Phase 6 — SPC

- I-MR;
- X-bar/R cuando corresponda;
- CL/UCL/LCL;
- OOC detection.

## Phase 7 — Diagnostics

- equipment × shift;
- equipment × product;
- prioritization;
- investigation signals.

## Phase 8 — Impact

- scrap loss;
- rework cost;
- What-If.

## Phase 9 — Dash UI

- industrial theme;
- control center;
- KPI cards;
- SPC;
- exceptions;
- capability.

## Phase 10 — Software Quality

- tests;
- coverage;
- lint;
- CI;
- dependency cleanup.

## Phase 11 — Portfolio

- README;
- screenshots;
- architecture diagram;
- demo;
- GitHub topics;
- release.


# 57. 🥇 Prioridades

El criterio será:

```text
Correctness
    ↓
Industrial realism
    ↓
Statistical validity
    ↓
UX
    ↓
Visual polish
```

No al revés.


# 58. 🚨 Reglas de oro

1. No presentar datos simulados como datos reales.
2. No afirmar causalidad a partir de correlaciones simples.
3. No interpretar Cp/Cpk sin supuestos.
4. No confundir specification limits y control limits.
5. No calcular KPIs con denominadores inválidos.
6. No mezclar lógica estadística con layout.
7. No aceptar datos inválidos silenciosamente.
8. No agregar funciones sin propósito.
9. Toda funcionalidad analítica importante debe tener tests.
10. Toda decisión de arquitectura importante debe quedar documentada.


# 59. 🧑‍🏫 Método de aprendizaje

Cada intervención técnica seguirá:

```text
1. Explain the problem
2. Explain the engineering idea
3. Explain the Python concept
4. Write the code
5. Run the code
6. Inspect the output
7. Test the result
8. Discuss edge cases
9. Commit
10. Document the learning
```

Nunca reduciré el proceso a “copia y pega”.


# 60. 🧪 Definition of Done

Una funcionalidad queda terminada cuando:

```text
Works
+
Validated
+
Tested
+
Documented
+
Integrated
```

Si solamente aparece en pantalla, todavía no está terminada.


# 61. 🎤 Entrevista técnica

Al final deberás poder explicar:

> “Desarrollé una aplicación de Manufacturing Analytics para una planta sintética de cuatro líneas de producción. Diseñé un modelo jerárquico de planta, línea, equipo y variable, generé datos reproducibles y construí un Data Quality Gate antes de cualquier análisis. Sobre ese universo validado implementé KPIs de calidad, análisis Pareto, capacidad Cp/Cpk y control estadístico de procesos. Luego desarrollé un motor de excepciones que cruza equipos, turnos y variables para priorizar investigaciones, además de un módulo What-If para estimar impacto potencial. La interfaz fue construida en Dash y la lógica analítica quedó separada de la presentación y cubierta mediante tests automatizados.”

La meta es que esta explicación sea verdadera porque el proyecto realmente lo implementará.


# 62. 📝 Registro de cambios

Cada modificación relevante deberá registrarse así:

```text
## YYYY-MM-DD — Change

### What changed
...

### Why
...

### Files
...

### Tests
...

### Result
...

### Learning
...
```


# 63. 📌 Estado inicial de esta especificación

```text
Domain                         🟡 Defined
Industrial model               🟡 Defined
4 lines                        ✅ Defined
~23 equipment model            ✅ Defined
10 critical assets             ✅ Defined conceptually
Products                       🟡 Planned
Synthetic data                 🟡 Planned
Data Quality Gate              ✅ Existing concept
KPI engine                     ✅ Existing baseline
Capability engine              ✅ Existing baseline
Dash migration                 ⏳ Next
SPC engine                     ⏳ Planned
Diagnostic engine              ⏳ Planned
Impact analysis                ⏳ Planned
What-If                        ⏳ Planned
Industrial UI                  ⏳ Planned
Testing                        ✅ Existing baseline
Coverage                       ⏳ Planned
CI/CD                          ⏳ Planned
README final                   ⏳ Planned
GitHub release                 ⏳ Planned
```

Importante: el código histórico del prototipo tenía una estructura distinta de líneas/máquinas. Esa diferencia no se ocultará. El nuevo modelo industrial será implementado y validado explícitamente.


# 64. 🚀 Primer bloque real de trabajo

No se deben crear todos los módulos de una sola vez.

Orden obligatorio:

```text
AUDIT
  ↓
MODEL
  ↓
DATA
  ↓
VALIDATION
  ↓
ANALYTICS
  ↓
SPC
  ↓
DIAGNOSTICS
  ↓
DASH
  ↓
TEST
  ↓
CI
  ↓
PORTFOLIO
```

Primera intervención técnica:

1. auditar el repositorio actual;
2. revisar código Streamlit existente;
3. confirmar tests;
4. confirmar dependencias;
5. conservar lógica analítica útil;
6. cerrar el modelo industrial;
7. implementar el nuevo generador;
8. validar el dataset;
9. actualizar tests;
10. iniciar migración a Dash.

No se empieza por CSS.


# 65. 🏁 Objetivo final

```text
                    INDUSTRIAL KPI INTELLIGENCE
                              │
                              ▼
                        DATA INGESTION
                              │
                              ▼
                       DATA QUALITY GATE
                              │
                              ▼
                      INDUSTRIAL DATA MODEL
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
            KPI              SPC           CAPABILITY
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                      EXCEPTION ENGINE
                              │
                              ▼
                      DIAGNOSTIC SUPPORT
                              │
                              ▼
                       IMPACT / WHAT-IF
                              │
                              ▼
                       DECISION SUPPORT
                              │
                              ▼
                      CONTINUOUS IMPROVEMENT
```

La aplicación debe demostrar:

> **Sé tomar datos industriales, validar su calidad, estructurarlos según una lógica operacional, transformarlos en indicadores confiables, analizarlos estadísticamente, detectar desviaciones y convertir esos resultados en información útil para priorizar decisiones de producción y calidad.**

La tecnología es el medio:

```text
Python
Pandas
NumPy
Dash
Plotly
Pytest
Git
GitHub Actions
```

La propuesta profesional es:

```text
Industrial Data Analytics
+
Quality Engineering
+
Process Improvement
+
Operations Intelligence
```


# 66. 🧠 Principio final

El proyecto no busca fingir que es una planta real.

Busca demostrar que sabemos:

```text
modelar un problema industrial
        +
construir datos plausibles
        +
validarlos
        +
analizarlos correctamente
        +
visualizarlos profesionalmente
        +
convertirlos en soporte para decisiones
```

La definición de realismo será:

```text
Realistic ≠ Fake complexity

Realistic =
correct relationships
+
plausible process logic
+
valid statistics
+
traceable assumptions
+
usable interface
+
reproducible software
```

Este será el estándar 10/10 para toda la construcción.
