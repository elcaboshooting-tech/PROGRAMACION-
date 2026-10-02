import tkinter as tk
from tkinter import ttk


class CalculadoraTkinter(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Calculadora 2 - Tkinter")
        self.geometry("360x480")
        self.resizable(False, False)

        self.historial = []
        self.operacion_actual = ""

        self.init_ui()

    def init_ui(self):
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Pantalla de entrada
        self.pantalla = ttk.Entry(
            main_frame, font=("Arial", 18), justify="right"
        )
        self.pantalla.pack(fill=tk.X, pady=(0, 10))

        # Rejilla de botones
        grid_frame = ttk.Frame(main_frame)
        grid_frame.pack(fill=tk.BOTH, expand=True)

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

        for texto, fila, col in botones:
            btn = ttk.Button(
                grid_frame,
                text=texto,
                command=lambda t=texto: self.al_pulsar_boton(t),
            )
            btn.grid(row=fila, column=col, sticky="nsew", padx=2, pady=2)

        for i in range(4):
            grid_frame.rowconfigure(i, weight=1)
            grid_frame.columnconfigure(i, weight=1)

        # Historial
        lbl_historial = ttk.Label(
            main_frame, text="Historial (Últimas 5):", font=("Arial", 10, "bold")
        )
        lbl_historial.pack(anchor="w", pady=(10, 2))

        self.lista_historial = tk.Listbox(
            main_frame, height=5, font=("Arial", 10)
        )
        self.lista_historial.pack(fill=tk.BOTH, expand=True)

    def al_pulsar_boton(self, texto):
        if texto == "C":
            self.operacion_actual = ""
            self.actualizar_pantalla("")
        elif texto == "=":
            self.calcular_resultado()
        else:
            self.operacion_actual += texto
            self.actualizar_pantalla(self.operacion_actual)

    def actualizar_pantalla(self, valor):
        self.pantalla.delete(0, tk.END)
        self.pantalla.insert(0, valor)

    def calcular_resultado(self):
        if not self.operacion_actual:
            return

        try:
            resultado = eval(self.operacion_actual)
            if isinstance(resultado, float) and resultado.is_integer():
                resultado = int(resultado)

            expresion = f"{self.operacion_actual} = {resultado}"
            self.actualizar_pantalla(str(resultado))
            self.agregar_al_historial(expresion)
            self.operacion_actual = str(resultado)

        except ZeroDivisionError:
            self.actualizar_pantalla("Error: Div / 0")
            self.operacion_actual = ""
        except Exception:
            self.actualizar_pantalla("Error")
            self.operacion_actual = ""

    def agregar_al_historial(self, item):
        self.historial.append(item)
        if len(self.historial) > 5:
            self.historial.pop(0)

        self.lista_historial.delete(0, tk.END)
        for op in self.historial:
            self.lista_historial.insert(tk.END, op)


if __name__ == "__main__":
    app = CalculadoraTkinter()
    app.mainloop()