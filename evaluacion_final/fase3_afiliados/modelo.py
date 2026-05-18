from collections import deque


class EstructuraDatosAfiliado:
    """Clase que representa los datos de un afiliado de la Caja Compensándote."""

    def __init__(self, tipoIdentificacion: str, numeroIdentificacion: str,
                 nombreCompleto: str, ingresosActuales: float,
                 servicioDeseado: str, modalidadEmpleo: str,
                 tarifaAfiliacion: float, fechaAfiliacion: str):
        self.tipoIdentificacion = tipoIdentificacion
        self.numeroIdentificacion = numeroIdentificacion
        self.nombreCompleto = nombreCompleto
        self.ingresosActuales = ingresosActuales
        self.servicioDeseado = servicioDeseado
        self.modalidadEmpleo = modalidadEmpleo
        self.tarifaAfiliacion = tarifaAfiliacion
        self.fechaAfiliacion = fechaAfiliacion

    def aLista(self) -> tuple:
        """Retorna los atributos del afiliado como tupla para el Treeview."""
        return (
            self.tipoIdentificacion,
            self.numeroIdentificacion,
            self.nombreCompleto,
            f"${self.ingresosActuales:,.0f}",
            self.servicioDeseado,
            self.modalidadEmpleo,
            f"${self.tarifaAfiliacion:,.0f}",
            self.fechaAfiliacion
        )


class GestorEstructuras:
    """Gestiona las tres estructuras de datos: Pila, Cola y Lista."""

    def __init__(self):
        self.pila = []           # Estructura Pila — LIFO (list)
        self.cola = deque()      # Estructura Cola — FIFO (collections.deque)
        self.lista = []          # Estructura Lista — orden de inserción (list)

    # --- PILA ---
    def apilar(self, afiliado: EstructuraDatosAfiliado):
        """Apila un afiliado en la cima de la Pila (push)."""
        self.pila.append(afiliado)

    def desapilar(self):
        """Desapila y retorna el último afiliado de la Pila (pop)."""
        if self.pila:
            return self.pila.pop()
        return None

    def obtenerPila(self) -> list:
        """Retorna una copia de la pila actual."""
        return list(self.pila)

    # --- COLA ---
    def encolar(self, afiliado: EstructuraDatosAfiliado):
        """Encola un afiliado al final de la Cola."""
        self.cola.append(afiliado)

    def desencolar(self):
        """Desencola y retorna el primer afiliado de la Cola."""
        if self.cola:
            return self.cola.popleft()
        return None

    def obtenerCola(self) -> list:
        """Retorna la cola actual como lista."""
        return list(self.cola)

    # --- LISTA ---
    def agregarALista(self, afiliado: EstructuraDatosAfiliado):
        """Agrega un afiliado al final de la Lista."""
        self.lista.append(afiliado)

    def eliminarDeLista(self, numeroId: str) -> bool:
        """Elimina un afiliado de la Lista por número de identificación."""
        for i, afiliado in enumerate(self.lista):
            if afiliado.numeroIdentificacion == numeroId:
                self.lista.pop(i)
                return True
        return False

    def buscarEnLista(self, numeroId: str) -> bool:
        """Verifica si un afiliado existe en la Lista."""
        return any(a.numeroIdentificacion == numeroId for a in self.lista)

    def obtenerLista(self) -> list:
        """Retorna una copia de la lista actual."""
        return list(self.lista)
