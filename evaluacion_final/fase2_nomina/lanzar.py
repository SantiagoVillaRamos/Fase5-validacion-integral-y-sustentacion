"""
Fase 2 — Sistema de Nómina Constructora Mejor.
Punto de entrada adaptado para la aplicación integradora.
Lanza la UI directamente sin login propio.
"""

import sys
import os

# Asegura que el directorio de fase2_nomina esté en el path
_BASE = os.path.dirname(__file__)
if _BASE not in sys.path:
    sys.path.insert(0, _BASE)


def lanzar(master) -> None:
    """
    Abre la ventana de la Fase 2 como Toplevel sobre el master dado.
    Al cerrarla, el master (menú principal) queda visible de nuevo.
    """
    from infrastructure.adapters.output.in_memory_repository import InMemoryRepository
    from infrastructure.adapters.output.txt_reporte_adapter import TxtReporteAdapter
    from application.services.nomina_service import NominaService
    from infrastructure.adapters.input.tkinter_adapter import TkinterAdapter

    repositorio = InMemoryRepository()
    generador_reporte = TxtReporteAdapter(ruta_archivo="reporte_nomina.txt")
    servicio = NominaService(
        repositorio=repositorio,
        generador_reporte=generador_reporte,
    )

    app = TkinterAdapter(servicio=servicio, master=master)
    app.ejecutar()
