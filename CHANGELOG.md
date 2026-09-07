# Changelog

Todo lo registrado aquí corresponde a commits reales del repositorio,
verificados con `pytest` y `ruff` en cada paso. No hay entradas
reconstruidas ni inferidas.

## Migración Streamlit → Dash

- Arquitectura Dash completa: `src/` (lógica pura, sin Dash) + `dashboard/`
  (callbacks delgados) + tests por módulo.
- Eliminación completa del código legacy de Streamlit (`app.py` y
  `components/`) una vez alcanzada paridad funcional en Dash.
- `requirements.txt` limpio (sin Streamlit), `pyproject.toml` con
  configuración real de Ruff y pytest.

## Motor de diagnóstico priorizado (`src/diagnostics.py`)

- Combina hotspots de equipo/turno, capacidad de proceso (Cp/Cpk) y
  concentración de Pareto en hallazgos rankeados por severidad
  (PRIORITY / WATCH / INFO).
- Umbrales documentados y calibrados contra el dataset real del
  proyecto (no arbitrarios).
- Panel Dash con resumen ejecutivo automático y tarjetas por hallazgo.

## Capacidad de proceso (Cp/Cpk)

- `src/capability.py` (ya existente) conectado a Dash: selector de
  variable, histograma con LSL/USL/Promedio, clasificación Six Sigma.
- Bug real corregido: `config/quality_config.yaml` no tenía la sección
  `quality.variables_criticas` que el módulo necesitaba — la capacidad
  de proceso devolvía 0 variables hasta corregirlo.

## Control estadístico de proceso (`src/control_charts.py`)

- Carta I-MR (Individuals — Moving Range): límites de control
  calculados desde el rango móvil, detección de puntos fuera de
  control (regla Western Electric #1).
- Complementa a Cp/Cpk: Cp/Cpk mide si el proceso cumple especificación;
  esto mide si el proceso está en control estadístico.

## Análisis operacional con drill-down

- Ranking comparativo por línea/máquina/turno/operador, color-codificado
  con los mismos umbrales del motor de diagnóstico.
- Clic en una barra muestra el detalle (FPY, defectos, causa principal)
  de ese grupo específico.

## Interfaz y experiencia visual

- Tema oscuro "sala de control industrial" (`assets/style.css`),
  aplicado también a las figuras Plotly vía helper compartido
  (`aplicar_tema_oscuro`).
- Navegación por pestañas (Diagnóstico / Calidad / Capacidad / Control /
  Operacional) en vez de scroll largo — filtros globales siempre visibles.
- Pasada de minimalismo: sin degradados decorativos, jerarquía
  tipográfica clara (números grandes, etiquetas discretas).

## Bugs reales encontrados y corregidos (con evidencia)

- **CSS no cargaba**: Dash resolvía `assets/` relativo al módulo
  equivocado — corregido con `assets_folder` explícito.
- **Error de React** ("objects are not valid as a React child"): un
  callback enviaba una figura Plotly completa a la prop `children` de
  un `html.Div` en vez de a la prop `figure` de un `dcc.Graph`.
  Verificado y corregido a nivel de servidor (petición HTTP real al
  endpoint de callback de Dash).
- **"N/D" traducido como "Dakota del Norte"** por el traductor del
  navegador — reemplazado por texto sin ambigüedad ("Sin datos").

## Infraestructura

- CI en GitHub Actions: `ruff check` + `pytest --cov` en cada push.
- Deploy listo para Render (`Procfile`, `render.yaml`, `gunicorn`),
  probado con una petición HTTP real al servidor de producción.

## Estado actual

- **194 tests**, 100% pasando.
- Cobertura ~91% en `src/` y `dashboard/`.
- `ruff check .` limpio.
