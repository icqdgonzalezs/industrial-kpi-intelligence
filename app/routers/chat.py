# app/routers/chat.py
"""Router del chat con LLM (Groq).

Responsabilidad:
    - Recibir la consulta del usuario vía HTMX (form-urlencoded).
    - Verificar autenticación (JWT).
    - Cargar los KPIs desde SQLite.
    - Delegar al service `consultar_llm`.
    - Renderizar un HTML parcial con la respuesta.

No contiene lógica de IA: eso vive en `app/services/llm_chat.py`.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from app.auth import get_current_user
from app.db import get_session
from app.models import KPI, User
from app.services.llm_chat import consultar_llm
from app.templates_config import templates

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_class=HTMLResponse)
async def chat(
    request: Request,
    query: Annotated[str, Form(min_length=1, max_length=500)],
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> HTMLResponse:
    """Endpoint del chat: recibe query, consulta al LLM, devuelve HTML parcial.

    Protegido con JWT (Depends(get_current_user)). Sin token válido → 401.

    HTMX envía el form como `application/x-www-form-urlencoded`, por eso
    usamos `Form(...)` en vez de un BaseModel Pydantic.

    Siempre devuelve 200 con un parcial HTML. El estado de error va en el
    template, no en el status code (más simple para HTMX).
    """
    kpis = session.exec(select(KPI)).all()

    try:
        resultado = await consultar_llm(query, kpis)
        contexto: dict[str, object] = {
            "ok": True,
            "query": query,
            "respuesta": resultado["respuesta"],
            "tokens": resultado["tokens_prompt"] + resultado["tokens_completion"],
            "elapsed_ms": resultado["elapsed_ms"],
        }
    except TimeoutError:
        contexto = {
            "ok": False,
            "query": query,
            "error": "El asistente tardó demasiado en responder. Reintentá.",
        }
    except RuntimeError as exc:
        # Típicamente GROQ_API_KEY no configurada
        contexto = {
            "ok": False,
            "query": query,
            "error": f"Configuración del asistente incompleta: {exc}",
        }
    except Exception as exc:  # noqa: BLE001
        # Red de seguridad: cualquier error inesperado del SDK de Groq
        contexto = {
            "ok": False,
            "query": query,
            "error": f"Error inesperado del asistente ({type(exc).__name__}).",
        }

    return templates.TemplateResponse(
        request=request,
        name="partials/_chat_response.html",
        context=contexto,
    )
