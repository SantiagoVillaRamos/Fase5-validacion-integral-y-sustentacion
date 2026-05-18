"""
Puerto de ENTRADA: NominaServicePort
Define el contrato que el núcleo de aplicación expone hacia el exterior.
Los adaptadores de entrada (UI, CLI, API REST, etc.) invocan esta interfaz
sin conocer la implementación del servicio.
"""
from abc import ABC, abstractmethod
from domain.entities.empleado import Empleado


class NominaServicePort(ABC):
    """
    Puerto de entrada (Input Port / Driving Port).
    Expone los casos de uso del sistema de nómina.
    """

    @abstractmethod
    def registrar_empleado(self, nombre: str, descripcion_cargo: str, dias_trabajados: int) -> Empleado:
        """
        Caso de uso: registrar un nuevo empleado en el sistema.
        Retorna la entidad Empleado creada y persistida.
        """
        ...

    @abstractmethod
    def calcular_pago(self, nombre: str, descripcion_cargo: str, dias_trabajados: int) -> int:
        """
        Caso de uso: calcular el pago de un empleado sin persistirlo.
        Útil para previsualizar el monto antes de guardar.
        """
        ...

    @abstractmethod
    def obtener_todos_los_empleados(self) -> list[Empleado]:
        """
        Caso de uso: obtener la lista completa de empleados registrados.
        """
        ...

    @abstractmethod
    def generar_reporte(self) -> str:
        """
        Caso de uso: disparar la generación del reporte de nómina.
        Retorna un mensaje con el resultado.
        """
        ...
