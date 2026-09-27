# app/templates_config.py
"""Configuración compartida de Jinja2Templates.

Centraliza la instanciación de Jinja2Templates para que main.py y los
routers compartan un único objeto. Evita duplicar el directorio base
y mantener dos caches de templates.
"""
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
