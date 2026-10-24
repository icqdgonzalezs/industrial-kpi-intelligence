"""Tests de CORS (Seg.3).

Verifican que el middleware CORS está configurado y responde
a requests con Origin header (simulando un frontend cross-origin).
"""


def test_cors_headers_en_get_kpis(client):
    """CORS debe permitir requests cross-origin a /kpis/."""
    response = client.get("/kpis/", headers={"Origin": "http://example.com"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://example.com"


def test_cors_preflight_options(client):
    """CORS debe responder al preflight OPTIONS."""
    response = client.options(
        "/kpis/",
        headers={
            "Origin": "http://example.com",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://example.com"
