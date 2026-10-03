"""Crea el primer user admin leyendo credenciales de env vars.

Idempotente: si el email ya existe, no hace nada y sale con 0.

Uso local (contra SQLite):
    ADMIN_EMAIL=admin@example.com ADMIN_PASSWORD=xxxxxxxx \
        python scripts/seed_admin.py

Uso contra Railway:
    - Via Console web de Railway (recomendado, ver TRASPASO sección 11).
    - Via Railway CLI: railway run python scripts/seed_admin.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Python agrega scripts/ a sys.path[0] cuando corrés `python scripts/seed_admin.py`,
# NO la raíz del proyecto. Sin esto, `from app.auth import ...` falla con
# ModuleNotFoundError. Insertamos la raíz del proyecto en sys.path antes de
# importar el paquete app.
_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from sqlmodel import Session, select  # noqa: E402

from app.auth import hash_password  # noqa: E402
from app.db import create_db_and_tables, engine  # noqa: E402
from app.models import User  # noqa: E402

MIN_PASSWORD_LEN = 8


def _fail(msg: str) -> None:
    print(f"✗ {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    email = (os.getenv("ADMIN_EMAIL") or "").strip().lower()
    password = os.getenv("ADMIN_PASSWORD") or ""

    if not email:
        _fail("ADMIN_EMAIL es requerido.")
    if not password:
        _fail("ADMIN_PASSWORD es requerido.")
    if len(password) < MIN_PASSWORD_LEN:
        _fail(f"ADMIN_PASSWORD debe tener >= {MIN_PASSWORD_LEN} caracteres.")
    if "@" not in email:
        _fail(f"ADMIN_EMAIL inválido: {email!r}")

    create_db_and_tables()

    with Session(engine) as session:
        existing = session.exec(select(User).where(User.email == email)).first()
        if existing:
            print(f"⏭  User {email} ya existe (id={existing.id}). Skip.")
            return

        user = User(email=email, hashed_password=hash_password(password))
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"✅ User {email} creado (id={user.id}).")


if __name__ == "__main__":
    main()
