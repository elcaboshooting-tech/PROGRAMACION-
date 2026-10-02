import flet as ft


def main(page: ft.Page):
    page.title = "Portal Académico - Sistema de Registro de Estudiantes"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 1000
    page.window.height = 680
    page.padding = 20

    # Base de datos en memoria
    estudiantes = {}

    # --- CONTROLES DEL FORMULARIO ---
    input_id = ft.TextField(
        label="Matrícula / ID", hint_text="Ej: 1001", width=320
    )
    input_nombre = ft.TextField(
        label="Nombre Completo", hint_text="Nombre del estudiante", width=320
    )
    input_email = ft.TextField(
        label="Correo Electrónico",
        hint_text="correo@universidad.edu",
        width=320,
    )

    combo_carrera = ft.Dropdown(
        label="Carrera",
        width=320,
        options=[
            ft.dropdown.Option("Ingeniería de Sistemas"),
            ft.dropdown.Option("Ingeniería Agronómica"),
            ft.dropdown.Option("Arquitectura"),
            ft.dropdown.Option("Medicina"),
            ft.dropdown.Option("Derecho"),
        ],
        value="Ingeniería de Sistemas",
    )

    rg_turno = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="Mañana", label="Mañana"),
                ft.Radio(value="Tarde", label="Tarde"),
                ft.Radio(value="Noche", label="Noche"),
            ]
        ),
        value="Mañana",
    )

    chk_beca = ft.Checkbox(label="Becado")
    chk_extranjero = ft.Checkbox(label="Extranjero")

    input_buscar = ft.TextField(
        label="Buscar por ID", width=180, height=40
    )

    # --- TABLA DE DATOS ---
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Matrícula")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Carrera")),
            ft.DataColumn(ft.Text("Turno")),
            ft.DataColumn(ft.Text("Becado")),
        ],
        rows=[],
    )

    # --- COMPONENTE DIÁLOGO MODAL ---
    def abrir_dialogo(titulo, contenido):
        def cerrar_dialogo(e):
            page.close(dlg)

        dlg = ft.AlertDialog(
            title=ft.Text(titulo, weight=ft.FontWeight.BOLD),
            content=contenido,
            actions=[ft.Button("Cerrar", on_click=cerrar_dialogo)],
        )
        page.open(dlg)

    def mostrar_alerta(mensaje):
        abrir_dialogo("Atención", ft.Text(mensaje))

    # --- FUNCIONES Y LÓGICA ---
    def validar_datos():
        mat = input_id.value.strip() if input_id.value else ""
        nom = input_nombre.value.strip() if input_nombre.value else ""
        email = input_email.value.strip() if input_email.value else ""

        if not mat or not nom or not email:
            mostrar_alerta("Todos los campos obligatorios deben ser llenados.")
            return False
        if not mat.isdigit():
            mostrar_alerta("La matrícula debe contener únicamente números.")
            return False
        if "@" not in email:
            mostrar_alerta("Ingrese un correo electrónico válido.")
            return False
        return True

    def actualizar_tabla():
        tabla.rows.clear()
        for mat, est in estudiantes.items():
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(est["Matrícula"])),
                        ft.DataCell(ft.Text(est["Nombre"])),
                        ft.DataCell(ft.Text(est["Carrera"])),
                        ft.DataCell(ft.Text(est["Turno"])),
                        ft.DataCell(ft.Text(est["Becado"])),
                    ],
                    on_select_changed=lambda e, m=mat: cargar_seleccion(m),
                )
            )
        page.update()

    def registrar_estudiante(e):
        if not validar_datos():
            return

        mat = input_id.value.strip()
        datos = {
            "Matrícula": mat,
            "Nombre": input_nombre.value.strip(),
            "Correo": input_email.value.strip(),
            "Carrera": combo_carrera.value,
            "Turno": rg_turno.value,
            "Becado": "Sí" if chk_beca.value else "No",
            "Extranjero": "Sí" if chk_extranjero.value else "No",
        }

        estudiantes[mat] = datos
        actualizar_tabla()
        limpiar_formulario(None)
        mostrar_alerta(f"Estudiante {datos['Nombre']} registrado con éxito.")

    def limpiar_formulario(e):
        input_id.value = ""
        input_nombre.value = ""
        input_email.value = ""
        combo_carrera.value = "Ingeniería de Sistemas"
        rg_turno.value = "Mañana"
        chk_beca.value = False
        chk_extranjero.value = False
        page.update()

    def mostrar_ficha(datos):
        col_info = ft.Column(
            [
                ft.Text(f"Matrícula: {datos['Matrícula']}"),
                ft.Text(f"Nombre: {datos['Nombre']}"),
                ft.Text(f"Correo: {datos['Correo']}"),
                ft.Text(f"Carrera: {datos['Carrera']}"),
                ft.Text(f"Turno: {datos['Turno']}"),
                ft.Text(f"Becado: {datos['Becado']}"),
                ft.Text(f"Extranjero: {datos['Extranjero']}"),
            ],
            tight=True,
        )
        abrir_dialogo("Ficha Académica del Estudiante", col_info)

    def buscar_estudiante(e):
        mat = input_buscar.value.strip() if input_buscar.value else ""
        if mat in estudiantes:
            mostrar_ficha(estudiantes[mat])
        else:
            mostrar_alerta(
                "No se encontró ningún estudiante con esa matrícula."
            )

    def cargar_seleccion(mat):
        if mat in estudiantes:
            est = estudiantes[mat]
            input_id.value = est["Matrícula"]
            input_nombre.value = est["Nombre"]
            input_email.value = est["Correo"]
            combo_carrera.value = est["Carrera"]
            rg_turno.value = est["Turno"]
            chk_beca.value = est["Becado"] == "Sí"
            chk_extranjero.value = est["Extranjero"] == "Sí"
            page.update()

    def eliminar_estudiante(e):
        mat = input_id.value.strip() if input_id.value else ""
        if mat in estudiantes:
            del estudiantes[mat]
            actualizar_tabla()
            limpiar_formulario(None)
            mostrar_alerta("Registro eliminado correctamente.")
        else:
            mostrar_alerta(
                "Selecciona un estudiante válido ingresando su ID o seleccionando una fila de la tabla."
            )

    def ver_ficha_click(e):
        mat = input_id.value.strip() if input_id.value else ""
        if mat in estudiantes:
            mostrar_ficha(estudiantes[mat])
        else:
            mostrar_alerta("Selecciona o ingresa una matrícula válida primero.")

    # --- DISEÑO Y DISTRIBUCIÓN (LAYOUT) ---
    form_card = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Registro de Estudiantes",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="blue200",
                ),
                input_id,
                input_nombre,
                input_email,
                combo_carrera,
                ft.Text("Turno:", weight=ft.FontWeight.W_500),
                rg_turno,
                ft.Text("Condición:", weight=ft.FontWeight.W_500),
                ft.Row([chk_beca, chk_extranjero]),
                ft.Row(
                    [
                        ft.Button(
                            "Registrar",
                            on_click=registrar_estudiante,
                            bgcolor="blue400",
                            color="black",
                        ),
                        ft.Button(
                            "Limpiar", on_click=limpiar_formulario
                        ),
                    ]
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=15,
        bgcolor="#1e1e2e",
        border_radius=10,
        width=360,
    )

    table_card = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        input_buscar,
                        ft.Button("Buscar", on_click=buscar_estudiante),
                        ft.Button(
                            "Ver Ficha", on_click=ver_ficha_click
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color="red400",
                            on_click=eliminar_estudiante,
                        ),
                    ]
                ),
                ft.Column([tabla], scroll=ft.ScrollMode.ALWAYS, expand=True),
            ]
        ),
        padding=15,
        bgcolor="#1e1e2e",
        border_radius=10,
        expand=True,
    )

    page.add(
        ft.Row(
            [form_card, table_card],
            expand=True,
            alignment=ft.MainAxisAlignment.START,
        )
    )


if __name__ == "__main__":
    ft.run(main)