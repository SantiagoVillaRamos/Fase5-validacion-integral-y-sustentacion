"""
Evaluación Final — Menú Principal.
Opciones:
  1. Fase 2 — Nómina Constructora Mejor
  2. Fase 3 — Control de Afiliados Compensándote
  3. Fase 4 — Árbol Binario de Búsqueda
  4. Salir
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# ── Paleta ──────────────────────────────────────────────────────────────────
BG        = "#0A0F1E"
HEADER_BG = "#111827"
CARD_BG   = "#1E293B"
BORDER    = "#3B82F6"
TEXT_MAIN = "#F1F5F9"
TEXT_DIM  = "#94A3B8"

OPCIONES = [
    {
        "icono":     "🏗️",
        "titulo":    "Fase 2 — Nómina",
        "subtitulo": "Sistema de Nómina · Constructora Mejor",
        "desc":      "Gestión de empleados: cargos, días trabajados y cálculo de pagos.",
        "color":     "#2563EB",
        "hover":     "#3B82F6",
        "modulo":    "fase2_nomina",
    },
    {
        "icono":     "👥",
        "titulo":    "Fase 3 — Afiliados",
        "subtitulo": "Control de Afiliados · Compensándote",
        "desc":      "Estructuras Pila, Cola y Lista para registro de afiliados.",
        "color":     "#059669",
        "hover":     "#10B981",
        "modulo":    "fase3_afiliados",
    },
    {
        "icono":     "🌳",
        "titulo":    "Fase 4 — Árbol Binario",
        "subtitulo": "Árbol Binario de Búsqueda (BST)",
        "desc":      "Inserción, búsqueda y recorridos Preorden, Inorden y Posorden.",
        "color":     "#7C3AED",
        "hover":     "#8B5CF6",
        "modulo":    "fase4_arbol",
    },
    {
        "icono":     "🚪",
        "titulo":    "Salir",
        "subtitulo": "Cerrar la aplicación",
        "desc":      "Finaliza la ejecución del programa.",
        "color":     "#B91C1C",
        "hover":     "#EF4444",
        "modulo":    None,
    },
]

BASE_DIR = os.path.dirname(__file__)


class MenuPrincipal:
    """Menú principal con 4 opciones para el proyecto integrador."""

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._win = tk.Toplevel(root)
        self._win.title("Evaluación Final — Menú Principal")
        self._win.configure(bg=BG)
        self._win.resizable(False, False)
        self._win.protocol("WM_DELETE_WINDOW", self._salir)
        self._build_ui()
        self._center(560, 680)
        self._root.withdraw()

    # ------------------------------------------------------------------ #
    #  UI                                                                  #
    # ------------------------------------------------------------------ #

    def _build_ui(self) -> None:
        # Header
        hdr = tk.Frame(self._win, bg=HEADER_BG, pady=22)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🎓  Evaluación Final",
                 font=("Helvetica", 20, "bold"),
                 bg=HEADER_BG, fg=TEXT_MAIN).pack()
        tk.Label(hdr, text="Santiago Villa · Estructuras de Datos · UNAD 2026",
                 font=("Helvetica", 9),
                 bg=HEADER_BG, fg=TEXT_DIM).pack(pady=(4, 0))
        tk.Frame(hdr, bg=BORDER, height=3).pack(fill="x", pady=(14, 0))

        # Subtítulo
        tk.Label(self._win,
                 text="Seleccione una aplicación para continuar:",
                 font=("Helvetica", 10),
                 bg=BG, fg=TEXT_DIM).pack(pady=(18, 10))

        # Tarjetas de opciones
        contenido = tk.Frame(self._win, bg=BG)
        contenido.pack(padx=32, pady=(0, 24), fill="both", expand=True)

        for i, op in enumerate(OPCIONES):
            self._crear_tarjeta(contenido, op, i)

    def _crear_tarjeta(self, padre: tk.Frame, op: dict, idx: int) -> None:
        card = tk.Frame(padre, bg=CARD_BG, pady=0, cursor="hand2")
        card.pack(fill="x", pady=6)

        # Barra de color lateral
        barra = tk.Frame(card, bg=op["color"], width=5)
        barra.pack(side="left", fill="y")

        inner = tk.Frame(card, bg=CARD_BG, padx=16, pady=14)
        inner.pack(side="left", fill="both", expand=True)

        # Fila superior: ícono + título + subtítulo
        top = tk.Frame(inner, bg=CARD_BG)
        top.pack(fill="x")
        tk.Label(top, text=op["icono"],
                 font=("Helvetica", 22),
                 bg=CARD_BG, fg=op["color"]).pack(side="left", padx=(0, 10))
        info = tk.Frame(top, bg=CARD_BG)
        info.pack(side="left", fill="x", expand=True)
        tk.Label(info, text=op["titulo"],
                 font=("Helvetica", 12, "bold"),
                 bg=CARD_BG, fg=TEXT_MAIN, anchor="w").pack(fill="x")
        tk.Label(info, text=op["subtitulo"],
                 font=("Helvetica", 8),
                 bg=CARD_BG, fg=TEXT_DIM, anchor="w").pack(fill="x")

        # Descripción
        tk.Label(inner, text=op["desc"],
                 font=("Helvetica", 9),
                 bg=CARD_BG, fg=TEXT_DIM,
                 anchor="w", wraplength=440).pack(fill="x", pady=(6, 0))

        # Eventos hover y click
        widgets = [card, barra, inner, top]

        def on_enter(e, c=card, b=barra, o=op):
            c.config(bg=o["hover"])
            b.config(bg=o["hover"])
            for w in c.winfo_children():
                _cambiar_bg(w, o["hover"])

        def on_leave(e, c=card, b=barra, o=op):
            c.config(bg=CARD_BG)
            b.config(bg=o["color"])
            for w in c.winfo_children():
                _cambiar_bg(w, CARD_BG)

        def on_click(e, o=op):
            self._lanzar(o)

        for w in [card, barra, inner] + list(inner.winfo_children()):
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
            w.bind("<Button-1>", on_click)
        for row_frame in top.winfo_children():
            row_frame.bind("<Enter>", on_enter)
            row_frame.bind("<Leave>", on_leave)
            row_frame.bind("<Button-1>", on_click)

    # ------------------------------------------------------------------ #
    #  Acciones                                                            #
    # ------------------------------------------------------------------ #

    def _lanzar(self, op: dict) -> None:
        if op["modulo"] is None:
            self._salir()
            return

        modulo_path = os.path.join(BASE_DIR, op["modulo"])
        if modulo_path not in sys.path:
            sys.path.insert(0, modulo_path)

        modulo = op["modulo"]
        if modulo == "fase2_nomina":
            import fase2_nomina.lanzar as m
        elif modulo == "fase3_afiliados":
            import fase3_afiliados.lanzar as m
        elif modulo == "fase4_arbol":
            import fase4_arbol.lanzar as m
        else:
            return

        self._win.withdraw()
        m.lanzar(self._root)
        self._win.deiconify()

    def _salir(self) -> None:
        if messagebox.askyesno("Salir", "¿Desea cerrar la Evaluación Final?",
                               parent=self._win):
            self._root.destroy()

    # ------------------------------------------------------------------ #
    #  Utilidades                                                          #
    # ------------------------------------------------------------------ #

    def _center(self, w: int, h: int) -> None:
        self._win.update_idletasks()
        sw = self._win.winfo_screenwidth()
        sh = self._win.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self._win.geometry(f"{w}x{h}+{x}+{y}")


def _cambiar_bg(widget: tk.Widget, color: str) -> None:
    """Cambia el bg de un widget y todos sus hijos recursivamente."""
    try:
        widget.config(bg=color)
    except tk.TclError:
        pass
    for child in widget.winfo_children():
        _cambiar_bg(child, color)
