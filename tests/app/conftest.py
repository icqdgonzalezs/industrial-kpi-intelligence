# tests/app/conftest.py
"""Fixtures compartidas para tests del stack FastAPI."""
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.auth import create_access_token, hash_password
from app.db import get_session
from app.main import app
from app.models import User


@pytest.fixture(autouse=True)
def _reset_rate_limiter() -> Generator[None, None, None]:
    """Resetea el storage del limiter entre tests.

    Sin esto, el estado global de slowapi contamina los tests que
    ejecutan POST /chat/ varias veces (como el de rate limit). El
    limiter almacena contadores por IP en memoria y persisten entre
    tests del mismo proceso pytest.
    """
    from app.limiter import reset_all

    reset_all()
    yield
    reset_all()


@pytest.fixture(name="session")
def session_fixture() -> Generator[Session, None, None]:
    """Sesión contra SQLite en memoria. Aislada por test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """TestClient con la DB real sustituida por la DB en memoria."""
    def get_session_override() -> Generator[Session, None, None]:
        yield session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(session: Session) -> dict[str, str]:
    """Crea un usuario en la DB de test y devuelve headers con JWT.

    No usa el endpoint /auth/login (evita dependencia circular con
    `client`). Genera el token directo con `create_access_token`.
    """
    user = User(
        email="test@example.com",
        hashed_password=hash_password("testpassword123"),
    )
    session.add(user)
    session.commit()

    token = create_access_token(subject=user.email)
    return {"Authorization": f"Bearer {token}"}