# 🎯 TRASPASO MAESTRO — Industrial KPI Intelligence

> 📌 **Propósito:** documento autocontenido para arrancar un chat nuevo sin perder contexto.
> 📥 **Instrucción de uso:** pegar este archivo completo como PRIMER mensaje en un chat nuevo.
> 🗓️ **Última actualización:** sesión cerrada al final de Semana 3/8, Fase 4a completa.

---

## 📖 ÍNDICE

1. [Instrucciones para el asistente](#-instrucciones-para-el-asistente-leer-primero)
2. [Ficha del proyecto](#1️⃣-ficha-del-proyecto)
3. [Estado actual exacto](#2️⃣-estado-actual-exacto)
4. [Línea temporal de commits](#3️⃣-línea-temporal-de-commits)
5. [Decisiones técnicas clave](#4️⃣-decisiones-técnicas-clave-con-rationale)
6. [Estado de tests y calidad](#5️⃣-estado-de-tests-y-calidad)
7. [Deuda técnica conocida](#6️⃣-deuda-técnica-conocida)
8. [Roadmap pendiente](#7️⃣-roadmap-pendiente)
9. [Reglas operativas no negociables](#8️⃣-reglas-operativas-no-negociables)
10. [Historial de errores](#9️⃣-️-historial-de-errores--no-repetir)
11. [Archivos clave y comandos](#-archivos-clave-y-comandos)
12. [Próximo paso exacto](#1️⃣1️⃣--próximo-paso-exacto)
13. [Mensaje de transición](#1️⃣2️⃣--mensaje-de-transición-para-pegar-en-chat-nuevo)
14. [Notas de mentor](#1️⃣3️⃣--notas-de-mentor-para-el-próximo-asistente)

---

## 🔴 INSTRUCCIONES PARA EL ASISTENTE (leer primero)

Estás retomando un proyecto en curso. Antes de responder:

| # | Regla |
|---|---|
| 1 | **Leer completo este archivo.** No asumir nada que no esté acá. |
| 2 | **Actuar como ingeniero de software + mentor.** El usuario es autodidacta y valora explicaciones pedagógicas breves. |
| 3 | **Respetar reglas no negociables** (sección 8). No proponer alternativas que las violen. |
| 4 | **Antes de tocar código: leer el archivo.** Regla absoluta del proyecto. |
| 5 | **Verificar con `git status` antes de cada `git add`.** No confiar en la memoria. |
| 6 | **Un fix = un commit.** No mezclar propósitos. |
| 7 | **No commitear sin: pytest verde + ruff limpio + verificación visual.** |
| 8 | **Si algo falla, pedir datos crudos** (salida de terminal, log de CI), no proponer fixes por especulación. |
| 9 | **Estilo de respuesta:** directo, técnico, sin relleno. Markdown con tablas y bloques de código. Español. |
| 10 | **No repetir contexto que ya está acá.** El usuario ya lo sabe; solo aportar valor nuevo. |

> 🎯 **Próximo paso concreto del proyecto:** ver [sección 11](#1️⃣1️⃣--próximo-paso-exacto).

---

## 1️⃣ FICHA DEL PROYECTO

| Campo | Valor |
|---|---|
| 🏭 **Producto** | Industrial KPI Intelligence — dashboard industrial para PYMES manufactureras LatAm/España |
| 🌐 **Ecosistema** | Primer producto de 5 SaaS (Industrial Operations Intelligence) |
| 🛠️ **Stack** | Python 3.11.9 · Plotly Dash 4.4.1 · Plotly · pandas · numpy |
| 🧪 **Testing** | pytest 9.1.1 · ruff · GitHub Actions CI/CD |
| 📏 **Estándares aplicables** | ISA-95 · TPM (OEE) · NIST 6.1.3 / ISO 22514 (Pp/Ppk) · AIAG SPC · OWASP · ISA-101 (HMI) · WCAG 2.1 |
| ⚖️ **Licencia** | Elastic License 2.0 (nunca MIT) |
| 👤 **Usuario** | David González Santibáñez — Ing. Civil Químico + dev autodidacta |
| 📅 **Semana** | 3 de 8 |
| ✅ **Tests actuales** | **359 passed** |
| 🟢 **CI** | 2/2 verde (workflow Tests, run #50) |
| 🧹 **Working tree** | Limpio, rama `main` sincronizada con `origin/main` |
| 📊 **Producto 1 (MVP)** | ~75% |
| 🌍 **Ecosistema completo** | ~15% (1 de 5 productos) |
| 🔗 **Repo** | github.com/icqdgonzalezs/industrial-kpi-intelligence |
| 📂 **Ruta local** | `/Users/violeta/Projects/industrial-operations-intelligence/industrial-kpi-intelligence` |

---

## 2️⃣ ESTADO ACTUAL EXACTO

### ✅ Cerrado (commiteado + pusheado + CI verde)

- ✅ Bloques UX-1, UX-2, UX-3 (base visual del dashboard)
- ✅ Bloque 3A: adapter EN→ES + loader rewired a dataset canónico (18,078 filas)
- ✅ Fix σ del generador (σ=2.0 / 0.63)
- ✅ Fix SPC: Regla 1 contextualizada con falsos positivos esperados
- ✅ Refactor thresholds a YAML (SSOT)
- ✅ Fix σ minúscula (σ vs Σ)
- ✅ Fix labels del histograma (arriba del plot, `yref='paper'`)
- ✅ Fix tipografía ISA-101 (16px bold blanco)
- ✅ Fix color de líneas (gris neutro vs cian)
- ✅ **Fix #4** (`45903d2`): 4 KPIs de spec performance (PPM total, % dentro, % bajo LSL, % sobre USL)
- ✅ **Fix #5** (`fd1a338`): barras horizontales en Operacional (17 equipos legibles)
- ✅ **Bloque 5.5** (`fd1a338`): segmented control + microcopy + bugfix clickData + border removal
- ✅ **Fix #6** (`0426de3`): timestamp de frescura del dataset en header
- ✅ **Fix #7** (`cf89311`): escala AIAG SPC de clasificación Ppk (4 niveles)
- ✅ **Fix #5.6** (`303497f`): SSOT de labels visibles vía `LABELS_EJES_DIMENSION`
- ✅ **Fase 4a** (`be6fac9`): Iconografía no cromática en semáforos (WCAG 2.1 §1.4.1)

### 🟡 En curso

> **Nada.** Sesión cerrada. Working tree limpio.

### ⏳ Pendiente (roadmap en [sección 7](#7️⃣-roadmap-pendiente))

- ⏳ **Doc + σ** — README (343→359) + VISION.md + ARCHITECTURE.md + migrar Ppk a YAML **(PRÓXIMO PASO)**
- ⏳ **Fase 3a** — Export CSV por tab
- ⏳ **Fase 3b** — Loading + empty states
- ⏳ **Fase 3c** — Chip de filtros activos
- ⏳ **Bloque 3B** — Docker + Compose

---

## 3️⃣ LÍNEA TEMPORAL DE COMMITS

| Run | Commit | Descripción | Tests |
|:---:|---|---|:---:|
| #50 | `be6fac9` | Merge PR #5 — Fase 4a Iconografía semáforos | **359** |
| #49 | `c758e7f` | Feat Fase 4a — Iconografía semáforos (WCAG 2.1) | 359 |
| #48 | `303497f` | Fix #5.6 — SSOT label eje Y Operacional | 343 |
| #47 | `cf89311` | Fix #7 — Escala AIAG SPC de Ppk | 335 |
| #46 | `0426de3` | Fix #6 — Timestamp de frescura | 316 |
| #45 | `fd1a338` | Fix #5 + Bloque 5.5 | 295 |
| #44 | `73e7cbc` | ❌ (superseded por force-with-lease) | — |
| #43 | `45903d2` | Fix #4 — KPIs de spec | 284 |
| #42 | `63682a6` | Fix color de líneas | 279 |
| #41 | `a4813c4` | Fix tipografía ISA-101 | 279 |
| #40 | `6607570` | Fix labels histograma | 274 |
| #39 | `2a235f0` | Fix σ minúscula | 274 |
| #38 | `65fe368` | Refactor thresholds a YAML | 274 |
| #37 | `8214670` | Fix SPC Regla 1 | 270 |
| — | `70bb3da`, `20dbdee` | Bloque 3A adapter EN→ES | 270 |
| — | `cbfa067` | UX-3 color semántico KPIs | 270 |
| — | `0721133`, `4d23f96` | UX-1/UX-2 base visual | 267 |

📈 **Evolución de tests:**
`263` → `270` → `274` → `279` → `284` → `290` → `295` → `316` → `335` → `343` → **`359`**

---

## 4️⃣ DECISIONES TÉCNICAS CLAVE (con rationale)

### 4.1 🔄 Patrón strangler para migración EN→ES

- ⚠️ **Problema:** dashboard leía CSV legacy ES, mientras dataset canónico EN estaba huérfano.
- ✅ **Solución:** `src/schema_adapter.py` traduce EN→ES antes de devolver el DataFrame.
- 🎯 **Fundamento:** migrar incrementalmente sin big-bang. Cero riesgo en módulos consumidores.
- 💡 **Lección:** separar traducción de negocio permite migraciones sin downtime.

### 4.2 🗃️ SSOT en YAML para umbrales

- ⚠️ **Problema:** umbrales KPI hardcodeados + docstring que mentía.
- ✅ **Solución:** externalizar a `config/quality_config.yaml` (sección `kpi_thresholds`).
- 🎯 **Fundamento:** SSOT + DRY. Desbloquea onboarding SaaS multi-cliente.
- 💡 **Lección:** docstring que promete algo que el código no cumple = deuda técnica camuflada.

### 4.3 📈 SPC contextualizado (Regla 1 con falsos positivos)

- ⚠️ **Problema:** banner decía "48 puntos fuera de control" en rojo. Alarmante.
- ✅ **Solución:** `resumen_control_estadistico()` calcula esperados = n × 0.0027.
- 🎯 **Fundamento:** con n=18,078 el esperado es ~49. Reportar 48 como alerta era incorrecto.
- 💡 **Lección:** en SPC con muestras grandes, siempre reportar observados vs esperados.

### 4.4 🏭 Rendimiento vs Capacidad (Fix #4)

- ⚠️ **Problema:** Ppk=1.33 decía "excelente" sin dato del lote real.
- ✅ **Solución:** 4 KPIs nuevos: % dentro, % bajo LSL, % sobre USL, PPM total.
- 🎯 **Fundamento:** capacidad ≠ rendimiento. Ppk dice el potencial; PPM dice lo que pasó.
- 🔍 **Hallazgo:** Peso PPM=55 (verde) vs Longitud PPM=221 (ámbar), ambos con Ppk=1.33.
- 💡 **Lección:** Ppk solo oculta diferencias de rendimiento real.

### 4.5 🖥️ ISA-101 para HMI industrial

- ⚠️ **Problema:** labels del histograma tapaban barras.
- ✅ **Solución:** labels 16px bold blanco fuera del plot (`yref='paper'`), líneas grises dashed 1.8px.
- 🎯 **Fundamento:** ISA-101 exige legibilidad a 1-2 m. Diferenciación por posición, no por color.
- 💡 **Lección:** "datos medidos" y "referencias calculadas" deben ocupar canales visuales distintos.

### 4.6 🎯 Escala AIAG SPC para clasificación Ppk (Fix #7)

- ⚠️ **Problema:** banner decía "Capaz (excelente)" con Ppk=1.33. Falso: 1.33 es umbral inferior de "Capaz".
- ✅ **Solución:** escala de 4 niveles:

| Color | Rango | Clasificación |
|:---:|---|---|
| 🟢 | `Ppk ≥ 1.67` | **Clase mundial** |
| 🟡 | `1.33 ≤ Ppk < 1.67` | **Capaz** |
| 🟠 | `1.00 ≤ Ppk < 1.33` | **Marginal** |
| 🔴 | `Ppk < 1.00` | **No capaz** |

- 📚 **Fuente:** AIAG SPC (Chrysler/Ford/GM), NIST 6.1.3, ISO 22514. Convención de facto, no normada.
- 🛠️ **Implementación:** función pura `clasificar_ppk()` + constantes `UMBRAL_PPK_*`. Cada mensaje del banner cita el umbral numérico.
- 💡 **Lección:** en software industrial, el copy técnico es funcionalidad. Un banner incorrecto es un bug real.

### 4.7 🏷️ SSOT de labels visibles (Fix #5.6)

- ⚠️ **Problema:** `str.capitalize()` sobre value de dataset producía "Maquina" (sin tilde) en eje Y.
- ✅ **Solución:** `LABELS_EJES_DIMENSION = {value: label}` derivado de `DIMENSIONES_DISPONIBLES`. Función pura `_label_dimension()` con fallback.
- 🎯 **Fundamento:** SSOT + DRY. Agregar dimensiones no requiere tocar 2 lugares.
- 💡 **Lección:** cada string visible al usuario debe venir de un único lugar.

### 4.8 ♿ Iconografía no cromática en semáforos (Fase 4a — WCAG 2.1 §1.4.1)

- ⚠️ **Problema:** el color era el único canal para severidad. ~8% de los hombres son daltónicos.
- ✅ **Solución:** SSOT `dashboard/severity_icons.py` con `prefijar_icono()`. Aplicado en `_span_kpi` (KPIs top) y `_span_rendimiento` (capacidad PPM).
- 🎯 **Fundamento:** WCAG 2.1 §1.4.1 + ISA-101 (redundancia de canales en alarmas críticas).
- 🔍 **Hallazgo visual:** Peso (PPM=55, ✓ verde) y Longitud (PPM=221, ⚠ ámbar) con el MISMO Ppk=1.33 ahora se distinguen por color Y por icono.
- 💡 **Lección:** la accesibilidad no es "nice to have". Es funcionalidad industrial.

---

## 5️⃣ ESTADO DE TESTS Y CALIDAD

| Archivo | Tests | Cobertura conceptual |
|---|:---:|---|
| `test_capability.py` | 37 | Pp/Ppk + clasificar_ppk + rendimiento spec |
| `test_capability_callbacks.py` | 20 | Callbacks + `_estado_capacidad` + iconos semáforos |
| `test_control_charts.py` | 10 | I-MR + Western Electric |
| `test_control_charts_callbacks.py` | 2 | Wiring del callback |
| `test_dash_app.py` | 11 | Callbacks top + filtros |
| `test_data_generator.py` | 15 | Generador determinista seed=42 |
| `test_data_loader.py` | 13 | Adapter + manejo de errores |
| `test_dataset_metadata.py` | 21 | Frescura del dataset (16 parametrizados) |
| `test_diagnostics.py` / `_callbacks` | 13 + 5 | Findings + Pareto |
| `test_filter_engine.py` | 11 | Filtrado por línea/equipo/turno/operador |
| `test_kpi_callbacks.py` | 4 | `_span_kpi` con iconos semáforos |
| `test_kpi_presenter.py` | 4 | Formateo + clasificación |
| `test_kpi_thresholds.py` | 19 | Función pura + refactor SSOT |
| `test_kpis.py` | 32 | FPY, defectos, scrap, reproceso |
| `test_oee.py` / `_presenter` | 25 + 6 | OEE (A×P×Q) ISA-95 |
| `test_operational_analysis_callbacks.py` | 30 | Drill-down + `_label_dimension` |
| `test_plant_overview.py` / `_components` | 6 + 5 | Vista de planta |
| `test_quality_performance_callbacks.py` | 10 | FPY, Pareto |
| `test_quality_performance_components.py` | 7 | Componentes UI |
| `test_quality_performance_spec.py` | 6 | Especificación |
| `test_schema_adapter.py` | 11 | Adapter EN→ES |
| `test_severity_icons.py` | 9 | `prefijar_icono` + SSOT iconos |
| `test_utils.py` | 5 | Utilidades |
| `test_validation.py` | 22 | Validación de contratos |
| **TOTAL** | **359** | ✅ Todos verdes |

---

## 6️⃣ DEUDA TÉCNICA CONOCIDA

| # | Deuda | Impacto | Prioridad |
|:---:|---|---|:---:|
| 1 | README dice "263 passing" (real: 359) | Cosmético | 🟢 Baja |
| 2 | ~~Capacidad: dos verdades no explicadas~~ | — | ✅ Resuelta (Fix #7) |
| 3 | ~~Sin timestamp de datos en header~~ | — | ✅ Resuelta (Fix #6) |
| 4 | ~~Barras verticales con 17 labels ilegibles~~ | — | ✅ Resuelta (Fix #5) |
| 5 | Sin export CSV/PDF por tab | Adopción | 🟠 Media |
| 6 | Sin loading / empty states | Robustez | 🟡 Media |
| 7 | ~~Sin iconografía en semáforos (solo color)~~ | — | ✅ Resuelta (Fase 4a) |
| 8 | Docker + Compose pendiente | Deploy | 🟠 Media |
| 9 | Umbrales Ppk hardcodeados (deberían ir a YAML) | Mantenibilidad | 🟡 Media |
| 10 | Falta VISION.md y ARCHITECTURE.md | Escalabilidad | 🟡 Media |

---

## 7️⃣ ROADMAP PENDIENTE

| Fase | Fix/Feature | Estimación | Prioridad |
|:---:|---|:---:|:---:|
| **Doc + σ** | **README + VISION + ARCHITECTURE + migrar Ppk a YAML — PRÓXIMO PASO** | 1 h | 🟡 Media |
| 3a | Export CSV por tab | 3 h | 🟠 Media |
| 3b | Loading + empty states | 2 h | 🟡 Media |
| 3c | Chip de filtros activos | 1 h | 🟢 Baja |
| 5 | Docker + Compose (Bloque 3B) | 2 h | 🟠 Media |

> 💡 **Nota:** Docker (Bloque 3B) queda para el final de Fase 3-4, cuando el producto esté visualmente estable. Dockerizar algo que va a rediseñarse es trabajo tirado.

---

## 8️⃣ REGLAS OPERATIVAS NO NEGOCIABLES

### 💻 Terminal (protocolo de arranque)

```bash
cd /Users/violeta/Projects/industrial-operations-intelligence/industrial-kpi-intelligence
source venv/bin/activate
which python   # debe mostrar .../venv/bin/python
```

### 🐙 Git (versión antigua del cliente)

| ✅ Correcto | ❌ Incorrecto |
|---|---|
| Usar `git checkout` para descartar cambios. | Nunca `git switch` ni `git restore`. |
| `git push --force-with-lease` si es necesario (con verificación previa). | Nunca `git push --force` sin `git fetch` previo. |
| Autenticación con Personal Access Token (PAT), no contraseña. | Nunca password en texto plano. |

### ✍️ Commits

- Conventional Commits: `feat:`, `fix:`, `refactor:`, `docs:`, `style:`, `test:`, `chore:`, `polish:`.
- Un fix = un commit. No mezclar propósitos.
- Mensaje en inglés, cuerpo en español si aplica.

### 🤖 CI/CD

- 2/2 checks verdes antes de mergear. Sin excepción.
- Cualquier push dispara el workflow Tests (~50 s).

### 🎨 UX / CSS

- Ver el archivo antes de tocar. Nunca editar a ciegas.
- Verificación visual con `⌘ + Shift + R` (hard reload) obligatoria.
- **Regla C.1:** sin números no hay cierre.

### 💾 Código

- Idioma del código: inglés. Docs y comentarios: español.
- Arquitectura: `src/` (lógica) / `dashboard/` (presentación) / `tests/`.
- Nomenclatura de capacidad: `world_class` / `capable` / `marginal` / `not_capable`.
- Nomenclatura de severidad CSS: `success` / `warning` / `danger` / `neutral`.

### 🛠️ Protocolo de cada fix

1. Leer los archivos involucrados (`grep` + `cat`).
2. Diagnosticar causa raíz, no síntoma.
3. Grep amplio si se tocan strings/constantes: `grep -rn "string_viejo" src/ dashboard/ tests/`.
4. Escribir código + tests juntos.
5. Correr gates: `pytest` + `ruff check .`.
6. Verificación visual con `⌘ + Shift + R`.
7. `git status` antes del add.
8. `git add` con paths textuales (no escribir a mano).
9. `git status` post-add (verificar N archivos staged).
10. Commit con mensaje conventional.
11. Push y verificar CI 2/2 verde.

---

## 9️⃣ ⚠️ HISTORIAL DE ERRORES — NO REPETIR

| ❌ Error | ✅ Correcto |
|---|---|
| Editar CSS a ciegas | Ver el archivo antes de tocarlo |
| Wildcard `div[class*="Select"]` | Selectores específicos, sin wildcards |
| `plotly_dark` pisa trazas | Aplicar tema oscuro sin tocar configuración de trazas |
| Reconstruir archivos sin ver el original | Leer el archivo primero, siempre |
| Decir "reemplaza solo la función X" | Pasar el archivo completo cuando es chico |
| `git switch` / `git restore` | Usar `git checkout` |
| `git push --force` sin verificar | `git push --force-with-lease` primero |
| Asumir que el CSS se aplicó | Verificación visual con `⌘ + Shift + R` |
| Commitear sin tests verdes | Gates primero: `pytest` + `ruff check .` |
| Aplicar solo parte de un bloque de archivos | Checklist completo: los N archivos o ninguno |
| Commit sin `git add` previo | `add` → `status` → `commit` → `push` (4 pasos) |
| Copiar totales de una era previa a los tests | Recalcular desde el CSV actual |
| `git push` sin `fetch` previo | `git fetch origin` + `git log origin/main` antes |
| Asumir ubicación de archivo por nombre | Confirmar con los imports en tests + `ls` |
| `font.weight` en Plotly annotations | No existe. Usar HTML `<b>...</b>` |
| Cian sobre cian | Referencias en gris neutro, datos en color |
| `git add` con path mal escrito | TAB para autocompletar + `git status` antes del commit |
| Commitear test que importa símbolo NO staged | Regla del grafo de imports: archivo + sus dependencias, juntos |
| Grep de reconocimiento con scope angosto | `grep -rn "string_viejo" src/ dashboard/ tests/` |
| Asumir que Plotly devuelve el mismo tipo | Al testear atributos de Plotly, comparar contra `tuple(...)` |
| Apilar señales redundantes (posición + color + número + borde) | Una jerarquía visual por atributo |
| Diagnosticar fallo de CI sin leer el log | Pedir `git log -1 --stat` + `git status` + log del run rojo |
| Password de GitHub en `git push` | Personal Access Token (PAT) + `credential.helper osxkeychain` |
| Modelo LLM hardcodeado sin fallback | Escalera de modelos o verificar catálogo vigente |
| Heredoc largo pegado en terminal (>2KB) | Usar `pbpaste > archivo` (portapapeles → disco directo) |

---

## 🔟 📁 ARCHIVOS CLAVE Y COMANDOS

### 🗂️ Estructura del proyecto

```text
industrial-kpi-intelligence/
├── assets/
│   └── style.css                          # Tema oscuro + chips + timestamp
├── config/
│   ├── generator_config.yaml              # σ=2.0 / 0.63, seed=42
│   ├── plant_config.yaml                  # Maestro de líneas/equipos
│   └── quality_config.yaml                # Límites spec + kpi_thresholds (SSOT)
├── dashboard/
│   ├── app_layout.py                      # Header + timestamp frescura
│   ├── dash_app.py                        # Entry point + metadata_dataset
│   ├── capability_callbacks.py            # Fix #7 + Fase 4a (iconos)
│   ├── kpi_callbacks.py                   # Fase 4a: _span_kpi con iconos
│   ├── operational_analysis_components.py # Chips + LABELS_EJES_DIMENSION
│   ├── operational_analysis_callbacks.py  # Barras horizontales + _label_dimension
│   ├── kpi_presenter.py                   # Delega a src/kpi_thresholds
│   ├── severity_icons.py                  # Fase 4a: SSOT iconos (NUEVO)
│   └── ...
├── src/
│   ├── capability.py                      # clasificar_ppk + UMBRAL_PPK_*
│   ├── dataset_metadata.py                # Fix #6: frescura
│   ├── kpi_thresholds.py                  # SSOT, lee YAML
│   ├── schema_adapter.py                  # Adapter EN→ES
│   ├── data_generator.py                  # Generador determinista
│   └── ...
├── tests/
│   └── 27 archivos, 359 tests
├── data/raw/
│   └── synthetic_production_data.csv      # 18,078 filas, esquema EN + cola ES
└── pyproject.toml                          # config pytest + ruff
```

### ⌨️ Comandos verificados

```bash
# Activar entorno
cd /Users/violeta/Projects/industrial-operations-intelligence/industrial-kpi-intelligence
source venv/bin/activate

# Gates
pytest                          # 359 passed
ruff check .                    # All checks passed!

# Regenerar dataset (si hay que tocar σ)
python -m src.data_generator

# Verificar dataset
python -c "import pandas as pd; df = pd.read_csv('data/raw/synthetic_production_data.csv'); print('filas:', len(df))"

# Arrancar dashboard
python -m dashboard.dash_app    # http://127.0.0.1:8050
lsof -ti:8050 | xargs kill -9   # si el puerto está ocupado

# Commit conventional (heredoc)
git add <archivos>
git status                      # ← verificar los N archivos staged
git commit -F - <<'EOF'
feat(scope): título

Cuerpo explicando el por qué.
EOF
git push origin main

# Escribir archivos largos sin truncamiento (macOS Mojave)
pbpaste > archivo.md            # portapapeles → disco (evita buffer de terminal)
```

---

## 1️⃣1️⃣ 🎯 PRÓXIMO PASO EXACTO

### 📚 Doc + σ — Consolidación (README + VISION + ARCHITECTURE + SSOT Ppk)

**Objetivo:** cerrar 3 deudas técnicas de bajo esfuerzo antes de features nuevas.

**Tareas:**

| # | Tarea | Descripción |
|:---:|---|---|
| 1 | **README.md** | Actualizar "263 passing" a "359 passing". Añadir badge de CI. Actualizar porcentaje MVP. |
| 2 | **VISION.md** (nuevo) | Explicar los 5 productos del ecosistema, mercado objetivo (PYMES manufactureras LatAm/España), propuesta de valor. |
| 3 | **ARCHITECTURE.md** (nuevo) | Diagrama de capas (`src/` lógica vs `dashboard/` presentación), patrón SSOT, decisiones clave (sección 4 de este doc). |
| 4 | **σ (SSOT Ppk)** | Migrar umbrales Ppk (`UMBRAL_PPK_*` de `capability.py`) a `config/quality_config.yaml` sección `ppk_thresholds`. Análogo al refactor de `kpi_thresholds` (sección 4.2). |

- ⏱️ **Estimación:** 1 h total.
- 📊 **Impacto:** MVP +1-2%, sin features nuevas, solo consolidación.

**Primeros comandos a correr (leer antes de tocar):**

```bash
# 1. Ver el README actual
cat README.md

# 2. Ver los umbrales Ppk hardcodeados
grep -n "UMBRAL_PPK" src/capability.py

# 3. Ver la estructura del YAML actual (referencia para el nuevo)
cat config/quality_config.yaml
```

### 🗺️ Después de Doc + σ (orden sugerido)

1. **Fase 3a** — Export CSV por tab (3 h)
2. **Fase 3b** — Loading + empty states (2 h)
3. **Fase 3c** — Chip de filtros activos (1 h)
4. **Bloque 3B** — Docker + Compose (2 h, decisión build vs volumen pendiente)

---

## 1️⃣2️⃣ 💬 MENSAJE DE TRANSICIÓN (para pegar en chat nuevo)

```text
Contexto: pego abajo el TRASPASO_MAESTRO del proyecto Industrial KPI Intelligence.
Soy David, Ing. Civil Químico + dev autodidacta, semana 3/8 del Producto 1.

Estado: Fase 4a cerrada, 359 tests, CI verde, working tree limpio.
Próximo paso: Doc + σ (README + VISION + ARCHITECTURE + SSOT Ppk).

Reglas clave que espero que respetes:
- Leer el archivo antes de tocar (regla absoluta)
- git status antes de cada git add
- Un fix = un commit
- Verificación visual con ⌘ + Shift + R obligatoria
- pytest + ruff verdes antes de commitear

Actuá como ingeniero de software senior + mentor. Directo, técnico,
sin relleno. Español. Markdown con tablas y bloques de código.

[PEGAR TODO EL CONTENIDO DE TRASPASO_MAESTRO.md ABAJO]
```

---

## 1️⃣3️⃣ 🎓 NOTAS DE MENTOR (para el próximo asistente)

Este usuario **no es un junior**. Es un ingeniero químico con criterio técnico real. Ha demostrado en esta sesión:

- 🔍 **Detectar bugs por inspección visual** (el "Capaz (excelente)" con Ppk=1.33, el clickData persistente).
- 📊 **Pedir diagnóstico con datos** cuando CI falla, no con fe (Regla #8).
- 🔄 **Aceptar reversiones** cuando una decisión no funciona (workflow de IA review, revertido y limpio).
- 🎯 **Mantener disciplina en cada fix:** leer → diagnosticar → escribir → testear → verificar → commitear.
- ⚖️ **Decidir con criterio cuándo parar** (no usar modelos gratuitos de menor calidad aunque fueran gratis).

### 🎯 Cómo tratarlo

- Como **colega senior**, no como aprendiz.
- **Explicá el por qué** de las decisiones técnicas, no solo el cómo.
- **Citá normas industriales** cuando aplique (ISA-101, AIAG SPC, NIST 6.1.3, ISO 22514, WCAG 2.1).
- **Valorá la honestidad** por sobre la complacencia. Si una decisión es mala, decilo con datos. Si una estimación se desvía, corregila.
- **No quiere halagos**, quiere producto de calidad.

---

> 📌 **Fin del TRASPASO_MAESTRO.**
> Última actualización: Semana 3/8, Fase 4a cerrada.
> Próxima sesión: Doc + σ.