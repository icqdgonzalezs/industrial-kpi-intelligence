"""Callback de navegación: muestra el contenido de la pestaña activa, oculta el resto.

Los componentes de las demás pestañas permanecen montados (display:none) para
que sus callbacks sigan funcionando sin importar cuál pestaña esté activa —
solo cambia la visibilidad, no el árbol de componentes.
"""

from __future__ import annotations

from dash import Input, Output

from dashboard.app_layout import TABS


def registrar_callbacks_tabs(app) -> None:
    @app.callback(
        [Output(f"{tab_id}-content", "style") for tab_id, _ in TABS],
        Input("tabs-principal", "value"),
    )
    def callback_cambiar_tab(tab_activo):
        return [
            {"display": "block" if tab_id == tab_activo else "none"} for tab_id, _ in TABS
        ]
