"""
Capa de Aplicación: NominaService
Implementa el puerto de entrada NominaServicePort.
Orquesta los casos de uso coordinando las entidades del dominio
y los puertos de salida (repositorio y generador de reporte).
No conoce detalles de UI ni de almacenamiento concreto.
"""
from domain.entities.cargo import Cargo
from domain.entities.empleado import Empleado
from domain.ports.input.nomina_service_port import NominaServicePort
from domain.ports.output.empleado_repository_port import EmpleadoRepositoryPort
from domain.ports.output.reporte_port import ReportePort


class NominaService(NominaServicePort):
    """
    Servicio de aplicación que implementa el puerto de entrada.
    Recibe sus dependencias por inyección (Dependency Injection),
    cumpliendo con el principio de Inversión de Dependencias (SOLID-D).
    """

    def __init__(
        self,
        repositorio: EmpleadoRepositoryPort,
        generador_reporte: ReportePort,
    ) -> None:
        """
        Args:
            repositorio: Puerto de salida para persistencia de empleados.
            generador_reporte: Puerto de salida para generación de reportes.
        """
        self._repositorio = repositorio
        self._generador_reporte = generador_reporte

    # ------------------------------------------------------------------ #
    # Casos de uso (implementación del puerto de entrada)
    # ------------------------------------------------------------------ #

    def registrar_empleado(
        self, nombre: str, descripcion_cargo: str, dias_trabajados: int
    ) -> Empleado:
        """
        Caso de uso: crear y persistir un nuevo empleado.
        Convierte el input crudo en entidades del dominio y delega la persistencia.
        """
        cargo = Cargo.desde_descripcion(descripcion_cargo)
        empleado = Empleado(nombre, cargo, dias_trabajados)
        self._repositorio.guardar(empleado)
        return empleado

    def calcular_pago(
        self, nombre: str, descripcion_cargo: str, dias_trabajados: int
    ) -> int:
        """
        Caso de uso: calcular el pago sin persistir.
        Crea una entidad temporal y usa su lógica de negocio.
        """
        cargo = Cargo.desde_descripcion(descripcion_cargo)
        empleado_temporal = Empleado(nombre, cargo, dias_trabajados)
        return empleado_temporal.calcular_pago()

    def obtener_todos_los_empleados(self) -> list[Empleado]:
        """
        Caso de uso: consultar todos los empleados registrados.
        Delega la consulta al repositorio a través del puerto de salida.
        """
        return self._repositorio.obtener_todos()

    def generar_reporte(self) -> str:
        """
        Caso de uso: generar el reporte de nómina.
        Delega al generador de reporte a través del puerto de salida.
        """
        empleados = self._repositorio.obtener_todos()
        return self._generador_reporte.generar(empleados)
