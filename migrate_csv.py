# migrate_csv.py
import pandas as pd
from sqlmodel import Session

from app.db import create_db_and_tables, engine
from app.models import KPI

# 1. Crear las tablas (sin argumentos, como está definido en app/db.py)
create_db_and_tables()

# 2. Leer el CSV
df = pd.read_csv("kpis.csv")

# 3. Insertar filas en la base de datos
with Session(engine) as session:
    for _, row in df.iterrows():
        kpi = KPI(
            nombre=row["nombre"],
            valor=float(row["valor"]),
            unidad=row["unidad"],
            timestamp=pd.to_datetime(row["timestamp"]).to_pydatetime(),
            linea_produccion=row["linea_produccion"]
        )
        session.add(kpi)
    session.commit()

print("✅ Migración completada con éxito.")

