import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk

# Configuración visual global
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class DetalleEstudianteWindow(ctk.CTkToplevel):
    """Ventana emergente secundaria para ver la ficha del estudiante."""

    def __init__(self, parent, datos):
        super().__init__(parent)
        self.title("Ficha Académica del Estudiante")
        self.geometry("400x340")
        self.grab_set()  # Ventana modal (bloquea la principal hasta cerrar)

        # Título
        lbl_titulo = ctk.CTkLabel(
            self,
            text="DETALLE DEL REGISTRO",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#89b4fa",
        )
        lbl_titulo.pack(pady=15)

        # Datos
        frame_datos = ctk.CTkFrame(self)
        frame_datos.pack(fill="both", expand=True, padx=20, pady=10)

        for clave, valor in datos.items():
            lbl_item = ctk.CTkLabel(
                frame_datos,
                text=f"{clave}: {valor}",
                font=ctk.CTkFont(size=13),
                anchor="w",
            )
            lbl_item.pack(fill="x", padx=15, pady=4)

        # Botón Cerrar
        btn_cerrar = ctk.CTkButton(
            self,
            text="Aceptar / Cerrar",
            command=self.destroy,
            fg_color="#89b4fa",
            text_color="#11111b",
        )
        btn_cerrar.pack(pady=15)


