"""
Main window for Fase4SantiagoVilla.

Layout (two-column):
  Left  : large canvas that draws the BST graphically.
  Right : three stacked panels for Preorden, Inorden, Posorden traversals.

Controls:
  - Entry field for node value
  - Buttons: Agregar Nodo | Buscar Nodo | Limpiar | Salir
"""

import tkinter as tk
from tkinter import messagebox


# ── Palette ────────────────────────────────────────────────────────────────
BG           = "#0D1B2A"
PANEL_BG     = "#1B2A3B"
HEADER_BG    = "#0F3460"
BORDER       = "#1F6FEB"
ACCENT       = "#1F6FEB"
ACCENT_HOVER = "#388BFD"
BTN_RED      = "#C0392B"
BTN_RED_H    = "#E74C3C"
BTN_GREEN    = "#1A7F4B"
BTN_GREEN_H  = "#27AE60"
BTN_ORANGE   = "#B7620A"
BTN_ORANGE_H = "#E67E22"
TEXT_MAIN    = "#E6EDF3"
TEXT_DIM     = "#8B949E"
ENTRY_BG     = "#0D1117"
NODE_FILL    = "#1F6FEB"
NODE_BORDER  = "#58A6FF"
NODE_FOUND   = "#F79618"
NODE_TEXT    = "#FFFFFF"
EDGE_COLOR   = "#3D8EC9"
TRAV_FILL    = "#1A5276"
TRAV_BORDER  = "#3498DB"
ARROW_COLOR  = "#58A6FF"

FONT_TITLE  = ("Helvetica", 14, "bold")
FONT_HEADER = ("Helvetica", 10, "bold")
FONT_LABEL  = ("Helvetica", 10)
FONT_BTN    = ("Helvetica", 10, "bold")
FONT_NODE   = ("Helvetica", 10, "bold")
FONT_TNODE  = ("Helvetica", 9,  "bold")

# Drawing constants
NODE_R   = 22      # radius of BST node circle
TNODE_R  = 16      # radius of traversal node circle
V_GAP    = 72      # vertical gap between BST levels


