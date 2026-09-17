# 🎯 Vision — Industrial Operations Intelligence

> 📌 **Propósito:** documento ejecutivo de visión estratégica del ecosistema.
> 📥 **Audiencia:** reclutadores técnicos, clientes potenciales, colaboradores.
> 🗓️ **Última actualización:** Semana 3/8, Fase 4a cerrada.

---

## 🌟 Misión

Dar acceso a las **PYMES manufactureras de Chile y Latinoamérica** a herramientas de inteligencia operacional que hoy solo están disponibles para grandes corporaciones. Empaquetamos **conocimiento industrial profundo** (ISA-95, AIAG SPC, ISO 22005, HACCP) como **software autoinstalable, asequible y alineado con la normativa chilena e internacional**.

**Principio rector:** cada componente del ecosistema debe responder a un problema operacional real, poder defenderse técnicamente y cumplir con los estándares que las auditorías exigen.

---

## 🔥 El problema

Las PyMEs manufactureras chilenas enfrentan una **brecha tecnológica**:

| Desafío | Realidad PyME | Estándar enterprise |
|---|---|---|
| **Trazabilidad** | Excel + papel | SAP MII, Wonderware, Ignition |
| **KPIs de calidad** | Planillas manuales | Power BI + Data Warehouse |
| **Mantenimiento** | Reactivo (falla → arreglo) | Predictivo con IoT + ML |
| **Optimización** | Intuición del operario | Solvers + Digital Twin |
| **Cumplimiento** | Auditorías con carpetas | Sistemas certificados ISO |

**Consecuencias:**
- **Riesgo regulatorio:** D.S. 977 (RSA), Ley 20.606, SAG, FSMA (exportación) exigen trazabilidad completa en <4 horas. Las PyMEs no pueden cumplir con Excel.
- **Pérdida de competitividad:** no pueden exportar a mercados que exigen certificación ISO 22005 / HACCP.
- **Decisiones sin datos:** los supervisores deciden con intuición, no con SPC.

---

## 🏭 El producto: Industrial KPI Intelligence

**¿Qué hace?** Dashboard industrial que calcula KPIs de calidad en tiempo real:
- **FPY** (First Pass Yield), tasas de defectos, scrap, reproceso.
- **Análisis de capacidad** (Pp/Ppk) según AIAG SPC / NIST 6.1.3 / ISO 22514.
- **Control estadístico de proceso** (cartas I-MR, Regla 1 de Western Electric).
- **Pareto 80/20** para priorización de causas.
- **OEE** (Overall Equipment Effectiveness) bajo ISA-95 / TPM.
- **Diagnóstico priorizado** (PRIORITY / WATCH / INFO).

**¿En qué se diferencia?**
- **Estándares industriales reales:** no es un dashboard genérico. Cada métrica cita su norma.
- **Accesibilidad WCAG 2.1:** iconografía no cromática (✓ ⚠ ✕) para operarios daltónicos.
- **ISA-101:** legibilidad a 1-2 m, como exige un HMI industrial.
- **Autoinstalable:** `pip install -r requirements.txt && python -m dashboard.dash_app`.

---

## 🌐 El ecosistema: 6 productos

Roadmap cognitivo: **Registrar → Analyze → Simulate → Predict → Optimize → Decide**

| # | Producto | Pregunta de negocio | Stack principal | Normas aplicables | Estado |
|:---:|---|---|---|---|:---:|
| **00** | **Industrial Traceability Intelligence** | ¿De dónde vino? | FastAPI · SQLModel · Jinja2 · python-barcode | **ISO 22005 · NCh 2983 · D.S. 977 (RSA) · Ley 20.606 · HACCP · GS1 · SAG** | 🆕 Propuesto |
| **01** | **Industrial KPI Intelligence** | ¿Qué está ocurriendo? | Python · Dash · pytest · GH Actions | **ISA-95 · AIAG SPC · NIST 6.1.3 · ISO 22514 · ISA-101 · WCAG 2.1** | ✅ |
| **02** | **Production Digital Twin** | ¿Qué podría ocurrir? | Python · SimPy · NumPy | **ISO 9001 · NCh 2728 · ISA-95 · TPM** | ✅ |
| **03** | **Predictive Maintenance Intelligence** | ¿Qué podría fallar? | Python · Scikit-learn · SQL | **ISO 55000 / NCh-ISO 55001 · EN 13306 · TPM · ISO 10816** | 🚧 |
| **04** | **Industrial Process Optimizer** | ¿Cuál es la mejor alternativa? | Python · SciPy · OR-Tools | **ISO 9001 · NCh 2728 · ISO 50001 · Ley 21.305** | 🚧 |
| **05** | **Industrial AI Copilot** | ¿Qué debería investigar o decidir? | Python · LLM · RAG | **Ley 19.628 · Ley 21.719 · ISO/IEC 27001 · ISO/IEC 42001** | 🚧 |

### Detalle por producto

#### 00 · Industrial Traceability Intelligence

- **Foco:** trazabilidad end-to-end: recepción → proceso → calidad → paletizado → despacho.
- **MVP inicial:** vertical agroindustrial (fruta), cliente real validado.
- **Arquitectura:** núcleo genérico + verticales por industria (agro, pharma, automotriz).
- **Funcionalidades:** genealogía de lotes, recall/recal, etiquetas GS1 DataMatrix, roles por área.
- **Normativa chilena:** NCh 2983:2011 (adopción de ISO 22005:2007), D.S. 977 (RSA), Ley 20.606 (etiquetado), SAG (exportación frutícola), HACCP.
- **Normativa internacional:** GS1 (GTIN, SSCC, GS1-128), FSMA (FDA, si exporta a EE.UU.), Reglamento UE 178/2002.

