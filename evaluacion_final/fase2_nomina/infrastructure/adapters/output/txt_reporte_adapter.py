"""
Adaptador de SALIDA: TxtReporteAdapter
Implementa el puerto ReportePort generando un archivo .txt con el reporte.
Gracias al puerto, el servicio de aplicación no sabe si el reporte
se exporta a TXT, PDF, email u otro medio.
"""
import os
from datetime import datetime
from domain.entities.empleado import Empleado
from domain.ports.output.reporte_port import ReportePort


class TxtReporteAdapter(ReportePort):
    """
    Adaptador de salida que implementa ReportePort.
    Exporta el reporte de nómina a un archivo de texto plano.
    """

    def __init__(self, ruta_archivo: str = "reporte_nomina.txt") -> None:
        self._ruta_archivo = ruta_archivo

    def generar(self, empleados: list[Empleado]) -> str:
        """
        Genera el archivo reporte_nomina.txt.
        Implementa el contrato definido en ReportePort.
        """
        if not empleados:
            return "⚠️ No hay empleados registrados para generar el reporte."

        total_nomina = sum(e.calcular_pago() for e in empleados)
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        lineas = [
            "=" * 50,
            "        REPORTE DE NÓMINA - CONSTRUCTORA MEJOR",
            f"        Generado el: {timestamp}",
            "=" * 50,
            "",
        ]

        for i, emp in enumerate(empleados, start=1):
            lineas += [
                f"  Empleado #{i}",
                f"    Nombre          : {emp.nombre}",
                f"    Cargo           : {emp.cargo.descripcion}",
                f"    Días trabajados : {emp.dias_trabajados}",
                f"    Salario diario  : ${emp.cargo.get_salario_diario():,}",
                f"    Total a pagar   : ${emp.calcular_pago():,}",
                "  " + "-" * 44,
            ]

        lineas += [
            "",
            f"  TOTAL NÓMINA: ${total_nomina:,}",
            f"  Empleados:    {len(empleados)}",
            "=" * 50,
        ]

        contenido = "\n".join(lineas)

        with open(self._ruta_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)

        ruta_absoluta = os.path.abspath(self._ruta_archivo)
        return f"✅ Reporte exportado correctamente en:\n{ruta_absoluta}"
