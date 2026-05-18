"""
Puerto de SALIDA: EmpleadoRepositoryPort
Define el contrato que cualquier mecanismo de persistencia debe cumplir.
El dominio solo conoce esta interfaz, nunca la implementación concreta.
"""
from abc import ABC, abstractmethod
from domain.entities.empleado import Empleado


class EmpleadoRepositoryPort(ABC):
    """
    Puerto de salida (Output Port) para la persistencia de empleados.
    Separa el dominio de los detalles de almacenamiento (memoria, BD, archivo, etc.).
    """

    @abstractmethod
    def guardar(self, empleado: Empleado) -> None:
        """Persiste un empleado en el repositorio."""
        ...

    @abstractmethod
    def obtener_todos(self) -> list[Empleado]:
        """Retorna la lista completa de empleados registrados."""
        ...
