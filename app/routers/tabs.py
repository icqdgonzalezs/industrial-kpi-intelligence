from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.auth import get_current_user
from app.services.dataset_loader import cargar_dataset_filtrado
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

    # Reutilizamos la lógica pura de src/ (SSOT)
    hallazgos = generar_diagnostico(df, config) if not df.empty else []

    return templates.TemplateResponse(
        request=request,
        name="partials/_tab_diagnostics.html",
        context={"hallazgos": hallazgos},
    )
