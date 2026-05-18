"""
Punto de entrada: main.py
Responsabilidad única: componer todas las dependencias (Dependency Injection)
y lanzar la aplicación.
Aquí es donde los puertos se conectan con sus adaptadores concretos.
"""
import sys
import os

# Asegura que el directorio raíz del proyecto esté en el path de Python
sys.path.insert(0, os.path.dirname(__file__))

# -- Adaptadores de SALIDA (infraestructura) --
from infrastructure.adapters.output.in_memory_repository import InMemoryRepository
from infrastructure.adapters.output.txt_reporte_adapter import TxtReporteAdapter

# -- Servicio de aplicación --
from application.services.nomina_service import NominaService

# -- Adaptador de ENTRADA (UI) --
from infrastructure.adapters.input.tkinter_adapter import TkinterAdapter


def main() -> None:
    """
    Composición de dependencias (Composition Root).

    Flujo de conexión:
        Adaptadores de salida → NominaService (puerto de entrada)
                                   ↑
                            TkinterAdapter (adaptador de entrada)

    Ninguna capa conoce los detalles de implementación de otra;
    solo se comunican a través de los puertos (interfaces abstractas).
    """
    # 1. Instanciar adaptadores de salida
    repositorio = InMemoryRepository()
    generador_reporte = TxtReporteAdapter(ruta_archivo="reporte_nomina.txt")

    # 2. Inyectar los adaptadores en el servicio de aplicación
    servicio = NominaService(
        repositorio=repositorio,
        generador_reporte=generador_reporte,
    )

    # 3. Inyectar el servicio en el adaptador de entrada y ejecutar
    app = TkinterAdapter(servicio=servicio)
    app.ejecutar()


if __name__ == "__main__":
    main()
