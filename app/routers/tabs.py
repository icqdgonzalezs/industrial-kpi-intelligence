from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.auth import get_current_user
from app.services.dataset_loader import cargar_dataset_filtrado
from src.capability import resumen_capacidad
from src.diagnostics import generar_diagnostico

router = APIRouter(prefix="/tabs", tags=["Tabs"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/diagnostics")
async def tab_diagnostics(
    request: Request,
    current_user: dict = Depends(get_current_user),  # noqa: B008
):
    """Tab de Diagnóstico: carga datos, genera hallazgos y renderiza el partial."""
    df, config = cargar_dataset_filtrado()

    if not df.empty:
        # Calculamos la tabla de capacidad (DataFrame) que diagnostics.py necesita
        capacidad = resumen_capacidad(df, config)
        hallazgos = generar_diagnostico(df, capacidad)
    else:
        hallazgos = []

    return templates.TemplateResponse(
        request=request,
        name="partials/_tab_diagnostics.html",
        context={"hallazgos": hallazgos},
    )
