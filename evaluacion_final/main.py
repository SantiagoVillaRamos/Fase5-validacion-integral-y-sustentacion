"""
Evaluación Final — Punto de entrada principal.
Arranca el login centralizado. Contraseña: 8246
"""

import sys
import os

# Asegura que el directorio raíz de evaluacion_final esté en el path
_ROOT = os.path.dirname(__file__)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from login_window import LoginWindow


def main() -> None:
    app = LoginWindow()
    app.ejecutar()


if __name__ == "__main__":
    main()
