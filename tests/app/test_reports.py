"""Tests del reporte ejecutivo narrado por LLM (IA.3).

Cobertura:
    - Unit: construir_prompt_ejecutivo (puro, determinista).
    - Integración: GET /reports/executive (auth, rate limit,
      polimorfismo HTML/JSON, 422 rango inválido, df vacío).

Estrategia: mockear cargar_dataset_filtrado, calcular_kpis_ejecutivos
y generar_reporte_ejecutivo. No depende del CSV real ni de Groq.
"""
from __future__ import annotations

import pandas as pd
import pytest

from app.services.llm_reports import construir_prompt_ejecutivo

# =========================================================================
# Unit: prompt puro
# =========================================================================


def test_prompt_incluye_secciones_ejecutivas() -> None:
    """El system prompt pide estructura Titular/Drivers/Recomendación."""
    kpis = {
        "oee": {
            "oee": 0.82,
            "clasificacion": "world_class",
            "disponibilidad": 0.90,
            "rendimiento": 0.95,
            "calidad": 0.96,
        },
        "operacional": {
            "fpy": 0.96,
            "tasa_defectos": 0.04,
            "tasa_scrap": 0.02,
            "tasa_reproceso": 0.02,
            "ppm": 40000.0,
            "total_producidas": 1000,
            "total_defectuosas": 40,
        },
        "top_defectos": [
            {"defecto": "porosidad", "frecuencia": 20, "porcentaje": 50.0},
        ],
    }
    contexto = {"linea": "L1", "desde": "2026-01-01", "hasta": "2026-01-31", "n_lotes": 500}

    system, user = construir_prompt_ejecutivo(kpis, contexto)

    assert "CFO" in system
    assert "COO" in system
    assert "Titular" in system
    assert "Drivers" in system
    assert "Recomendación" in system
    assert "L1" in user
    assert "0.8200" in user
    assert "40000.0" in user
    assert "porosidad" in user


def test_prompt_con_dicts_vacios_no_crashea() -> None:
    """Dicts vacíos → defaults seguros, sin KeyError."""
    system, user = construir_prompt_ejecutivo({}, {})
    assert system
    assert "sin defectos registrados" in user
    assert "todas las líneas" in user


def test_prompt_es_determinista() -> None:
    """Mismo input → mismo output (función pura)."""
    kpis = {"oee": {"oee": 0.5}, "operacional": {"fpy": 0.9, "ppm": 100.0}}
    ctx = {"linea": "L2"}
    a = construir_prompt_ejecutivo(kpis, ctx)
    b = construir_prompt_ejecutivo(kpis, ctx)
    assert a == b


# =========================================================================
# Fixtures de integración
# =========================================================================


@pytest.fixture
def mock_dataset_ok(monkeypatch):
    """Mockea carga de dataset + cálculo de KPIs."""
    df = pd.DataFrame({"dummy": [1, 2, 3]})

    def fake_cargar(linea=None, desde=None, hasta=None):
        return df, {}

    def fake_kpis(_df):
        return {
            "oee": {"oee": 0.82, "clasificacion": "world_class"},
            "operacional": {"fpy": 0.96, "ppm": 40000.0},
            "top_defectos": [],
            "n_registros": 3,
        }

    monkeypatch.setattr("app.routers.reports.cargar_dataset_filtrado", fake_cargar)
    monkeypatch.setattr("app.routers.reports.calcular_kpis_ejecutivos", fake_kpis)
    return df


@pytest.fixture
def mock_reporte_ok(monkeypatch):
    """Mockea la llamada al LLM: respuesta determinista."""

    async def fake(_kpis, _contexto):
        return {
            "respuesta": "Titular: OEE al 82%.\n\nDrivers: ...\n\nRecomendación: ...",
            "tokens_prompt": 100,
            "tokens_completion": 200,
            "elapsed_ms": 1234,
            "modelo": "test-model",
        }

    monkeypatch.setattr("app.routers.reports.generar_reporte_ejecutivo", fake)
    return fake


# =========================================================================
# Integración: endpoint
# =========================================================================


def test_reports_executive_401_sin_auth(client) -> None:
    """Sin JWT → 401."""
    r = client.get("/reports/executive")
    assert r.status_code == 401


def test_reports_executive_200_json(
    client, auth_headers, mock_dataset_ok, mock_reporte_ok
) -> None:
    """Con JWT y sin HX-Request → JSON con reporte narrado."""
    r = client.get("/reports/executive", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert "OEE" in data["reporte"]
    assert data["meta"]["modelo"] == "test-model"
    assert data["meta"]["tokens_prompt"] == 100


def test_reports_executive_200_html_htmx(
    client, auth_headers, mock_dataset_ok, mock_reporte_ok
) -> None:
    """Con HX-Request → HTML parcial."""
    headers = {**auth_headers, "HX-Request": "true"}
    r = client.get("/reports/executive", headers=headers)
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    assert "Reporte ejecutivo" in r.text
    assert "OEE" in r.text


def test_reports_executive_422_rango_invalido(client, auth_headers) -> None:
    """desde > hasta → 422."""
    r = client.get(
        "/reports/executive?desde=2026-02-01&hasta=2026-01-01",
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_reports_executive_200_sin_datos(client, auth_headers, monkeypatch) -> None:
    """df vacío → ok:false en JSON, sin llamar al LLM."""
    monkeypatch.setattr(
        "app.routers.reports.cargar_dataset_filtrado",
        lambda **kw: (pd.DataFrame(), {}),
    )
    r = client.get("/reports/executive", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "No hay datos" in data["error"]


def test_reports_executive_rate_limit_429(
    client, auth_headers, mock_dataset_ok, mock_reporte_ok
) -> None:
    """31° request en la misma ventana → 429."""
    for _ in range(30):
        r = client.get("/reports/executive", headers=auth_headers)
        assert r.status_code == 200
    r = client.get("/reports/executive", headers=auth_headers)
    assert r.status_code == 429


def test_reports_executive_200_parametros_vacios_htmx(
    client, auth_headers, mock_dataset_ok, mock_reporte_ok
) -> None:
    """HTMX envía inputs vacíos como ``?linea=&desde=&hasta=``.

    Regresión: FastAPI debe tratar "" como "no provisto", no como
    "provisto con valor inválido". Sin este fix, el endpoint
    devolvía 422 al clickear "Generar reporte" sin filtros.
    """
    r = client.get(
        "/reports/executive?linea=&desde=&hasta=",
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["ok"] is True
