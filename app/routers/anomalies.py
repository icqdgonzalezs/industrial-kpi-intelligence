import json

from fastapi import APIRouter, Depends, Query, Request, Response
from fastapi.templating import Jinja2Templates

from app.auth import get_current_user
from app.limiter import rate_limit
from app.schemas import Anomalia
from app.services.anomaly_detector import detectar_anomalias
from app.services.dataset_loader import cargar_dataset_filtrado

router = APIRouter(prefix="/anomalies", tags=["Anomalías"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
@rate_limit(max_requests=30, window_seconds=60)
async def detectar(
    request: Request,
    kpi: str = Query(..., description="KPI a analizar (ej. oee, ppm, cpk)"),
    linea: str | None = Query(None, description="Línea de producción (opcional)"),
    current_user: dict = Depends(get_current_user)  # noqa: B008
) -> Response:
    """Endpoint para detección de anomalías estadísticas."""
    
    # 1. Cargar datos filtrados
    df, _ = cargar_dataset_filtrado(linea=linea)
    
    # 2. Detectar anomalías (lista de dicts)
    resultados_raw = detectar_anomalias(df, columna_kpi=kpi, columna_linea="linea")
    
    # 3. Validar con Pydantic
    anomalias = [Anomalia(**r) for r in resultados_raw]
    
    # 4. Respuesta polimórfica (HTML para HTMX, JSON para API)
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            request=request,
            name="partials/_anomalies_response.html",
            context={"anomalias": anomalias}
        )
    return Response(content=json.dumps([a.model_dump() for a in anomalias]), media_type="application/json")
