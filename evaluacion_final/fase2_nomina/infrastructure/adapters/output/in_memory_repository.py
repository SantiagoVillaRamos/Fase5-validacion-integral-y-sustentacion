"""
Adaptador de SALIDA: InMemoryRepository
Implementa el puerto EmpleadoRepositoryPort usando una lista en memoria.
Es intercambiable por cualquier otra implementación (SQLite, JSON, CSV)
sin modificar el dominio ni la capa de aplicación.
"""
from domain.entities.empleado import Empleado
from domain.ports.output.empleado_repository_port import EmpleadoRepositoryPort


class InMemoryRepository(EmpleadoRepositoryPort):
    """
    Adaptador de salida que implementa el repositorio de empleados en memoria.
    Usa una lista de Python como estructura de datos interna.
    """

    def __init__(self) -> None:
        self._empleados: list[Empleado] = []

    def guardar(self, empleado: Empleado) -> None:
        """
        Agrega el empleado a la lista interna.
        Implementa el contrato definido en EmpleadoRepositoryPort.
        """
        self._empleados.append(empleado)

    def obtener_todos(self) -> list[Empleado]:
        """
        Retorna una copia de la lista de empleados para evitar
        modificaciones externas directas al estado interno.
        """
        return list(self._empleados)
