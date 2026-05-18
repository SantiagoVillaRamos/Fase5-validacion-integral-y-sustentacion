"""
Adaptador de ENTRADA: TkinterAdapter — Fase 2 Adaptado.
Modificado para integrarse al proyecto Evaluación Final.
Abre como Toplevel sobre el master dado (menú principal).
"""
import tkinter as tk
from tkinter import messagebox

from domain.entities.cargo import Cargo
from domain.ports.input.nomina_service_port import NominaServicePort


class TkinterAdapter:
    """
    Adaptador de entrada que abre la UI de Nómina como Toplevel
    sobre la ventana maestra del proyecto integrador.
    """

    def __init__(self, servicio: NominaServicePort, master: tk.Tk = None) -> None:
        self._servicio = servicio
        self._master = master
        if master:
            self._ventana = tk.Toplevel(master)
            self._ventana.protocol("WM_DELETE_WINDOW", self._cerrar)
        else:
            self._ventana = tk.Tk()
        self._construir_ui()

    def _cerrar(self) -> None:
        """Cierra esta ventana y muestra de nuevo el menú principal."""
        self._ventana.destroy()
        if self._master:
            self._master.deiconify()

    # ------------------------------------------------------------------ #
    # Construcción de la interfaz
    # ------------------------------------------------------------------ #

    def _construir_ui(self) -> None:
        v = self._ventana
        v.title("Sistema de Nómina - Constructora Mejor")
        v.geometry("420x420")
        v.resizable(False, False)
        v.configure(bg="#1e1e2e")

        estilo_label = {"bg": "#1e1e2e", "fg": "#cdd6f4", "font": ("Inter", 10)}
        estilo_entry = {"bg": "#313244", "fg": "#cdd6f4", "insertbackground": "#cdd6f4",
                        "relief": "flat", "font": ("Inter", 10)}
        estilo_btn = {"bg": "#89b4fa", "fg": "#1e1e2e", "activebackground": "#74c7ec",
                      "relief": "flat", "font": ("Inter", 10, "bold"), "cursor": "hand2",
                      "padx": 10, "pady": 5}

        tk.Label(v, text="🏗 Sistema de Nómina", bg="#1e1e2e",
                 fg="#89b4fa", font=("Inter", 14, "bold")).pack(pady=(20, 5))
        tk.Label(v, text="Constructora Mejor", **estilo_label).pack(pady=(0, 15))

        tk.Label(v, text="Nombre del empleado", **estilo_label).pack(anchor="w", padx=30)
        self._entry_nombre = tk.Entry(v, width=40, **estilo_entry)
        self._entry_nombre.pack(padx=30, pady=(2, 10), ipady=4)

        tk.Label(v, text="Cargo", **estilo_label).pack(anchor="w", padx=30)
        self._cargo_var = tk.StringVar(value=Cargo.INGENIERO.descripcion)
        menu_cargo = tk.OptionMenu(v, self._cargo_var, *Cargo.listar_descripciones())
        menu_cargo.config(bg="#313244", fg="#cdd6f4", activebackground="#45475a",
                          relief="flat", font=("Inter", 10), width=33)
        menu_cargo.pack(padx=30, pady=(2, 10), anchor="w")

        tk.Label(v, text="Días trabajados", **estilo_label).pack(anchor="w", padx=30)
        self._entry_dias = tk.Entry(v, width=40, **estilo_entry)
        self._entry_dias.pack(padx=30, pady=(2, 15), ipady=4)

        frame_botones = tk.Frame(v, bg="#1e1e2e")
        frame_botones.pack()
        tk.Button(frame_botones, text="💰 Calcular Pago",
                  command=self._on_calcular, **estilo_btn).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="💾 Guardar",
                  command=self._on_guardar, **estilo_btn).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="📄 Reporte",
                  command=self._on_reporte, **estilo_btn).grid(row=0, column=2, padx=5)

        self._label_resultado = tk.Label(v, text="", bg="#1e1e2e",
                                         fg="#a6e3a1", font=("Inter", 11, "bold"))
        self._label_resultado.pack(pady=10)

        tk.Button(v, text="← Volver al Menú", command=self._cerrar,
                  bg="#585b70", fg="#cdd6f4", activebackground="#45475a",
                  relief="flat", font=("Inter", 9, "bold"),
                  cursor="hand2", padx=12, pady=5).pack(pady=(0, 10))

    # ------------------------------------------------------------------ #
    # Manejadores de eventos
    # ------------------------------------------------------------------ #

    def _leer_inputs(self) -> tuple:
        nombre = self._entry_nombre.get().strip()
        cargo = self._cargo_var.get()
        dias_str = self._entry_dias.get().strip()

        if not nombre or not dias_str:
            raise ValueError("Todos los campos son obligatorios.")
        if not dias_str.isdigit() or int(dias_str) <= 0:
            raise ValueError("Los días trabajados deben ser un número entero positivo.")
        return nombre, cargo, int(dias_str)

    def _on_calcular(self) -> None:
        try:
            nombre, cargo, dias = self._leer_inputs()
            total = self._servicio.calcular_pago(nombre, cargo, dias)
            cargo_obj = Cargo.desde_descripcion(cargo)
            salario_diario = cargo_obj.get_salario_diario()
            self._mostrar_resultado_pago(nombre, cargo, dias, salario_diario, total)
        except ValueError as e:
            messagebox.showwarning("Datos inválidos", str(e), parent=self._ventana)
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e), parent=self._ventana)

    def _mostrar_resultado_pago(self, nombre, cargo, dias, salario_diario, total) -> None:
        ventana = tk.Toplevel(self._ventana)
        ventana.title("Resultado del Cálculo")
        ventana.geometry("400x420")
        ventana.resizable(False, False)
        ventana.configure(bg="#1e1e2e")
        ventana.grab_set()
        ventana.transient(self._ventana)
        ventana.update_idletasks()
        x = self._ventana.winfo_x() + (self._ventana.winfo_width() // 2) - 200
        y = self._ventana.winfo_y() + (self._ventana.winfo_height() // 2) - 210
        ventana.geometry(f"+{x}+{y}")

        frame_header = tk.Frame(ventana, bg="#89b4fa", pady=18)
        frame_header.pack(fill="x")
        tk.Label(frame_header, text="💰 Resumen de Pago", bg="#89b4fa",
                 fg="#1e1e2e", font=("Inter", 14, "bold")).pack()
        tk.Label(frame_header, text="Constructora Mejor", bg="#89b4fa",
                 fg="#1e1e2e", font=("Inter", 9)).pack()

        frame_card = tk.Frame(ventana, bg="#313244", padx=24, pady=20)
        frame_card.pack(fill="x", padx=20, pady=(16, 10))

        def fila(etiqueta, valor, color_valor="#cdd6f4"):
            f = tk.Frame(frame_card, bg="#313244")
            f.pack(fill="x", pady=4)
            tk.Label(f, text=etiqueta, bg="#313244", fg="#6c7086",
                     font=("Inter", 9), anchor="w").pack(side="left")
            tk.Label(f, text=valor, bg="#313244", fg=color_valor,
                     font=("Inter", 9, "bold"), anchor="e").pack(side="right")

        fila("👤  Empleado", nombre)
        fila("🏗️  Cargo", cargo)
        fila("📅  Días trabajados", f"{dias} días")
        fila("💵  Salario diario", f"${salario_diario:,.0f}")

        tk.Frame(frame_card, bg="#45475a", height=1).pack(fill="x", pady=(10, 6))
        tk.Label(frame_card, text="TOTAL A PAGAR", bg="#313244",
                 fg="#6c7086", font=("Inter", 8, "bold")).pack()
        tk.Label(frame_card, text=f"${total:,.0f}", bg="#313244",
                 fg="#a6e3a1", font=("Inter", 22, "bold")).pack(pady=(2, 0))
        tk.Label(frame_card, text="COP", bg="#313244",
                 fg="#6c7086", font=("Inter", 8)).pack()

        tk.Label(ventana, text=f"${salario_diario:,.0f} × {dias} días = ${total:,.0f}",
                 bg="#1e1e2e", fg="#45475a", font=("Inter", 8)).pack(pady=(0, 10))
        tk.Button(ventana, text="Cerrar", command=ventana.destroy,
                  bg="#f38ba8", fg="#1e1e2e", activebackground="#eba0ac",
                  relief="flat", font=("Inter", 10, "bold"),
                  cursor="hand2", padx=20, pady=6).pack(pady=(0, 18))

    def _on_guardar(self) -> None:
        try:
            nombre, cargo, dias = self._leer_inputs()
            empleado = self._servicio.registrar_empleado(nombre, cargo, dias)
            self._label_resultado.config(
                text=f"✅ Guardado: {empleado.nombre} — ${empleado.calcular_pago():,.0f}",
                fg="#a6e3a1"
            )
            self._entry_nombre.delete(0, tk.END)
            self._entry_dias.delete(0, tk.END)
        except ValueError as e:
            messagebox.showwarning("Datos inválidos", str(e), parent=self._ventana)
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e), parent=self._ventana)

    def _on_reporte(self) -> None:
        mensaje = self._servicio.generar_reporte()
        ventana_reporte = tk.Toplevel(self._ventana)
        ventana_reporte.title("Reporte de Nómina")
        ventana_reporte.configure(bg="#1e1e2e")
        ventana_reporte.geometry("520x420")

        frame = tk.Frame(ventana_reporte, bg="#1e1e2e")
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        tk.Label(frame, text="📋 Reporte de Nómina", bg="#1e1e2e",
                 fg="#89b4fa", font=("Inter", 12, "bold")).pack(pady=(0, 10))

        empleados = self._servicio.obtener_todos_los_empleados()
        if not empleados:
            tk.Label(frame, text="No hay empleados registrados.", bg="#1e1e2e",
                     fg="#f38ba8", font=("Inter", 10)).pack()
        else:
            texto = tk.Text(frame, bg="#313244", fg="#cdd6f4", font=("Courier", 9),
                            relief="flat", wrap="none")
            scroll = tk.Scrollbar(frame, command=texto.yview)
            texto.configure(yscrollcommand=scroll.set)
            scroll.pack(side="right", fill="y")
            texto.pack(fill="both", expand=True)
            for emp in empleados:
                texto.insert(tk.END, f"{'─'*44}\n")
                texto.insert(tk.END, f"  Nombre  : {emp.nombre}\n")
                texto.insert(tk.END, f"  Cargo   : {emp.cargo.descripcion}\n")
                texto.insert(tk.END, f"  Días    : {emp.dias_trabajados}\n")
                texto.insert(tk.END, f"  Total   : ${emp.calcular_pago():,}\n")
            total = sum(e.calcular_pago() for e in empleados)
            texto.insert(tk.END, f"{'═'*44}\n")
            texto.insert(tk.END, f"  TOTAL NÓMINA : ${total:,}\n")
            texto.config(state="disabled")
        tk.Label(frame, text=mensaje, bg="#1e1e2e", fg="#a6e3a1",
                 font=("Inter", 8), wraplength=480, justify="left").pack(pady=(10, 0))

    # ------------------------------------------------------------------ #
    # Ejecución
    # ------------------------------------------------------------------ #

    def ejecutar(self) -> None:
        if self._master:
            self._master.withdraw()
            self._ventana.wait_window()
        else:
            self._ventana.mainloop()
