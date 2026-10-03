# app/routers/auth.py
"""Router de autenticación: login, logout y perfil del usuario actual.

Endpoints:
    - POST /auth/login  → valida credenciales, setea cookie + devuelve JWT.
                          Detecta HTMX: responde HTML con HX-Redirect, o JSON.
    - POST /auth/logout → borra la cookie de sesión.
    - GET  /auth/me     → devuelve el usuario autenticado.

Decisiones de seguridad:
    - Mismo mensaje ("Credenciales inválidas") para email inexistente y
      password incorrecta → previene user enumeration.
    - Timing-safe: verify_password() SIEMPRE corre, incluso si el user
      no existe, para no filtrar información por timing.
    - Cookie HttpOnly: JS no puede leerla → XSS-safe. SameSite=Lax.
    - `secure` controlado por env var COOKIE_SECURE (false en dev,
      true en Railway).
"""
from __future__ import annotations

import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import Session, select

from app.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    COOKIE_NAME,
    create_access_token,
    get_current_user,
    verify_password,
)
from app.db import get_session
from app.models import User
from app.schemas import UserLogin, UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])

_INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credenciales inválidas",
    headers={"WWW-Authenticate": "Bearer"},
)

_DUMMY_HASH = (
    "$2b$12$0000000000000000000000uNh7s6Vw4rKqO8gqvt6hHk9j4z7Mx7wGe"
)

_COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"


def _is_htmx(request: Request) -> bool:
    """Detecta si el request viene de HTMX."""
    return request.headers.get("HX-Request") == "true"


def _set_auth_cookie(response: Response, token: str) -> None:
    """Setea la cookie HttpOnly con el JWT."""
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        samesite="lax",
        secure=_COOKIE_SECURE,
        path="/",
    )


@router.post("/login")
def login(
    request: Request,
    credentials: UserLogin,
    session: Annotated[Session, Depends(get_session)],
) -> Response:
    """Autentica un usuario. Responde según el cliente:

    - HTMX (dashboard): cookie + `HX-Redirect: /` en éxito, HTML en error.
    - API REST (JSON): cookie + body `{access_token, token_type}`.
    """
    user = session.exec(
        select(User).where(User.email == credentials.email)
    ).first()

    hash_to_check = user.hashed_password if user else _DUMMY_HASH
    password_ok = verify_password(credentials.password, hash_to_check)

    htmx = _is_htmx(request)

    if user is None or not password_ok:
        if htmx:
            return HTMLResponse(content="Credenciales inválidas", status_code=200)
        raise _INVALID_CREDENTIALS

    if not user.is_active:
        if htmx:
            return HTMLResponse(content="Usuario desactivado", status_code=200)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado",
        )

    token = create_access_token(subject=user.email)

    if htmx:
        response = HTMLResponse(content="", status_code=200)
        _set_auth_cookie(response, token)
        response.headers["HX-Redirect"] = "/"
        return response

    response = JSONResponse(
        content={"access_token": token, "token_type": "bearer"}
    )
    _set_auth_cookie(response, token)
    return response


@router.post("/logout")
def logout() -> Response:
    """Borra la cookie de sesión. Idempotente, no requiere auth."""
    response = JSONResponse(content={"ok": True})
    response.delete_cookie(key=COOKIE_NAME, path="/")
    return response


@router.get("/me", response_model=UserPublic)
def me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserPublic:
    """Devuelve los datos públicos del usuario autenticado."""
    return UserPublic(
        id=current_user.id,  # type: ignore[arg-type]
        email=current_user.email,  # type: ignore[arg-type]
        is_active=current_user.is_active,
        created_at=current_user.created_at,
    )
