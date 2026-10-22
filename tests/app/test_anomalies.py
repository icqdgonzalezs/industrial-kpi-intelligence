from fastapi.testclient import TestClient


def test_anomalies_requires_auth(client: TestClient):
    """Sin token, debe devolver 401."""
    response = client.get("/anomalies/?kpi=oee")
    assert response.status_code == 401

def test_anomalies_missing_kpi(client: TestClient, auth_headers: dict):
    """Sin el parámetro kpi, debe devolver 422."""
    response = client.get("/anomalies/", headers=auth_headers)
    assert response.status_code == 422

def test_anomalies_html_response(client: TestClient, auth_headers: dict):
    """Con HX-Request, debe devolver HTML."""
    response = client.get(
        "/anomalies/?kpi=oee",
        headers={**auth_headers, "HX-Request": "true"}
    )
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "No se encontraron anomalías" in response.text or "table" in response.text

def test_anomalies_json_response(client: TestClient, auth_headers: dict):
    """Sin HX-Request, debe devolver JSON."""
    response = client.get("/anomalies/?kpi=oee", headers=auth_headers)
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    data = response.json()
    assert isinstance(data, list)

def test_anomalies_rate_limit(client: TestClient, auth_headers: dict):
    """Debe respetar el rate limit (30/min)."""
    for _ in range(30):
        client.get("/anomalies/?kpi=oee", headers=auth_headers)
    response = client.get("/anomalies/?kpi=oee", headers=auth_headers)
    assert response.status_code == 429
