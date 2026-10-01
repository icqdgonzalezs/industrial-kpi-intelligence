# app/auth.py
"""Autenticación con JWT (PyJWT) y hashing de passwords con bcrypt.

Responsabilidad:
    - Hash y verificación de passwords (bcrypt directo, sin passlib).
    - Creación y verificación de JSON Web Tokens (PyJWT).
    - Dependency `get_current_user` para inyectar el usuario autenticado
      en endpoints protegidos.

Decisiones de seguridad:
    - Algoritmo HS256 EXPLÍCITO. Nunca se acepta `alg=none`.
    - SECRET_KEY desde variable de entorno (fallback solo para dev).
    - Token de vida corta (24 h en v1, sin refresh).
    - Payload mínimo: solo `sub` (email) + `exp`. Nunca datos sensibles.
    - Password truncado a 72 bytes ANTES de bcrypt (límite del algoritmo).
      El schema de entrada valida el máximo, pero truncamos por defensa.
"""
from __future__ import annotations

import os
import warnings
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session, select

from app.db import get_session
from app.models import User

# ============================================================
# Configuración
# ============================================================

# Algoritmo JWT. Fijo por seguridad (evita ataque alg=none).
ALGORITHM = "HS256"

# Vida del access token (en minutos).
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

# Límite de bcrypt: no procesa passwords >72 bytes.
# Truncamos defensivamente en hash y verify para consistencia.
BCRYPT_MAX_BYTES = 72

# SECRET_KEY: en producción viene de env var.
_SECRET_KEY_ENV = os.getenv("SECRET_KEY")
if not _SECRET_KEY_ENV:
    warnings.warn(
        "SECRET_KEY no configurada. Usando fallback INSECURO solo para dev. "
        "En producción configurar SECRET_KEY con `openssl rand -hex 32`.",
        RuntimeWarning,
        stacklevel=1,
    )
    _SECRET_KEY_ENV = "dev-insecure-secret-change-me-and-over-32-bytes-please"

SECRET_KEY: str = _SECRET_KEY_ENV


# ============================================================
# Password hashing (bcrypt directo)
# ============================================================

def _to_bytes_truncated(password: str) -> bytes:
    """Convierte password a bytes UTF-8 truncados a 72 bytes (límite bcrypt)."""
    return password.encode("utf-8")[:BCRYPT_MAX_BYTES]


def hash_password(plain_password: str) -> str:
    """Hashea un password con bcrypt.

    Args:
        plain_password: Password en texto plano.

    Returns:
        Hash bcrypt (~60 chars) como string, seguro para guardar en la DB.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(_to_bytes_truncated(plain_password), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica un password contra su hash bcrypt.

    Args:
        plain_password: Password en texto plano a verificar.
        hashed_password: Hash bcrypt almacenado (string).

    Returns:
        True si coincide, False si no.
    """
    try:
        return bcrypt.checkpw(
            _to_bytes_truncated(plain_password),
            hashed_password.encode("utf-8"),
        )
    except (ValueError, TypeError):
        # Hash malformado o encoding inválido → tratar como no válido.
        return False


# ============================================================
# JWT (creación / verificación)
# ============================================================

def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    """Crea un JWT firmado con HS256.

    Args:
        subject: Identificador del usuario (típicamente el email).
        expires_delta: Vida del token. Default: ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        Token JWT codificado como string.
    """
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload: dict[str, Any] = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """Decodifica y valida un JWT.

    Args:
        token: JWT a verificar.

    Returns:
        Payload decodificado.

    Raises:
        InvalidTokenError: si el token es inválido o expirado.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


# ============================================================
# OAuth2 scheme (para Swagger UI "Authorize")
# ============================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ============================================================
# Dependency: usuario actual
# ============================================================

_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Credenciales inválidas",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_session)],
) -> User:
    """Dependency que inyecta el usuario autenticado en endpoints protegidos.

    Flujo:
        1. Extrae el JWT del header Authorization: Bearer <token>.
        2. Verifica firma y expiración.
        3. Busca el usuario en la DB por email.
        4. Verifica que esté activo.
        5. Devuelve el modelo User.

    Raises:
        HTTPException 401: si el token es inválido, expirado, el usuario
        no existe, o está desactivado.
    """
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if not email or not isinstance(email, str):
            raise _CREDENTIALS_EXCEPTION
    except InvalidTokenError as exc:
        raise _CREDENTIALS_EXCEPTION from exc

    user = session.exec(select(User).where(User.email == email)).first()
    if user is None:
        raise _CREDENTIALS_EXCEPTION
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado",
        )
    return user
