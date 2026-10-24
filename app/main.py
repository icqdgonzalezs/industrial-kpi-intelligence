from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from app.auth import get_current_user, get_current_user_optional
from app.db import create_db_and_tables, get_session
from app.models import KPI, User
from app.routers.anomalies import router as anomalies_router
from app.routers.auth import router as auth_router
from app.routers.chat import router as chat_router
from app.routers.diagnostics import router as diagnostics_router
from app.routers.reports import router as reports_router
from app.schemas import KPICreate
from app.templates_config import templates


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

# CORS: permite que clientes externos (frontends en otros dominios) consuman la API.
# En desarrollo usamos "*"; en producción restringir a dominios específicos.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(diagnostics_router)
app.include_router(reports_router)
app.include_router(anomalies_router) # <-- NUEVO ROUTER


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    """Página de login. Pública."""
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={},
    )


@app.get("/", response_class=HTMLResponse)
def dashboard(
    request: Request,
    session: Session = Depends(get_session),
    current_user: User | None = Depends(get_current_user_optional),
):
    """Dashboard principal. Requiere autenticación.

    Si el usuario no está autenticado, redirige a /login (302).
    No usamos get_current_user (que lanza 401) porque queremos
    redirigir en vez de mostrar un 401 JSON crudo en el navegador.
    """
    if current_user is None:
        return RedirectResponse(url="/login", status_code=302)

    kpis = session.exec(select(KPI)).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"kpis": kpis, "user": current_user},
    )


@app.get("/kpis/", response_model=list[KPI])
def get_kpis(session: Session = Depends(get_session)) -> list[KPI]:
    """Lista de KPIs. Público (mismo criterio que /auth/login)."""
    return session.exec(select(KPI)).all()


@app.post("/kpis/", response_model=KPI, status_code=201)
def create_kpi(
    kpi_data: KPICreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> KPI:
    """Crea un KPI. Requiere autenticación."""
    kpi = KPI(**kpi_data.model_dump())
    session.add(kpi)
    session.commit()
    session.refresh(kpi)
    return kpi