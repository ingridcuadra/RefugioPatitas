from utils.formatear_texto import formatear_titulo, agregar_separador
from utils.navegar_menu import elegir_opcion
from modulos.atencion_veterinaria import obtener_historial_animal
from utils.validaciones import incrementar_id, validar_numero_seleccionado, confirmar_accion
from utils.funciones import leer_registros, guardar_registro, pedir_fecha, encontrar_registro_por_id


ESTADOS_ANIMAL = ("en_refugio", "en_adopcion", "adoptado")
ARCHIVO_ANIMALES_RUTA = "archivos/animales.json"
animales = leer_registros(ARCHIVO_ANIMALES_RUTA)
ESPECIES = ("perro", "gato", "otro")


def leer_animales():
    return leer_registros(ARCHIVO_ANIMALES_RUTA)

def submenu_animales():
    while True:
        formatear_titulo("ANIMALES DEL REFUGIO")
        print("  1. Cargar un animal nuevo")
        print("  2. Ver listado de animales")
        print("  3. Buscar un animal")
        print("  4. Cambiar estado de un animal")
        print("  5. Dar de baja un animal")
        print("  9. Volver al menú principal")
        opcion = elegir_opcion({"1", "2", "3", "4", "5", "9"})
        if opcion == "1":
            cargar_animal()
        elif opcion == "2":
            listar_animales()
        elif opcion == "3":
            buscar_animal()
        elif opcion == "4":
            modificar_estado_animal()
        elif opcion == "5":
            eliminar_animal()
        elif opcion == "9":
            break


def cargar_animal():
    formatear_titulo("NUEVO ANIMAL")
    nombre = input("Nombre: ").strip()
    
    print("\nEspecies disponibles:")
    print("Especie: 1) perro  2) gato  3) otro")
    idx = validar_numero_seleccionado("Elegí (1-3): ", 1, 3)
    especie = ESPECIES[idx - 1]

    edad = validar_numero_seleccionado("Edad aproximada (años): ", 0) # Valida que el usuario ingrese un número entero y que esté dentro del rango permitido.
    fecha_ingreso = pedir_fecha("Fecha de ingreso")
    historia = input("Historia de cómo llegó: ").strip()

    animal = {
        "id": incrementar_id(animales),
        "nombre": nombre,
        "especie": especie,
        "edad_aproximada": edad,
        "fecha_ingreso": fecha_ingreso,
        "estado": "en_refugio",
        "historia": historia
    }

    animales.append(animal)
    guardar_registro(ARCHIVO_ANIMALES_RUTA, animales)
    print(f"\n✅ {nombre} fue registrado con ID #{animal['id']}")


def mostrar_animal(animal):
    agregar_separador()

    print(f"ID #{animal['id']} | {animal['nombre']} ({animal['especie']})")
    print(f"Edad: {animal['edad_aproximada']} años")
    print(f"Estado: {animal['estado']}")
    print("Fecha ingreso:", animal["fecha_ingreso"])
    print(f"Historia: {animal['historia']}")

    #mostrar el historial veterinario del animal si es que lo tiene
    
    historial = obtener_historial_animal(animal["id"])
    print("\nHistorial veterinario:")

    if not historial:
        print("Sin atenciones registradas.")
    else:
        for atencion in historial:
            print(
                f"- {atencion['fecha'].strftime('%d/%m/%Y')} "
                f"| {atencion['tipo']} "
                f"| {atencion['observaciones']}"
            )

def listar_animales():
    formatear_titulo("LISTADO DE ANIMALES")
    print("  Filtrar por: 1) Todos  2) En refugio  3) En adopción  4) Adoptados")
    opcion = elegir_opcion({"1", "2", "3", "4"})
    filtros = {
        "1": None,
        "2": "en_refugio",
        "3": "en_adopcion",
        "4": "adoptado",
    }
    estado_filtro = filtros[opcion]
    lista = [a for a in animales if estado_filtro is None or a["estado"] == estado_filtro]

    if not lista:
        print("  No hay animales que coincidan.")
        return
    for a in lista:
        mostrar_animal(a)

    agregar_separador()
    print(f"  Total: {len(lista)} animal/es.")


def buscar_por_nombre_o_id():
    texto = input("Ingresá nombre o número de ficha: ").strip()

    if texto.isdigit():
        resultado = [
            animal
            for animal in animales
            if animal["id"] == int(texto)
        ]
    else:
        resultado = [
            animal
            for animal in animales
            if texto.lower() in animal["nombre"].lower()
        ]

    return resultado

def buscar_animal():
    formatear_titulo("BUSCAR ANIMAL")

    resultados = buscar_por_nombre_o_id()

    if not resultados:
        print("No se encontró ningún animal.")
        return

    for animal in resultados:
        mostrar_animal(animal)

    agregar_separador()


def modificar_estado_animal():
    formatear_titulo("MODIFICAR ESTADO DE ANIMAL")
    resultados = buscar_por_nombre_o_id()

    if not resultados:
        print("No se encontró ningún animal.")
        return
    animal = resultados[0]
    mostrar_animal(animal)

    print("Estados disponibles: 1) en refugio 2) en adopción 3) adoptado")
    opcion = elegir_opcion({"1", "2", "3"})
    nuevo_estado = ESTADOS_ANIMAL[int(opcion) - 1]
    if animal["estado"] == nuevo_estado:
        print(f"El nuevo estado es el mismo que el actual ({nuevo_estado}). No se realizarán cambios.")
    else:
        print(f"Cambiando estado de #{animal['nombre']} de '{animal['estado']}' a '{nuevo_estado}'")
        animal["estado"] = nuevo_estado

    guardar_registro(ARCHIVO_ANIMALES_RUTA, animales)



def eliminar_animal():
    formatear_titulo("ELIMINAR ANIMAL")
    resultados = buscar_por_nombre_o_id()
    if not resultados:
            print("No se encontró ningún animal.")
            return
    for animal in resultados:
        mostrar_animal(animal)
        if confirmar_accion(f"¿Eliminar a #{animal['nombre']}?"):
            animales.remove(animal)
            guardar_registro(ARCHIVO_ANIMALES_RUTA, animales)
            print("✅ Animal eliminado.")


#prueba para que funcione el modulo de ingrid

def cambiar_estado_animal(id_animal, index_estado):
    animales = leer_animales()

    if id_animal is None:
        return
    
    if index_estado is None:
        return
    
    animal = encontrar_registro_por_id(id_animal, animales)
    animal["estado"] = ESTADOS_ANIMAL[index_estado]

    guardar_registro(ARCHIVO_ANIMALES_RUTA, animales)
