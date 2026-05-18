class Nodo:
    """Represents a single node in a Binary Search Tree."""

    def __init__(self, valor: int):
        """
        Initialize a node with an integer value.

        Args:
            valor: Integer value stored in this node.
        """
        self.valor: int = valor
        self.izquierdo: "Nodo | None" = None
        self.derecho: "Nodo | None" = None

    def __repr__(self) -> str:
        return f"Nodo({self.valor})"
