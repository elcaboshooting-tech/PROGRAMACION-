import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CalculadoraPySide6(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora 1 - PySide6")
        self.setFixedSize(350, 530)

        # Estado interno
        self.historial = []
        self.operacion_actual = ""

        self.init_ui()

    def init_ui(self):
        # --- BARRA DE MENÚ ---
        menu_bar = self.menuBar()

        # Menú Archivo
        menu_archivo = menu_bar.addMenu("&Archivo")

        accion_limpiar = QAction("Limpiar Pantalla", self)
        accion_limpiar.setShortcut("Ctrl+L")
        accion_limpiar.triggered.connect(lambda: self.al_pulsar_boton("C"))
        menu_archivo.addAction(accion_limpiar)

        accion_borrar_historial = QAction("Borrar Historial", self)
        accion_borrar_historial.triggered.connect(self.limpiar_historial)
        menu_archivo.addAction(accion_borrar_historial)

        menu_archivo.addSeparator()

        accion_salir = QAction("Salir", self)
        accion_salir.setShortcut("Ctrl+Q")
        accion_salir.triggered.connect(self.close)
        menu_archivo.addAction(accion_salir)

        # Menú Ayuda
        menu_ayuda = menu_bar.addMenu("&Ayuda")
        accion_acerca = QAction("Acerca de", self)
        accion_acerca.triggered.connect(self.mostrar_acerca_de)
        menu_ayuda.addAction(accion_acerca)

        # --- CONTENEDOR PRINCIPAL ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Pantalla de visualización
        self.pantalla = QLineEdit()
        self.pantalla.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.pantalla.setReadOnly(True)
        self.pantalla.setStyleSheet("font-size: 20px; padding: 8px;")
        layout.addWidget(self.pantalla)

        # Rejilla de botones
        grid_layout = QGridLayout()
        botones = [
            ("7", 0, 0),
            ("8", 0, 1),
            ("9", 0, 2),
            ("/", 0, 3),
            ("4", 1, 0),
            ("5", 1, 1),
            ("6", 1, 2),
            ("*", 1, 3),
            ("1", 2, 0),
            ("2", 2, 1),
            ("3", 2, 2),
            ("-", 2, 3),
            ("0", 3, 0),
            ("C", 3, 1),
            ("=", 3, 2),
            ("+", 3, 3),
        ]

        for texto, fila, columna in botones:
            btn = QPushButton(texto)
            btn.setStyleSheet("font-size: 16px; min-height: 40px;")
            btn.clicked.connect(
                lambda checked, t=texto: self.al_pulsar_boton(t)
            )
            grid_layout.addWidget(btn, fila, columna)

        layout.addLayout(grid_layout)

        # Historial de operaciones
        lbl_historial = QLabel("Historial (Últimas 5):")
        layout.addWidget(lbl_historial)

        self.lista_historial = QListWidget()
        self.lista_historial.setMaximumHeight(120)
        layout.addWidget(self.lista_historial)

    def al_pulsar_boton(self, texto):
        if texto == "C":
            self.operacion_actual = ""
            self.pantalla.setText("")
        elif texto == "=":
            self.calcular_resultado()
        else:
            self.operacion_actual += texto
            self.pantalla.setText(self.operacion_actual)

    def calcular_resultado(self):
        if not self.operacion_actual:
            return

        try:
            resultado = eval(self.operacion_actual)
            if isinstance(resultado, float) and resultado.is_integer():
                resultado = int(resultado)

            expresion = f"{self.operacion_actual} = {resultado}"
            self.pantalla.setText(str(resultado))
            self.agregar_al_historial(expresion)
            self.operacion_actual = str(resultado)

        except ZeroDivisionError:
            self.pantalla.setText("Error: Div / 0")
            self.operacion_actual = ""
        except Exception:
            self.pantalla.setText("Error")
            self.operacion_actual = ""

    def agregar_al_historial(self, item):
        self.historial.append(item)
        if len(self.historial) > 5:
            self.historial.pop(0)

        self.lista_historial.clear()
        for op in self.historial:
            self.lista_historial.addItem(op)

    def limpiar_historial(self):
        self.historial.clear()
        self.lista_historial.clear()

    def mostrar_acerca_de(self):
        QMessageBox.information(
            self,
            "Acerca de",
            "Calculadora desarrollada en PySide6.\n\n"
            "Desarrollada por: Kevin Garay Romero\n"
            "Incluye soporte para historial y operaciones básicas."
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = CalculadoraPySide6()
    ventana.show()
    sys.exit(app.exec())