#### 01 · Industrial KPI Intelligence

- **Foco:** KPIs de calidad, capacidad, SPC, OEE.
- **Normativa:** ISA-95, AIAG SPC, NIST 6.1.3, ISO 22514, ISA-101, WCAG 2.1.
- **Normativa chilena:** aplicable como herramienta de control interno para auditorías ISO 9001 / NCh 2728.

#### 02 · Production Digital Twin

- **Foco:** simulación de línea, cuellos de botella, análisis what-if.
- **Stack:** SimPy (eventos discretos), NumPy.
- **Normativa:** ISO 9001, NCh 2728, ISA-95, TPM.

#### 03 · Predictive Maintenance Intelligence

- **Foco:** predecir fallas. RUL (Remaining Useful Life).
- **Stack:** Scikit-learn, SQL, integración IoT.
- **Normativa:** ISO 55000 / NCh-ISO 55001, EN 13306, ISO 10816, TPM.

#### 04 · Industrial Process Optimizer

- **Foco:** encontrar la mejor configuración de proceso.
- **Stack:** SciPy, OR-Tools.
- **Normativa:** ISO 9001, NCh 2728, ISO 50001, Ley 21.305.

#### 05 · Industrial AI Copilot

- **Foco:** asistente inteligente que sugiere qué investigar o decidir.
- **Stack:** LLM + RAG sobre datos de planta.
- **Normativa:** Ley 19.628, Ley 21.719 (vigencia Dic 2026), ISO/IEC 27001, ISO/IEC 42001.

---

## 🎯 Mercado objetivo

| Segmento | Descripción | Productos prioritarios |
|---|---|---|
| **Foco inicial** | PyMEs agroindustriales (fruta, alimentos) de Chile | 00 + 01 |
| **Fase 2** | PyMEs manufactureras generales (LatAm/España) | 01 + 02 + 03 |
| **Fase 3** | Medianas empresas (200-1000 empleados) | Los 6 productos |
| **Fase 4** | Exportación a mercados regulados (UE, EE.UU.) | 00 + 05 |

**Canal inicial:** venta directa + LinkedIn. El cliente agroindustrial que pidió trazabilidad es el **primer caso de éxito**.

---

## 💡 Diferenciación

1. **Conocimiento industrial real.** No es un dashboard genérico: cada métrica cita su norma.
2. **Cumplimiento normativo chileno.** Diseñado para auditorías SAG, D.S. 977, Ley 20.606, NCh 2728.
3. **Autoinstalable y asequible.** Sin consultoría de $50.000 USD. Sin SAP. `pip install` y funciona.
4. **Accesibilidad y usabilidad.** WCAG 2.1, ISA-101, iconografía no cromática.
5. **Licenciamiento justo.** Elastic License 2.0: leer, correr y aprender. No revender como SaaS competidor.
6. **Ecosistema coherente.** 6 productos que cubren el ciclo operacional completo.

---

## 🗺️ Roadmap estratégico

| Fase | Productos | Hito | Estado |
|:---:|---|---|:---:|
| **1** | 01 | KPI Intelligence MVP, 390 tests, CI verde | ✅ |
| **2** | 00 | Traceability MVP para cliente agro | 🆕 En diseño |
| **3** | 02 + 03 | Digital Twin + Predictive Maintenance | 🚧 |
| **4** | 04 + 05 | Process Optimizer + AI Copilot | 🚧 |
| **5** | Todos | Ecosistema integrado + API unificada | ⏳ |

---

## 📊 Métricas de éxito por fase

| Fase | Métrica | Meta |
|:---:|---|---|
| 1 | Tests verdes | 390 |
| 1 | CI | 2/2 verde |
| 2 | Cliente agro validado | 1 caso de éxito |
| 2 | Trazabilidad completa | <4 horas (exigencia regulatoria) |
| 2 | Etiquetas GS1 | 100% compatibles |
| 3 | RUL (predicción de fallas) | >80% precisión |
| 4 | Reducción consumo energético | 10-30% |
| 5 | Ecosistema integrado | API unificada |

---

## 📚 Normativa aplicable (resumen ejecutivo)

| Norma | Ámbito | Productos |
|---|---|---|
| **ISA-95** | Jerarquía de planta industrial | 01, 02, 03, 00 |
| **AIAG SPC** | Control estadístico de proceso | 01 |
| **NIST 6.1.3 / ISO 22514** | Capacidad de proceso (Pp/Ppk) | 01 |
| **ISA-101** | HMI industrial | 01 |
| **WCAG 2.1** | Accesibilidad web | 01, 05, 00 |
| **ISO 22005 / NCh 2983** | Trazabilidad alimentaria | 00 |
| **D.S. 977 (RSA)** | Reglamento Sanitario de Alimentos | 00 |
| **Ley 20.606** | Etiquetado nutricional | 00 |
| **HACCP** | Puntos críticos de control | 00 |
| **GS1** | Barcodes (GTIN, SSCC, DataMatrix) | 00 |
| **ISO 55000 / NCh-ISO 55001** | Gestión de activos | 03 |
| **EN 13306** | Terminología de mantenimiento | 03 |
| **ISO 9001 / NCh 2728** | Gestión de calidad | 02, 03, 04 |
| **ISO 50001** | Eficiencia energética | 04 |
| **Ley 21.305** | Eficiencia energética Chile | 04 |
| **Ley 19.628** | Protección de datos personales | 05 |
| **Ley 21.719** | Nueva Ley de Protección de Datos | 05 |
| **ISO/IEC 27001** | Seguridad de la información | 05 |
| **ISO/IEC 42001** | Gestión de IA | 05 |

---

> 📌 **Fin del VISION.md.**
> Próxima actualización: cuando se cierre el MVP de Trazabilidad (Producto 00).
