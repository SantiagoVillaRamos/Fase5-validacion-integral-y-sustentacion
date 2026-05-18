from models.nodo import Nodo


class ArbolBinarioBusqueda:
    """
    Binary Search Tree with a maximum depth of 4 levels.
    Supports insert, search, clear, and the three standard traversals.
    """

    MAX_NIVELES: int = 4

    def __init__(self) -> None:
        self.raiz: Nodo | None = None

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def insertar(self, valor: int) -> None:
        """
        Insert an integer value into the BST.

        Raises:
            ValueError:    Value already exists in the tree.
            OverflowError: Insertion would exceed MAX_NIVELES.
        """
        nivel = self._nivel_insercion(valor)        # raises ValueError if duplicate
        if nivel > self.MAX_NIVELES:
            raise OverflowError(
                f"No es posible agregar el nodo {valor}.\n"
                f"Se alcanzó el nivel máximo permitido ({self.MAX_NIVELES} niveles)."
            )
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_rec(self.raiz, valor)

    def buscar(self, valor: int) -> bool:
        """Return True if value exists in the tree, False otherwise."""
        return self._buscar_rec(self.raiz, valor)

    def limpiar(self) -> None:
        """Remove all nodes from the tree."""
        self.raiz = None

    def esta_vacio(self) -> bool:
        return self.raiz is None

    def inorden(self) -> list:
        """Left → Root → Right traversal (produces sorted sequence)."""
        result: list = []
        self._inorden_rec(self.raiz, result)
        return result

    def preorden(self) -> list:
        """Root → Left → Right traversal."""
        result: list = []
        self._preorden_rec(self.raiz, result)
        return result

    def posorden(self) -> list:
        """Left → Right → Root traversal."""
        result: list = []
        self._posorden_rec(self.raiz, result)
        return result

    def altura(self) -> int:
        """Current height of the tree (root counts as level 1)."""
        return self._altura_rec(self.raiz)

    def contar_nodos(self) -> int:
        return self._contar_rec(self.raiz)

    # ------------------------------------------------------------------ #
    #  Private helpers                                                     #
    # ------------------------------------------------------------------ #

    def _nivel_insercion(self, valor: int) -> int:
        """
        Calculate what level a new value would occupy.
        Raises ValueError if the value already exists.
        """
        nodo, nivel = self.raiz, 1
        while nodo is not None:
            if valor < nodo.valor:
                nodo, nivel = nodo.izquierdo, nivel + 1
            elif valor > nodo.valor:
                nodo, nivel = nodo.derecho, nivel + 1
            else:
                raise ValueError(f"El valor {valor} ya existe en el árbol.")
        return nivel

    def _insertar_rec(self, nodo: Nodo, valor: int) -> None:
        if valor < nodo.valor:
            if nodo.izquierdo is None:
                nodo.izquierdo = Nodo(valor)
            else:
                self._insertar_rec(nodo.izquierdo, valor)
        else:
            if nodo.derecho is None:
                nodo.derecho = Nodo(valor)
            else:
                self._insertar_rec(nodo.derecho, valor)

    def _buscar_rec(self, nodo: Nodo | None, valor: int) -> bool:
        if nodo is None:
            return False
        if valor == nodo.valor:
            return True
        if valor < nodo.valor:
            return self._buscar_rec(nodo.izquierdo, valor)
        return self._buscar_rec(nodo.derecho, valor)

    def _inorden_rec(self, nodo: Nodo | None, result: list) -> None:
        if nodo:
            self._inorden_rec(nodo.izquierdo, result)
            result.append(nodo.valor)
            self._inorden_rec(nodo.derecho, result)

    def _preorden_rec(self, nodo: Nodo | None, result: list) -> None:
        if nodo:
            result.append(nodo.valor)
            self._preorden_rec(nodo.izquierdo, result)
            self._preorden_rec(nodo.derecho, result)

    def _posorden_rec(self, nodo: Nodo | None, result: list) -> None:
        if nodo:
            self._posorden_rec(nodo.izquierdo, result)
            self._posorden_rec(nodo.derecho, result)
            result.append(nodo.valor)

    def _altura_rec(self, nodo: Nodo | None) -> int:
        if nodo is None:
            return 0
        return 1 + max(self._altura_rec(nodo.izquierdo),
                       self._altura_rec(nodo.derecho))

    def _contar_rec(self, nodo: Nodo | None) -> int:
        if nodo is None:
            return 0
        return 1 + self._contar_rec(nodo.izquierdo) + self._contar_rec(nodo.derecho)
