"""
Puerto de SALIDA: ReportePort
Define el contrato para generar reportes de nómina.
Permite cambiar el destino del reporte (TXT, PDF, pantalla, email)
sin modificar la lógica de negocio.
"""
from abc import ABC, abstractmethod


class ReportePort(ABC):
    """
    Puerto de salida (Output Port) para la generación de reportes.
    El servicio de aplicación invoca este puerto sin conocer el formato concreto.
    """

    @abstractmethod
    def generar(self, empleados: list) -> str:
        """
        Genera el reporte de nómina para la lista de empleados.
        Retorna un mensaje informando el resultado de la operación.
        """
        ...
