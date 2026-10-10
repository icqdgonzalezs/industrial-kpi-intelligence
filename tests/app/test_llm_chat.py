# tests/app/test_llm_chat.py
"""Tests del service `llm_chat` (configuración del modelo).

Cubre:
    - MODELO_DEFAULT existe y es string no vacío.
    - MODELO_DEFAULT respeta la env var `GROQ_MODEL`.
    - MODELO_DEFAULT usa el fallback si la env var no está.

Por qué `importlib.reload`: MODELO_DEFAULT es una constante de módulo
evaluada en import time. Para probar distintos valores de env var hay
que recargar el módulo.
"""
from __future__ import annotations

import importlib

import pytest


@pytest.fixture(autouse=True)
def _recargar_modulo_al_final() -> None:
    """Recarga `app.services.llm_chat` al final de cada test.

    Sin esto, la env var modificada con `monkeypatch.setenv` (o el
    reload) contaminaría otros tests del proceso pytest.
    """
    yield
    import app.services.llm_chat as llm_chat

    importlib.reload(llm_chat)


def test_modelo_default_es_string_no_vacio() -> None:
    """MODELO_DEFAULT siempre existe y no es vacío."""
    from app.services.llm_chat import MODELO_DEFAULT

    assert isinstance(MODELO_DEFAULT, str)
    assert MODELO_DEFAULT  # no vacío


def test_modelo_default_respeta_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Con GROQ_MODEL seteada, MODELO_DEFAULT la usa."""
    monkeypatch.setenv("GROQ_MODEL", "modelo-test-custom")

    import app.services.llm_chat as llm_chat

    importlib.reload(llm_chat)

    assert llm_chat.MODELO_DEFAULT == "modelo-test-custom"


def test_modelo_default_usa_fallback_sin_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Sin GROQ_MODEL (ni en .env), MODELO_DEFAULT cae al fallback.

    Se bloquea `load_dotenv` para aislar el test de cualquier
    GROQ_MODEL que pudiera estar en el `.env` local.
    """
    monkeypatch.delenv("GROQ_MODEL", raising=False)
    monkeypatch.setattr("dotenv.load_dotenv", lambda *a, **kw: None)

    import app.services.llm_chat as llm_chat

    importlib.reload(llm_chat)

    assert llm_chat.MODELO_DEFAULT == "openai/gpt-oss-120b"