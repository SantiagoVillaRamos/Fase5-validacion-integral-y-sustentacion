"""
Fase 3 — Control de Afiliados Compensándote.
Punto de entrada adaptado para el proyecto integrador.
Lanza el FormularioPrincipal directamente sin login propio.
"""

import sys
import os

_BASE = os.path.dirname(__file__)
if _BASE not in sys.path:
    sys.path.insert(0, _BASE)


def lanzar(master) -> None:
    """
    Abre el FormularioPrincipal de la Fase 3 como Toplevel
    sobre el master dado. Al cerrarlo, el menú principal reaparece.
    """
    from main_form import FormularioPrincipal
    app = FormularioPrincipal(master=master)
    app.ejecutar()
