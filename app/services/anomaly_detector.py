import pandas as pd


def _detectar_zscore(serie: pd.Series, umbral: float = 3.0) -> list[dict]:
    """Detecta outliers usando z-score sobre una serie temporal o agrupada."""
    if len(serie) < 5:
        return []
    
    media = serie.mean()
    std = serie.std()
    
    if std == 0 or pd.isna(std):
        return []
        
    z_scores = (serie - media) / std
    anomalias = []
    
    for idx, z in z_scores.items():
        if abs(z) > umbral:
            anomalias.append({
                "metodo": "zscore",
                "valor": float(serie[idx]),
                "esperado": float(media),
                "desviacion": float(z),
                "descripcion": f"Valor atípico: {serie[idx]:.2f} (esperado ~{media:.2f}, Z={z:.1f})"
            })
    return anomalias

def _detectar_iqr(serie: pd.Series, factor: float = 1.5) -> list[dict]:
    """Detecta outliers usando el Rango Intercuartílico (IQR)."""
    if len(serie) < 5:
        return []
        
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    iqr = q3 - q1
    
    if iqr == 0:
        return []
        
    limite_inf = q1 - (factor * iqr)
    limite_sup = q3 + (factor * iqr)
    
    anomalias = []
    for _, val in serie.items():
        if val < limite_inf or val > limite_sup:
            anomalias.append({
                "metodo": "iqr",
                "valor": float(val),
                "esperado": float(serie.median()),
                "desviacion": 0.0,
                "descripcion": f"Fuera de rango IQR: {val:.2f} (rango {limite_inf:.2f} - {limite_sup:.2f})"
            })
    return anomalias

def detectar_anomalias(df: pd.DataFrame, columna_kpi: str, columna_linea: str = "linea") -> list[dict]:
    """
    Orquestador principal. Itera por línea para detectar anomalías locales.
    Retorna una lista de dicts lista para ser validada por Pydantic.
    """
    resultados = []
    
    if columna_linea not in df.columns or columna_kpi not in df.columns:
        return []
        
    for linea, grupo in df.groupby(columna_linea):
        # 1. Buscar anomalías por Z-Score
        for a in _detectar_zscore(grupo[columna_kpi]):
            a["kpi"] = columna_kpi
            a["linea"] = str(linea)
            a["severidad"] = "critica" if abs(a["desviacion"]) > 4 else "alta"
            resultados.append(a)
            
        # 2. Buscar anomalías por IQR (solo si Z-Score no las atrapó)
        valores_z_anomalos = {a["valor"] for a in resultados if a["linea"] == str(linea)}
        for a in _detectar_iqr(grupo[columna_kpi]):
            if a["valor"] not in valores_z_anomalos:
                a["kpi"] = columna_kpi
                a["linea"] = str(linea)
                a["severidad"] = "media"
                resultados.append(a)
                
    # Ordenar por severidad (critica > alta > media)
    prioridad = {"critica": 1, "alta": 2, "media": 3, "baja": 4}
    resultados.sort(key=lambda x: prioridad.get(x["severidad"], 5))
    return resultados
