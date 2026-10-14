"""Router del diagnóstico asistido por LLM (IA.2).

Responsabilidad:
    - Recibir la petición (línea + rango temporal) vía HTMX o JSON.
    - Verificar autenticación (JWT).
    - Aplicar rate limit (30/min por IP).
    - Cargar dataset filtrado + config de calidad.
    - Calcular capacidad de proceso (Pp/Ppk).
    - Generar findings priorizados con ``src.diagnostics``.
    - Delegar la narración al service ``llm_diagnostics``.
    - Renderizar HTML parcial (HTMX) o JSON (API), según HX-Request.

No contiene lógica de IA ni de dominio: eso vive en ``app/services/``
y ``src/``.
"""
from __future__ import annotations

import logging
from datetime import date
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from fastapi.responses import JSONResponse

from app.auth import get_current_user
from app.limiter import rate_limit
from app.models import User
from app.services.dataset_loader import cargar_dataset_filtrado
from app.services.llm_diagnostics import diagnosticar
from app.templates_config import templates
from src.capability import resumen_capacidad
from src.diagnostics import generar_diagnostico

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/diagnostics", tags=["diagnostics"])


@router.get("/ai")
@rate_limit(max_requests=30, window_seconds=60)
async def diagnostics_ai(
    request: Request,
    linea: Annotated[str | None, Query(min_length=1, max_length=10)] = None,
    desde: Annotated[date | None, Query()] = None,
    hasta: Annotated[date | None, Query()] = None,
    current_user: Annotated[User, Depends(get_current_user)] = None,  # noqa: ARG001
) -> Response:
    """Diagnóstico narrado por LLM a partir de los findings priorizados.

    Protegido con JWT. Rate limit: 30 req/min por IP.

    Query params (todos opcionales):
        linea: identificador de línea (ej. "L1"). ``None`` = todas.
        desde: fecha inferior inclusiva (ISO 8601). ``None`` = sin cota.
        hasta: fecha superior inclusiva (ISO 8601). ``None`` = sin cota.
    """
    if desde is not None and hasta is not None and desde > hasta:
        raise HTTPException(
            status_code=422,
            detail="El rango es inválido: 'desde' debe ser <= 'hasta'.",
        )

    df, config = cargar_dataset_filtrado(linea=linea, desde=desde, hasta=hasta)

    contexto: dict[str, Any] = {
        "linea": linea,
        "desde": desde.isoformat() if desde else None,
        "hasta": hasta.isoformat() if hasta else None,
        "n_lotes": int(len(df)),
    }

    if df.empty:
        return _respuesta(
            request,
            ok=False,
            error="No hay datos para los filtros seleccionados.",
            findings=[],
            diagnostico="",
            contexto=contexto,
        )

    # Generación de findings priorizados (determinista, en src/).
    try:
        variables_config = config.get("quality", {}).get("variables_criticas") or {}
        capacidad_df = resumen_capacidad(df, variables_config) if variables_config else None
        findings_df = generar_diagnostico(df, capacidad=capacidad_df)
        findings = findings_df.to_dict("records")
    except ValueError as exc:
        logger.warning("Dataset incompatible con diagnóstico: %s", exc)
        return _respuesta(
            request,
            ok=False,
            error=f"Datos no compatibles con el análisis: {exc}",
            findings=[],
            diagnostico="",
            contexto=contexto,
        )

    # Narración vía LLM (async, con timeout y manejo de errores).
    try:
        resultado = await diagnosticar(findings, contexto)
    except TimeoutError:
        return _respuesta(
            request,
            ok=False,
            error="El diagnóstico tardó demasiado. Reintentá en unos segundos.",
            findings=findings,
            diagnostico="",
            contexto=contexto,
        )
    except RuntimeError as exc:
        return _respuesta(
            request,
            ok=False,
            error=f"Configuración del asistente incompleta: {exc}",
            findings=findings,
            diagnostico="",
            contexto=contexto,
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Error inesperado en el diagnóstico")
        return _respuesta(
            request,
            ok=False,
            error=f"Error inesperado del asistente ({type(exc).__name__}).",
            findings=findings,
            diagnostico="",
            contexto=contexto,
        )

    return _respuesta(
        request,
        ok=True,
        error="",
        findings=findings,
        diagnostico=resultado["respuesta"],
        contexto={
            **contexto,
            "modelo": resultado["modelo"],
            "tokens_prompt": resultado["tokens_prompt"],
            "tokens_completion": resultado["tokens_completion"],
            "elapsed_ms": resultado["elapsed_ms"],
        },
    )


def _respuesta(
    request: Request,
    *,
    ok: bool,
    error: str,
    findings: list[dict[str, Any]],
    diagnostico: str,
    contexto: dict[str, Any],
) -> Response:
    """Renderiza HTML parcial (HTMX) o JSON (API) según el header."""
    payload: dict[str, Any] = {
        "ok": ok,
        "findings": findings,
        "meta": contexto,
    }
    if ok:
        payload["diagnostico"] = diagnostico
    else:
        payload["error"] = error

    if request.headers.get("HX-Request") == "true":
        return templates.TemplateResponse(
            request=request,
            name="partials/_diagnostics_ai_response.html",
            context=payload,
        )
    return JSONResponse(payload)
