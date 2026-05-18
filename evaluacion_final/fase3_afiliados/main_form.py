"""
Módulo FormularioPrincipal — Control de Afiliados.
Adaptado para el proyecto integrador Evaluación Final.
Capa: Presentación / Patrón MVC simplificado.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
import logica
from modelo import EstructuraDatosAfiliado, GestorEstructuras

# ─── Opciones de campos ──────────────────────────────────────
TIPOS_ID  = ["CC", "CE", "NUIP", "PAS"]
SERVICIOS = ["Subsidio de desempleo", "Ingreso a parque",
             "Curso de formación", "Paquete de viaje", "Medicina preventiva"]
ESTRUCTURAS = ["Pila", "Cola", "Lista"]
COLUMNAS = ("Tipo ID", "Núm. ID", "Nombre", "Ingresos",
            "Servicio", "Modalidad", "Tarifa", "Fecha")

# ─── Paleta de colores ───────────────────────────────────────
CP  = "#1565C0"   # primario
CPO = "#0D47A1"   # primario oscuro
CA  = "#42A5F5"   # acento
CF  = "#F5F7FA"   # fondo
CB  = "#FFFFFF"   # blanco

# ─── Tipografías ─────────────────────────────────────────────
F_LBL  = ("Segoe UI", 9, "bold")
F_CAM  = ("Segoe UI", 9)
F_BTN  = ("Segoe UI", 9, "bold")


class FormularioPrincipal:
    """Formulario principal del sistema Caja Compensándote — Control de Afiliados."""

    def __init__(self, master=None):
        self._master = master
        if master:
            self.ventana = tk.Toplevel(master)
            self.ventana.protocol("WM_DELETE_WINDOW", self._cerrar)
        else:
            self.ventana = tk.Tk()
        self.ventana.title("Caja Compensándote – Control de Afiliados")
        self.ventana.configure(bg=CF)

        # ── Intentar maximizar ──────────────────────────────
        try:
            self.ventana.state("zoomed")
        except Exception:
            self.ventana.attributes("-zoomed", True)

        # ── Estado de la aplicación ─────────────────────────
        self.gestorEstructuras = GestorEstructuras()
        self.varModalidad  = tk.StringVar(value="Empleado")
        self.varEstructura = tk.StringVar()
        self.varTarifa     = tk.StringVar(value="$ 0")
        self.varReporte    = tk.StringVar(value="---")

        self._configurarEstilos()
        self._construirUI()

    # ══════════════════════════════════════════════════════════
    # ESTILOS
    # ══════════════════════════════════════════════════════════
    def _configurarEstilos(self):
        est = ttk.Style()
        est.theme_use("clam")
        est.configure("TFrame",      background=CF)
        est.configure("TLabel",      background=CF, font=F_CAM)
        est.configure("TRadiobutton", background=CF, font=F_CAM)
        est.configure("TCombobox",   font=F_CAM)
        est.configure("Treeview",    font=F_CAM, rowheight=24)
        est.configure("Treeview.Heading", font=F_LBL,
                      background=CP, foreground=CB)
        est.map("Treeview", background=[("selected", CA)])

    # ══════════════════════════════════════════════════════════
    # CONSTRUCCIÓN DE LA INTERFAZ
    # ══════════════════════════════════════════════════════════
    def _construirUI(self):
        self._crearEncabezado()
        contenido = ttk.Frame(self.ventana)
        contenido.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        contenido.columnconfigure(0, weight=1)
        contenido.columnconfigure(1, weight=3)
        contenido.rowconfigure(0, weight=1)
        self._crearPanelFormulario(contenido)
        self._crearPanelTreeview(contenido)
        self._crearPanelBotones()

    def _crearEncabezado(self):
        frm = tk.Frame(self.ventana, bg=CP, height=52)
        frm.pack(fill=tk.X)
        frm.pack_propagate(False)
        tk.Label(frm, text="🏢  Caja Compensándote — Control de Afiliados",
                 font=("Segoe UI", 13, "bold"),
                 bg=CP, fg=CB).pack(side=tk.LEFT, padx=18, pady=10)

    # ── Panel izquierdo: formulario ───────────────────────────
    def _crearPanelFormulario(self, padre):
        frm = ttk.LabelFrame(padre, text=" Datos del Afiliado ", padding=(12, 6))
        frm.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
        frm.columnconfigure(1, weight=1)

        campos = [
            ("Tipo de Identificación:",  self._addComboTipoId),
            ("Núm. de Identificación:",  self._addEntryNumId),
            ("Nombre Completo:",         self._addEntryNombre),
            ("Ingresos Actuales ($):",   self._addEntryIngresos),
            ("Servicio Deseado:",        self._addComboServicio),
            ("Modalidad de Empleo:",     self._addRadioModalidad),
            ("Tarifa de Afiliación ($):",self._addEntryTarifa),
            ("Fecha de Afiliación:",     self._addDateEntry),
        ]
        for fila, (texto, creador) in enumerate(campos):
            ttk.Label(frm, text=texto, font=F_LBL).grid(
                row=fila, column=0, sticky="w", pady=4, padx=(0, 6))
            creador(frm, fila)

        # ── Separador ──────────────────────────────────────
        sep_row = len(campos)
        ttk.Separator(frm, orient="horizontal").grid(
            row=sep_row, column=0, columnspan=2, sticky="ew", pady=10)

        # ── Selector de estructura ─────────────────────────
        ttk.Label(frm, text="Ver estructura:", font=F_LBL).grid(
            row=sep_row+1, column=0, sticky="w", pady=4, padx=(0, 6))
        self.comboEstructura = ttk.Combobox(
            frm, values=ESTRUCTURAS, state="readonly",
            textvariable=self.varEstructura, font=F_CAM)
        self.comboEstructura.grid(row=sep_row+1, column=1, sticky="ew", pady=4)
        self.comboEstructura.bind("<<ComboboxSelected>>", self._actualizarTreeview)

        # ── Campo Reporte ──────────────────────────────────
        ttk.Label(frm, text="Reporte:", font=F_LBL).grid(
            row=sep_row+2, column=0, sticky="w", pady=4, padx=(0, 6))
        entReporte = ttk.Entry(frm, textvariable=self.varReporte,
                               state="readonly", font=F_CAM)
        entReporte.grid(row=sep_row+2, column=1, sticky="ew", pady=4)

    # ── Creadores de campos individuales ─────────────────────
    def _addComboTipoId(self, frm, fila):
        self.comboTipoId = ttk.Combobox(frm, values=TIPOS_ID,
                                         state="readonly", font=F_CAM)
        self.comboTipoId.grid(row=fila, column=1, sticky="ew", pady=4)

    def _addEntryNumId(self, frm, fila):
        vcmd = (self.ventana.register(lambda v: v.isdigit() or v == ""), "%P")
        self.entryNumId = ttk.Entry(frm, validate="key",
                                     validatecommand=vcmd, font=F_CAM)
        self.entryNumId.grid(row=fila, column=1, sticky="ew", pady=4)

    def _addEntryNombre(self, frm, fila):
        vcmd = (self.ventana.register(
            lambda v: all(c.isalpha() or c.isspace() for c in v) if v else True), "%P")
        self.entryNombre = ttk.Entry(frm, validate="key",
                                      validatecommand=vcmd, font=F_CAM)
        self.entryNombre.grid(row=fila, column=1, sticky="ew", pady=4)

    def _addEntryIngresos(self, frm, fila):
        vcmd = (self.ventana.register(self._validarDecimal), "%P")
        self.entryIngresos = ttk.Entry(frm, validate="key",
                                        validatecommand=vcmd, font=F_CAM)
        self.entryIngresos.grid(row=fila, column=1, sticky="ew", pady=4)
        self.entryIngresos.bind("<FocusOut>", self._actualizarTarifa)

    def _addComboServicio(self, frm, fila):
        self.comboServicio = ttk.Combobox(frm, values=SERVICIOS,
                                           state="readonly", font=F_CAM)
        self.comboServicio.grid(row=fila, column=1, sticky="ew", pady=4)
        self.comboServicio.bind("<<ComboboxSelected>>", self._actualizarTarifa)

    def _addRadioModalidad(self, frm, fila):
        sub = ttk.Frame(frm)
        sub.grid(row=fila, column=1, sticky="w", pady=4)
        for valor in ("Empleado", "Independiente"):
            ttk.Radiobutton(sub, text=valor, variable=self.varModalidad,
                             value=valor, command=self._actualizarTarifa
                             ).pack(side=tk.LEFT, padx=(0, 12))

    def _addEntryTarifa(self, frm, fila):
        self.entryTarifa = ttk.Entry(frm, textvariable=self.varTarifa,
                                      state="readonly", font=F_CAM)
        self.entryTarifa.grid(row=fila, column=1, sticky="ew", pady=4)

    def _addDateEntry(self, frm, fila):
        self.dateEntryFecha = DateEntry(
            frm, width=18, date_pattern="dd/mm/yyyy",
            background=CP, foreground=CB, borderwidth=2, font=F_CAM)
        self.dateEntryFecha.grid(row=fila, column=1, sticky="w", pady=4)

    # ── Panel derecho: Treeview ───────────────────────────────
    def _crearPanelTreeview(self, padre):
        frm = ttk.LabelFrame(padre, text=" Registros de Afiliados ", padding=(8, 5))
        frm.grid(row=0, column=1, sticky="nsew", pady=5)
        frm.columnconfigure(0, weight=1)
        frm.rowconfigure(0, weight=1)

        scrollV = ttk.Scrollbar(frm, orient=tk.VERTICAL)
        scrollH = ttk.Scrollbar(frm, orient=tk.HORIZONTAL)

        self.treeAfiliados = ttk.Treeview(
            frm, columns=COLUMNAS, show="headings",
            yscrollcommand=scrollV.set, xscrollcommand=scrollH.set)

        scrollV.config(command=self.treeAfiliados.yview)
        scrollH.config(command=self.treeAfiliados.xview)

        anchos = [68, 110, 165, 105, 165, 110, 105, 90]
        for col, w in zip(COLUMNAS, anchos):
            self.treeAfiliados.heading(col, text=col)
            self.treeAfiliados.column(col, width=w, minwidth=60, anchor="center")

        self.treeAfiliados.grid(row=0, column=0, sticky="nsew")
        scrollV.grid(row=0, column=1, sticky="ns")
        scrollH.grid(row=1, column=0, sticky="ew")
        self.treeAfiliados.tag_configure("par",   background="#E3F2FD")
        self.treeAfiliados.tag_configure("impar", background=CB)

    # ── Panel inferior: botones ───────────────────────────────
    def _cerrar(self) -> None:
        """Cierra esta ventana y restaura el menú principal."""
        self.ventana.destroy()
        if self._master:
            self._master.deiconify()

    def _crearPanelBotones(self):
        frm = tk.Frame(self.ventana, bg=CPO, height=54)
        frm.pack(fill=tk.X, side=tk.BOTTOM)
        frm.pack_propagate(False)

        botones = [
            ("✅  Registrar", CP,       self._registrar),
            ("🧹  Limpiar",  "#455A64", self._limpiarFormulario),
            ("📊  Reporte",  "#00796B", self._generarReporte),
            ("🗑️  Eliminar", "#D32F2F", self._eliminar),
            ("← Menú",      "#37474F", self._cerrar),
        ]
        for texto, color, cmd in botones:
            tk.Button(frm, text=texto, font=F_BTN,
                      bg=color, fg=CB, relief=tk.FLAT,
                      padx=16, pady=7, cursor="hand2",
                      activebackground=CPO, activeforeground=CB,
                      command=cmd).pack(side=tk.LEFT, padx=6, pady=8)

    # ══════════════════════════════════════════════════════════
    # VALIDACIONES
    # ══════════════════════════════════════════════════════════
    def _validarDecimal(self, valor: str) -> bool:
        if valor == "":
            return True
        try:
            float(valor)
            return True
        except ValueError:
            return valor == "." or (valor.count(".") == 1 and valor.replace(".", "").isdigit())

    def _validarCamposObligatorios(self) -> bool:
        checks = [
            (not self.comboTipoId.get(),        "Debe seleccionar el tipo de identificación."),
            (not self.entryNumId.get().strip(),  "Debe ingresar el número de identificación."),
            (not self.entryNombre.get().strip(), "Debe ingresar el nombre completo."),
            (not self.entryIngresos.get().strip(),"Debe ingresar los ingresos actuales."),
            (not self.comboServicio.get(),       "Debe seleccionar el servicio deseado."),
            (not self.varEstructura.get(),       "Debe seleccionar una estructura de datos."),
        ]
        for condicion, mensaje in checks:
            if condicion:
                messagebox.showwarning("Campo requerido", mensaje, parent=self.ventana)
                return False
        if float(self.entryIngresos.get()) < 1_000_000:
            messagebox.showwarning("Ingresos inválidos",
                "Los ingresos mínimos son $1.000.000.", parent=self.ventana)
            return False
        return True

    # ══════════════════════════════════════════════════════════
    # CÁLCULO DE TARIFA
    # ══════════════════════════════════════════════════════════
    def _actualizarTarifa(self, event=None):
        ingStr  = self.entryIngresos.get().strip()
        servicio = self.comboServicio.get()
        modalidad = self.varModalidad.get()
        if ingStr and servicio and modalidad:
            try:
                ing = float(ingStr)
                if ing >= 1_000_000:
                    tarifa = logica.calcularTarifa(ing, modalidad, servicio)
                    self.varTarifa.set(f"${tarifa:,.0f}")
                    return
            except ValueError:
                pass
        self.varTarifa.set("$ 0")

    # ══════════════════════════════════════════════════════════
    # TREEVIEW
    # ══════════════════════════════════════════════════════════
    def _actualizarTreeview(self, event=None):
        for item in self.treeAfiliados.get_children():
            self.treeAfiliados.delete(item)

        estructura = self.varEstructura.get()
        if estructura == "Pila":
            registros = self.gestorEstructuras.obtenerPila()
        elif estructura == "Cola":
            registros = self.gestorEstructuras.obtenerCola()
        elif estructura == "Lista":
            registros = self.gestorEstructuras.obtenerLista()
        else:
            registros = []

        for i, afiliado in enumerate(registros):
            tag = "par" if i % 2 == 0 else "impar"
            self.treeAfiliados.insert("", tk.END, values=afiliado.aLista(), tags=(tag,))

        self._actualizarCampoReporte()

    def _actualizarCampoReporte(self):
        estructura = self.varEstructura.get()
        if estructura == "Pila":
            self.varReporte.set(logica.obtenerReportePila(self.gestorEstructuras.pila))
        elif estructura == "Cola":
            self.varReporte.set(logica.obtenerReporteCola(self.gestorEstructuras.cola))
        elif estructura == "Lista":
            self.varReporte.set(logica.obtenerReporteLista(self.gestorEstructuras.lista))
        else:
            self.varReporte.set("---")

    # ══════════════════════════════════════════════════════════
    # ACCIONES DE BOTONES (Controller)
    # ══════════════════════════════════════════════════════════
    def _registrar(self):
        """Valida y registra un afiliado en la estructura seleccionada."""
        if not self._validarCamposObligatorios():
            return

        ing = float(self.entryIngresos.get())
        tarifaStr = self.varTarifa.get().replace("$", "").replace(",", "").strip()
        tarifa = float(tarifaStr) if tarifaStr and tarifaStr != "0" else 0.0

        afiliado = EstructuraDatosAfiliado(
            tipoIdentificacion=self.comboTipoId.get(),
            numeroIdentificacion=self.entryNumId.get().strip(),
            nombreCompleto=self.entryNombre.get().strip(),
            ingresosActuales=ing,
            servicioDeseado=self.comboServicio.get(),
            modalidadEmpleo=self.varModalidad.get(),
            tarifaAfiliacion=tarifa,
            fechaAfiliacion=self.dateEntryFecha.get()
        )
        estructura = self.varEstructura.get()
        if estructura == "Pila":
            self.gestorEstructuras.apilar(afiliado)
        elif estructura == "Cola":
            self.gestorEstructuras.encolar(afiliado)
        elif estructura == "Lista":
            self.gestorEstructuras.agregarALista(afiliado)

        self._actualizarTreeview()
        messagebox.showinfo("Registro exitoso",
            f"Afiliado registrado en la {estructura}.", parent=self.ventana)

    def _limpiarFormulario(self):
        """Limpia todos los campos sin afectar los registros del Treeview."""
        self.comboTipoId.set("")
        self.entryNumId.delete(0, tk.END)
        self.entryNombre.delete(0, tk.END)
        self.entryIngresos.delete(0, tk.END)
        self.comboServicio.set("")
        self.varModalidad.set("Empleado")
        self.varTarifa.set("$ 0")

    def _generarReporte(self):
        """Calcula y muestra el reporte de la estructura seleccionada."""
        if not self.varEstructura.get():
            messagebox.showwarning("Sin estructura",
                "Seleccione una estructura de datos.", parent=self.ventana)
            return
        self._actualizarCampoReporte()

    def _eliminar(self):
        """Elimina un registro según el comportamiento de la estructura seleccionada."""
        estructura = self.varEstructura.get()
        if not estructura:
            messagebox.showwarning("Sin estructura",
                "Seleccione una estructura de datos.", parent=self.ventana)
            return

        # Verificar que la estructura no esté vacía
        mapVacio = {
            "Pila": not self.gestorEstructuras.pila,
            "Cola": not self.gestorEstructuras.cola,
            "Lista": not self.gestorEstructuras.lista,
        }
        if mapVacio[estructura]:
            messagebox.showinfo("Estructura vacía",
                f"La {estructura} no tiene registros.", parent=self.ventana)
            return

        if estructura == "Lista":
            numeroId = simpledialog.askstring(
                "Eliminar de Lista",
                "Ingrese el número de identificación del afiliado:",
                parent=self.ventana)
            if not numeroId:
                return
            if not self.gestorEstructuras.buscarEnLista(numeroId.strip()):
                messagebox.showerror("No encontrado",
                    f"No existe afiliado con ID '{numeroId}' en la Lista.",
                    parent=self.ventana)
                return
            if not messagebox.askyesno("Confirmar",
                    f"¿Eliminar al afiliado con ID '{numeroId}' de la Lista?",
                    parent=self.ventana):
                return
            self.gestorEstructuras.eliminarDeLista(numeroId.strip())
        else:
            if not messagebox.askyesno("Confirmar",
                    f"¿Eliminar el registro de la {estructura}?",
                    parent=self.ventana):
                return
            if estructura == "Pila":
                self.gestorEstructuras.desapilar()
            elif estructura == "Cola":
                self.gestorEstructuras.desencolar()

        self._actualizarTreeview()
        messagebox.showinfo("Eliminado",
            f"Registro eliminado de la {estructura}.", parent=self.ventana)

    def ejecutar(self):
        """Inicia el loop principal de la ventana."""
        if self._master:
            self._master.withdraw()
            self.ventana.wait_window()
        else:
            self.ventana.mainloop()
