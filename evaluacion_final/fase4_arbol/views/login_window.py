"""
Login window for Fase4SantiagoVilla.

Shows application name, student name, date and a masked password field.
The generic password is "ARBOL".
"""

import tkinter as tk
from tkinter import messagebox
from datetime import date


# ── Palette ────────────────────────────────────────────────────────────────
BG           = "#0D1B2A"   # deep navy
CARD_BG      = "#1B2A3B"   # dark card
BORDER       = "#1F6FEB"   # electric blue
ACCENT       = "#1F6FEB"
ACCENT_HOVER = "#388BFD"
TEXT_MAIN    = "#E6EDF3"
TEXT_DIM     = "#8B949E"
ENTRY_BG     = "#0D1117"
ERR_COLOR    = "#FF6B6B"
SUCCESS      = "#3FB950"
FONT_TITLE   = ("Helvetica", 18, "bold")
FONT_LABEL   = ("Helvetica", 10)
FONT_VALUE   = ("Helvetica", 10, "bold")
FONT_BTN     = ("Helvetica", 11, "bold")
FONT_SMALL   = ("Helvetica", 9)


class LoginWindow(tk.Toplevel):
    """
    Initial access form.
    Displays app info and validates the generic password before
    opening the main BST window.
    """

    def __init__(self, master: tk.Tk, controlador, on_success) -> None:
        """
        Args:
            master:      Root Tk window.
            controlador: Controlador instance for password verification.
            on_success:  Callback executed when login succeeds.
        """
        super().__init__(master)
        self._ctrl = controlador
        self._on_success = on_success

        self.title("Acceso — Fase4SantiagoVilla")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_ui()
        self._center()
        self.grab_set()   # modal

    # ------------------------------------------------------------------ #
    #  UI construction                                                     #
    # ------------------------------------------------------------------ #

    def _build_ui(self) -> None:
        # ── Outer container ──────────────────────────────────────────── #
        outer = tk.Frame(self, bg=BG, padx=30, pady=30)
        outer.pack(expand=True, fill="both")

        # ── Card ─────────────────────────────────────────────────────── #
        card = tk.Frame(outer, bg=CARD_BG, bd=0, relief="flat",
                        padx=35, pady=30)
        card.pack(expand=True, fill="both")

        # Top accent bar
        bar = tk.Frame(card, bg=BORDER, height=4)
        bar.pack(fill="x", pady=(0, 20))

        # ── Header ───────────────────────────────────────────────────── #
        tk.Label(card, text="🌳", font=("Helvetica", 36), bg=CARD_BG,
                 fg=ACCENT).pack()
        tk.Label(card, text="Fase4SantiagoVilla",
                 font=FONT_TITLE, bg=CARD_BG, fg=TEXT_MAIN).pack(pady=(4, 2))
        tk.Label(card,
                 text="Árbol Binario de Búsqueda — Estructuras de Datos",
                 font=FONT_SMALL, bg=CARD_BG, fg=TEXT_DIM).pack()

        # Divider
        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", pady=18)

        # ── Info rows ────────────────────────────────────────────────── #
        info_frame = tk.Frame(card, bg=CARD_BG)
        info_frame.pack(fill="x")

        rows = [
            ("Estudiante",  "Santiago Villa"),
            ("Curso",       "Estructuras de Datos — UNAD"),
            ("Fecha",       date.today().strftime("%d de %B de %Y")),
        ]
        for label, value in rows:
            row = tk.Frame(info_frame, bg=CARD_BG, pady=3)
            row.pack(fill="x")
            tk.Label(row, text=f"{label}:", font=FONT_LABEL,
                     bg=CARD_BG, fg=TEXT_DIM, width=12,
                     anchor="w").pack(side="left")
            tk.Label(row, text=value, font=FONT_VALUE,
                     bg=CARD_BG, fg=TEXT_MAIN,
                     anchor="w").pack(side="left")

        # Divider
        tk.Frame(card, bg="#2D333B", height=1).pack(fill="x", pady=18)

        # ── Password field ───────────────────────────────────────────── #
        pw_frame = tk.Frame(card, bg=CARD_BG)
        pw_frame.pack(fill="x")

        tk.Label(pw_frame, text="Contraseña:", font=FONT_LABEL,
                 bg=CARD_BG, fg=TEXT_DIM).pack(anchor="w")

        entry_wrap = tk.Frame(pw_frame, bg=BORDER, padx=1, pady=1)
        entry_wrap.pack(fill="x", pady=(5, 0))

        self._pw_var = tk.StringVar()
        self._pw_entry = tk.Entry(
            entry_wrap,
            textvariable=self._pw_var,
            show="*",
            font=("Helvetica", 13),
            bg=ENTRY_BG,
            fg=TEXT_MAIN,
            insertbackground=TEXT_MAIN,
            bd=0,
            relief="flat",
            highlightthickness=0,
        )
        self._pw_entry.pack(fill="x", ipady=8, padx=2, pady=2)
        self._pw_entry.bind("<Return>", lambda _e: self._ingresar())

        # Status label (shows error/hint)
        self._status_var = tk.StringVar(value="Ingrese la contraseña genérica para continuar")
        self._status_lbl = tk.Label(
            card,
            textvariable=self._status_var,
            font=FONT_SMALL,
            bg=CARD_BG,
            fg=TEXT_DIM,
            wraplength=340,
        )
        self._status_lbl.pack(pady=(8, 0))

        # ── Login button ─────────────────────────────────────────────── #
        btn_frame = tk.Frame(card, bg=CARD_BG)
        btn_frame.pack(fill="x", pady=(20, 0))

        self._btn = tk.Button(
            btn_frame,
            text="  Ingresar  ",
            font=FONT_BTN,
            bg=ACCENT,
            fg="white",
            activebackground=ACCENT_HOVER,
            activeforeground="white",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self._ingresar,
            padx=20,
            pady=10,
        )
        self._btn.pack(fill="x")
        self._btn.bind("<Enter>", lambda _e: self._btn.config(bg=ACCENT_HOVER))
        self._btn.bind("<Leave>", lambda _e: self._btn.config(bg=ACCENT))

        # Footer
        tk.Label(card,
                 text="UNAD · Quinto Semestre · 2026",
                 font=FONT_SMALL, bg=CARD_BG, fg=TEXT_DIM).pack(pady=(16, 0))

        self._pw_entry.focus_set()

    # ------------------------------------------------------------------ #
    #  Actions                                                             #
    # ------------------------------------------------------------------ #

    def _ingresar(self) -> None:
        pw = self._pw_var.get()
        if not pw:
            self._set_status("El campo de contraseña no puede estar vacío.", ERR_COLOR)
            return

        if self._ctrl.verificar_contrasena(pw):
            self._set_status("Acceso concedido. Cargando...", SUCCESS)
            self.after(400, self._abrir_principal)
        else:
            self._set_status("Contraseña incorrecta. Intente nuevamente.", ERR_COLOR)
            self._pw_var.set("")
            self._pw_entry.focus_set()

    def _abrir_principal(self) -> None:
        self.destroy()
        self._on_success()

    def _on_close(self) -> None:
        self.master.destroy()

    def _set_status(self, msg: str, color: str) -> None:
        self._status_var.set(msg)
        self._status_lbl.config(fg=color)

    # ------------------------------------------------------------------ #
    #  Utilities                                                           #
    # ------------------------------------------------------------------ #

    def _center(self) -> None:
        self.update_idletasks()
        w, h = 440, 560
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")
