from modulos.atencion_veterinaria import obtener_historial_animal
from utils.formatear_texto import formatear_titulo, agregar_separador
from utils.navegar_menu import elegir_opcion
from utils.validaciones import incrementar_id, validar_numero_seleccionado, confirmar_accion
from utils.funciones import leer_registros, guardar_registro, pedir_fecha, encontrar_registro_por_id,seleccionar_por_id

ESTADOS_ANIMAL = ("en_refugio", "en_adopcion", "adoptado")
ARCHIVO_ANIMALES_RUTA = "archivos/animales.json"
ESPECIES = ("Perro", "Gato", "Otro")
animales = leer_registros(ARCHIVO_ANIMALES_RUTA)

def cargar_animal():
    formatear_titulo("NUEVO ANIMAL")
    nombre = input("Nombre: ").strip()
    print("\nEspecies disponibles:")
    print("Especie: 1) Perro  2) Gato  3) Otro")
    idx = validar_numero_seleccionado("Elegí (1-3): ", 1, 3)
    especie = ESPECIES[idx - 1]
    edad = validar_numero_seleccionado("Edad aproximada (años): ", 0) # Valida que el usuario ingrese un número entero y que esté dentro del rango permitido.
    fecha_ingreso = pedir_fecha("Fecha de ingreso")
    historia = input("Historia de cómo llegó: ").strip()

    animal = {
        "id": incrementar_id(animales),
        "nombre": nombre.capitalize(),
        "especie": especie,
        "edad_aproximada": edad,
        "fecha_ingreso": fecha_ingreso,
        "estado": ESTADOS_ANIMAL[0],
        "historia": historia.capitalize()
    }

    animales.append(animal)
    guardar_registro(ARCHIVO_ANIMALES_RUTA, animales)
    print(f"\n✅ {nombre} fue registrado con ID #{animal['id']}")

def mostrar_animal(animal):
    agregar_separador()

    print(f"ID #{animal['id']} | {animal['nombre']} ({animal['especie']})")
    print(f"Edad: {animal['edad_aproximada']} años")
    print(f"Estado: {animal['estado']}")
    print(f"Fecha ingreso: {animal['fecha_ingreso']}")
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
    opcion = elegir_opcion("¿Por cuál filtramos?", {"1", "2", "3", "4"})
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
    
    elementos_lista = 'animal' if len(lista) == 1 else 'animales'
    print(f"  Total: {len(lista)} {elementos_lista}.")

def buscar_por_nombre_o_id():
    texto = input("Ingresá nombre o ID: ").strip()

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
        print("No se encontró ningún animal que coincida con la búsqueda.")
        return

    for animal in resultados:
        mostrar_animal(animal)

    agregar_separador()

def dar_baja_animal():
    formatear_titulo("DAR DE BAJA A UN ANIMAL")
    resultados = buscar_por_nombre_o_id()

    if not resultados:
        print("No se encontró el animal buscado")
        return
    
    for animal in resultados:
        if confirmar_accion(f"¿Estás seguro de que deseas dar de baja a {animal['nombre']}? Esta acción no se puede deshacer."):
            animales.remove(animal)
            guardar_registro(ARCHIVO_ANIMALES_RUTA, animales)
            print("Animal dado de baja con éxito.")

def cambiar_estado_animal(id_animal, index_estado):
    if id_animal is None:
        return
    
    if index_estado is None:
        return
    
    animal = encontrar_registro_por_id(id_animal, animales)
    animal["estado"] = ESTADOS_ANIMAL[index_estado]

    guardar_registro(ARCHIVO_ANIMALES_RUTA, animales)

def pasar_animal_a_en_adopcion():
    if not animales:
        print("Aún no hay animales cargados. Carga uno antes de cambiar un estado.")
        return
    
    animal = seleccionar_por_id(animales)
    if animal is None:
        return

    animal["estado"] = ESTADOS_ANIMAL[1]

    guardar_registro(ARCHIVO_ANIMALES_RUTA, animales)
    print(f"\n✅ El estado del animal #{animal['id']} se cambió con éxito.")
    mostrar_animal(animal)

def submenu_animales():
    while True:
        formatear_titulo("ANIMALES DEL REFUGIO")
        print("  1. Cargar un animal nuevo")
        print("  2. Ver listado de animales")
        print("  3. Buscar un animal")
        print("  4. Cambiar estado de un animal a 'En adopción'")
        print("  5. Dar de baja un animal")
        print("  9. Volver al menú principal")
        opcion = elegir_opcion("¿Qué querés hacer?", {"1", "2", "3", "4", "5", "9"})
        match opcion:
            case "1":
                cargar_animal()
            case "2":
                listar_animales()
            case "3":
                buscar_animal()
            case "4":
                pasar_animal_a_en_adopcion()
            case "5":
                dar_baja_animal()
            case "9":
                break