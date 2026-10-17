"""Servicio de reportes ejecutivos narrados por LLM (IA.3).

Toma los KPIs agregados de ``app.services.executive_kpis`` y los narra
en lenguaje natural vía Groq con tono ejecutivo (CFO/COO), no operativo.

Diseño (consistente con ``llm_diagnostics.py``):
    - Reutiliza cliente Groq singleton, modelo y timeout de
      ``app.services.llm_chat`` (SSOT para configuración del LLM).
    - ``construir_prompt_ejecutivo`` es puro y determinista: testeable
      sin Groq.
    - ``generar_reporte_ejecutivo`` hace la llamada async.

Diferencia clave con IA.2:
    - IA.2 (diagnóstico)  → audiencia: jefe de planta. Tono técnico.
      Cita Cp/Ppk/UCL. Estructura: qué pasa / por qué importa / qué hacer.
    - IA.3 (reporte)      → audiencia: CFO/COO. Tono de negocio.
      Traduce a impacto: pts de OEE, % scrap como costo, PPM como proxy
      de satisfacción. Estructura: titular / drivers / recomendación.

Regla anti-alucinación: el prompt instruye a usar EXCLUSIVAMENTE los
valores del contexto. Si falta un KPI, el LLM debe decir "sin dato".
"""
from __future__ import annotations

import asyncio
import time
from typing import Any

from app.services.llm_chat import (
    MODELO_DEFAULT,
    TIMEOUT_LLM,
    cliente_groq,
)

# System prompt: rol ejecutivo + estructura fija + anti-alucinación.
# Distinto al SYSTEM_PROMPT de chat y de diagnostics por diseño.
SYSTEM_PROMPT = (
    "Eres un analista senior de operaciones industriales que reporta "
    "directamente al CFO y COO de una manufacturera. Tu trabajo es "
    "traducir métricas de planta a implicancias de negocio: costo, "
    "capacidad, riesgo operacional.\n\n"
    "Reglas:\n"
    "- Respondé en español, tono ejecutivo. No operativo-técnico.\n"
    "- Estructurá la respuesta en 3 secciones: "
    "(1) Titular, (2) Drivers, (3) Recomendación.\n"
    "- Longitud: 250-400 palabras. Una página como máximo.\n"
    "- Traducí métricas a impacto de negocio: puntos de OEE, % de scrap "
    "como costo de calidad, PPM como proxy de satisfacción de cliente.\n"
    "- Citá estándares solo si aportan al ejecutivo: TPM (OEE), "
    "ISO 22514 (capacidad). No cites ISA-95 ni AIAG SPC en un reporte "
    "ejecutivo: son ruido para esta audiencia.\n"
    "- Usá EXCLUSIVAMENTE los valores numéricos provistos en el bloque "
    "'KPIs del período'. Si un dato no está, decí 'sin dato'. "
    "No inventes cifras ni tendencias.\n"
    "- No propongas acciones que requieran datos que no tenés."
)


