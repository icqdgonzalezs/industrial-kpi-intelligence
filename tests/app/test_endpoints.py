# tests/app/test_endpoints.py
"""Tests de los endpoints FastAPI con TestClient.

Los POST están protegidos con JWT (Depends(get_current_user)).
Los GET son públicos por ahora (se protegerán con login UI).
"""
from datetime import datetime

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import KPI


def _seed_kpi(
    session: Session,
    nombre: str = "OEE",
    valor: float = 85.5,
    linea: str = "L1",
) -> KPI:
    """Helper: inserta un KPI de prueba."""
    kpi = KPI(
        nombre=nombre,
        valor=valor,
        unidad="%",
        timestamp=datetime(2026, 9, 23, 12, 0),
        linea_produccion=linea,
    )
    session.add(kpi)
    session.commit()
    session.refresh(kpi)
    return kpi


# ---------- GET /kpis/ (público) ----------

def test_get_kpis_vacio(client: TestClient):
    """DB vacía → lista vacía, 200."""
    response = client.get("/kpis/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_kpis_con_datos(client: TestClient, session: Session):
    """DB con 2 KPIs → los devuelve."""
    _seed_kpi(session, "OEE", 85.5)
    _seed_kpi(session, "MTTR", 45.2, "L2")

    response = client.get("/kpis/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["nombre"] == "OEE"
    assert data[1]["nombre"] == "MTTR"


# ---------- POST /kpis/ (protegido) ----------

def test_post_kpi_sin_auth_devuelve_401(client: TestClient):
    """POST sin token → 401."""
    payload = {
        "nombre": "OEE",
        "valor": 85.5,
        "unidad": "%",
        "timestamp": "2026-09-23T10:00:00",
        "linea_produccion": "L1",
    }
    response = client.post("/kpis/", json=payload)
    assert response.status_code == 401


def test_post_kpi_con_auth_invalido_devuelve_401(client: TestClient):
    """POST con token inválido → 401."""
    payload = {
        "nombre": "OEE",
        "valor": 85.5,
        "unidad": "%",
        "timestamp": "2026-09-23T10:00:00",
        "linea_produccion": "L1",
    }
    response = client.post(
        "/kpis/",
        json=payload,
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 401


def test_post_kpi_crea_registro(
    client: TestClient, auth_headers: dict[str, str]
):
    """POST válido con auth → 201 + body con id asignado."""
    payload = {
        "nombre": "Disponibilidad",
        "valor": 95.2,
        "unidad": "%",
        "timestamp": "2026-09-23T10:00:00",
        "linea_produccion": "L3",
    }
    response = client.post("/kpis/", json=payload, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["nombre"] == "Disponibilidad"
    assert data["valor"] == 95.2


def test_post_kpi_persiste(
    client: TestClient, auth_headers: dict[str, str]
):
    """POST crea → GET posterior lo devuelve."""
    payload = {
        "nombre": "Scrap",
        "valor": 0.5,
        "unidad": "%",
        "timestamp": "2026-09-23T11:00:00",
        "linea_produccion": "L4",
    }
    client.post("/kpis/", json=payload, headers=auth_headers)

    response = client.get("/kpis/")
    nombres = [k["nombre"] for k in response.json()]
    assert "Scrap" in nombres


def test_post_kpi_rechaza_payload_invalido(
    client: TestClient, auth_headers: dict[str, str]
):
    """Falta campos obligatorios → 422 (con auth válida)."""
    response = client.post(
        "/kpis/", json={"nombre": "Incompleto"}, headers=auth_headers
    )
    assert response.status_code == 422


def test_post_kpi_rechaza_timestamp_invalido(
    client: TestClient, auth_headers: dict[str, str]
):
    """Timestamp no parseable → 422 (con auth válida)."""
    payload = {
        "nombre": "OEE",
        "valor": 85.5,
        "unidad": "%",
        "timestamp": "no-es-fecha",
        "linea_produccion": "L1",
    }
    response = client.post("/kpis/", json=payload, headers=auth_headers)
    assert response.status_code == 422


# ---------- GET / (dashboard, público) ----------

def test_dashboard_sin_datos(client: TestClient):
    """DB vacía → HTML con empty state."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "No hay KPIs registrados todavía" in response.text


def test_dashboard_con_datos(client: TestClient, session: Session):
    """DB con datos → tabla HTML renderizada."""
    _seed_kpi(session, "OEE", 85.5, "L1")
    _seed_kpi(session, "MTTR", 45.2, "L2")

    response = client.get("/")
    assert response.status_code == 200
    assert "Industrial KPI Intelligence" in response.text
    assert "OEE" in response.text
    assert "MTTR" in response.text
    assert "<table>" in response.text


def test_dashboard_formatea_valor_2_decimales(client: TestClient, session: Session):
    """valor 85.5 → se muestra como 85.50."""
    _seed_kpi(session, "OEE", 85.5)
    response = client.get("/")
    assert "85.50" in response.text
