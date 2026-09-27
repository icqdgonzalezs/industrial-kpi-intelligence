# tests/app/test_chat.py
"""Tests del endpoint /chat/ con mock del servicio LLM.

El mock evita pegarle a Groq en cada test. Se testea la orquestación
del router (validación, manejo de errores, render del template), no
el LLM en sí (eso se validó manualmente end-to-end).
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


# ---------- Happy path ----------

def test_chat_devuelve_200_html(client: TestClient, mock_llm_ok: None) -> None:
    """POST válido → 200 con content-type text/html."""
    response = client.post("/chat/", data={"query": "¿Cómo está todo?"})
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_chat_incluye_respuesta_del_llm(client: TestClient, mock_llm_ok: None) -> None:
    """La respuesta del LLM aparece en el HTML."""
    response = client.post("/chat/", data={"query": "test"})
    assert "Respuesta mock para testing." in response.text


def test_chat_incluye_metricas_totales(client: TestClient, mock_llm_ok: None) -> None:
    """Muestra tokens sumados (prompt + completion) y elapsed_ms."""
    response = client.post("/chat/", data={"query": "test"})
    assert "150 tokens" in response.text  # 100 + 50
    assert "42 ms" in response.text


def test_chat_preserva_la_query_original(client: TestClient, mock_llm_ok: None) -> None:
    """El HTML muestra la pregunta del usuario."""
    response = client.post("/chat/", data={"query": "Pregunta única de prueba"})
    assert "Pregunta única de prueba" in response.text


# ---------- Validación ----------

def test_chat_rechaza_query_vacio(client: TestClient) -> None:
    """query vacío → 422 (Form min_length=1)."""
    response = client.post("/chat/", data={"query": ""})
    assert response.status_code == 422


def test_chat_rechaza_query_demasiado_largo(client: TestClient) -> None:
    """query > 500 caracteres → 422 (Form max_length=500)."""
    response = client.post("/chat/", data={"query": "x" * 501})
    assert response.status_code == 422


def test_chat_rechaza_sin_query(client: TestClient) -> None:
    """Sin campo query → 422."""
    response = client.post("/chat/")
    assert response.status_code == 422


# ---------- Manejo de errores ----------

def test_chat_maneja_timeout(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """TimeoutError del LLM → HTML con mensaje de timeout."""

    async def raise_timeout(query: str, kpis: Sequence[Any]) -> dict[str, Any]:
        raise TimeoutError("LLM timeout")

    monkeypatch.setattr("app.routers.chat.consultar_llm", raise_timeout)

    response = client.post("/chat/", data={"query": "test"})
    assert response.status_code == 200
    assert "tardó demasiado" in response.text


def test_chat_maneja_error_generico(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Error inesperado del SDK → HTML con mensaje genérico + nombre del error."""

    async def raise_error(query: str, kpis: Sequence[Any]) -> dict[str, Any]:
        raise ValueError("Error raro")

    monkeypatch.setattr("app.routers.chat.consultar_llm", raise_error)

    response = client.post("/chat/", data={"query": "test"})
    assert response.status_code == 200
    assert "Error inesperado" in response.text
    assert "ValueError" in response.text


# ---------- Dashboard incluye chat ----------

def test_dashboard_incluye_seccion_chat(client: TestClient) -> None:
    """El dashboard raíz incluye el formulario HTMX del chat."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Asistente de planta" in response.text
    assert 'hx-post="/chat/"' in response.text
    assert "htmx.min.js" in response.text
