"""
Entidad de dominio: Empleado
Contiene la lógica de negocio pura. No depende de ningún framework,
base de datos ni UI. Es el corazón de la arquitectura hexagonal.
"""
from domain.entities.cargo import Cargo


class Empleado:
    """
    Representa un empleado de la constructora.
    Encapsula su nombre, cargo asignado y días trabajados.
    Contiene la regla de negocio para calcular su pago total.
    """

    def __init__(self, nombre: str, cargo: Cargo, dias_trabajados: int):
        self._validar(nombre, dias_trabajados)
        self._nombre = nombre
        self._cargo = cargo
        self._dias_trabajados = dias_trabajados

    # ------------------------------------------------------------------ #
    # Validaciones de dominio
    # ------------------------------------------------------------------ #

    @staticmethod
    def _validar(nombre: str, dias_trabajados: int) -> None:
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del empleado no puede estar vacío.")
        if not isinstance(dias_trabajados, int) or dias_trabajados <= 0:
            raise ValueError("Los días trabajados deben ser un entero positivo.")

    # ------------------------------------------------------------------ #
    # Lógica de negocio
    # ------------------------------------------------------------------ #

    def calcular_pago(self) -> int:
        """
        Regla de negocio: pago = salario_diario_del_cargo × días_trabajados.
        Retorna el total a pagar en pesos.
        """
        return self._cargo.get_salario_diario() * self._dias_trabajados

    # ------------------------------------------------------------------ #
    # Propiedades (acceso de solo lectura)
    # ------------------------------------------------------------------ #

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def cargo(self) -> Cargo:
        return self._cargo

    @property
    def dias_trabajados(self) -> int:
        return self._dias_trabajados

    # ------------------------------------------------------------------ #
    # Representación
    # ------------------------------------------------------------------ #

    def __repr__(self) -> str:
        return (
            f"Empleado(nombre='{self._nombre}', "
            f"cargo={self._cargo.descripcion}, "
            f"dias={self._dias_trabajados}, "
            f"pago=${self.calcular_pago():,})"
        )
