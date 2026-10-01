# app/routers/auth.py
"""Router de autenticación: login y perfil del usuario actual.

Endpoints:
    - POST /auth/login → recibe credenciales, devuelve JWT.
    - GET  /auth/me    → devuelve el usuario autenticado.

Decisiones de seguridad:
    - Mismo mensaje ("Credenciales inválidas") para email inexistente y
      password incorrecta → previene user enumeration.
    - Ejecución timing-safe: verify_password() SIEMPRE corre, incluso si
      el user no existe, para no filtrar información por timing.
"""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.auth import (
    create_access_token,
    get_current_user,
    verify_password,
)
from app.db import get_session
from app.models import User
from app.schemas import Token, UserLogin, UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])

# Mensaje unificado. NUNCA revelar si el email existe o no.
_INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credenciales inválidas",
    headers={"WWW-Authenticate": "Bearer"},
)

# Hash dummy para timing-safe check cuando el user no existe.
# Es un hash bcrypt válido de un password arbitrario. Nunca se usará
# para autenticar (verify_password devolverá False), pero fuerza que
# bcrypt se ejecute siempre → tiempo de respuesta constante.
_DUMMY_HASH = (
    "$2b$12$0000000000000000000000uNh7s6Vw4rKqO8gqvt6hHk9j4z7Mx7wGe"
)


@router.post("/login", response_model=Token)
def login(
    credentials: UserLogin,
    session: Annotated[Session, Depends(get_session)],
) -> Token:
    """Autentica un usuario y devuelve un JWT.

    Flujo:
        1. Buscar User por email.
        2. Verificar password contra el hash (o un dummy si el user no existe).
        3. Devolver 401 con mensaje genérico si algo falla.
        4. Devolver 403 si el usuario está desactivado.
        5. Generar JWT y devolverlo.
    """
    user = session.exec(
        select(User).where(User.email == credentials.email)
    ).first()

    # Timing-safe: SIEMPRE ejecutar bcrypt, incluso si el user no existe.
    # Si no, un atacante podría medir la latencia para saber si un email existe.
    hash_to_check = user.hashed_password if user else _DUMMY_HASH
    password_ok = verify_password(credentials.password, hash_to_check)

    if user is None or not password_ok:
        raise _INVALID_CREDENTIALS

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado",
        )

    token = create_access_token(subject=user.email)
    return Token(access_token=token)


@router.get("/me", response_model=UserPublic)
def me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserPublic:
    """Devuelve los datos públicos del usuario autenticado.

    Útil para:
        - Verificar que el token es válido.
        - Mostrar el email del usuario en la UI.
        - Testear el sistema completo end-to-end.
    """
    return UserPublic(
        id=current_user.id,  # type: ignore[arg-type]
        email=current_user.email,  # type: ignore[arg-type]
        is_active=current_user.is_active,
        created_at=current_user.created_at,
    )
