"""
Módulo de Lógica de Negocio — Cálculo de tarifas y reportes.
Capa: Lógica de Negocio (Arquitectura en 3 Capas).
"""

from collections import deque


def calcularTarifa(ingresosActuales: float, modalidadEmpleo: str, servicioDeseado: str) -> float:
    """Calcula la tarifa de afiliación según ingresos, modalidad y servicio."""
    tarifaBase = _obtenerTarifaBase(ingresosActuales, modalidadEmpleo)
    ajusteServicio = _obtenerAjusteServicio(ingresosActuales, servicioDeseado)
    return tarifaBase + ajusteServicio


def _obtenerTarifaBase(ingresosActuales: float, modalidadEmpleo: str) -> float:
    """Determina la tarifa base según la modalidad de empleo y el rango de ingresos."""
    if modalidadEmpleo == "Empleado":
        if 1_000_000 <= ingresosActuales < 2_000_000:
            return 45_000
        elif 2_000_000 <= ingresosActuales < 3_000_000:
            return 60_000
        elif 3_000_000 <= ingresosActuales < 4_000_000:
            return 75_000
        elif 4_000_000 <= ingresosActuales < 5_000_000:
            return 90_000
        elif ingresosActuales >= 5_000_000:
            return 150_000

    elif modalidadEmpleo == "Independiente":
        if 1_000_000 <= ingresosActuales < 2_000_000:
            return 10_000
        elif 2_000_000 <= ingresosActuales < 3_000_000:
            return 20_000
        elif 3_000_000 <= ingresosActuales < 4_000_000:
            return 30_000
        elif 4_000_000 <= ingresosActuales < 5_000_000:
            return 40_000
        elif ingresosActuales >= 5_000_000:
            return 80_000

    return 0.0


def _obtenerAjusteServicio(ingresosActuales: float, servicioDeseado: str) -> float:
    """Calcula el ajuste adicional a la tarifa según el servicio deseado."""
    ajustes = {
        "Subsidio de desempleo": 0.0,
        "Ingreso a parque": 2_500.0,
        "Curso de formación": 7_500.0,
        "Paquete de viaje": 10_000.0,
    }
    if servicioDeseado in ajustes:
        return ajustes[servicioDeseado]
    elif servicioDeseado == "Medicina preventiva":
        return ingresosActuales * 0.10
    return 0.0


def obtenerReportePila(pila: list) -> str:
    """Calcula la suma de las tarifas de afiliación de los registros en la Pila."""
    if not pila:
        return "Sin registros"
    totalTarifas = sum(a.tarifaAfiliacion for a in pila)
    return f"Suma de tarifas: ${totalTarifas:,.0f}"


def obtenerReporteCola(cola: deque) -> str:
    """Retorna la cantidad de registros actualmente en la Cola."""
    cantidadRegistros = len(cola)
    if cantidadRegistros == 0:
        return "Sin registros"
    return f"Cantidad de registros: {cantidadRegistros}"


def obtenerReporteLista(lista: list) -> str:
    """Calcula el promedio de los ingresos actuales de los registros en la Lista."""
    if not lista:
        return "Sin registros"
    promedioIngresos = sum(a.ingresosActuales for a in lista) / len(lista)
    return f"Promedio de ingresos: ${promedioIngresos:,.0f}"
