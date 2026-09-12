

# ---------------------------------------------------------------------
# clasificar_kpis (nuevo — sistema de color semántico del top)
# ---------------------------------------------------------------------


def test_clasificar_kpis_produccion_siempre_neutral():
    from dashboard.kpi_presenter import clasificar_kpis

    resultado = clasificar_kpis({"fpy": 0.5, "tasa_defectos": 0.5, "tasa_scrap": 0.5})

    assert resultado["produccion"] == "neutral"


def test_clasificar_kpis_fpy_es_higher_is_better():
    from dashboard.kpi_presenter import clasificar_kpis

    base = {"tasa_defectos": 0.0, "tasa_scrap": 0.0}

    assert clasificar_kpis({**base, "fpy": 0.97})["fpy"] == "success"
    assert clasificar_kpis({**base, "fpy": 0.92})["fpy"] == "warning"
    assert clasificar_kpis({**base, "fpy": 0.80})["fpy"] == "danger"


def test_clasificar_kpis_defectos_y_scrap_son_lower_is_better():
    from dashboard.kpi_presenter import clasificar_kpis

    base = {"fpy": 1.0}

    resultado_bueno = clasificar_kpis({**base, "tasa_defectos": 0.02, "tasa_scrap": 0.005})
    assert resultado_bueno["defectos"] == "success"
    assert resultado_bueno["scrap"] == "success"

    resultado_malo = clasificar_kpis({**base, "tasa_defectos": 0.08, "tasa_scrap": 0.03})
    assert resultado_malo["defectos"] == "danger"
    assert resultado_malo["scrap"] == "danger"


def test_clasificar_kpis_falla_si_faltan_kpis_numericos():
    import pytest

    from dashboard.kpi_presenter import clasificar_kpis

    with pytest.raises(ValueError, match="Faltan KPI requeridos para clasificar"):
        clasificar_kpis({"fpy": 0.95})