class MainWindow(tk.Toplevel):
    """
    Principal interface: BST canvas + traversal panels + controls.
    """

    def __init__(self, master: tk.Tk, controlador) -> None:
        super().__init__(master)
        self._ctrl = controlador

        self.title("Árbol Binario de Búsqueda — Fase4SantiagoVilla")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self._salir)

        self._build_ui()
        self._center()
        self._refresh_all()

    # ------------------------------------------------------------------ #
    #  UI construction                                                     #
    # ------------------------------------------------------------------ #

    def _build_ui(self) -> None:
        # ── Title bar ────────────────────────────────────────────────── #
        title_bar = tk.Frame(self, bg=HEADER_BG, pady=8)
        title_bar.pack(fill="x")
        tk.Label(
            title_bar,
            text="🌳  Árbol Binario de Búsqueda  |  Fase4SantiagoVilla  |  Santiago Villa",
            font=FONT_TITLE, bg=HEADER_BG, fg=TEXT_MAIN,
        ).pack()

        # ── Controls bar ─────────────────────────────────────────────── #
        ctrl_bar = tk.Frame(self, bg=PANEL_BG, pady=10, padx=14)
        ctrl_bar.pack(fill="x")

        tk.Label(ctrl_bar, text="Valor del nodo:", font=FONT_LABEL,
                 bg=PANEL_BG, fg=TEXT_DIM).pack(side="left", padx=(0, 6))

        entry_wrap = tk.Frame(ctrl_bar, bg=BORDER, padx=1, pady=1)
        entry_wrap.pack(side="left", padx=(0, 16))
        self._entry_var = tk.StringVar()
        self._entry = tk.Entry(
            entry_wrap,
            textvariable=self._entry_var,
            font=("Helvetica", 12),
            bg=ENTRY_BG, fg=TEXT_MAIN,
            insertbackground=TEXT_MAIN,
            bd=0, relief="flat",
            width=10,
        )
        self._entry.pack(ipady=6, padx=2, pady=2)
        self._entry.bind("<Return>", lambda _e: self._agregar())

        # Buttons
        buttons = [
            ("Agregar Nodo",  self._agregar,  BTN_GREEN,  BTN_GREEN_H),
            ("Buscar Nodo",   self._buscar,   ACCENT,     ACCENT_HOVER),
            ("Limpiar",       self._limpiar,  BTN_ORANGE, BTN_ORANGE_H),
            ("Salir",         self._salir,    BTN_RED,    BTN_RED_H),
        ]
        for text, cmd, bg, hover in buttons:
            b = tk.Button(
                ctrl_bar, text=text, font=FONT_BTN,
                bg=bg, fg="white", activebackground=hover,
                activeforeground="white", bd=0, relief="flat",
                cursor="hand2", padx=14, pady=7, command=cmd,
            )
            b.pack(side="left", padx=4)
            b.bind("<Enter>", lambda e, h=hover: e.widget.config(bg=h))
            b.bind("<Leave>", lambda e, n=bg:   e.widget.config(bg=n))

        # Status bar
        self._status_var = tk.StringVar(value="Listo. Ingrese un valor entero y presione 'Agregar Nodo'.")
        tk.Label(ctrl_bar, textvariable=self._status_var, font=("Helvetica", 9),
                 bg=PANEL_BG, fg=TEXT_DIM).pack(side="right", padx=8)

        # ── Main body (two columns) ───────────────────────────────────── #
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=10, pady=10)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        # LEFT: tree panel
        self._tree_canvas = self._make_panel(body, "📊  Árbol Binario de Búsqueda", 0, 0)

        # RIGHT: three traversal panels
        right = tk.Frame(body, bg=BG)
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        right.rowconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)
        right.rowconfigure(2, weight=1)
        right.columnconfigure(0, weight=1)

        self._pre_canvas  = self._make_panel(right, "🔵  Preorden  (Raíz → Izq → Der)",  0, 0, rowspan=1)
        self._in_canvas   = self._make_panel(right, "🟢  Inorden   (Izq → Raíz → Der)",  1, 0, rowspan=1)
        self._post_canvas = self._make_panel(right, "🟠  Posorden  (Izq → Der → Raíz)",  2, 0, rowspan=1)

    def _make_panel(self, parent, title: str, row: int, col: int,
                    rowspan: int = 1) -> tk.Canvas:
        """Create a labelled panel and return its inner canvas."""
        frame = tk.Frame(parent, bg=PANEL_BG, bd=0)
        frame.grid(row=row, column=col, rowspan=rowspan,
                   sticky="nsew", padx=3, pady=3)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

        # Panel header
        hdr = tk.Frame(frame, bg=HEADER_BG, pady=5)
        hdr.grid(row=0, column=0, sticky="ew")
        tk.Label(hdr, text=title, font=FONT_HEADER,
                 bg=HEADER_BG, fg=TEXT_MAIN).pack(anchor="w", padx=10)

        # Canvas
        canvas = tk.Canvas(frame, bg=PANEL_BG, bd=0, highlightthickness=0)
        canvas.grid(row=1, column=0, sticky="nsew")
        return canvas

    # ------------------------------------------------------------------ #
    #  Button handlers                                                     #
    # ------------------------------------------------------------------ #

    def _agregar(self) -> None:
        texto = self._entry_var.get().strip()
        resultado = self._ctrl.agregar_nodo(texto)

        if resultado["success"]:
            self._entry_var.set("")
            self._entry.focus_set()
            self._set_status(resultado["message"], "#3FB950")
            self._refresh_all()
        else:
            if resultado["tipo_error"] == "tipo":
                messagebox.showerror(
                    "Dato inválido",
                    resultado["message"],
                    parent=self,
                )
            elif resultado["tipo_error"] == "nivel":
                messagebox.showerror(
                    "Nivel máximo alcanzado",
                    resultado["message"],
                    parent=self,
                )
            else:
                messagebox.showwarning(
                    "Valor duplicado",
                    resultado["message"],
                    parent=self,
                )
            self._set_status(resultado["message"], "#FF6B6B")
            self._entry.select_range(0, "end")
            self._entry.focus_set()

    def _buscar(self) -> None:
        texto = self._entry_var.get().strip()
        resultado = self._ctrl.buscar_nodo(texto)

        if resultado.get("tipo_error") == "tipo":
            messagebox.showerror("Dato inválido", resultado["message"], parent=self)
            self._set_status(resultado["message"], "#FF6B6B")
            return

        if resultado.get("tipo_error") == "vacio":
            messagebox.showinfo("Árbol vacío", resultado["message"], parent=self)
            self._set_status(resultado["message"], "#F79618")
            return

        if resultado["encontrado"]:
            self._set_status(resultado["message"], "#3FB950")
            messagebox.showinfo("Nodo encontrado", resultado["message"], parent=self)
        else:
            self._set_status(resultado["message"], "#FF6B6B")
            messagebox.showwarning("Nodo no encontrado", resultado["message"], parent=self)

        self._refresh_all()   # redraw to show/hide highlight

    def _limpiar(self) -> None:
        if self._ctrl.get_arbol().esta_vacio():
            messagebox.showinfo("Árbol vacío",
                                "El árbol ya está vacío.", parent=self)
            return
        if messagebox.askyesno("Limpiar árbol",
                               "¿Desea eliminar todos los nodos del árbol?",
                               parent=self):
            self._ctrl.limpiar()
            self._entry_var.set("")
            self._set_status("Árbol limpiado correctamente.", TEXT_DIM)
            self._refresh_all()

    def _salir(self) -> None:
        if messagebox.askyesno("Salir", "¿Desea cerrar la aplicación?",
                               parent=self):
            self.destroy()

    # ------------------------------------------------------------------ #
    #  Drawing                                                             #
    # ------------------------------------------------------------------ #

    def _refresh_all(self) -> None:
        self.update_idletasks()
        self._draw_tree()
        travs = self._ctrl.get_traversals()
        self._draw_traversal(self._pre_canvas,  travs["preorden"])
        self._draw_traversal(self._in_canvas,   travs["inorden"])
        self._draw_traversal(self._post_canvas, travs["posorden"])

    # ── BST canvas ───────────────────────────────────────────────────── #

    def _draw_tree(self) -> None:
        canvas = self._tree_canvas
        canvas.delete("all")
        arbol = self._ctrl.get_arbol()

        if arbol.esta_vacio():
            self._canvas_msg(canvas, "El árbol está vacío.\nAgregue nodos para comenzar.")
            return

        cw = canvas.winfo_width()  or 500
        cx = cw // 2               # horizontal center
        # x_offset for level-2 nodes: 1/4 of canvas width feels good for 4 levels
        x_offset = cw // 4

        self._draw_node(canvas, arbol.raiz, cx, 40, x_offset,
                        self._ctrl.get_nodo_buscado())

    def _draw_node(self, canvas, nodo, x: int, y: int,
                   x_off: int, found_val) -> None:
        if nodo is None:
            return

        next_off = max(x_off // 2, NODE_R + 6)

        # Draw edges first (behind nodes)
        if nodo.izquierdo:
            canvas.create_line(x, y, x - x_off, y + V_GAP,
                               fill=EDGE_COLOR, width=2)
        if nodo.derecho:
            canvas.create_line(x, y, x + x_off, y + V_GAP,
                               fill=EDGE_COLOR, width=2)

        # Recurse children
        self._draw_node(canvas, nodo.izquierdo, x - x_off, y + V_GAP, next_off, found_val)
        self._draw_node(canvas, nodo.derecho,   x + x_off, y + V_GAP, next_off, found_val)

        # Draw this node
        fill = NODE_FOUND if nodo.valor == found_val else NODE_FILL
        canvas.create_oval(
            x - NODE_R, y - NODE_R, x + NODE_R, y + NODE_R,
            fill=fill, outline=NODE_BORDER, width=2,
        )
        canvas.create_text(x, y, text=str(nodo.valor),
                           fill=NODE_TEXT, font=FONT_NODE)

    # ── Traversal canvas ─────────────────────────────────────────────── #

    def _draw_traversal(self, canvas: tk.Canvas, values: list) -> None:
        canvas.delete("all")
        canvas.update_idletasks()

        if not values:
            self._canvas_msg(canvas, "(vacío)")
            return

        cw = canvas.winfo_width()  or 400
        ch = canvas.winfo_height() or 120

        r        = TNODE_R
        h_space  = r * 2 + 18      # horizontal slot per node
        pad_x    = 14
        pad_y    = 14

        # How many nodes fit per row?
        per_row  = max(1, (cw - 2 * pad_x) // h_space)

        x = pad_x + r
        y = pad_y + r

        for i, val in enumerate(values):
            # Wrap to next row if needed
            if i > 0 and i % per_row == 0:
                x  = pad_x + r
                y += r * 2 + 24

            # Arrow from previous node (skip at row start and first node)
            if i > 0 and (i % per_row) != 0:
                ax = x - h_space + r
                canvas.create_line(
                    ax, y, x - r, y,
                    fill=ARROW_COLOR, width=2,
                    arrow=tk.LAST, arrowshape=(8, 10, 4),
                )

            # Node circle
            canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=TRAV_FILL, outline=TRAV_BORDER, width=2,
            )
            canvas.create_text(x, y, text=str(val),
                               fill=NODE_TEXT, font=FONT_TNODE)
            x += h_space

    # ------------------------------------------------------------------ #
    #  Utilities                                                           #
    # ------------------------------------------------------------------ #

    def _canvas_msg(self, canvas: tk.Canvas, msg: str) -> None:
        cw = canvas.winfo_width()  or 300
        ch = canvas.winfo_height() or 150
        canvas.create_text(cw // 2, ch // 2, text=msg,
                           fill=TEXT_DIM, font=("Helvetica", 10),
                           justify="center")

    def _set_status(self, msg: str, color: str) -> None:
        self._status_var.set(msg)

    def _center(self) -> None:
        self.update_idletasks()
        w, h = 1180, 720
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x  = (sw - w) // 2
        y  = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.minsize(900, 600)