def _formatear_kpis(kpis: dict[str, Any]) -> str:
    """Formatea el dict de KPIs como texto plano para el prompt.

    Determinista: no usa timestamps ni ordenamiento implícito.
    Maneja dicts vacíos con defaults seguros (nunca KeyError).
    """
    oee = kpis.get("oee", {})
    op = kpis.get("operacional", {})
    top = kpis.get("top_defectos", [])

    lineas: list[str] = [
        "### OEE agregado (TPM)",
        f"- OEE: {float(oee.get('oee', 0.0)):.4f} "
        f"(clasificación: {oee.get('clasificacion', 'sin dato')})",
        f"- Disponibilidad: {float(oee.get('disponibilidad', 0.0)):.4f}",
        f"- Rendimiento: {float(oee.get('rendimiento', 0.0)):.4f}",
        f"- Calidad: {float(oee.get('calidad', 0.0)):.4f}",
        "",
        "### Operacional",
        f"- FPY (First Pass Yield): {float(op.get('fpy', 0.0)):.4f}",
        f"- Tasa de defectos: {float(op.get('tasa_defectos', 0.0)):.4f}",
        f"- Tasa de scrap: {float(op.get('tasa_scrap', 0.0)):.4f}",
        f"- Tasa de reproceso: {float(op.get('tasa_reproceso', 0.0)):.4f}",
        f"- PPM (partes por millón): {float(op.get('ppm', 0.0)):.1f}",
        f"- Unidades producidas: {int(op.get('total_producidas', 0))}",
        f"- Unidades defectuosas: {int(op.get('total_defectuosas', 0))}",
        "",
        "### Top defectos por frecuencia",
    ]

    if top:
        for i, d in enumerate(top, 1):
            lineas.append(
                f"{i}. {d.get('defecto', '?')}: "
                f"{int(d.get('frecuencia', 0))} unidades "
                f"({float(d.get('porcentaje', 0.0)):.2f}% del total)"
            )
    else:
        lineas.append("(sin defectos registrados en el período)")

    return "\n".join(lineas)


def construir_prompt_ejecutivo(
    kpis: dict[str, Any],
    contexto: dict[str, Any],
) -> tuple[str, str]:
    """Construye (system_prompt, user_prompt) para el reporte ejecutivo.

    Función pura: mismo input → mismo output.

    Args:
        kpis: Dict de ``app.services.executive_kpis.calcular_kpis_ejecutivos``.
        contexto: Dict con keys opcionales: linea, desde, hasta, n_lotes.

    Returns:
        Tupla (system_prompt, user_prompt) lista para Groq.
    """
    linea = contexto.get("linea") or "todas las líneas"
    desde = contexto.get("desde") or "sin cota inferior"
    hasta = contexto.get("hasta") or "sin cota superior"
    n_lotes = int(contexto.get("n_lotes", 0))

    cuerpo = _formatear_kpis(kpis)

    user = (
        f"Contexto de producción:\n"
        f"- Línea: {linea}\n"
        f"- Período: {desde} a {hasta}\n"
        f"- Registros analizados: {n_lotes}\n\n"
        f"KPIs del período:\n"
        f"{cuerpo}\n\n"
        f"Tarea: producí un reporte ejecutivo de una página para el CFO "
        f"y el COO. Seguí la estructura de 3 secciones (Titular / Drivers "
        f"/ Recomendación). Traducí los números a impacto de negocio."
    )
    return SYSTEM_PROMPT, user


async def generar_reporte_ejecutivo(
    kpis: dict[str, Any],
    contexto: dict[str, Any],
) -> dict[str, Any]:
    """Llama a Groq y devuelve el reporte narrado + métricas.

    Args:
        kpis: KPIs agregados del período.
        contexto: Dict con linea, desde, hasta, n_lotes.

    Returns:
        Dict con: respuesta (str), tokens_prompt (int),
        tokens_completion (int), elapsed_ms (int), modelo (str).

    Raises:
        RuntimeError: si ``GROQ_API_KEY`` no está configurada.
        TimeoutError: si el LLM tarda más de ``TIMEOUT_LLM`` segundos.
        groq.APIError: si Groq devuelve un error de API.
    """
    system, user = construir_prompt_ejecutivo(kpis, contexto)
    cliente = cliente_groq()
    inicio = time.perf_counter()

    async with asyncio.timeout(TIMEOUT_LLM):
        respuesta = await cliente.chat.completions.create(
            model=MODELO_DEFAULT,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.2,
            max_tokens=900,
        )

    elapsed_ms = int((time.perf_counter() - inicio) * 1000)
    eleccion = respuesta.choices[0]
    usage = respuesta.usage

    return {
        "respuesta": eleccion.message.content or "",
        "tokens_prompt": usage.prompt_tokens if usage else 0,
        "tokens_completion": usage.completion_tokens if usage else 0,
        "elapsed_ms": elapsed_ms,
        "modelo": MODELO_DEFAULT,
    }
