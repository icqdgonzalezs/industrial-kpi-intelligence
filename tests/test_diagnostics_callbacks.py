from __future__ import annotations

import pandas as pd
import pytest

from dashboard.diagnostics_callbacks import crear_resumen_ejecutivo


def _diagnostico(severidades: list[str]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "severidad": severidades,
            "categoria": ["Equipo"] * len(severidades),
            "titulo": ["t"] * len(severidades),
            "mensaje": ["m"] * len(severidades),
            "score": [1.0] * len(severidades),
        }
    )


def test_resumen_ejecutivo_dataset_vacio():
    assert crear_resumen_ejecutivo(pd.DataFrame()) == (
        "No hay datos suficientes para generar un diagnóstico."
    )


def test_resumen_ejecutivo_sin_hallazgos_relevantes():
    diagnostico = _diagnostico(["INFO", "INFO"])
    resumen = crear_resumen_ejecutivo(diagnostico)
    assert "Sin hallazgos" in resumen


def test_resumen_ejecutivo_con_priority_y_watch():
    diagnostico = _diagnostico(["PRIORITY", "WATCH", "WATCH", "INFO"])
    resumen = crear_resumen_ejecutivo(diagnostico)
    assert "1 prioritario" in resumen
    assert "2 en seguimiento" in resumen


def test_resumen_ejecutivo_solo_priority_plural():
    diagnostico = _diagnostico(["PRIORITY", "PRIORITY"])
    resumen = crear_resumen_ejecutivo(diagnostico)
    assert "2 prioritarios" in resumen
    assert "en seguimiento" not in resumen


@pytest.fixture
def dash_app_con_callbacks():
    from dash import Dash, html

    from dashboard.diagnostics_callbacks import registrar_callbacks_diagnostics

    app = Dash(__name__)
    app.layout = html.Div()
    registrar_callbacks_diagnostics(app)
    return app


def test_registrar_callbacks_diagnostics_no_falla(dash_app_con_callbacks):
    assert len(dash_app_con_callbacks.callback_map) >= 1
