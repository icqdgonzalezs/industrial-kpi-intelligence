# Industrial KPI Intelligence — Documentación Técnica

> Todo lo descrito aquí es verificable ejecutando `pytest tests/ -v` y
> `ruff check .` en este repositorio. No hay pasos reconstruidos ni
> inferidos — donde algo no está probado, se marca explícitamente.

---

## 1. Resumen ejecutivo

**Industrial KPI Intelligence** es una plataforma de *Manufacturing
Analytics / Quality Engineering* orientada a soporte de decisiones:
convierte datos de producción y calidad en KPIs, control estadístico
de proceso (SPC), capacidad Six Sigma (Cp/Cpk) y un motor de
diagnóstico que prioriza qué requiere atención primero.

**No es:** un sistema de control de planta, no envía comandos a PLC,
no reemplaza MES/SCADA/ERP/LIMS. El dataset es sintético, reproducible
(semilla fija) y documentado — la planta es ficticia.

---

## 2. Arquitectura conceptual
CSV + config/quality_config.yaml
│
▼
data_loader.cargar_datos()
│
▼
filter_engine.aplicar_filtros() ←── Control Center (filtros globales)
│
▼
dcc.Store("store-datos-filtrados")
│
┌────────┼────────┬─────────────┬──────────────┐
▼ ▼ ▼ ▼ ▼
KPI Capability Control Operational Diagnostics
Charts Analysis (consume Capability
vía store-capacidad)
│ │ │ │ │
└────────┴─────────┴─────────────┴──────────────┘
▼
UI Dash — navegación por pestañas


Principios:
- `src/` es lógica pura — nunca importa Dash.
- Los callbacks de `dashboard/` nunca calculan estadística, solo
  orquestan: leen el store, llaman a `src/`, devuelven figuras/texto.
- Reproducibilidad: `RANDOM_SEED = 42` en el generador sintético.
- Un solo tema visual compartido (`aplicar_tema_oscuro`) para que
  todas las figuras Plotly se vean consistentes.

---

## 3. Modelo de datos real

Confirmado ejecutando `cargar_datos()` sobre `data/calidad_muestra.csv`:

- **250 lotes**, 2 líneas (L1, L2) × 4 máquinas cada una → **8 equipos**
  (`L1-M01`…`L1-M04`, `L2-M01`…`L2-M04`).
- **3 turnos**: Mañana, Tarde, Noche.
- Columnas: `lote, fecha, linea, maquina, equipo, turno, operador,
  unidades_producidas, unidades_defectuosas, unidades_reproceso,
  unidades_scrap, defecto_tipo, peso_promedio, longitud_promedio`.
- Variables críticas evaluadas (Cp/Cpk y carta de control), desde
  `config/quality_config.yaml → quality.variables_criticas`:

  | Variable | LSL | USL |
  |---|---|---|
  | Peso (`peso_promedio`) | 492.0 | 508.0 |
  | Longitud (`longitud_promedio`) | 117.5 | 122.5 |

> Nota: `config/quality_config.yaml` también contiene una sección
> `variables:` mucho más amplia (17 variables agrupadas por etapa de
> proceso — FILL, SEAM, CHECK, CAPPER, FFS, SEAL, PACK), heredada de
> una fase de planificación más ambiciosa. Ese bloque no está conectado
> a ningún módulo activo hoy — es documentación de una posible
> expansión futura, no un dato del dataset actual.

---

## 4. Catálogo técnico de módulos

### `src/` — lógica pura, sin Dash

