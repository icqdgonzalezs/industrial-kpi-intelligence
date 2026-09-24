# app/services/llm_chat.py
"""Servicio de chat con LLM (Groq).

Responsabilidad:
    - Construir el contexto con los KPIs de la DB.
    - Llamar al LLM de Groq vía SDK async.
    - Devolver la respuesta en texto plano + métricas.

No depende de FastAPI ni de la capa HTTP. Recibe KPIs como secuencia
y devuelve un dict. Testeable con mock del cliente Groq.
"""
from __future__ import annotations

import asyncio
import os
import time
from collections.abc import Sequence
from typing import Any

from dotenv import load_dotenv
from groq import AsyncGroq

# Cargar .env una sola vez al importar el módulo
load_dotenv()

# Modelo por defecto (producción en Groq).
# Notas:
#   - "llama-3.3-70b-versatile" y "llama-3.1-8b-instant" fueron deprecados
#     el 2026-08-16. Groq recomienda "openai/gpt-oss-120b" como reemplazo.
#   - Alternativa liviana (menor latencia, menor calidad): "openai/gpt-oss-20b".
MODELO_DEFAULT = "openai/gpt-oss-120b"

# Timeout de la llamada al LLM (segundos)
TIMEOUT_LLM = 10.0

# System prompt: rol, tono y reglas del asistente
SYSTEM_PROMPT = (
    "Eres un asistente experto en operaciones industriales y analítica "
    "de manufactura. Trabajas en una planta de producción y respondes "
    "preguntas sobre los KPIs del sistema.\n\n"
    "Reglas:\n"
    "- Respondé en español, de forma directa y técnica.\n"
    "- Cuando aplique, citá estándares: ISA-95 (OEE), TPM, NIST 6.1.3 "
    "(Pp/Ppk), AIAG SPC (Western Electric).\n"
    "- Si la pregunta no se puede responder con los KPIs disponibles, "
    "decilo explícitamente y sugerí qué dato haría falta.\n"
    "- No inventes valores. Usá solo los KPIs del contexto.\n"
    "- Máximo 3 párrafos cortos."
)

# Cliente singleton (lazy init)
_cliente: AsyncGroq | None = None


def cliente_groq() -> AsyncGroq:
    """Devuelve un cliente Groq singleton.

    Raises:
        RuntimeError: si GROQ_API_KEY no está configurada.
    """
    global _cliente
    if _cliente is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY no configurada. Definila en el archivo .env."
            )
        _cliente = AsyncGroq(api_key=api_key)
    return _cliente


def construir_contexto(kpis: Sequence[Any]) -> str:
    """Formatea una lista de KPIs como texto plano para el prompt.

    Args:
        kpis: Secuencia de objetos con atributos nombre, valor, unidad,
              linea_produccion y timestamp.

    Returns:
        Texto con un KPI por línea, o mensaje si la lista está vacía.
    """
    if not kpis:
        return "(No hay KPIs registrados en el sistema.)"

    lineas = [
        f"- {k.nombre}: {k.valor:.2f} {k.unidad} "
        f"(línea {k.linea_produccion}, {k.timestamp:%Y-%m-%d %H:%M})"
        for k in kpis
    ]
    return "\n".join(lineas)


async def consultar_llm(query: str, kpis: Sequence[Any]) -> dict[str, Any]:
    """Consulta al LLM con el query + contexto de KPIs.

    Args:
        query: Pregunta del usuario en lenguaje natural.
        kpis: Secuencia de KPIs actuales.

    Returns:
        Dict con: respuesta (str), tokens_prompt (int), tokens_completion (int),
        elapsed_ms (int).

    Raises:
        RuntimeError: si la API key no está configurada.
        TimeoutError: si el LLM tarda más de TIMEOUT_LLM segundos.
        groq.APIError: si Groq devuelve un error de API.
    """
    contexto = construir_contexto(kpis)
    user_message = f"KPIs actuales:\n{contexto}\n\nPregunta: {query}"

    cliente = cliente_groq()
    inicio = time.perf_counter()

    async with asyncio.timeout(TIMEOUT_LLM):
        respuesta = await cliente.chat.completions.create(
            model=MODELO_DEFAULT,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.3,
            max_tokens=500,
        )

    elapsed_ms = int((time.perf_counter() - inicio) * 1000)
    eleccion = respuesta.choices[0]
    usage = respuesta.usage

    return {
        "respuesta": eleccion.message.content or "",
        "tokens_prompt": usage.prompt_tokens if usage else 0,
        "tokens_completion": usage.completion_tokens if usage else 0,
        "elapsed_ms": elapsed_ms,
    }
