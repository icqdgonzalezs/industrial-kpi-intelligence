# app/limiter.py
"""Rate limiting simple basado en ventana deslizante en memoria.

Reemplaza a slowapi: el decorador nativo de slowapi no enforza el
límite en este entorno (FastAPI/Starlette custom). Una implementación
mínima con `deque` de timestamps es más confiable y testeable.

Limitaciones conocidas:
    - Estado en memoria → no compartido entre workers. Con uvicorn
      single-worker (Railway default) es suficiente.
    - La clave incluye IP + nombre del endpoint.

Uso:
    from app.limiter import rate_limit

    @router.post("/chat/")
    @rate_limit(max_requests=30, window_seconds=60)
    async def chat(request: Request, ...): ...
"""
from __future__ import annotations

import functools
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable
from time import monotonic
from typing import Any

from fastapi import HTTPException, Request, status

# Contadores por clave. defaultdict para no inicializar manualmente.
_HITS: dict[str, deque[float]] = defaultdict(deque)


def rate_limit(
    max_requests: int, window_seconds: int
) -> Callable[..., Any]:
    """Decorador de rate limiting con ventana deslizante.

    Args:
        max_requests: Cantidad máxima de requests en la ventana.
        window_seconds: Tamaño de la ventana en segundos.

    Raises:
        HTTPException 429: si se supera el límite dentro de la ventana.
    """
    def decorator(
        func: Callable[..., Awaitable[Any]],
    ) -> Callable[..., Awaitable[Any]]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Localizar el Request. FastAPI lo pasa como kwarg.
            request: Request | None = kwargs.get("request")
            if request is None:
                for a in args:
                    if isinstance(a, Request):
                        request = a
                        break
            if request is None:
                # Sin request no podemos limitar. Dejamos pasar (no
                # debería ocurrir con FastAPI + firma correcta).
                return await func(*args, **kwargs)

            client_ip = request.client.host if request.client else "unknown"
            key = f"{client_ip}:{func.__qualname__}"
            now = monotonic()
            hits = _HITS[key]

            # Descartar hits fuera de la ventana.
            while hits and now - hits[0] > window_seconds:
                hits.popleft()

            if len(hits) >= max_requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=(
                        f"Demasiadas solicitudes. "
                        f"Límite: {max_requests} cada {window_seconds}s."
                    ),
                )

            hits.append(now)
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def reset_all() -> None:
    """Limpia todos los contadores. Solo para tests."""
    _HITS.clear()