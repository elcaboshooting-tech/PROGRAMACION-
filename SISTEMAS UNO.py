import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class DetalleEstudianteDialog(QDialog):
    """Ventana emergente (QDialog) para visualizar o confirmar la ficha del estudiante."""

    def __init__(self, datos, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ficha Académica del Estudiante")
        self.resize(400, 320)
        self.setStyleSheet(
            """
            QDialog { background-color: #1e1e2e; color: #ffffff; }
            QLabel { color: #cdd6f4; font-size: 13px; }
            QPushButton { background-color: #89b4fa; color: #11111b; font-weight: bold; padding: 8px; border-radius: 5px; }
            QPushButton:hover { background-color: #b4befe; }
        """
        )

        layout = QVBoxLayout(self)

        titulo = QLabel(" DETALLE DEL REGISTRO")
        titulo.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #89b4fa; margin-bottom: 10px;"
        )
        layout.addWidget(titulo)

        for clave, valor in datos.items():
            lbl = QLabel(f"**{clave}:** {valor}")
            layout.addWidget(lbl)

        btn_cerrar = QPushButton("Aceptar / Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)


class SistemaEstudiantes(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "Portal Académico - Sistema de Registro de Estudiantes"
        )
        self.resize(950, 600)

        # Base de datos en memoria
        self.estudiantes = {}

        self.init_ui()
        self.aplicar_estilos()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout Principal Horizontal (Izquierda Formulario, Derecha Tabla)
        main_layout = QHBoxLayout(main_widget)

        # --- SECCIÓN IZQUIERDA: FORMULARIO (QFormLayout) ---
        panel_izq = QWidget()
        layout_izq = QVBoxLayout(panel_izq)

        lbl_titulo = QLabel("Registro de Estudiantes")
        lbl_titulo.setObjectName("titulo_seccion")
        layout_izq.addWidget(lbl_titulo)

        form_layout = QFormLayout()

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("Ej: 1001")
        form_layout.addRow(QLabel("Matrícula / ID:"), self.input_id)

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre completo")
        form_layout.addRow(QLabel("Estudiante:"), self.input_nombre)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("correo@universidad.edu")
        form_layout.addRow(QLabel("Correo Electrónico:"), self.input_email)

        self.combo_carrera = QComboBox()
        self.combo_carrera.addItems(
            [
                "Ingeniería de Sistemas",
                "Ingeniería Agronómica",
                "Arquitectura",
                "Medicina",
                "Derecho",
            ]
        )
        form_layout.addRow(QLabel("Carrera:"), self.combo_carrera)

        # Radio Buttons para Turno
        layout_turno = QHBoxLayout()
        self.rb_manana = QRadioButton("Mañana")
        self.rb_tarde = QRadioButton("Tarde")
        self.rb_noche = QRadioButton("Noche")
        self.rb_manana.setChecked(True)
        layout_turno.addWidget(self.rb_manana)
        layout_turno.addWidget(self.rb_tarde)
        layout_turno.addWidget(self.rb_noche)
        form_layout.addRow(QLabel("Turno:"), layout_turno)

        # Checkboxes para condiciones adicionales
        layout_checks = QHBoxLayout()
        self.chk_beca = QCheckBox("Becado")
        self.chk_extranjero = QCheckBox("Extranjero")
        layout_checks.addWidget(self.chk_beca)
        layout_checks.addWidget(self.chk_extranjero)
        form_layout.addRow(QLabel("Condición:"), layout_checks)

        layout_izq.addLayout(form_layout)

        # Botones de Acción
        layout_botones = QHBoxLayout()
        self.btn_guardar = QPushButton("Registrar")
        self.btn_limpiar = QPushButton("Limpiar")
        layout_botones.addWidget(self.btn_guardar)
        layout_botones.addWidget(self.btn_limpiar)
        layout_izq.addLayout(layout_botones)

        # --- SECCIÓN DERECHA: BÚSQUEDA Y TABLA DE DATOS ---
        panel_der = QWidget()
        layout_der = QVBoxLayout(panel_der)

        # Barra de Búsqueda
        layout_busqueda = QHBoxLayout()
        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("Buscar por ID de matrícula...")
        self.btn_buscar = QPushButton("Buscar")
        self.btn_ver_detalle = QPushButton("Ver Ficha")
        self.btn_eliminar = QPushButton("Eliminar")

        layout_busqueda.addWidget(self.input_buscar)
        layout_busqueda.addWidget(self.btn_buscar)
        layout_busqueda.addWidget(self.btn_ver_detalle)
        layout_busqueda.addWidget(self.btn_eliminar)
        layout_der.addLayout(layout_busqueda)

        # Tabla de Registros
        self.tabla = QTableWidget(0, 5)
        self.tabla.setHorizontalHeaderLabels(
            ["Matrícula", "Nombre", "Carrera", "Turno", "Becado"]
        )
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout_der.addWidget(self.tabla)

        # Ensamblado del Layout Principal
        main_layout.addWidget(panel_izq, 40)
        main_layout.addWidget(panel_der, 60)

        # Conexión de Señales / Eventos
        self.btn_guardar.clicked.connect(self.registrar_estudiante)
        self.btn_limpiar.clicked.connect(self.limpiar_formulario)
        self.btn_buscar.clicked.connect(self.buscar_estudiante)
        self.btn_ver_detalle.clicked.connect(self.mostrar_detalle)
        self.btn_eliminar.clicked.connect(self.eliminar_estudiante)
        self.tabla.itemClicked.connect(self.cargar_estudiante_seleccionado)

    def aplicar_estilos(self):
        qss = """
            QMainWindow { background-color: #181825; }
            QWidget { color: #cdd6f4; font-family: 'Segoe UI', sans-serif; }
            #titulo_seccion { font-size: 18px; font-weight: bold; color: #89b4fa; margin-bottom: 10px; }
            QLineEdit, QComboBox { background-color: #313244; border: 1px solid #45475a; border-radius: 6px; padding: 6px; color: #ffffff; }
            QLineEdit:focus, QComboBox:focus { border: 1px solid #89b4fa; }
            QPushButton { background-color: #89b4fa; color: #11111b; font-weight: bold; border-radius: 6px; padding: 8px 12px; }
            QPushButton:hover { background-color: #b4befe; }
            QTableWidget { background-color: #1e1e2e; border: 1px solid #45475a; gridline-color: #313244; color: #ffffff; }
            QHeaderView::section { background-color: #313244; color: #89b4fa; font-weight: bold; padding: 5px; border: none; }
            QCheckBox, QRadioButton { color: #cdd6f4; }
        """
        self.setStyleSheet(qss)

    def validar_datos(self):
        mat = self.input_id.text().strip()
        nom = self.input_nombre.text().strip()
        email = self.input_email.text().strip()

        if not mat or not nom or not email:
            QMessageBox.warning(
                self,
                "Validación Error",
                "Todos los campos obligatorios deben ser llenados.",
            )
            return False
        if not mat.isdigit():
            QMessageBox.warning(
                self,
                "Validación Error",
                "La matrícula debe contener únicamente números.",
            )
            return False
        if "@" not in email:
            QMessageBox.warning(
                self, "Validación Error", "Ingrese un correo electrónico válido."
            )
            return False
        return True

    def registrar_estudiante(self):
        if not self.validar_datos():
            return

        mat = self.input_id.text().strip()

        # Determinar Turno
        turno = "Mañana"
        if self.rb_tarde.isChecked():
            turno = "Tarde"
        elif self.rb_noche.isChecked():
            turno = "Noche"

        datos = {
            "Matrícula": mat,
            "Nombre": self.input_nombre.text().strip(),
            "Correo": self.input_email.text().strip(),
            "Carrera": self.combo_carrera.currentText(),
            "Turno": turno,
            "Becado": "Sí" if self.chk_beca.isChecked() else "No",
            "Extranjero": "Sí" if self.chk_extranjero.isChecked() else "No",
        }

        self.estudiantes[mat] = datos
        self.actualizar_tabla()
        self.limpiar_formulario()
        QMessageBox.information(
            self, "Éxito", f"Estudiante {datos['Nombre']} registrado con éxito."
        )

    def actualizar_tabla(self):
        self.tabla.setRowCount(0)
        for mat, est in self.estudiantes.items():
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(est["Matrícula"]))
            self.tabla.setItem(row, 1, QTableWidgetItem(est["Nombre"]))
            self.tabla.setItem(row, 2, QTableWidgetItem(est["Carrera"]))
            self.tabla.setItem(row, 3, QTableWidgetItem(est["Turno"]))
            self.tabla.setItem(row, 4, QTableWidgetItem(est["Becado"]))

    def limpiar_formulario(self):
        self.input_id.clear()
        self.input_nombre.clear()
        self.input_email.clear()
        self.combo_carrera.setCurrentIndex(0)
        self.rb_manana.setChecked(True)
        self.chk_beca.setChecked(False)
        self.chk_extranjero.setChecked(False)

    def buscar_estudiante(self):
        mat = self.input_buscar.text().strip()
        if mat in self.estudiantes:
            est = self.estudiantes[mat]
            dlg = DetalleEstudianteDialog(est, self)
            dlg.exec()
        else:
            QMessageBox.warning(
                self, "Sin Resultados", "No se encontró ningún estudiante con esa matrícula."
            )

    def mostrar_detalle(self):
        row = self.tabla.currentRow()
        if row >= 0:
            mat = self.tabla.item(row, 0).text()
            dlg = DetalleEstudianteDialog(self.estudiantes[mat], self)
            dlg.exec()
        else:
            QMessageBox.information(
                self,
                "Selección requerida",
                "Selecciona una fila de la tabla primero.",
            )

    def cargar_estudiante_seleccionado(self, item):
        row = item.row()
        mat = self.tabla.item(row, 0).text()
        if mat in self.estudiantes:
            est = self.estudiantes[mat]
            self.input_id.setText(est["Matrícula"])
            self.input_nombre.setText(est["Nombre"])
            self.input_email.setText(est["Correo"])
            self.combo_carrera.setCurrentText(est["Carrera"])
            if est["Turno"] == "Mañana":
                self.rb_manana.setChecked(True)
            elif est["Turno"] == "Tarde":
                self.rb_tarde.setChecked(True)
            else:
                self.rb_noche.setChecked(True)
            self.chk_beca.setChecked(est["Becado"] == "Sí")
            self.chk_extranjero.setChecked(est["Extranjero"] == "Sí")

    def eliminar_estudiante(self):
        row = self.tabla.currentRow()
        if row < 0:
            QMessageBox.warning(
                self, "Atención", "Selecciona un estudiante de la tabla para eliminar."
            )
            return

        mat = self.tabla.item(row, 0).text()
        respuesta = QMessageBox.question(
            self,
            "Confirmación",
            f"¿Estás seguro de eliminar al estudiante con matrícula {mat}?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if respuesta == QMessageBox.Yes:
            del self.estudiantes[mat]
            self.actualizar_tabla()
            self.limpiar_formulario()
            QMessageBox.information(self, "Eliminado", "Registro eliminado correctamente.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SistemaEstudiantes()
    window.show()
    sys.exit(app.exec())