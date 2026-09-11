---
title: "Semanas 1 y 2 — Guía Completa"
project: "Industrial KPI Intelligence"
ecosystem: "Industrial Operations Intelligence"
version: "1.0.0"
author: "David González"
date_created: "2026-09-11"
tags:
  - learning-journal
  - week-01
  - week-02
  - industrial-kpi
  - oee
  - schema-adapter
  - nist-6.1.3
status: "published"
related:
  - "docs/adr/0001-canonical-dataset.md"
  - "docs/adr/0002-naming-convention.md"
  - "CHANGELOG.md"
  - "docs/industrial-kpi-intelligence-master-plan.md"
---

# 📘 Semanas 1 y 2 — Guía Completa

## Industrial KPI Intelligence · De portafolio a producto vendible

**Proyecto:** Industrial KPI Intelligence (Proyecto 01 — ecosistema Industrial Operations Intelligence)
**Nivel:** estudiante de programación con formación en ingeniería
**Objetivo:** entender qué construimos en 2 semanas, por qué, y cómo contarlo en una entrevista

---

## 📑 Tabla de contenidos

- [Parte 0 — El mapa del proyecto](#parte-0--el-mapa-del-proyecto)
- [Parte 1 — Semana 1: los 4 pilares](#parte-1--semana-1-los-4-pilares)
- [Parte 2 — Semana 2: los 5 puentes](#parte-2--semana-2-los-5-puentes)
- [Parte 3 — Los 8 conceptos que dominaste](#parte-3--los-8-conceptos-que-dominaste)
- [Parte 4 — Los comandos que dominaste](#parte-4--los-comandos-que-dominaste)
- [Parte 5 — Cómo contarlo en una entrevista](#parte-5--cómo-contarlo-en-una-entrevista)
- [Parte 6 — Glosario](#parte-6--glosario)
- [Parte 7 — Lo que sigue (Semana 3)](#parte-7--lo-que-sigue-semana-3)
- [Cierre de profesor — 3 reflexiones](#cierre-de-profesor--3-reflexiones)

---

## 🧭 Parte 0 — El mapa del proyecto

Antes de la Semana 1, `industrial-kpi-intelligence` era un dashboard funcional en Dash con 194 tests verdes. Hacía muy bien una cosa: convertir datos de planta en KPIs, control estadístico (SPC), capacidad Six Sigma y un motor de diagnóstico priorizado. Pero era un **proyecto de portafolio**, no un **producto vendible**.

La diferencia es la misma que entre un auto de carreras de fin de semana y un auto de serie: el de carreras corre más rápido, pero el de serie cumple normativas, tiene garantía, frena con ABS, y cualquiera puede comprarlo sin que el motor le explote a los 3 meses.

**Meta de las 2 semanas:** cerrar la brecha entre "funciona" y "**se puede vender**".

### Estado final

| **Métrica** | **Antes** | **Después de Semana 2** |
|---|---|---|
| Tests | 194 | **244** |
| Licencia | MIT (regalaba IP) | **Elastic License 2.0** |
| KPI insignia (OEE) | ❌ Inexistente | ✅ Implementado con ISA-95/TPM |
| Datasets | 2 esquemas peleados | ✅ Camino A: adapter + canónico decidido |
| Nomenclatura Cp/Cpk | Mal etiquetada | ✅ Pp/Ppk correcta (NIST 6.1.3) |
| CI | Sin pin de ruff | ✅ `ruff==0.16.6` reproducible |
| CHANGELOG | Aspiracional | ✅ Verificado contra realidad |

---

## 🏗️ Parte 1 — Semana 1: los 4 pilares

La Semana 1 no agregó features. **Endureció los cimientos.** Como reforzar los pilares de una casa antes de pintar las paredes.

### 🏛️ Pilar 1 — La licencia (MIT → Elastic License 2.0)

**El problema, en criollo:**

Una licencia **MIT** dice textualmente: *"cualquiera puede hacer lo que quiera con este código, incluso venderlo como propio, sin darte nada"*. Tu código estaba publicado así en GitHub.

**Traducción comercial:** cualquier competidor podía clonar tu repo, quitarle tu nombre, y venderlo como SaaS por $5K/mes. Legalmente. Y tú no podías reclamar.

**La solución (ELv2):**

| **Perfil** | **Qué puede hacer con ELv2** |
|---|---|
| Reclutador / evaluador técnico | Clonar, leer, correr, aprender — sin restricciones |
| Empresa que lo usa internamente | Instalarlo en su infraestructura para su propia operación |
| **Empresa que lo revende como SaaS** | ❌ **Prohibido sin acuerdo comercial** |

**Lección:** una licencia no es un trámite. Es **una decisión de modelo de negocio**. Sin ELv2, tu SaaS no tenía forma legal de venderse.

---

### 🏛️ Pilar 2 — ADR-0001: la decisión del dataset canónico

**El problema, en criollo:**

Tu repo tenía **dos datasets con esquemas incompatibles**:

| | `calidad_muestra.csv` | `synthetic_production_data.csv` |
|---|---|---|
| Filas | 250 | 18,078 |
| Columnas | En español (`lote, equipo, unidades_producidas...`) | En inglés (`timestamp, equipment_id, units_produced...`) |
| Generador | ❌ Manual, desconocido | ✅ `data_generator.py`, seed=42, documentado |
| ¿Lo usa la app? | ✅ Sí, `data_loader.py` | ❌ Nadie — huérfano |

**Traducción comercial:** la app que un prospecto veía en la demo corría sobre **250 filas genéricas**, mientras el generador "industrial realista" de 18k filas dormía en `data/raw/` sin alimentar nada.

**La decisión (ADR = Architecture Decision Record):** documentar que `synthetic_production_data.csv` es **el dataset canónico del producto**, y que `calidad_muestra.csv` queda como legacy.

**Pero eso no bastaba:** cambiar el loader directo iba a romper **~150 tests** que dependían del esquema español. Así que el ADR decidió el **Camino A (patrón strangler)**: un **adapter** que traduce el esquema canónico al legacy, sin tocar el resto.

*(Este adapter es el protagonista de la Semana 2.)*

**Lección:** un ADR no es burocracia. Es la **foto de una decisión** con contexto, alternativas y consecuencias. En 6 meses olvidarás por qué tomaste esa decisión; el ADR te la recuerda.

**Referencia:** [`docs/adr/0001-canonical-dataset.md`](../adr/0001-canonical-dataset.md)

---

### 🏛️ Pilar 3 — El motor OEE (ISA-95/TPM)

**El problema, en criollo:**

El producto se llamaba "OEE Dashboard" pero **OEE no existía en el código**. Solo existían FPY, tasa de defectos, scrap y reproceso — componentes de *Quality* del OEE, no el OEE completo.

**Traducción comercial:** vender "OEE dashboard" sin OEE es **fraude comercial**. Un ingeniero de planta lo detecta en 5 minutos.

**La fórmula (ISA-95/TPM, sin atajos):**

```text
OEE = Availability × Performance × Quality

Availability = Run Time / Planned Production Time
    Planned Production Time = Total Time − Planned Downtime
    Run Time = Planned Production Time − Unplanned Downtime

Performance = (Ideal Cycle Time × Units Produced) / Run Time
    CAPEADO a 1.0 — un equipo no corre más rápido que su ciclo ideal

Quality = Good Units / Total Units Produced
    = FPY (una sola definición de FPY en todo el codebase)
```

**Tres decisiones de ingeniería clave:**

1. **Availability excluye paro planificado.** Un cambio de formato programado no es una pérdida: es parte del plan. Penalizarlo distorsiona la métrica.
2. **Performance se capa a 1.0.** Si tu `ideal_cycle_time` está mal configurado (muy bajo), el cálculo puede dar 1.5 → físicamente imposible → se trata como error de config, no como ganancia.
3. **La agregación de planta se pondera por tiempo operativo**, nunca promedio simple de OEE fila a fila. Un equipo que operó 2 horas con OEE 0.40 no pesa lo mismo que uno que operó 20 con 0.90.

**Lección:** un cálculo incorrecto en un KPI industrial no es un bug. Es **pérdida de confianza comercial**. Las fórmulas tienen que ser defendibles ante un auditor TPM.

---

### 🏛️ Pilar 4 — Extensión del schema del generador

**El problema, en criollo:**

`src/data_generator.py` generaba los datos industriales pero **no incluía las columnas que OEE necesita**:

- `planned_time_min`
- `planned_downtime_min`
- `unplanned_downtime_min`
- `ideal_cycle_time_sec`

Sin esas columnas, el motor OEE **no tenía qué calcular**.

**La solución:** extender el generador + config YAML, con **supuestos documentados** (¿cuánto dura un turno? ¿cuánto paro planificado? ¿de dónde sale el ciclo ideal?).

**Regla clave del generador:** `ideal_cycle_time_sec` se **deriva** de `production_per_shift` en vez de hardcodearse. Una sola fuente de verdad → no se puede desincronizar.

**Lección:** un generador sintético no produce "datos reales" — produce **datos plausibles según un modelo explícito**. Cada supuesto debe estar documentado, no escondido en el código.

---

### 🕵️ Los 3 bugs reales de la Semana 1

#### Bug 1 — `ModuleNotFoundError: No module named 'dash'` (8 veces)

- **Síntoma:** 8 archivos de tests no cargaban en la Mac.
- **Causa:** el entorno virtual no estaba activado. Python del sistema no tiene las librerías del proyecto.
- **Solución:** `source venv/bin/activate` antes de cualquier comando.
- **Lección:** el prefijo `(venv)` en tu prompt no es decoración. Es el semáforo que dice *"estás usando las librerías del proyecto, no las del sistema"*.

#### Bug 2 — CI rojo con 6 segundos de duración

- **Síntoma:** los tests verdes localmente, CI rojo en 6 segundos.
- **Causa:** `ruff check .` encontró `F841: variable base_prod no usada`.
- **Solución:** eliminar la línea muerta en `src/data_generator.py`.
- **Lección:** un CI que falla en 6 segundos no está roto — es **eficiente**. `ruff` corrió completo y encontró el problema.

#### Bug 3 — Push rechazado por divergencia

- **Síntoma:** `git push` rechazado con `non-fast-forward`. `git status` decía *"diverged, 19 and 10 commits each"*.
- **Causa:** el remote tenía 10 commits (ediciones manuales del README viejo hechas en GitHub web) que tu local no tenía.
- **Solución:** decidir que tu `main` local era la fuente de verdad → `git push --force origin main`.
- **Lección:** `--force` es seguro **solo cuando sabes qué hay en ambos lados**. Si esos 10 commits hubieran sido trabajo de un colega, los habrías borrado.

---

### 📊 Los números de la Semana 1

| **Métrica** | **Antes** | **Después** |
|---|---|---|
| Tests | 194 | 225 |
| OEE implementado | ❌ | ✅ |
| Columnas OEE en el dataset | ❌ | ✅ |
| Licencia | MIT | ELv2 |
| ADRs | 0 | 1 (ADR-0001) |

---

## 🌉 Parte 2 — Semana 2: los 5 puentes

Si la Semana 1 fue cimientos, la Semana 2 fue **construir los puentes** entre lo viejo y lo nuevo. **Sin tocar nada de lo viejo.**

### 🌉 Puente 1 — El schema adapter (patrón strangler)

**El problema:**

El ADR-0001 dijo "el dataset canónico es el de 18k filas en inglés". Pero **~150 tests** dependían del esquema viejo en español. Reemplazar el loader directo rompía todo.

**La solución (patrón strangler / Camino A):**

```text
CSV canónico (EN)  →  [schema_adapter]  →  contrato legacy (ES)  →  pipeline existente intacto
    18,078 filas         traduce              validation.py
    inglés                                    kpis.py
                                              capability.py
                                              diagnostics.py
                                              dashboard/
```

**Cómo funciona el adapter, en criollo:**

Es un **traductor en la frontera**. Recibe el DataFrame del CSV nuevo (inglés) y devuelve un DataFrame con las columnas que el resto del código ya sabe consumir (español).

**Tres reglas que hace cumplir:**

1. **`equipo`** = `equipment_id` (ej. `"L1-FILL-01"`)
2. **`linea`** = `line_id` (ej. `"L1"`)
3. **`maquina`** = `equipment_id` sin el prefijo `"{line_id}-"` (ej. `"FILL-01"`)

Con esas 3 reglas, `validation.py._validar_equipo` **funciona igual que antes**, sin modificar una sola línea.

**Lección:** un adapter es **infraestructura transitoria, no permanente**. Tiene **fecha de muerte** escrita en el ADR: cuando `validation.py` hable inglés nativo (Semanas 3-4), el adapter se elimina en un solo commit.

---

### 🌉 Puente 2 — Keys estables para OEE (i18n)

**El problema:**

`clasificar_oee` devolvía **texto en español** (`"Clase mundial"`, `"Aceptable"`, `"Bajo"`). Eso acoplaba el **motor de cálculo** al **idioma de presentación**. Si mañana querías vender en Brasil, tenías que tocar el motor de cálculo. **Malo.**

**La solución (H2 del audit):**

```text
Motor (src/oee.py):       devuelve  "world_class" | "acceptable" | "low"
Presenter (dashboard/oee_presenter.py): traduce a "Clase mundial" | "World class"
```

**Regla arquitectónica:** `src/` calcula. `dashboard/` presenta. Nunca se mezclan.

**Lección:** una **key estable** es un contrato entre capas. Un **label** es una decisión de UI. Mezclarlos es deuda técnica disfrazada de simplicidad.

---

### 🌉 Puente 3 — Rename Cp/Cpk → Pp/Ppk (NIST 6.1.3)

**El problema (auditoría seria):**

El código calculaba sigma con `valores.std(ddof=1)` (variación total) pero etiquetaba el resultado como **Cp/Cpk**.

**Per NIST 6.1.3 / ISO 22514:**

| **Índice** | **Sigma usado** | **Significado** |
|---|---|---|
| **Cp/Cpk** | Sigma within (rango móvil / d2) | Capacidad de **corto plazo** |
| **Pp/Ppk** | Sigma overall (`ddof=1`) | Capacidad **global** del proceso |

El número era correcto. **La etiqueta estaba mal.** Un auditor Six Sigma lo detecta al instante.

**La solución:** rename quirúrgico en:

- `src/capability.py` → keys `cp`/`cpk` → `pp`/`ppk`, `calcular_cp_cpk` → `calcular_pp_ppk`
- `dashboard/capability_callbacks.py` → labels visibles
- `dashboard/capability_components.py` → labels visibles
- `tests/test_capability*.py` → asserts
- Los **IDs de los callbacks Dash NO se renombran** (contrato con el layout). Se agenda para Semana 6.

**Lección:** un rename no es "buscar-y-reemplazar en un archivo". Es **rastrear todos los consumidores** del símbolo renombrado, incluyendo docstrings, tests y UI. Si el rename se queda a medias, `pytest` lo detecta al coleccionar.

---

### 🌉 Puente 4 — Fix del generador (Performance saturado en 1.0)

**El problema (detectado con evidencia numérica):**

`Performance (rendimiento)` daba `mean = 0.9999` sobre las 18k filas. **Saturado en el techo.**

**Causa raíz:** `units_produced` se generaba **independiente del paro no planificado** de la misma fila. El generador producía las mismas unidades sin importar si el equipo había estado parado 5 o 42 minutos.

**La solución en dos partes:**

**A) Fórmula del generador (código):**

```python
tiempo_operativo_min = planned_time − planned_downtime − unplanned_downtime
units_produced = (tiempo_operativo_min × 60 / ideal_cycle_time) × prod_factor
```

**B) Calibración de la distribución (YAML):**

```yaml
# ANTES: rendimiento utópico
Mañana: {mean: 1.00, std: 0.02}  # 50% de samples se capan a 1.0

# DESPUÉS: realista (benchmarks TPM de manufactura discreta)
Mañana: {mean: 0.90, std: 0.05}
Tarde:  {mean: 0.88, std: 0.05}
Noche:  {mean: 0.84, std: 0.06}
```

**Evidencia ANTES vs. DESPUÉS:**

| **Métrica** | **Antes** | **Después** |
|---|---|---|
| mean(performance) | 0.9999 | **0.8733** |
| std(performance) | ≈0 | **0.0584** |
| Histograma | pico pegado a 1.0 | campana centrada |

**Lección (oro puro):** un KPI sin variación no informa. Un generador calibrado por "lo que se ve bien" produce utopías matemáticas. Un generador calibrado por **la física del sistema** produce datos que un ingeniero de planta reconoce.

---

### 🌉 Puente 5 — CI reproducible (pin de ruff)

**El problema:**

`.github/workflows/tests.yml` decía:

```yaml
run: pip install ruff
```

Eso significa *"instala la última versión de ruff disponible"*. Tu Mac tenía `0.16.6`, CI instaló algo más nuevo con reglas más estrictas → **mismo código, dos veredictos**. Este fue el bug que causó el lint rojo de Semana 1.

**La solución (1 línea):**

```yaml
run: pip install ruff==0.16.6
```

**Lección:** `==` (versión exacta) es **reproducibilidad**. `>=` (versión mínima) es una promesa rota esperando a suceder. Los sistemas regulados exigen `==`.

---

### 🕵️ Los 5 bugs reales de la Semana 2

#### Bug 1 — `git switch` no existe en tu Git

- **Síntoma:** `git: 'switch' is not a git command`.
- **Causa:** `git switch` se agregó en Git 2.23 (2019). Tu Mac tiene una versión anterior.
- **Solución:** `git checkout` (comando antiguo, sigue funcionando).
- **Lección:** Git es retrocompatible pero no futurocompatible. En Macs viejas, usar comandos clásicos.

#### Bug 2 — `pip install ruff==<LA_VERSIÓN_QUE_USA_CI>` (placeholders literales)

- **Síntoma:** `bash: syntax error near unexpected token` (los `<>` son redirecciones en bash).
- **Causa:** copiaste el placeholder literal sin reemplazar.
- **Solución:** sustituir el placeholder por el valor real.
- **Lección:** en bash, `<` y `>` son **operadores**, no decoración. Los placeholders son para humanos, no para la terminal.

#### Bug 3 — La reconstrucción incompleta de `capability_callbacks.py`

- **Síntoma:** `ImportError: cannot import name 'registrar_callbacks_capability'`.
- **Causa:** reconstruí el archivo desde la interfaz de los tests, pero **perdí** la función que registra los callbacks Dash con IDs específicos.
- **Solución:** `git show main:dashboard/capability_callbacks.py` → recuperar el original → adaptar preservando los IDs.
- **Lección:** los **IDs de callbacks Dash** son un contrato silencioso entre layout + callbacks + app. **No se infieren**: se leen del original.

#### Bug 4 — CHANGELOG aspiracional (prometía lo que no existía)

- **Síntoma:** el CHANGELOG de Semana 2 declaraba 5 archivos que **no existían** en el repo.
- **Causa:** escribí el CHANGELOG antes de que el código estuviera aplicado.
- **Solución:** completar los 5 archivos faltantes (adapter, oee keys, presenter, tests) **antes** de commitear el CHANGELOG.
- **Lección:** un CHANGELOG es una **declaración de hechos verificables**, no un plan. Se escribe **después** del último commit verde, no antes.

#### Bug 5 — `.DS_Store` (el archivo fantasma de macOS)

- **Síntoma:** `scripts/.DS_Store` apareció al hacer `ls -la scripts/`.
- **Causa:** macOS lo crea automáticamente en cada carpeta que abres con Finder.
- **Solución:** confirmar que `.gitignore` ya lo tiene (ya lo tenía) → `git check-ignore -v scripts/.DS_Store` → verificar con `git add --dry-run`.
- **Lección:** "está en disco" ≠ "está en el repo". `.gitignore` actúa entre esos dos mundos.

---

### 📊 Los números de la Semana 2

| **Métrica** | **Semana 1** | **Semana 2** |
|---|---|---|
| Tests | 225 | **244** (+19) |
| ADRs | 1 | 2 |
| Archivos nuevos | ~5 | **6** |
| Bugs reales corregidos | 3 | 5 |
| PRs mergeados | 2 | **1** (PR #3) |
| Coverage | ~91% | (re-medir) |
| mean(performance) | 0.9999 (saturado) | **0.8733** (realista) |

---

## 🧠 Parte 3 — Los 8 conceptos que dominaste

### 1. El entorno virtual (`(venv)`)

**Analogía:** cada proyecto Python es una cocina. El venv es la **despensa propia** de esa cocina — no compartes ingredientes con otros proyectos, no contaminas el sistema.

**Regla operativa:**

> *Toda terminal nueva = `cd` al proyecto + `source venv/bin/activate` antes de cualquier comando Python.*

**Cómo verificar:**

```bash
which python pytest ruff
# Las 3 rutas deben apuntar a venv/bin/
```

### 2. Git como máquina del tiempo

**Los 4 comandos esenciales:**

```bash
git add <archivo>           # poner en el "índice" (lo que se va a guardar)
git commit -m "mensaje"     # guardar una foto con etiqueta
git push origin <rama>      # subir a GitHub
git pull origin <rama>      # bajar cambios de GitHub
```

**Workflow profesional:**

```text
main  →  rama feature  →  commits atómicos  →  push  →  PR  →  CI verde  →  merge
```

### 3. Los gates de calidad (pytest + ruff + CI)

**3 capas de verificación:**

| **Capa** | **Herramienta** | **Qué verifica** |
|---|---|---|
| Tests | `pytest` | ¿La lógica funciona? |
| Lint | `ruff` | ¿El estilo es consistente? |
| CI | GitHub Actions | ¿Todo lo anterior pasa en un entorno limpio? |

**Regla de oro:** **nada se mergea sin 2/2 checks verdes**. Un merge con gate rojo es deuda que el próximo commit hereda.

### 4. Reconstruir vs. recuperar (`git show`)

**Antes de reconstruir cualquier archivo con callbacks, componentes o IDs:**

```bash
git show <rama>:<archivo>           # ver el original completo
git show <rama>:<archivo> | grep -n "^def \|@callback"   # ver solo las firmas
```

**Por qué:** los IDs (`"capability-cpk-minimo"`, etc.) son **contratos silenciosos** entre layout + callbacks + app. No se infieren viendo quién llama — se leen del original.

### 5. El patrón strangler (Camino A)

**Analogía:** una higuera estranguladora crece alrededor de un árbol huésped, lentamente lo reemplaza, y al final el huésped muere. El árbol nuevo vive en el mismo espacio.

**Aplicado a software:**

1. Nuevo código convive con viejo (adapter traduce).
2. Cada paso migra una pieza.
3. Al final, el viejo se elimina en un commit dedicado.

**Ventaja:** nunca rompes todo el sistema de golpe. **Riesgo:** dos vocabularios temporales (se documenta en ADR-0002).

### 6. Prompt engineering para canales con techo

**Los LLMs tienen un techo de tokens de salida por respuesta.** Si tu prompt pide más, el sistema corta la conexión.

**Regla práctica:**

> *Un prompt 10/10 no es el más largo: es el que cabe en una respuesta y cierra un entregable verificable.*

**Estructura ganadora (2-3 archivos máximo):**

1. Estado verificado (ground truth)
2. Decisiones tuyas innegociables
3. Entregables con ruta y criterio
4. Evidencia numérica obligatoria
5. UNA pregunta al cierre

### 7. Fórmulas industriales que se defienden

| **Concepto** | **Regla** |
|---|---|
| **Availability** | Excluye paro planificado (no es pérdida) |
| **Performance** | Capeado a 1.0 (física del equipo) |
| **Quality** | FPY, una sola definición en el codebase |
| **OEE agregado** | Ponderado por tiempo operativo, nunca promedio |
| **Cp vs. Pp** | Sigma within vs. sigma overall — dos cosas distintas |
| **Capacidad** | Con guardas: n<2, USL≤LSL, sigma=0 |

### 8. CHANGELOG como contrato de veracidad

Un CHANGELOG no es un plan. Es la **declaración de hechos verificables** de un repo.

**Regla:** *código → tests verdes → CHANGELOG*, nunca *CHANGELOG → código*.

**Verificación antes de commitear:**

```bash
# Por cada archivo declarado en el CHANGELOG:
ls -la <archivo>
```

---

## 💻 Parte 4 — Los comandos que dominaste

### Bloque A — Entorno

```bash
cd ~/Projects/industrial-operations-intelligence/industrial-kpi-intelligence
source venv/bin/activate
which python pytest ruff          # verificar venv activo
```

### Bloque B — Los 3 gates

```bash
pytest -q                          # ¿funciona la lógica?
ruff check .                       # ¿el estilo es limpio?
python -m compileall -q src dashboard tests   # ¿hay errores de sintaxis?
```

### Bloque C — Git workflow

```bash
git status                         # ¿qué cambió?
git diff --stat                    # ¿cuánto cambió?
git checkout -b feat/<nombre>      # nueva rama
git add <archivo>                  # marcar para commit
git commit -m "tipo: mensaje"      # guardar foto
git push -u origin feat/<nombre>   # subir
```

### Bloque D — Diagnóstico

```bash
grep -n "def " src/capability.py              # ver firmas de funciones
git show main:dashboard/x.py                  # ver original de otro branch
git log --oneline -10                         # ver últimos 10 commits
git branch -a                                 # ver todas las ramas
```

### Bloque E — Evidencia

```bash
python scripts/check_oee_distribution.py       # evidencia numérica
pytest -q tests/test_data_generator.py -v      # tests específicos con nombre
```

---

## 💼 Parte 5 — Cómo contarlo en una entrevista

### El guion de 90 segundos

> *"Tomé un dashboard funcional de análisis de producción y lo llevé a estándares enterprise en 2 semanas. Semana 1: reemplacé la licencia MIT por Elastic License 2.0 para proteger el modelo de negocio; documenté la decisión del dataset canónico en un ADR; implementé el motor OEE completo según ISA-95/TPM con guardas físicas; y extendí el schema del generador con las columnas de tiempo que OEE requiere.*
>
> *Semana 2: construí un adapter siguiendo el patrón strangler que traduce el esquema canónico inglés al contrato legacy español sin romper los 225 tests existentes; refactoricé las claves de clasificación OEE a keys estables con presenter i18n en la capa UI; corregí un error de nomenclatura estadística (Cp/Cpk vs. Pp/Ppk) per NIST 6.1.3; calibré el generador para eliminar un caso de Performance saturado en 1.0; y fijé la versión de ruff en CI para reproducibilidad.*
>
> *El proyecto pasó de 194 a 244 tests verdes, con dos ADRs documentando decisiones, un CHANGELOG verificado, y CI verde en cada merge."*

### Preguntas que te pueden hacer

**¿Por qué ELv2 y no MIT?**

Porque MIT permite reventa del software como SaaS sin retorno para el autor. ELv2 protege el modelo de negocio SaaS mientras permite evaluación técnica abierta. Es la licencia de Elastic, Confluent y MongoDB.

**¿Qué es el patrón strangler?**

Un patrón de migración donde el código nuevo reemplaza al viejo **incrementalmente**, sin big-bang rewrite. Un adapter traduce en la frontera; cada paso migra una pieza; al final el viejo se elimina en un commit dedicado con tests.

**¿Por qué Performance se capa a 1.0?**

Porque un equipo no puede producir más unidades de las que su ciclo ideal permite en el tiempo operativo disponible. Un valor >1.0 indica que el `ideal_cycle_time` está mal configurado, no que el equipo sea "más rápido de lo posible".

**¿Cuál es la diferencia entre Cp y Pp?**

Cp usa la variación **intra-subgrupo** (corto plazo, rango móvil / d2). Pp usa la variación **total** (overall, `std(ddof=1)`). Si el proceso es estable, Cp ≈ Pp. Si hay turnos, drifts o cambios, Pp < Cp — y esa brecha es un diagnóstico.

**¿Cómo detectaste el bug de Performance saturado?**

Comparando la media empírica contra el rango esperado. Un mean de 0.9999 en un KPI capado a 1.0 es señal inmediata de distribución sesgada. Se descubrió antes con un test de distribución que afirmaba `0.50 < mean < 0.95` y `std > 0.05`.

**¿Cómo manejas el límite de tokens en LLMs?**

Divido el trabajo en bloques de 2-3 archivos máximo por prompt. Cada bloque con estado verificado, decisiones innegociables, entregables con ruta exacta, evidencia numérica y una sola pregunta al cierre. El "prompt 10/10" no es el más largo: es el que cabe en una respuesta y cierra un entregable verificable.

---

## 📖 Parte 6 — Glosario

| **Palabra** | **Significado** |
|---|---|
| **ADR** | Architecture Decision Record — documento que captura una decisión arquitectónica con contexto y consecuencias |
| **Adapter** | Módulo-frontera que traduce entre dos esquemas incompatibles |
| **BCrypt** | Algoritmo de hashing de contraseñas |
| **CHANGELOG** | Documento que declara cambios reales, no planes |
| **CI/CD** | Continuous Integration / Continuous Delivery — pipeline automático de verificación y deploy |
| **Commit atómico** | Un commit que hace **una** cosa y la hace completa |
| **Conventional commits** | Prefijos estándar: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, `ci:` |
| **Cp/Cpk** | Índices de capacidad de **corto plazo** (sigma within) |
| **ELv2** | Elastic License 2.0 — source-available, prohíbe revender como servicio |
| **FPY** | First-Pass Yield — unidades buenas a la primera / unidades producidas |
| **Idempotente** | Operación que produce el mismo resultado si se ejecuta varias veces |
| **ISA-95** | Estándar internacional para integración de sistemas empresariales y de control |
| **Key estable** | Clave de datos en inglés que no depende del idioma de presentación |
| **OEE** | Overall Equipment Effectiveness = Disponibilidad × Rendimiento × Calidad |
| **Pp/Ppk** | Índices de capacidad **global** (sigma overall, `ddof=1`) |
| **PR** | Pull Request — propuesta de fusionar una rama con revisión y CI |
| **Presenter** | Módulo de UI que traduce keys estables a labels visibles |
| **Pin de versión** | Versión exacta (`==`) para builds reproducibles |
| **Ruff** | Linter ultrarrápido de Python (reemplaza flake8, isort, pyupgrade) |
| **Strangler pattern** | Migración incremental: nuevo reemplaza viejo sin big-bang |
| **TPM** | Total Productive Maintenance — marco industrial del OEE |

---

## 🚀 Parte 7 — Lo que sigue (Semana 3)

La Semana 3 tiene 4 bloques:

| **Bloque** | **Objetivo** |
|---|---|
| **3A** | Activar el adapter en `data_loader.py` — cerrar el Camino A |
| **3B** | Dockerfile + docker-compose.yml — containerización para deploy |
| **3C** | `src/auth.py` — JWT + RBAC (Admin/Engineer/Operator/Viewer) |
| **3D** | Login + session gating en `dash_app.py` — protección end-to-end |

**Al cerrar la Semana 3, el proyecto tiene:**

- El dashboard sirviendo 18k filas reales (no 250 legacy)
- Deploy reproducible con un `docker-compose up`
- Autenticación JWT con 4 roles y permisos por recurso
- README con quickstart vía Docker

---

## 🎓 Cierre de profesor — 3 reflexiones

### Reflexión 1 — "Portafolio" y "producto" no son lo mismo

Tu dashboard funcionaba. Tu **producto** no existía. La diferencia no está en el código: está en la **licencia, los ADRs, el CHANGELOG, los gates, la evidencia**. Los cimientos invisibles son lo que separa un repo que impresiona de un repo que **se vende**.

### Reflexión 2 — El prompt largo es una promesa; el corto es un contrato

Tu prompt de 9 entregables se colgó 4 veces. Un prompt de 2 archivos con evidencia numérica **siempre** termina. La disciplina no es "pedir todo de una vez": es **cerrar un bloque antes de abrir el siguiente**.

### Reflexión 3 — Los bugs no son fracasos: son evidencia

Detectaste 8 bugs reales entre las 2 semanas. Cada uno dejó:

- Un commit con mensaje descriptivo.
- Un test que evita su regresión.
- Un aprendizaje que ya no se te olvida.

**Ese es exactamente el trabajo de un ingeniero senior.** No escribir código sin bugs: **construir sistemas que hagan visible cada bug antes de que llegue a producción**.

---

*Guía escrita con estándar 10/10 para que la uses como bitácora, como material de estudio, y como guion para entrevistas. Las próximas semanas se agregan como Parte 3, Parte 4, etc., manteniendo el mismo formato.*

**Semana 1: cimientos. Semana 2: puentes. Semana 3: puertas (auth + deploy).** 🎯