from utils.formatear_texto import formatear_titulo, agregar_separador
from utils.validaciones import incrementar_id, confirmar, validar_id_seleccionado, validar_email, validar_telefono
from utils.navegar_menu import elegir_opcion

adoptantes = []

TIPOS_VIVIENDA = (
    "casa_con_patio",
    "departamento",
    "casa_sin_patio"
)

def submenu_adoptantes():
    while True:
        formatear_titulo(" FAMILIAS ADOPTANTES")
        print("1. Registrar familia")
        print("2. Listar familias")
        print("3. Buscar familia")
        print("4. Actualizar datos de una familia")
        print("5. Eliminar familia")
        print("9. Volver al menu principal")

        opcion = elegir_opcion({"1", "2", "3", "4", "5", "9"})

        if opcion == "1":
            registrar_familia()
        elif opcion == "2":
            listar_adoptantes()
        elif opcion == "3":
            print("funcion pendiente")
        elif opcion == "4":
            print("funcion pendiente")
        elif opcion == "5":
            print("funcion pendiente")
        elif opcion == "9":
            break


def registrar_familia():
    formatear_titulo("NUEVA FAMILIA")

    dni = input("DNI: ").strip()
    if any(a["dni"] == dni for a in adoptantes):
        print("  ⚠  Ya existe una familia con ese DNI.")
        return
    nombre = input("Nombre completo: ").strip()
    telefono = validar_telefono()
    email = validar_email()

    print("\nTipo de vivienda:")
    print("1) Casa con patio 2) Departamento 3) Casa sin patio")
    idx = validar_id_seleccionado("Elegí (1-3): ", 1, 3)
    vivienda = TIPOS_VIVIENDA[(idx)-1]

    while True:
        respuesta = input(
            "¿Tiene otras mascotas? (s/n): "
        ).strip().lower()

        if respuesta in ("s", "n"):
            break

        print("⚠ Ingresá s o n.")
    otras_mascotas = respuesta == "s"

    adoptante = {
    "id": incrementar_id(adoptantes),
    "dni": dni,
    "nombre": nombre,
    "telefono": telefono,
    "email": email,
    "tipo_vivienda": vivienda,
    "otras_mascotas": otras_mascotas
    }
    adoptantes.append(adoptante)
    print(adoptantes)


def mostrar_adoptante(adoptante):
    agregar_separador()

    print(f"ID #{adoptante['id']} | "f"{adoptante['nombre']}")
    print(f"DNI: {adoptante['dni']}")
    print(f"Teléfono: {adoptante['telefono']}")
    print(f"Email: {adoptante['email']}")
    print(f"Vivienda: "f"{adoptante['tipo_vivienda']}")
    print(f"Otras mascotas: "f"{'Sí' if adoptante['otras_mascotas'] else 'No'}")


def listar_adoptantes():
    formatear_titulo("LISTADO DE FAMILIAS")

    if not adoptantes:
        print("No hay familias registradas.")
        return

    for adoptante in adoptantes:
        mostrar_adoptante(adoptante)

    agregar_separador()

    print(f"Total: {len(adoptantes)} familia/s.")