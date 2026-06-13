from utils.formatear_texto import formatear_titulo, agregar_separador
from utils.navegar_menu import elegir_opcion
from utils.validaciones import incrementar_id, confirmar, validar_id_seleccionado, validar_telefono
from datetime import date

colaboradores = []
TIPO_DE_APORTE= ("voluntario","donante","ambas")
TIPO_DE_TAREA= ("paseador de perros","alimento balanceado","atencion veterinaria gratuita", "otro")



def submenu_voluntarios_donantes():
    while True:
        formatear_titulo("COLABORADORES")

        print("  1. Registrar colaborador")
        print("  2. Ver listado de todos los colaboradores")
        print("  3. Buscar por tipo de aporte")
        print("  4. Buscar por nombre o por tipo de tarea que realiza")
        print("  5. Modificar fecha del ultimo aporte")
        print("  6. Registrar colaboración ")
        print("  7. Eliminar a un colaborador")
        print("  9. Volver al menú principal")

        opcion = elegir_opcion({"1", "2", "3", "4", "5","6","7", "9"})
        if opcion == "1":
           registrar_colaborador()
        elif opcion == "2":
            listar_colaboradores()
        elif opcion == "3":
           buscar_colaborador_por_tipo()
        elif opcion == "4":
            buscar_colaborador()
        elif opcion == "5":
            actualizar_fecha_ultimo_aporte()
        elif opcion == "6":
            registrar_colaboracion()
        elif opcion == "7":
            eliminar_colaborador()
        elif opcion == "9":
            break

def registrar_colaborador():
    formatear_titulo("NUEVO COLABORADOR")

   
    nombre = input("Nombre completo: ").strip()
    telefono = validar_telefono()

    # verificar si ya existe
    for colaborador in colaboradores:
        if colaborador["nombre"].lower() == nombre.lower() and colaborador["telefono"] == telefono:
            colaborador["cantidad_colaboraciones"] += 1
            colaborador["fecha_ultimo_aporte"] = date.today().strftime("%Y-%m-%d")

            print(
                f"\n✅ Ya existía {colaborador['nombre']}. "
                f"Se agregó una nueva colaboración."
            )
            return


    fecha_ultimo_aporte = date.today().strftime("%Y-%m-%d")

    print("\nTipo de aporte:")
    print("1) Voluntario 2) Donante 3) Ambas")
    idx = validar_id_seleccionado("Elegí (1-3): ", 1, 3)
    tipo_aporte = TIPO_DE_APORTE[(idx)-1]

    print("\nQué tarea hace o que recurso aporta:")
    print("1) Paseador de perros 2) Alimento Balanceado 3) Atención veterinaria gratuita 4) Otro")
    idx = validar_id_seleccionado("Elegí (1-4): ", 1, 4)
    tipo_tarea = TIPO_DE_TAREA[(idx)-1]


    colaborador = {
    "id": incrementar_id(colaboradores),
    "nombre": nombre,
    "telefono": telefono,
    "tipo_aporte": tipo_aporte,
    "tipo_tarea": tipo_tarea,
    "fecha_ultimo_aporte": fecha_ultimo_aporte, #por default es la fecha de hoy, si se quiere modificar es el boton  5 del menu
    "cantidad_colaboraciones": 1
    }
    colaboradores.append(colaborador)
    print(f"\n✅ Colaborador registrado")


def mostrar_colaborador(colaborador):
    agregar_separador()

    print(f"ID #{colaborador['id']} | "f"{colaborador['nombre']}")
    print(f"Teléfono: {colaborador['telefono']}")
    print(f"Tipo de aporte: {colaborador['tipo_aporte']}")
    print(f"Tipo de tarea: {colaborador['tipo_tarea']}")
    print(f"Fecha del último aporte: {colaborador['fecha_ultimo_aporte']}")
    print(f"Colaboraciones realizadas:{colaborador['cantidad_colaboraciones']}")

def listar_colaboradores():
    formatear_titulo("LISTADO DE COLABORADORES")

    if not colaboradores:
        print("No hay colaboradores registrados.")
        return
    
    for colaborador in colaboradores:
        mostrar_colaborador(colaborador)

    agregar_separador()

    print(f"total: {len(colaboradores)} colaborador/es.")


def buscar_por_nombre_o_tarea():
    texto = input("Ingresá nombre o tarea del colaborador: ").strip().lower()

    resultado = [
        colaborador
        for colaborador in colaboradores
        if texto.lower() in colaborador["nombre"].lower()
        or texto in colaborador["tipo_tarea"].lower()   
        ]
    
    return resultado

def buscar_colaborador():
    formatear_titulo("BUSCAR COLABORADOR")

    resultado = buscar_por_nombre_o_tarea()

    if not resultado:
        print("No se encontraron colaboradores que coincidan.")
        return

    for colaborador in resultado:
        mostrar_colaborador(colaborador)

    agregar_separador()


#buscar por tipo de aporte
def buscar_por_tipo_aporte():
    formatear_titulo("BUSCAR COLABORADOR POR TIPO DE APORTE")

    print("Tipo de aporte: 1) Voluntario 2) Donante 3) Ambos ")
    idx = validar_id_seleccionado("Elegí (1-3): ", 1, 3)
    tipo = TIPO_DE_APORTE[idx - 1]

    resultados = [
        colaborador
        for colaborador in colaboradores
        if colaborador["tipo_aporte"] == tipo
    ]

    return resultados

#utiliza la funcion de arriba
def buscar_colaborador_por_tipo():
    resultados = buscar_por_tipo_aporte()

    if not resultados:
        print("No se encontraron colaboradores con ese tipo de aportes.")
        return

    for colaborador in resultados:
        mostrar_colaborador(colaborador)

    agregar_separador()
    return resultados


def actualizar_fecha_ultimo_aporte():
    formatear_titulo("ACTUALIZAR FECHA DEL ULTIMO APORTE")

    resultados = buscar_por_nombre_o_tarea()
    if not resultados:
        print("No se encontró ningún colaborador.")
        return
    
    colaborador = resultados[0]
    mostrar_colaborador(colaborador)

    nueva_fecha = input("Ingrese la nueva fecha del último aporte(YYYY-MM-DD): ").strip()
    colaborador["fecha_ultimo_aporte"] = nueva_fecha
    print(f"✅ Fecha del ultimo aporte actualizada a {nueva_fecha}.")


def registrar_colaboracion():
    formatear_titulo("REGISTRAR COLABORACIÓN")

    resultados = buscar_por_nombre_o_tarea()

    if not resultados:
        print("No se encontró ningún colaborador.")
        return
    
    colaborador = resultados[0]

    colaborador["cantidad_colaboraciones"] += 1
    colaborador["fecha_ultimo_aporte"] = date.today()

    print(
        f"✅ {colaborador['nombre']} ahora tiene "
        f"{colaborador['cantidad_colaboraciones']} colaboraciones."
    )

def eliminar_colaborador():
    formatear_titulo("DAR DE BAJA COLABORADOR")
    resultados = buscar_por_nombre_o_tarea()
    if not resultados:
        print("No se encontró ningún colaborador.")
        return
    for colaborador in resultados:
        mostrar_colaborador(colaborador)

        if confirmar(f"¿Dar de baja a {colaborador['nombre']}?"):
            colaboradores.remove(colaborador)
            print("✅ Colaborador eliminado.")
        else:
            print("Operación cancelada.")

    agregar_separador()