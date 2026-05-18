"""
Fase 4 — Árbol Binario de Búsqueda.
Punto de entrada adaptado para el proyecto integrador.
Lanza MainWindow directamente sin login propio.
"""

import sys
import os

_BASE = os.path.dirname(__file__)
if _BASE not in sys.path:
    sys.path.insert(0, _BASE)


def lanzar(master) -> None:
    """
    Abre la MainWindow de la Fase 4 como Toplevel sobre el master dado.
    Al cerrarla, el menú principal reaparece.
    """
    from controllers.controlador import Controlador
    from views.main_window import MainWindow

    ctrl = Controlador()
    ventana = MainWindow(master, ctrl)
    master.withdraw()
    master.wait_window(ventana)
    master.deiconify()
