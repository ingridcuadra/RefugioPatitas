from utils.formatear_texto import formatear_titulo, agregar_separador
from utils.navegar_menu import elegir_opcion
from utils.validaciones import incrementar_id, confirmar, validar_id_seleccionado
from modulos.animales import animales
from datetime import date


atenciones = []
TIPOS_ATENCION = ("vacuna","desparasitacion","control", "cirugia", "otro")

def submenu_atencion_veterinaria():
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
            registrar_atencion()
        elif opcion == "2":
            listar_atenciones()
        elif opcion == "3":
            print("Función pendiente")
        elif opcion == "4":
            print("Función pendiente")
        elif opcion == "5":
            print("Función pendiente")
        elif opcion == "6":
            print("Función pendiente")
        elif opcion == "9":
            break


def registrar_atencion():
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
    #print(atenciones) sirve para el debugg, prueba
    print(f"\n✅ Atención registrada con ID #{atencion['id']}")


def mostrar_atencion(atencion):
    agregar_separador()

    nombre_animal = ""

    for animal in animales:
        if animal["id"] == atencion["id_animal"]:
            nombre_animal = animal["nombre"]
            break

    print(f"ID: {atencion['id']}")
    print(f"Animal: {nombre_animal}")
    print("Fecha:", atencion["fecha"].strftime("%d/%m/%Y"))
    print(f"Tipo: {atencion['tipo']}")
    print(f"Observaciones: {atencion['observaciones']}")

def listar_atenciones():
    formatear_titulo("LISTADO DE ATENCIONES")

    if not atenciones:
        print("No hay atenciones registradas.")
        return
    
    for atencion in atenciones:
        mostrar_atencion(atencion)

    agregar_separador()
    print(f"total {len(atenciones)} atencion/es registradas.")