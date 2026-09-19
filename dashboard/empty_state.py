"""Componente SSOT para estados vacíos del dashboard (Fase 3b.2).

Un empty state aparece cuando un filtro deja 0 filas en el dataset
filtrado. En vez de mostrar KPIs en "—", gráficos vacíos y mensajes
sueltos por cada tab, mostramos un único bloque consistente:

    📭
    Sin datos para el período seleccionado
    Ajustá los filtros o tocá "Restaurar filtros".

Diseño (ISA-101 HMI):
  - Icono grande pero discreto (opacidad reducida) para no competir
    con el resto del dashboard.
  - Mensaje principal en color primario (lectura a 1m).
  - Hint secundario en color muted, con la acción sugerida.

Uso típico en un callback:
    if filtrado.empty:
        return empty_state("Sin datos para el período seleccionado")

El componente usa las clases CSS del sistema de diseño:
  .empty-state          → contenedor (card con padding generoso)
  .empty-state-icon     → icono emoji
  .empty-state-message  → texto principal
  .empty-state-hint     → texto secundario (acción sugerida)
"""

from __future__ import annotations

from dash import html

# Icono default: buzón vacío. Se puede overridear por un icono más
# específico del dominio si el mensaje lo requiere.
ICONO_DEFAULT = "📭"


def empty_state(
    mensaje: str,
    hint: str | None = None,
    icono: str = ICONO_DEFAULT,
) -> html.Div:
    """Construye un bloque de estado vacío consistente para el dashboard.

    Parameters
    ----------
    mensaje : str
        Texto principal, describe QUÉ falta (ej: "Sin datos para el
        período seleccionado").
    hint : str | None
        Texto secundario con la acción sugerida (ej: "Ajustá los filtros
        o tocá Restaurar"). Si es None, no se muestra.
    icono : str
        Emoji o carácter Unicode para el icono. Default: buzón vacío.

    Returns
    -------
    html.Div
        Estructura HTML con las clases del sistema de diseño. Lista
        para ser devuelta directamente desde un callback como children
        de un contenedor.
    """
    children: list = [
        html.Div(icono, className="empty-state-icon"),
        html.Div(mensaje, className="empty-state-message"),
    ]

    if hint is not None:
        children.append(html.Div(hint, className="empty-state-hint"))

    return html.Div(children, className="empty-state")
