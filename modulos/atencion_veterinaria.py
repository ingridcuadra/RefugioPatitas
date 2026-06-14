from utils.formatear_texto import formatear_titulo, agregar_separador
from utils.navegar_menu import elegir_opcion
from utils.validaciones import incrementar_id, confirmar, validar_id_seleccionado
from datetime import date


atenciones = []
TIPOS_ATENCION = ("vacuna","desparasitacion","control", "cirugia", "otro")

def submenu_atencion_veterinaria(animales):
    while True:
        formatear_titulo("ATENCION VETERINARIA")

        print("  1. Registrar atención medica")
        print("  2. Ver listado de todas las atenciones")
        print("  3. Buscar por animal")
        print("  4. Buscar por tipo")
        print("  5. modificar atencion")
        print("  6. Eliminar una atencion")
        print("  9. Volver al menú principal")

        opcion = elegir_opcion({"1", "2", "3", "4", "5","6", "9"})
        if opcion == "1":
            registrar_atencion(animales)
        elif opcion == "2":
            listar_atenciones(animales)
        elif opcion == "3":
            buscar_atencion_por_animal(animales)
        elif opcion == "4":
            buscar_atencion_por_tipo(animales)
        elif opcion == "5":
            actualizar_atencion(animales)
        elif opcion == "6":
            eliminar_atencion(animales)
        elif opcion == "9":
            break


def registrar_atencion(animales):
    formatear_titulo("NUEVA ATENCION")

    id_animal = int(input("Ingrese ID del animal: "))
    animal_encontrado = None

    for animal in animales:
        if animal["id"] == id_animal:
            animal_encontrado = animal
            break 
        
    if animal_encontrado is None:
        print("No existe un animal con ese ID. Intentelo nuevamente")
        return
        
    #prints de opciones de tipo de atencion
    print("Tipo de atención: 1) vacuna  2) desparasitacion 3) control 4) cirugia 5) otro")

    idx = validar_id_seleccionado("Elegí (1-5): ", 1,5)
    tipo = TIPOS_ATENCION[idx - 1]
    
    observaciones = input("observaciones de la veterinaria: ").strip()

    atencion = {
        "id": incrementar_id(atenciones),
        "id_animal": id_animal,
        "fecha": date.today(),
        "tipo": tipo,
        "observaciones": observaciones,
        "proxima_atencion": None,

    }

    atenciones.append(atencion)
    print(f"\n✅ Atención registrada con ID #{atencion['id']}")


def mostrar_atencion(atencion, animales):
    agregar_separador()

    nombre_animal = ""

    for animal in animales:
        if animal["id"] == atencion["id_animal"]:
            nombre_animal = animal["nombre"]
            break

    print(f"ID: {atencion['id']}")
    print(f"Animal: {nombre_animal}")
    print(f"ID Animal: {animal["id"]}")
    print("Fecha:", atencion["fecha"].strftime("%d/%m/%Y"))
    print(f"Tipo: {atencion['tipo']}")
    print(f"Observaciones: {atencion['observaciones']}")


def listar_atenciones(animales):
    formatear_titulo("LISTADO DE ATENCIONES")

    if not atenciones:
        print("No hay atenciones registradas.")
        return
    
    for atencion in atenciones:
        mostrar_atencion(atencion, animales)

    agregar_separador()
    print(f"total {len(atenciones)} atencion/es registradas.")



def buscar_por_id_animal():
    id_animal = validar_id_seleccionado("Ingrese ID del animal:", 1)

    resultados = [
        atencion
        for atencion in atenciones
        if atencion["id_animal"] == id_animal
    ]

    return resultados

def buscar_atencion_por_animal(animales):
    formatear_titulo("BUSCAR ATENCION POR ANIMAL")
    resultados = buscar_por_id_animal()

    if not resultados:
        print("No se encontraron atenciones para ese animal")

    for atencion in resultados:
        mostrar_atencion(atencion, animales)

    agregar_separador()



def buscar_por_tipo():
    formatear_titulo("BUSCAR ATENCION POR TIPO")

    print("Tipo de atención: 1) vacuna 2) desparasitacion 3) control 4) cirugia 5) otro")
    idx = validar_id_seleccionado("Elegí (1-5): ", 1, 5)
    tipo = TIPOS_ATENCION[idx - 1]

    resultados = [
        atencion
        for atencion in atenciones
        if atencion["tipo"] == tipo
    ]

    return resultados

def buscar_atencion_por_tipo(animales):
    resultados = buscar_por_tipo()

    if not resultados:
        print("No se encontraron atenciones para ese tipo.")
        return

    for atencion in resultados:
        mostrar_atencion(atencion, animales)

    
    return resultados


def actualizar_atencion(animales):
    formatear_titulo("ACTUALIZAR ATENCION")

    id_atencion = validar_id_seleccionado("Ingrese ID de la atención a modificar: ")

    atencion_encontrada = None

    for atencion in atenciones:
        if atencion["id"] == id_atencion:
            atencion_encontrada = atencion
            break 

    if atencion_encontrada is None:
        print("No se encontró una atencion con ese ID.")
        return

    mostrar_atencion(atencion_encontrada, animales)

    print("Tipos disponibles: 1) Vacuna 2) Desparasitación 3) Control 4) Cirugia 5) Otro")
    idx = validar_id_seleccionado("Elegí (1-5): ",1,5)

    atencion_encontrada["tipo"] = TIPOS_ATENCION[idx - 1]

    nuevas_observaciones = input(f"Observaciones [{atencion_encontrada['observaciones']}]: ").strip()

    if nuevas_observaciones:
        atencion_encontrada["observaciones"] = nuevas_observaciones

    print("\n✅ Atención actualizada.")

#atencion veterinaria conectada a animal
def obtener_historial_animal(id_animal):
    historial = [
        atencion
        for atencion in atenciones
        if atencion["id_animal"] == id_animal
    ]

    return historial

def eliminar_atencion(animales):
    formatear_titulo("ELIMINAR ATENCION")
    id_atencion = validar_id_seleccionado("Ingrese ID de la atención: ",1)

    for atencion in atenciones:
        if atencion["id"] == id_atencion:
            mostrar_atencion(atencion, animales)
            if confirmar("¿Eliminar atención?"):
                atenciones.remove(atencion)
                print("✅ Atención eliminada.")

            return

    print("No existe esa atención.")
