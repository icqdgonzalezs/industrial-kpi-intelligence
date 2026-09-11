"""Tests for process capability calculations (Pp/Ppk)."""

import pandas as pd
import pytest

from src.capability import calcular_pp_ppk, resumen_capacidad


def test_pp_ppk_valores_conocidos():
    valores = pd.Series(
        [98, 99, 100, 101, 102, 100, 99, 101, 100, 100]
    )

    resultado = calcular_pp_ppk(
        valores,
        lsl=90,
        usl=110,
    )

    assert resultado["pp"] is not None
    assert resultado["ppk"] is not None
    assert resultado["n"] == 10
    assert resultado["clasificacion"] in {
        "Capaz (excelente)",
        "Marginal (monitorear)",
        "No capaz (acción requerida)",
    }


def test_pp_ppk_datos_insuficientes():
    resultado = calcular_pp_ppk(
        pd.Series([100]),
        lsl=90,
        usl=110,
    )

    assert resultado["pp"] is None
    assert resultado["ppk"] is None
    assert resultado["clasificacion"] == "Datos insuficientes"


def test_pp_ppk_limites_invalidos():
    resultado = calcular_pp_ppk(
        pd.Series([1, 2, 3]),
        lsl=110,
        usl=90,
    )

    assert resultado["pp"] is None
    assert resultado["ppk"] is None
    assert resultado["clasificacion"] == "Límites inválidos"


def test_pp_ppk_sin_variabilidad():
    resultado = calcular_pp_ppk(
        pd.Series([100, 100, 100]),
        lsl=90,
        usl=110,
    )

    assert resultado["pp"] == float("inf")
    assert resultado["ppk"] == float("inf")
    assert resultado["clasificacion"] == "Sin variabilidad"


def test_pp_ppk_descentrado_penaliza():
    valores = pd.Series(
        [104, 105, 106, 105, 104, 105, 106, 105]
    )

    resultado = calcular_pp_ppk(
        valores,
        lsl=90,
        usl=110,
    )

    assert resultado["ppk"] < resultado["pp"]


def test_pp_ppk_fuera_de_especificacion_sin_variabilidad():
    resultado = calcular_pp_ppk(
        pd.Series([120, 120, 120]),
        lsl=90,
        usl=110,
    )

    assert resultado["pp"] == float("inf")
    assert resultado["ppk"] == float("-inf")
    assert resultado["clasificacion"] == "No capaz (fuera de especificación)"


def test_pp_ppk_ignora_valores_no_validos():
    valores = pd.Series(
        [99, 100, "101", None, float("inf"), 102]
    )

    resultado = calcular_pp_ppk(
        valores,
        lsl=90,
        usl=110,
    )

    assert resultado["n"] == 4
    assert resultado["pp"] is not None
    assert resultado["ppk"] is not None


def test_resumen_capacidad():
    df = pd.DataFrame(
        {
            "peso": [98, 100, 102, 99, 101] * 10,
        }
    )

    config = {
        "peso": {
            "nombre": "Peso",
            "lsl": 90,
            "usl": 110,
        }
    }

    resultado = resumen_capacidad(df, config)

    assert len(resultado) == 1
    assert resultado.iloc[0]["variable"] == "Peso"
    assert resultado.iloc[0]["columna"] == "peso"


def test_resumen_capacidad_falla_si_falta_columna():
    df = pd.DataFrame({"peso": [98, 100, 102]})

    config = {
        "longitud": {
            "nombre": "Longitud",
            "lsl": 90,
            "usl": 110,
        }
    }

    with pytest.raises(ValueError, match="no existe"):
        resumen_capacidad(df, config)


def test_resumen_capacidad_falla_si_dataset_vacio():
    df = pd.DataFrame()

    config = {
        "peso": {
            "nombre": "Peso",
            "lsl": 90,
            "usl": 110,
        }
    }

    with pytest.raises(ValueError, match="vacío"):
        resumen_capacidad(df, config)


def test_calcular_pp_ppk_accepts_list_input():
    result = calcular_pp_ppk([499, 500, 501, 500], lsl=490, usl=510)
    assert result["n"] == 4


def test_calcular_pp_ppk_rejects_invalid_limits():
    result = calcular_pp_ppk([499, 500, 501], lsl=float("nan"), usl=510)
    assert result["clasificacion"] == "Límites inválidos"


def test_calcular_pp_ppk_marginal_classification():
    result = calcular_pp_ppk([497, 498, 502, 503], lsl=490, usl=510)
    assert result["clasificacion"] in {
        "Marginal (monitorear)",
        "Capaz (excelente)",
        "No capaz (acción requerida)",
    }


def test_calcular_pp_ppk_not_capable_classification():
    result = calcular_pp_ppk([480, 481, 482, 483], lsl=490, usl=510)
    assert result["clasificacion"] == "No capaz (acción requerida)"


def test_resumen_capacidad_requires_dataframe():
    try:
        resumen_capacidad([], {})
        raise AssertionError
    except TypeError as exc:
        assert "DataFrame" in str(exc)


def test_resumen_capacidad_requires_configuration_keys():
    df = pd.DataFrame({"peso": [499, 500, 501]})

    try:
        resumen_capacidad(
            df,
            {"peso": {"lsl": 490, "usl": 510}},
        )
        raise AssertionError
    except ValueError as exc:
        assert "nombre" in str(exc)