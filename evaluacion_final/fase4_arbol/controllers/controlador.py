from models.arbol_binario import ArbolBinarioBusqueda


class Controlador:
    """
    Mediator between the View and the Model.
    Validates user input and delegates all BST operations.
    """

    CONTRASENA: str = "ARBOL"

    def __init__(self) -> None:
        self.arbol: ArbolBinarioBusqueda = ArbolBinarioBusqueda()
        self.nodo_buscado: int | None = None

    # ------------------------------------------------------------------ #
    #  Authentication                                                      #
    # ------------------------------------------------------------------ #

    def verificar_contrasena(self, texto: str) -> bool:
        """Return True if the password matches the generic password."""
        return texto.strip() == self.CONTRASENA

    # ------------------------------------------------------------------ #
    #  Tree operations                                                     #
    # ------------------------------------------------------------------ #

    def agregar_nodo(self, texto: str) -> dict:
        """
        Validate input and insert a node.

        Returns a result dict:
            success   (bool)
            tipo_error (str) – 'tipo' | 'duplicado' | 'nivel' (on failure)
            message   (str)
            traversals (dict) – present only on success
        """
        try:
            valor = int(texto.strip())
        except ValueError:
            return {
                "success": False,
                "tipo_error": "tipo",
                "message": (
                    f'El valor "{texto}" no es un número entero válido.\n'
                    "Por favor ingrese únicamente números enteros."
                ),
            }

        try:
            self.arbol.insertar(valor)
            self.nodo_buscado = None
            return {
                "success": True,
                "message": f"Nodo {valor} agregado correctamente.",
                "traversals": self._traversals(),
            }
        except ValueError as exc:
            return {"success": False, "tipo_error": "duplicado", "message": str(exc)}
        except OverflowError as exc:
            return {"success": False, "tipo_error": "nivel", "message": str(exc)}

    def buscar_nodo(self, texto: str) -> dict:
        """
        Validate input and search for a node.

        Returns a result dict:
            success    (bool)
            encontrado (bool)
            tipo_error (str) – present on failure
            valor      (int) – parsed value
            message    (str)
        """
        try:
            valor = int(texto.strip())
        except ValueError:
            return {
                "success": False,
                "tipo_error": "tipo",
                "message": (
                    f'El valor "{texto}" no es un número entero válido.\n'
                    "Por favor ingrese únicamente números enteros."
                ),
            }

        if self.arbol.esta_vacio():
            return {
                "success": False,
                "tipo_error": "vacio",
                "message": "El árbol está vacío. Agregue nodos primero.",
            }

        encontrado = self.arbol.buscar(valor)
        self.nodo_buscado = valor if encontrado else None
        return {
            "success": encontrado,
            "encontrado": encontrado,
            "valor": valor,
            "message": (
                f"✔ El nodo {valor} fue encontrado en el árbol."
                if encontrado
                else f"✘ El nodo {valor} no existe en el árbol."
            ),
        }

    def limpiar(self) -> None:
        """Clear the entire tree."""
        self.arbol.limpiar()
        self.nodo_buscado = None

    # ------------------------------------------------------------------ #
    #  Accessors                                                           #
    # ------------------------------------------------------------------ #

    def get_arbol(self) -> ArbolBinarioBusqueda:
        return self.arbol

    def get_nodo_buscado(self) -> int | None:
        return self.nodo_buscado

    def get_traversals(self) -> dict:
        return self._traversals()

    def _traversals(self) -> dict:
        return {
            "preorden": self.arbol.preorden(),
            "inorden": self.arbol.inorden(),
            "posorden": self.arbol.posorden(),
        }
