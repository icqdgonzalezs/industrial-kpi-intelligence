"""Tests formales de autenticación.

Cubre:
    - POST /auth/login: éxito, credenciales malas, validación Pydantic.
    - GET /auth/me: token válido, sin token, inválido, expirado.
    - Endpoints protegidos: /kpis/ y /chat/ requieren auth.
    - POST /auth/logout: borra cookie, idempotente, no requiere auth.

Fixture compartida:
    `auth_headers` (conftest) crea el user `test@example.com` con
    password `testpassword123` y devuelve headers con JWT válido.
"""
from __future__ import annotations

from datetime import timedelta

from fastapi.testclient import TestClient

from app.auth import create_access_token

# Credenciales del user creado por la fixture `auth_headers`.
_TEST_EMAIL = "test@example.com"
_TEST_PASSWORD = "testpassword123"


# ============================================================
# POST /auth/login
# ============================================================

class TestLogin:
    def test_login_exitoso_retorna_200_token_y_cookie(
        self, client: TestClient, auth_headers: dict[str, str]
    ) -> None:
        response = client.post(
            "/auth/login",
            json={"email": _TEST_EMAIL, "password": _TEST_PASSWORD},
        )

        assert response.status_code == 200
        body = response.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"
        assert body["access_token"]  # no vacío

        # Cookie HttpOnly con el token.
        assert "access_token" in response.cookies

    def test_login_password_incorrecta_retorna_401(
        self, client: TestClient, auth_headers: dict[str, str]
    ) -> None:
        response = client.post(
            "/auth/login",
            json={"email": _TEST_EMAIL, "password": "wrongpassword123"},
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Credenciales inválidas"

    def test_login_email_inexistente_retorna_401(
        self, client: TestClient
    ) -> None:
        response = client.post(
            "/auth/login",
            json={"email": "noexiste@example.com", "password": "anypassword123"},
        )

        assert response.status_code == 401
        # Mismo mensaje que password incorrecta → no filtra existencia.
        assert response.json()["detail"] == "Credenciales inválidas"

    def test_login_password_corta_retorna_422(self, client: TestClient) -> None:
        response = client.post(
            "/auth/login",
            json={"email": _TEST_EMAIL, "password": "short"},
        )

        assert response.status_code == 422

    def test_login_email_invalido_retorna_422(self, client: TestClient) -> None:
        response = client.post(
            "/auth/login",
            json={"email": "no-es-un-email", "password": "password1234"},
        )

        assert response.status_code == 422


# ============================================================
# GET /auth/me
# ============================================================

class TestMe:
    def test_me_con_token_valido_retorna_200(
        self, client: TestClient, auth_headers: dict[str, str]
    ) -> None:
        response = client.get("/auth/me", headers=auth_headers)

        assert response.status_code == 200
        body = response.json()
        assert body["email"] == _TEST_EMAIL
        assert body["is_active"] is True
        # NUNCA debe exponer el hash.
        assert "hashed_password" not in body

    def test_me_sin_token_retorna_401(self, client: TestClient) -> None:
        response = client.get("/auth/me")
        assert response.status_code == 401

    def test_me_token_invalido_retorna_401(self, client: TestClient) -> None:
        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer no-es-un-jwt"},
        )
        assert response.status_code == 401

    def test_me_token_expirado_retorna_401(self, client: TestClient) -> None:
        expired = create_access_token(
            subject=_TEST_EMAIL,
            expires_delta=timedelta(seconds=-1),
        )
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {expired}"},
        )
        assert response.status_code == 401


# ============================================================
# Endpoints protegidos (POST /kpis/ y POST /chat/)
# ============================================================

class TestEndpointsProtegidos:
    def test_post_kpis_sin_auth_retorna_401(self, client: TestClient) -> None:
        response = client.post(
            "/kpis/",
            json={
                "nombre": "OEE",
                "valor": 85.5,
                "unidad": "%",
                "timestamp": "2026-10-05T12:00:00",
                "linea_produccion": "L1",
            },
        )
        assert response.status_code == 401

    def test_post_chat_sin_auth_retorna_401(self, client: TestClient) -> None:
        response = client.post("/chat/", data={"query": "test"})
        assert response.status_code == 401

    def test_post_kpis_con_auth_retorna_2xx(
        self, client: TestClient, auth_headers: dict[str, str]
    ) -> None:
        response = client.post(
            "/kpis/",
            headers=auth_headers,
            json={
                "nombre": "OEE",
                "valor": 85.5,
                "unidad": "%",
                "timestamp": "2026-10-05T12:00:00",
                "linea_produccion": "L1",
            },
        )
        assert response.status_code in (200, 201)


# ============================================================
# POST /auth/logout
# ============================================================

class TestLogout:
    def test_logout_borra_cookie(self, client: TestClient) -> None:
        response = client.post("/auth/logout")

        assert response.status_code == 200
        assert response.json() == {"ok": True}
        set_cookie = response.headers.get("set-cookie", "")
        assert "access_token=" in set_cookie

    def test_logout_es_idempotente(self, client: TestClient) -> None:
        first = client.post("/auth/logout")
        second = client.post("/auth/logout")

        assert first.status_code == 200
        assert second.status_code == 200

    def test_logout_no_requiere_auth(self, client: TestClient) -> None:
        # Sin headers, sin cookie.
        response = client.post("/auth/logout")
        assert response.status_code == 200