| Módulo | Responsabilidad |
|---|---|
| `data_generator.py` | Genera el dataset sintético (semilla fija, reproducible) |
| `validation.py` | Data Quality Gate — rechaza datasets inconsistentes |
| `kpis.py` | FPY, tasa de defectos/scrap/reproceso, Pareto, KPIs por dimensión, lote crítico |
| `capability.py` | Cp/Cpk con clasificación Six Sigma |
| `control_charts.py` | Carta I-MR: límites de control, detección de puntos fuera de control (Western Electric #1) |
| `diagnostics.py` | Motor de diagnóstico priorizado — combina las 4 fuentes anteriores en hallazgos rankeados |

### `dashboard/` — un par componente+callback por pestaña

`filter_*`, `data_*`, `kpi_*`, `quality_performance_*`, `capability_*`,
`control_charts_*`, `operational_analysis_*`, `diagnostics_*`,
`tabs_callbacks.py`, más `utils.py` (deserialización de stores + tema
Plotly compartido), `app_layout.py` (composición) y `dash_app.py`
(punto de entrada).

---

## 5. Testing y cobertura

Evolución real de la suite durante el desarrollo (checkpoints
verificados con `pytest -q` en cada etapa):
141 → 155 → 172 → 173 → 184 → 186 → 194 (estado actual)

Estado actual:
194 passed
ruff check . → All checks passed!
Cobertura combinada src/ + dashboard/ ≈ 91%


---

## 6. Incidentes reales y aprendizajes

Cada uno de estos ocurrió de verdad durante el desarrollo y se
verificó con evidencia (no son ejemplos ilustrativos):

- **Ejecución de runbook sin pausas reales**: un bloque de comandos
  con puntos de pausa ("avísame aquí") se pegó completo en terminal;
  los `echo` de pausa se imprimieron pero no detuvieron la ejecución,
  dejando 7 archivos vacíos committeados. Aprendizaje: usar heredocs
  con contenido real en vez de placeholders que dependen de que el
  usuario se detenga a pedir el siguiente paso.
- **CSS no cargaba**: Dash resuelve `assets/` por defecto relativo al
  módulo donde se crea la instancia (`dashboard/assets`), no a la raíz
  del proyecto — corregido con `assets_folder` explícito vía `pathlib`.
- **Error de React ("objects are not valid as a React child")**: un
  callback enviaba un `go.Figure` completo a la prop `children` de un
  `html.Div` en vez de a la prop `figure` de un `dcc.Graph`. Verificado
  y corregido a nivel de servidor, con una petición HTTP real al
  endpoint `/_dash-update-component`.
- **`config/quality_config.yaml` sin `variables_criticas`**: el
  archivo local no tenía la sección que Capacidad y Diagnóstico
  necesitan — devolvía 0 variables silenciosamente. Corregido
  agregando el bloque real, verificado con capacidad = 2 variables y
  diagnóstico = 6 hallazgos (antes 0 y 4).
- **"N/D" traducido como "Dakota del Norte"**: el traductor del
  navegador interpretó la abreviación como el estado de EE.UU. —
  reemplazado por texto sin ambigüedad ("Sin datos").
- **`sed -i` fallaba en macOS**: la sintaxis GNU (`sed -i '...'`) no es
  compatible con BSD sed de macOS — se resolvió usando Python para
  todas las ediciones de archivo en vez de `sed -i`.

---

## 7. Estado actual

✅ KPI Engine, Capability (Cp/Cpk), Control estadístico (I-MR),
Motor de diagnóstico priorizado, Operational Analysis con drill-down,
navegación por pestañas, tema visual oscuro, CI (ruff + pytest),
deploy listo (Procfile/render.yaml + gunicorn verificado).

🔲 Pendiente: deploy real en Render (link en vivo), capturas de
pantalla actualizadas para el README, video demo, nivelar el proyecto
02 (Production Digital Twin) al mismo estándar.

---

## 8. Valor para portafolio

Este proyecto se presenta como una plataforma de *decision support*
industrial, no como un dashboard aislado. Evidencia técnica concreta:
arquitectura con separación estricta lógica/presentación, 194 tests
automatizados, CI real, bugs reales documentados con su corrección
verificada (no solo features que "funcionan a la primera"), y un
motor de reglas de negocio (`diagnostics.py`) que va más allá de
mostrar gráficos.
