"""Servicio de diagnóstico asistido por LLM (IA.2).

Toma los findings priorizados de ``src.diagnostics.generar_diagnostico``
y los narra en lenguaje natural vía Groq. No contiene lógica HTTP ni
accede a la DB: recibe datos ya preparados y devuelve texto + métricas.

Diseño:
    - Reutiliza el cliente Groq singleton, el modelo y el timeout de
      ``app.services.llm_chat`` (SSOT para configuración del LLM).
    - ``construir_prompt`` es puro y determinista: testeable sin Groq.
    - ``diagnosticar`` hace la llamada async y devuelve dict con métricas.

Rol del LLM: ingeniero senior de procesos (distinto al de chat, que es
un asistente de KPIs). El chat conversa; el diagnóstico prescribe.
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

# System prompt: rol de ingeniero senior + estructura fija de respuesta.
# Distinto al SYSTEM_PROMPT de chat por diseño (ver docstring del módulo).
SYSTEM_PROMPT = (
    "Eres un ingeniero senior de procesos con 20 años de experiencia en "
    "manufactura discreta y continua. Analizas hallazgos priorizados de "
    "un panel de diagnóstico industrial y producís recomendaciones "
    "accionables para el jefe de planta.\n\n"
    "Reglas:\n"
    "- Respondé en español, directo y técnico.\n"
    "- Estructurá la respuesta en 3 secciones: (1) Qué está pasando, "
    "(2) Por qué importa, (3) Qué hacer primero.\n"
    "- Citá estándares cuando aplique: ISA-95 (OEE), TPM, "
    "NIST 6.1.3 / ISO 22514 (Pp/Ppk), AIAG SPC (Western Electric).\n"
    "- Si hay hallazgos con severidad PRIORITY, empezá por ellos.\n"
    "- No inventes valores. Usá solo los hallazgos del contexto.\n"
    "- Máximo 4 párrafos cortos."
)

# Orden canónico de severidad. Debe coincidir con
# ``src.diagnostics.SEVERIDAD_ORDEN`` para que el prompt refleje el
# mismo criterio de priorización que el panel visual.
_ORDEN_SEVERIDAD = {"PRIORITY": 0, "WATCH": 1, "INFO": 2}


def _formatear_findings(findings: list[dict[str, Any]]) -> str:
    """Formatea findings como texto plano, ordenados por severidad + score.

    Determinista: aplica ``sorted`` explícito para no depender del orden
    de iteración del input.

    Args:
        findings: Lista de hallazgos con keys severidad, categoria,
            titulo, mensaje, score.

    Returns:
        Texto con un hallazgo por bloque, o mensaje si la lista está vacía.
    """
    if not findings:
        return "(No se detectaron hallazgos que ameriten atención.)"

    ordenados = sorted(
        findings,
        key=lambda f: (
            _ORDEN_SEVERIDAD.get(str(f.get("severidad", "INFO")), 99),
            -float(f.get("score", 0.0)),
        ),
    )

    bloques = [
        f"[{f.get('severidad', '?')}] {f.get('titulo', '?')}\n"
        f"    {f.get('mensaje', '')}"
        for f in ordenados
    ]
    return "\n".join(bloques)


def construir_prompt(
    findings: list[dict[str, Any]],
    contexto: dict[str, Any],
) -> tuple[str, str]:
    """Construye (system_prompt, user_prompt). Función pura.

    Args:
        findings: Lista de hallazgos priorizados de
            ``src.diagnostics.generar_diagnostico``.
        contexto: Dict con keys opcionales: linea, desde, hasta, n_lotes.

    Returns:
        Tupla (system_prompt, user_prompt) lista para Groq.
    """
    linea = contexto.get("linea") or "todas las líneas"
    desde = contexto.get("desde") or "sin cota inferior"
    hasta = contexto.get("hasta") or "sin cota superior"
    n_lotes = int(contexto.get("n_lotes", 0))

    cuerpo = _formatear_findings(findings)

    user = (
        f"Contexto de producción:\n"
        f"- Línea: {linea}\n"
        f"- Período: {desde} a {hasta}\n"
        f"- Lotes analizados: {n_lotes}\n\n"
        f"Hallazgos priorizados del panel de diagnóstico:\n"
        f"{cuerpo}\n\n"
        f"Tarea: producí un diagnóstico narrado para el jefe de planta. "
        f"Seguí la estructura de 3 secciones (qué está pasando / por qué "
        f"importa / qué hacer primero)."
    )
    return SYSTEM_PROMPT, user


async def diagnosticar(
    findings: list[dict[str, Any]],
    contexto: dict[str, Any],
) -> dict[str, Any]:
    """Llama a Groq y devuelve el diagnóstico narrado + métricas.

    Args:
        findings: Lista de hallazgos priorizados.
        contexto: Dict con linea, desde, hasta, n_lotes.

    Returns:
        Dict con: respuesta (str), tokens_prompt (int),
        tokens_completion (int), elapsed_ms (int), modelo (str).

    Raises:
        RuntimeError: si ``GROQ_API_KEY`` no está configurada.
        TimeoutError: si el LLM tarda más de ``TIMEOUT_LLM`` segundos.
        groq.APIError: si Groq devuelve un error de API.
    """
    system, user = construir_prompt(findings, contexto)
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
            max_tokens=800,
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