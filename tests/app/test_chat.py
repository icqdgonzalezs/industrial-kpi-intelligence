# tests/app/test_chat.py
"""Tests del endpoint /chat/ con mock del servicio LLM.

El mock evita pegarle a Groq en cada test. Se testea la orquestación
del router (auth, validación, manejo de errores, render del template),
no el LLM en sí (eso se validó manualmente end-to-end).

El endpoint está protegido con JWT. Todos los POST requieren auth_headers.
"""
from collections.abc import Sequence
from typing import Any

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(name="mock_llm_ok")
def mock_llm_ok_fixture(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock de consultar_llm que devuelve una respuesta controlada."""

    async def fake_consultar_llm(query: str, kpis: Sequence[Any]) -> dict[str, Any]:
        return {
            "respuesta": "Respuesta mock para testing.",
            "tokens_prompt": 100,
            "tokens_completion": 50,
            "elapsed_ms": 42,
        }

    monkeypatch.setattr("app.routers.chat.consultar_llm", fake_consultar_llm)


# ---------- Auth ----------

def test_chat_sin_auth_devuelve_401(client: TestClient) -> None:
    """POST sin token → 401."""
    response = client.post("/chat/", data={"query": "test"})
    assert response.status_code == 401


def test_chat_con_auth_invalido_devuelve_401(client: TestClient) -> None:
    """POST con token inválido → 401."""
    response = client.post(
        "/chat/",
        data={"query": "test"},
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 401


# ---------- Happy path ----------

def test_chat_devuelve_200_html(
    client: TestClient,
    auth_headers: dict[str, str],
    mock_llm_ok: None,
) -> None:
    """POST válido con auth → 200 con content-type text/html."""
    response = client.post(
        "/chat/", data={"query": "¿Cómo está todo?"}, headers=auth_headers
    )
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_chat_incluye_respuesta_del_llm(
    client: TestClient,
    auth_headers: dict[str, str],
    mock_llm_ok: None,
) -> None:
    """La respuesta del LLM aparece en el HTML."""
    response = client.post(
        "/chat/", data={"query": "test"}, headers=auth_headers
    )
    assert "Respuesta mock para testing." in response.text


def test_chat_incluye_metricas_totales(
    client: TestClient,
    auth_headers: dict[str, str],
    mock_llm_ok: None,
) -> None:
    """Muestra tokens sumados (prompt + completion) y elapsed_ms."""
    response = client.post(
        "/chat/", data={"query": "test"}, headers=auth_headers
    )
    assert "150 tokens" in response.text  # 100 + 50
    assert "42 ms" in response.text


def test_chat_preserva_la_query_original(
    client: TestClient,
    auth_headers: dict[str, str],
    mock_llm_ok: None,
) -> None:
    """El HTML muestra la pregunta del usuario."""
    response = client.post(
        "/chat/",
        data={"query": "Pregunta única de prueba"},
        headers=auth_headers,
    )
    assert "Pregunta única de prueba" in response.text


# ---------- Validación ----------

def test_chat_rechaza_query_vacio(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """query vacío → 422 (Form min_length=1)."""
    response = client.post(
        "/chat/", data={"query": ""}, headers=auth_headers
    )
    assert response.status_code == 422


def test_chat_rechaza_query_demasiado_largo(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """query > 500 caracteres → 422 (Form max_length=500)."""
    response = client.post(
        "/chat/", data={"query": "x" * 501}, headers=auth_headers
    )
    assert response.status_code == 422


def test_chat_rechaza_sin_query(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """Sin campo query → 422."""
    response = client.post("/chat/", headers=auth_headers)
    assert response.status_code == 422


# ---------- Manejo de errores ----------

def test_chat_maneja_timeout(
    client: TestClient,
    auth_headers: dict[str, str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """TimeoutError del LLM → HTML con mensaje de timeout."""

    async def raise_timeout(query: str, kpis: Sequence[Any]) -> dict[str, Any]:
        raise TimeoutError("LLM timeout")

    monkeypatch.setattr("app.routers.chat.consultar_llm", raise_timeout)

    response = client.post(
        "/chat/", data={"query": "test"}, headers=auth_headers
    )
    assert response.status_code == 200
    assert "tardó demasiado" in response.text


def test_chat_maneja_error_generico(
    client: TestClient,
    auth_headers: dict[str, str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Error inesperado del SDK → HTML con mensaje genérico + nombre del error."""

    async def raise_error(query: str, kpis: Sequence[Any]) -> dict[str, Any]:
        raise ValueError("Error raro")

    monkeypatch.setattr("app.routers.chat.consultar_llm", raise_error)

    response = client.post(
        "/chat/", data={"query": "test"}, headers=auth_headers
    )
    assert response.status_code == 200
    assert "Error inesperado" in response.text
    assert "ValueError" in response.text


# ---------- Dashboard incluye chat ----------

def test_dashboard_incluye_seccion_chat(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """El dashboard raíz incluye el formulario HTMX del chat."""
    response = client.get("/", headers=auth_headers)
    assert response.status_code == 200
    assert "Asistente de planta" in response.text
    assert 'hx-post="/chat/"' in response.text
    assert "htmx.min.js" in response.text


# ============================================================
# Rate limiting (slowapi, 30/minute por IP)
# ============================================================

class TestRateLimit:
    """Verifica que POST /chat/ respeta el límite de 30/minuto."""

    def test_chat_bajo_limite_retorna_200(
        self,
        client: TestClient,
        auth_headers: dict[str, str],
        mock_llm_ok,
    ) -> None:
        """Un request aislado no debe tocar el límite."""
        response = client.post(
            "/chat/",
            headers=auth_headers,
            data={"query": "¿Cuál es el OEE?"},
        )
        assert response.status_code == 200

    def test_chat_supera_limite_retorna_429(
        self,
        client: TestClient,
        auth_headers: dict[str, str],
        mock_llm_ok,
    ) -> None:
        """El request 31 dentro del mismo minuto debe devolver 429."""
        # 30 requests permitidas (todas con mock instantáneo).
        for i in range(30):
            r = client.post(
                "/chat/",
                headers=auth_headers,
                data={"query": f"query {i}"},
            )
            assert r.status_code == 200, f"request {i} esperaba 200, fue {r.status_code}"

        # La 31° debe ser bloqueada por slowapi.
        r = client.post(
            "/chat/",
            headers=auth_headers,
            data={"query": "bloqueada"},
        )
        assert r.status_code == 429
