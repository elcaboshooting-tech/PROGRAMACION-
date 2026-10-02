import flet as ft


def main(page: ft.Page):
    # Configuración de la ventana principal
    page.title = "Calculadora con Historial"
    page.window.width = 700
    page.window.height = 480
    page.window.resizable = True
    page.padding = 15

    # Variable para guardar la expresión
    expresion = [""]

    # --- PANTALLA DE LA CALCULADORA ---
    display = ft.TextField(
        value="0",
        read_only=True,
        text_align="right",
        text_size=24,
        border_radius=8
    )

    # --- LISTA DEL HISTORIAL ---
    historial_list = ft.ListView(
        expand=True,
        spacing=5,
        padding=5,
        auto_scroll=True
    )

    # Lógica de los botones
    def click_boton(e):
        texto = e.control.data

        if texto == "C":
            expresion[0] = ""
            display.value = "0"

        elif texto == "⌫":
            expresion[0] = expresion[0][:-1]
            display.value = expresion[0] if expresion[0] else "0"

        elif texto == "=":
            if not expresion[0]:
                return
            try:
                # Reemplazo de operadores
                expr_eval = expresion[0].replace("×", "*").replace("÷", "/")
                resultado = eval(expr_eval)

                # Formato si es entero
                if isinstance(resultado, float) and resultado.is_integer():
                    resultado = int(resultado)

                # Agregar elemento al historial
                linea = f"{expresion[0]} = {resultado}"
                historial_list.controls.insert(
                    0, 
                    ft.Text(linea, size=15, weight="w500")
                )

                display.value = str(resultado)
                expresion[0] = str(resultado)

            except Exception:
                display.value = "Error"
                expresion[0] = ""

        else:
            if display.value in ["0", "Error"]:
                expresion[0] = texto
            else:
                expresion[0] += texto
            display.value = expresion[0]

        page.update()

    def borrar_historial(e):
        historial_list.controls.clear()
        page.update()

    # --- BOTONES DE LA CALCULADORA ---
    botones_def = [
        ["C", "⌫", "%", "/"],
        ["7", "8", "9", "*"],
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["0", ".", "="]
    ]

    grid_botones = ft.Column(spacing=6, expand=True)

    for fila in botones_def:
        row_controls = []
        for btn_text in fila:
            es_operador = btn_text in ["/", "*", "-", "+", "="]
            btn = ft.Button(
                content=ft.Text(btn_text, color="white" if es_operador else None),
                data=btn_text,
                on_click=click_boton,
                expand=True,
                bgcolor="blue" if es_operador else None,
            )
            row_controls.append(btn)
        grid_botones.controls.append(ft.Row(row_controls, spacing=6, expand=True))

    # --- SECCIÓN IZQUIERDA: CALCULADORA ---
    col_calculadora = ft.Column(
        controls=[display, grid_botones],
        expand=2,
        spacing=10
    )

    # --- SECCIÓN DERECHA: HISTORIAL ---
    col_historial = ft.Column(
        controls=[
            ft.Text("Historial de Operaciones", size=16, weight="bold"),
            ft.Container(
                content=historial_list,
                border=ft.Border.all(width=1, color="grey"),
                border_radius=8,
                expand=True,
                padding=5
            ),
            ft.Button(
                content=ft.Text("Borrar Historial"),
                icon="delete_outline",
                on_click=borrar_historial
            )
        ],
        expand=1,
        spacing=10
    )

    # Layout Principal
    layout_principal = ft.Row(
        controls=[
            col_calculadora,
            ft.VerticalDivider(width=1),
            col_historial
        ],
        expand=True,
        spacing=15
    )

    page.add(layout_principal)


if __name__ == "__main__":
    if hasattr(ft, "run"):
        ft.run(main)
    else:
        ft.app(target=main)