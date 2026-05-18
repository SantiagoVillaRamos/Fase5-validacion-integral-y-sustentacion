"""
Entidad de dominio: Cargo
Representa los cargos disponibles en la constructora con su respectivo salario diario.
Uso de Enum asegura que solo existan cargos válidos en el dominio.
"""
from enum import Enum


class Cargo(Enum):
    """
    Enumeración de cargos de la constructora.
    Cada cargo tiene asociado un salario diario en pesos.
    """
    INGENIERO = ("Ingeniero", 200_000)
    ARQUITECTO = ("Arquitecto", 180_000)
    MAESTRO_DE_OBRA = ("Maestro de obra", 120_000)
    OBRERO = ("Obrero", 80_000)

    def __init__(self, descripcion: str, salario_diario: int):
        self.descripcion = descripcion
        self.salario_diario = salario_diario

    def get_salario_diario(self) -> int:
        """Retorna el salario diario del cargo."""
        return self.salario_diario

    def __str__(self) -> str:
        return self.descripcion

    @classmethod
    def desde_descripcion(cls, descripcion: str) -> "Cargo":
        """
        Busca un Cargo por su descripción textual.
        Lanza ValueError si no se encuentra.
        """
        for cargo in cls:
            if cargo.descripcion == descripcion:
                return cargo
        raise ValueError(f"Cargo no reconocido: '{descripcion}'")

    @classmethod
    def listar_descripciones(cls) -> list:
        """Retorna la lista de descripciones de todos los cargos."""
        return [cargo.descripcion for cargo in cls]
