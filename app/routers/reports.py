"""Router del reporte ejecutivo narrado por LLM (IA.3).

Responsabilidad:
    - Recibir la petición (línea + rango temporal) vía HTMX o JSON.
    - Verificar autenticación (JWT).
    - Aplicar rate limit (30/min por IP).
    - Cargar dataset filtrado + config de calidad.
    - Calcular KPIs ejecutivos (OEE + operacional + top defectos).
    - Delegar la narración al service ``llm_reports``.
    - Renderizar HTML parcial (HTMX) o JSON (API), según HX-Request.

No contiene lógica de IA ni de dominio: eso vive en ``app/services/``
y ``src/``.
"""
from __future__ import annotations

import logging
from datetime import date
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from app.auth import get_current_user
from app.limiter import rate_limit
from app.models import User
from app.services.dataset_loader import cargar_dataset_filtrado
from app.services.executive_kpis import calcular_kpis_ejecutivos
from app.services.llm_reports import generar_reporte_ejecutivo
from app.templates_config import templates

logger = logging.getLogger(__name__)

def _limpiar(v: str | None) -> str | None:
    """HTMX envía inputs vacíos como ``""``. Los normalizamos a ``None``.

    Ver decisión IA.3: los filtros opcionales deben comportarse igual
    si el cliente omite el campo o lo envía vacío.
    """
    return v or None


def _parsear_fecha(v: str | None) -> date | None:
    """Parsea fecha ISO desde query param. ``""``/``None`` → ``None``."""
    if not v:
        return None
    try:
        return date.fromisoformat(v)
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=f"Fecha inválida: {v!r}. Esperado formato ISO 8601 (YYYY-MM-DD).",
        ) from None

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/executive")
@rate_limit(max_requests=30, window_seconds=60)
async def reports_executive(
    request: Request,
    linea: str | None = None,
    desde: str | None = None,
    hasta: str | None = None,
    current_user: Annotated[User, Depends(get_current_user)] = None,  # noqa: ARG001
) -> Response:
    """Reporte ejecutivo narrado por LLM a partir de KPIs agregados.

    Protegido con JWT. Rate limit: 30 req/min por IP.

    Query params (todos opcionales):
        linea: identificador de línea (ej. "L1"). ``None`` = todas.
        desde: fecha inferior inclusiva (ISO 8601). ``None`` = sin cota.
        hasta: fecha superior inclusiva (ISO 8601). ``None`` = sin cota.
    """
    # HTMX envía inputs vacíos como "". Normalizamos a None.
    linea = _limpiar(linea)
    if linea is not None and len(linea) > 10:
        raise HTTPException(
            status_code=422,
            detail="'linea' excede 10 caracteres.",
        )

    desde_date = _parsear_fecha(desde)
    hasta_date = _parsear_fecha(hasta)

    if desde_date is not None and hasta_date is not None and desde_date > hasta_date:
        raise HTTPException(
            status_code=422,
            detail="El rango es inválido: 'desde' debe ser <= 'hasta'.",
        )

    df, _config = cargar_dataset_filtrado(linea=linea, desde=desde_date, hasta=hasta_date)

    contexto: dict[str, Any] = {
        "linea": linea,
        "desde": desde_date.isoformat() if desde_date else None,
        "hasta": hasta_date.isoformat() if hasta_date else None,
        "n_lotes": int(len(df)),
    }

    if df.empty:
        return _respuesta(
            request,
            ok=False,
            error="No hay datos para los filtros seleccionados.",
            kpis={},
            reporte="",
            contexto=contexto,
        )

    try:
        kpis = calcular_kpis_ejecutivos(df)
    except ValueError as exc:
        logger.warning("Dataset incompatible con KPIs ejecutivos: %s", exc)
        return _respuesta(
            request,
            ok=False,
            error=f"Datos no compatibles con el análisis: {exc}",
            kpis={},
            reporte="",
            contexto=contexto,
        )

    try:
        resultado = await generar_reporte_ejecutivo(kpis, contexto)
    except TimeoutError:
        return _respuesta(
            request,
            ok=False,
            error="El reporte tardó demasiado. Reintentá en unos segundos.",
            kpis=kpis,
            reporte="",
            contexto=contexto,
        )
    except RuntimeError as exc:
        return _respuesta(
            request,
            ok=False,
            error=f"Configuración del asistente incompleta: {exc}",
            kpis=kpis,
            reporte="",
            contexto=contexto,
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Error inesperado en el reporte ejecutivo")
        return _respuesta(
            request,
            ok=False,
            error=f"Error inesperado del asistente ({type(exc).__name__}).",
            kpis=kpis,
            reporte="",
            contexto=contexto,
        )

    return _respuesta(
        request,
        ok=True,
        error="",
        kpis=kpis,
        reporte=resultado["respuesta"],
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
    kpis: dict[str, Any],
    reporte: str,
    contexto: dict[str, Any],
) -> Response:
    """Renderiza HTML parcial (HTMX) o JSON (API) según el header."""
    payload: dict[str, Any] = {
        "ok": ok,
        "kpis": kpis,
        "meta": contexto,
    }
    if ok:
        payload["reporte"] = reporte
    else:
        payload["error"] = error

    if request.headers.get("HX-Request") == "true":
        return templates.TemplateResponse(
            request=request,
            name="partials/_reports_executive_response.html",
            context=payload,
        )
    return JSONResponse(payload)
