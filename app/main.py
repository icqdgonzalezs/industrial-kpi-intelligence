from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlmodel import Session, select

from app.db import create_db_and_tables, get_session
from app.models import KPI
from app.schemas import KPICreate


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/kpis/", response_model=list[KPI])
def get_kpis(session: Session = Depends(get_session)) -> list[KPI]:
    return session.exec(select(KPI)).all()


@app.post("/kpis/", response_model=KPI, status_code=201)
def create_kpi(kpi_data: KPICreate, session: Session = Depends(get_session)) -> KPI:
    # Convertimos el schema Pydantic al modelo SQLModel (tabla)
    kpi = KPI(**kpi_data.model_dump())
    session.add(kpi)
    session.commit()
    session.refresh(kpi)
    return kpi


