"""
Evaluación Final — Ventana de Login Centralizada.
Contraseña genérica: 8246
"""

import tkinter as tk
from tkinter import messagebox

# ── Paleta de colores ──────────────────────────────────────────────────────
BG          = "#0A0F1E"
CARD_BG     = "#111827"
BORDER      = "#3B82F6"
ACCENT      = "#3B82F6"
ACCENT_H    = "#60A5FA"
TEXT_MAIN   = "#F1F5F9"
TEXT_DIM    = "#94A3B8"
ENTRY_BG    = "#1E293B"
ERR_COLOR   = "#EF4444"
SUCCESS_CLR = "#22C55E"

CONTRASENA_VALIDA = "8246"


class LoginWindow:
    """
    Ventana de acceso de la aplicación integradora.
    Muestra: nombre de la app, nombre del estudiante y campo de contraseña.
    """

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Evaluación Final — Acceso")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self._build_ui()
        self._center(440, 580)

    # ------------------------------------------------------------------ #
    #  Construcción UI                                                     #
    # ------------------------------------------------------------------ #

    def _build_ui(self) -> None:
        outer = tk.Frame(self.root, bg=BG, padx=28, pady=28)
        outer.pack(expand=True, fill="both")

        # ── Card ──────────────────────────────────────────────────────── #
        card = tk.Frame(outer, bg=CARD_BG, padx=36, pady=32)
        card.pack(expand=True, fill="both")

        # Barra superior de acento
        tk.Frame(card, bg=BORDER, height=4).pack(fill="x", pady=(0, 22))

        # Ícono y título
        tk.Label(card, text="🎓", font=("Helvetica", 40),
                 bg=CARD_BG, fg=ACCENT).pack()
        tk.Label(card, text="Evaluación Final",
                 font=("Helvetica", 20, "bold"),
                 bg=CARD_BG, fg=TEXT_MAIN).pack(pady=(6, 2))
        tk.Label(card, text="Estructuras de Datos — UNAD",
                 font=("Helvetica", 9),
                 bg=CARD_BG, fg=TEXT_DIM).pack()

        # Divider
        tk.Frame(card, bg="#1E3A5F", height=1).pack(fill="x", pady=18)

        # Info del estudiante
        info = tk.Frame(card, bg=CARD_BG)
        info.pack(fill="x")
        rows = [
            ("Estudiante", "Santiago Villa"),
            ("Curso",      "Estructuras de Datos"),
            ("UNAD",       "Quinto Semestre · 2026"),
        ]
        for label, value in rows:
            row = tk.Frame(info, bg=CARD_BG, pady=3)
            row.pack(fill="x")
            tk.Label(row, text=f"{label}:", font=("Helvetica", 9),
                     bg=CARD_BG, fg=TEXT_DIM, width=12,
                     anchor="w").pack(side="left")
            tk.Label(row, text=value, font=("Helvetica", 9, "bold"),
                     bg=CARD_BG, fg=TEXT_MAIN, anchor="w").pack(side="left")

        # Divider
        tk.Frame(card, bg="#1E3A5F", height=1).pack(fill="x", pady=18)

        # Campo contraseña
        pw_frame = tk.Frame(card, bg=CARD_BG)
        pw_frame.pack(fill="x")
        tk.Label(pw_frame, text="Contraseña de acceso:",
                 font=("Helvetica", 10),
                 bg=CARD_BG, fg=TEXT_DIM).pack(anchor="w")

        wrap = tk.Frame(pw_frame, bg=BORDER, padx=1, pady=1)
        wrap.pack(fill="x", pady=(6, 0))
        self._pw_var = tk.StringVar()
        self._pw_entry = tk.Entry(
            wrap,
            textvariable=self._pw_var,
            show="*",
            font=("Helvetica", 14),
            bg=ENTRY_BG, fg=TEXT_MAIN,
            insertbackground=TEXT_MAIN,
            bd=0, relief="flat",
        )
        self._pw_entry.pack(fill="x", ipady=9, padx=2, pady=2)
        self._pw_entry.bind("<Return>", lambda _: self._ingresar())
        self._pw_entry.focus_set()

        # Label de estado
        self._status_var = tk.StringVar(value="Ingrese la contraseña para continuar")
        self._status_lbl = tk.Label(
            card,
            textvariable=self._status_var,
            font=("Helvetica", 9),
            bg=CARD_BG, fg=TEXT_DIM, wraplength=340,
        )
        self._status_lbl.pack(pady=(10, 0))

        # Botón Ingresar
        btn_frame = tk.Frame(card, bg=CARD_BG)
        btn_frame.pack(fill="x", pady=(18, 0))
        self._btn = tk.Button(
            btn_frame, text="  Ingresar  ",
            font=("Helvetica", 12, "bold"),
            bg=ACCENT, fg="white",
            activebackground=ACCENT_H, activeforeground="white",
            bd=0, relief="flat", cursor="hand2",
            command=self._ingresar,
            padx=20, pady=11,
        )
        self._btn.pack(fill="x")
        self._btn.bind("<Enter>", lambda _: self._btn.config(bg=ACCENT_H))
        self._btn.bind("<Leave>", lambda _: self._btn.config(bg=ACCENT))

    # ------------------------------------------------------------------ #
    #  Acciones                                                            #
    # ------------------------------------------------------------------ #

    def _ingresar(self) -> None:
        pw = self._pw_var.get().strip()
        if not pw:
            self._set_status("El campo de contraseña no puede estar vacío.", ERR_COLOR)
            return
        if pw == CONTRASENA_VALIDA:
            self._set_status("Acceso concedido. Cargando...", SUCCESS_CLR)
            self.root.after(350, self._abrir_menu)
        else:
            self._set_status("Contraseña incorrecta. Intente nuevamente.", ERR_COLOR)
            self._pw_var.set("")
            self._pw_entry.focus_set()

    def _abrir_menu(self) -> None:
        from menu_principal import MenuPrincipal
        self.root.withdraw()
        MenuPrincipal(self.root)

    def _set_status(self, msg: str, color: str) -> None:
        self._status_var.set(msg)
        self._status_lbl.config(fg=color)

    # ------------------------------------------------------------------ #
    #  Utilidades                                                          #
    # ------------------------------------------------------------------ #

    def _center(self, w: int, h: int) -> None:
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def ejecutar(self) -> None:
        self.root.mainloop()
