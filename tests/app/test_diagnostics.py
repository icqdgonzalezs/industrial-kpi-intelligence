"""Tests del endpoint /diagnostics/ai (IA.2) y del servicio llm_diagnostics.

Estructura en 2 niveles:
    - Unidad: ``construir_prompt`` se testea sin HTTP ni LLM.
    - Integración: ``TestClient`` + mock de ``diagnosticar`` (no toca Groq).

El endpoint está protegido con JWT. Todos los GET requieren auth_headers.
El rate limit se resetea entre tests vía fixture autouse de conftest.
"""
from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.services.llm_diagnostics import construir_prompt

# ---------------------------------------------------------------------
# Fixtures locales (consistente con test_chat.py: no van a conftest)
# ---------------------------------------------------------------------


@pytest.fixture(name="mock_diagnosticar_ok")
def mock_diagnosticar_ok_fixture(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock de ``diagnosticar`` que devuelve un diagnóstico controlado."""

    async def fake_diagnosticar(
        findings: list[dict[str, Any]], contexto: dict[str, Any]
    ) -> dict[str, Any]:
        return {
            "respuesta": "## Qué está pasando\nMock de diagnóstico para testing.",
            "tokens_prompt": 200,
            "tokens_completion": 100,
            "elapsed_ms": 42,
            "modelo": "openai/gpt-oss-120b",
        }

    monkeypatch.setattr("app.routers.diagnostics.diagnosticar", fake_diagnosticar)


# ---------------------------------------------------------------------
# Unidad — construir_prompt (sin HTTP, sin LLM)
# ---------------------------------------------------------------------


def test_construir_prompt_incluye_findings() -> None:
    """El prompt del usuario refleja los títulos/categorías de los findings."""
    findings = [
        {
            "severidad": "PRIORITY",
            "categoria": "Capacidad de proceso",
            "titulo": "Variable: Peso",
            "mensaje": "Cpk = 0.85 (No capaz).",
            "score": 0.48,
        },
        {
            "severidad": "WATCH",
            "categoria": "Turno",
            "titulo": "Turno: Mañana",
            "mensaje": "Tasa de defectos 1.2x el promedio.",
            "score": 1.2,
        },
    ]
    contexto = {"linea": "L1", "desde": "2024-01-01", "hasta": "2024-01-31", "n_lotes": 621}

    system, user = construir_prompt(findings, contexto)

    assert "ingeniero senior" in system
    # El user_prompt debe incluir contexto y findings.
    assert "L1" in user
    assert "621" in user
    assert "Variable: Peso" in user
    assert "Turno: Mañana" in user
    # Orden: PRIORITY antes que WATCH (aunque vengan al revés).
    idx_priority = user.index("Variable: Peso")
    idx_watch = user.index("Turno: Mañana")
    assert idx_priority < idx_watch, "El orden por severidad no se respetó"


def test_construir_prompt_es_determinista() -> None:
    """Mismo input → mismo output (sin timestamps ni random)."""
    findings = [
        {
            "severidad": "PRIORITY",
            "categoria": "Equipo",
            "titulo": "Equipo: DEPAL-01",
            "mensaje": "Tasa 1.5x el promedio.",
            "score": 1.5,
        }
    ]
    contexto = {"linea": None, "desde": None, "hasta": None, "n_lotes": 18078}

    p1 = construir_prompt(findings, contexto)
    p2 = construir_prompt(findings, contexto)
    assert p1 == p2


def test_construir_prompt_sin_findings() -> None:
    """Sin findings, el prompt lo dice explícitamente (no se inventa datos)."""
    contexto = {"linea": None, "desde": None, "hasta": None, "n_lotes": 100}
    _, user = construir_prompt([], contexto)
    assert "No se detectaron hallazgos" in user


# ---------------------------------------------------------------------
# Integración — endpoints
# ---------------------------------------------------------------------


def test_endpoint_sin_auth_devuelve_401(client: TestClient) -> None:
    """GET sin token → 401."""
    response = client.get("/diagnostics/ai")
    assert response.status_code == 401


def test_endpoint_con_auth_devuelve_200_json(
    client: TestClient,
    auth_headers: dict[str, str],
    mock_diagnosticar_ok: None,
) -> None:
    """GET con auth → 200 + JSON con ok, diagnostico, findings, meta."""
    response = client.get(
        "/diagnostics/ai",
        params={"linea": "L1", "desde": "2024-01-01", "hasta": "2024-01-31"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert "diagnostico" in data
    assert isinstance(data["findings"], list)
    assert data["meta"]["linea"] == "L1"
    assert data["meta"]["n_lotes"] > 0


def test_endpoint_con_hx_request_devuelve_html(
    client: TestClient,
    auth_headers: dict[str, str],
    mock_diagnosticar_ok: None,
) -> None:
    """GET con header HX-Request → HTML (no JSON)."""
    response = client.get(
        "/diagnostics/ai",
        params={"linea": "L1"},
        headers={**auth_headers, "HX-Request": "true"},
    )
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Diagnóstico" in response.text


def test_endpoint_rango_invalido_devuelve_422(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    """desde > hasta → 422 antes de tocar datos."""
    response = client.get(
        "/diagnostics/ai",
        params={"desde": "2024-12-31", "hasta": "2024-01-01"},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_endpoint_linea_inexistente_devuelve_ok_false(
    client: TestClient,
    auth_headers: dict[str, str],
    mock_diagnosticar_ok: None,
) -> None:
    """Línea sin datos → 200 con ok:false (no rompe el flujo)."""
    response = client.get(
        "/diagnostics/ai",
        params={"linea": "L99"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is False
    assert "No hay datos" in data["error"]
    assert data["findings"] == []


def test_endpoint_rate_limit_429(
    client: TestClient,
    auth_headers: dict[str, str],
    mock_diagnosticar_ok: None,
) -> None:
    """Request 31 en la misma ventana → 429."""
    for _ in range(30):
        r = client.get(
            "/diagnostics/ai",
            params={"linea": "L1", "desde": "2024-01-01", "hasta": "2024-01-31"},
            headers=auth_headers,
        )
        assert r.status_code == 200

    r31 = client.get(
        "/diagnostics/ai",
        params={"linea": "L1", "desde": "2024-01-01", "hasta": "2024-01-31"},
        headers=auth_headers,
    )
    assert r31.status_code == 429