class SistemaEstudiantesCTK(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Portal Académico - Sistema de Registro de Estudiantes")
        self.geometry("950x620")

        # Base de datos en memoria
        self.estudiantes = {}

        self.init_ui()

    def init_ui(self):
        # Frame Principal (Horizontal)
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # --- SECCIÓN IZQUIERDA: FORMULARIO ---
        panel_izq = ctk.CTkFrame(main_frame, width=380)
        panel_izq.pack(side="left", fill="both", padx=10, pady=10)

        lbl_titulo = ctk.CTkLabel(
            panel_izq,
            text="Registro de Estudiantes",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#89b4fa",
        )
        lbl_titulo.pack(pady=10)

        # Campos de texto
        self.input_id = ctk.CTkEntry(
            panel_izq, placeholder_text="Matrícula / ID (Ej: 1001)"
        )
        self.input_id.pack(fill="x", padx=15, pady=5)

        self.input_nombre = ctk.CTkEntry(
            panel_izq, placeholder_text="Nombre completo"
        )
        self.input_nombre.pack(fill="x", padx=15, pady=5)

        self.input_email = ctk.CTkEntry(
            panel_izq, placeholder_text="correo@universidad.edu"
        )
        self.input_email.pack(fill="x", padx=15, pady=5)

        # Combo Carrera
        lbl_carrera = ctk.CTkLabel(panel_izq, text="Carrera:")
        lbl_carrera.pack(anchor="w", padx=15, pady=(5, 0))
        self.combo_carrera = ctk.CTkOptionMenu(
            panel_izq,
            values=[
                "Ingeniería de Sistemas",
                "Ingeniería Agronómica",
                "Arquitectura",
                "Medicina",
                "Derecho",
            ],
        )
        self.combo_carrera.pack(fill="x", padx=15, pady=5)

        # RadioButtons Turno
        lbl_turno = ctk.CTkLabel(panel_izq, text="Turno:")
        lbl_turno.pack(anchor="w", padx=15, pady=(5, 0))
        self.var_turno = tk.StringVar(value="Mañana")

        frame_turno = ctk.CTkFrame(panel_izq, fg_color="transparent")
        frame_turno.pack(fill="x", padx=15, pady=5)
        ctk.CTkRadioButton(
            frame_turno, text="Mañana", variable=self.var_turno, value="Mañana"
        ).pack(side="left", padx=5)
        ctk.CTkRadioButton(
            frame_turno, text="Tarde", variable=self.var_turno, value="Tarde"
        ).pack(side="left", padx=5)
        ctk.CTkRadioButton(
            frame_turno, text="Noche", variable=self.var_turno, value="Noche"
        ).pack(side="left", padx=5)

        # Checkboxes Condición
        lbl_cond = ctk.CTkLabel(panel_izq, text="Condición:")
        lbl_cond.pack(anchor="w", padx=15, pady=(5, 0))
        frame_checks = ctk.CTkFrame(panel_izq, fg_color="transparent")
        frame_checks.pack(fill="x", padx=15, pady=5)

        self.chk_beca = ctk.CTkCheckBox(frame_checks, text="Becado")
        self.chk_beca.pack(side="left", padx=10)
        self.chk_extranjero = ctk.CTkCheckBox(frame_checks, text="Extranjero")
        self.chk_extranjero.pack(side="left", padx=10)

        # Botones Formulario
        frame_btn_form = ctk.CTkFrame(panel_izq, fg_color="transparent")
        frame_btn_form.pack(fill="x", padx=15, pady=15)
        btn_guardar = ctk.CTkButton(
            frame_btn_form, text="Registrar", command=self.registrar_estudiante
        )
        btn_guardar.pack(side="left", expand=True, padx=5)
        btn_limpiar = ctk.CTkButton(
            frame_btn_form,
            text="Limpiar",
            command=self.limpiar_formulario,
            fg_color="#45475a",
        )
        btn_limpiar.pack(side="left", expand=True, padx=5)

        # --- SECCIÓN DERECHA: BÚSQUEDA Y TABLA ---
        panel_der = ctk.CTkFrame(main_frame)
        panel_der.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Barra de Búsqueda
        frame_search = ctk.CTkFrame(panel_der, fg_color="transparent")
        frame_search.pack(fill="x", pady=10)

        self.input_buscar = ctk.CTkEntry(
            frame_search, placeholder_text="Buscar ID..."
        )
        self.input_buscar.pack(side="left", fill="x", expand=True, padx=5)

        btn_buscar = ctk.CTkButton(
            frame_search, text="Buscar", width=80, command=self.buscar_estudiante
        )
        btn_buscar.pack(side="left", padx=3)

        btn_ficha = ctk.CTkButton(
            frame_search,
            text="Ver Ficha",
            width=80,
            command=self.mostrar_detalle,
        )
        btn_ficha.pack(side="left", padx=3)

        btn_eliminar = ctk.CTkButton(
            frame_search,
            text="Eliminar",
            width=80,
            fg_color="#f38ba8",
            command=self.eliminar_estudiante,
        )
        btn_eliminar.pack(side="left", padx=3)

        # Tabla Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#1e1e2e",
            foreground="#cdd6f4",
            fieldbackground="#1e1e2e",
            rowheight=25,
        )
        style.configure(
            "Treeview.Heading",
            background="#313244",
            foreground="#89b4fa",
            font=("Segoe UI", 10, "bold"),
        )

        columns = ("Matrícula", "Nombre", "Carrera", "Turno", "Becado")
        self.tabla = ttk.Treeview(
            panel_der, columns=columns, show="headings", selectmode="browse"
        )

        for col in columns:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=110, anchor="center")

        self.tabla.pack(fill="both", expand=True, pady=10)

        # EVENTO BIND CORREGIDO (Seguro contra problemas de codificación):
        evento_seleccion = f"<{'<'}TreeviewSelect{'>'}>"
        self.tabla.bind(evento_seleccion, self.cargar_seleccion)

    def validar_datos(self):
        mat = self.input_id.get().strip()
        nom = self.input_nombre.get().strip()
        email = self.input_email.get().strip()

        if not mat or not nom or not email:
            messagebox.showwarning(
                "Error", "Todos los campos obligatorios deben ser llenados."
            )
            return False
        if not mat.isdigit():
            messagebox.showwarning(
                "Error", "La matrícula debe contener únicamente números."
            )
            return False
        if "@" not in email:
            messagebox.showwarning("Error", "Ingrese un correo electrónico válido.")
            return False
        return True

    def registrar_estudiante(self):
        if not self.validar_datos():
            return

        mat = self.input_id.get().strip()

        datos = {
            "Matrícula": mat,
            "Nombre": self.input_nombre.get().strip(),
            "Correo": self.input_email.get().strip(),
            "Carrera": self.combo_carrera.get(),
            "Turno": self.var_turno.get(),
            "Becado": "Sí" if self.chk_beca.get() == 1 else "No",
            "Extranjero": "Sí" if self.chk_extranjero.get() == 1 else "No",
        }

        self.estudiantes[mat] = datos
        self.actualizar_tabla()
        self.limpiar_formulario()
        messagebox.showinfo("Éxito", f"Estudiante {datos['Nombre']} registrado.")

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for mat, est in self.estudiantes.items():
            self.tabla.insert(
                "",
                "end",
                values=(
                    est["Matrícula"],
                    est["Nombre"],
                    est["Carrera"],
                    est["Turno"],
                    est["Becado"],
                ),
            )

    def limpiar_formulario(self):
        self.input_id.delete(0, tk.END)
        self.input_nombre.delete(0, tk.END)
        self.input_email.delete(0, tk.END)
        self.combo_carrera.set("Ingeniería de Sistemas")
        self.var_turno.set("Mañana")
        self.chk_beca.deselect()
        self.chk_extranjero.deselect()

    def buscar_estudiante(self):
        mat = self.input_buscar.get().strip()
        if mat in self.estudiantes:
            DetalleEstudianteWindow(self, self.estudiantes[mat])
        else:
            messagebox.showwarning(
                "Sin resultados", "No se encontró ningún estudiante con esa matrícula."
            )

    def mostrar_detalle(self):
        selected = self.tabla.selection()
        if selected:
            item = self.tabla.item(selected[0])
            mat = item["values"][0]
            DetalleEstudianteWindow(self, self.estudiantes[str(mat)])
        else:
            messagebox.showinfo(
                "Atención", "Selecciona una fila de la tabla primero."
            )

    def cargar_seleccion(self, event):
        selected = self.tabla.selection()
        if selected:
            item = self.tabla.item(selected[0])
            mat = str(item["values"][0])
            if mat in self.estudiantes:
                est = self.estudiantes[mat]
                self.limpiar_formulario()
                self.input_id.insert(0, est["Matrícula"])
                self.input_nombre.insert(0, est["Nombre"])
                self.input_email.insert(0, est["Correo"])
                self.combo_carrera.set(est["Carrera"])
                self.var_turno.set(est["Turno"])
                if est["Becado"] == "Sí":
                    self.chk_beca.select()
                if est["Extranjero"] == "Sí":
                    self.chk_extranjero.select()

    def eliminar_estudiante(self):
        selected = self.tabla.selection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un estudiante de la tabla.")
            return

        mat = str(self.tabla.item(selected[0])["values"][0])
        if messagebox.askyesno(
            "Confirmación", f"¿Eliminar estudiante con matrícula {mat}?"
        ):
            del self.estudiantes[mat]
            self.actualizar_tabla()
            self.limpiar_formulario()


if __name__ == "__main__":
    app = SistemaEstudiantesCTK()
    app.mainloop()