from utils.formatear_texto import formatear_titulo
from utils.navegar_menu import elegir_opcion
from utils.validaciones import validar_numero_seleccionado
from utils.funciones import (incrementar_id, obtener_fecha_hoy, leer_registros, guardar_registro, buscar_por_id)
from modulos.animales import leer_animales
from modulos.adoptantes import leer_adoptantes

ARCHIVO_ADOPCIONES_RUTA = "archivos/adopciones.json"
ESTADOS_ADOPCION = ("Activa", "Revertida")

def leer_adopciones():
    return leer_registros(ARCHIVO_ADOPCIONES_RUTA)

def nombre_desde_registro(registro):
    if registro is None:
        return "Sin nombre"
    return registro.get("nombre") or registro.get("nombre_completo") or "Sin nombre"

def nombre_por_id(id_registro, registros):
    registro = next((r for r in registros if r["id"] == id_registro), None)
    return nombre_desde_registro(registro)

def describir_adopcion(adopcion):
    nombre_animal = nombre_por_id(adopcion["id_animal"], leer_animales())
    nombre_adoptante = nombre_por_id(adopcion["id_adoptante"], leer_adoptantes())
    seguimientos = len(adopcion.get("seguimientos", []))

    return (
        f"Adopción #{adopcion['id']} — {nombre_animal} → {nombre_adoptante} "
        f"| {adopcion['estado']} | {adopcion['fecha_adopcion']} "
        f"| {seguimientos} nota(s) de seguimiento"
    )

def mostrar_adopcion(adopcion):
    print(describir_adopcion(adopcion))
    for nota in adopcion.get("seguimientos", []):
        print(f"  · {nota['fecha_seguimiento']}: {nota['nota_seguimiento']}")

def seleccionar_registro_por_id(registros, tipo):
    if not registros:
        print(f"No hay {tipo} cargados. Registralos antes en su módulo.")
        return None

    print(f"{tipo.capitalize()} disponibles:")
    for registro in registros:
        print(f"ID #{registro['id']} — {nombre_desde_registro(registro)}")

    id_elegido = validar_numero_seleccionado("Ingresá el ID: ", minimo=1)
    registro_encontrado = next(
        (r for r in registros if r["id"] == id_elegido),
        None,
    )

    if registro_encontrado is None:
        print("ID no encontrado.")
    return registro_encontrado

def seleccionar_adopcion_por_id(adopciones):
    resultados = buscar_por_id(adopciones)

    if not resultados:
        print("No se encontró ninguna adopción con ese ID.")
        return None
    return resultados[0]

def validar_adopcion_activa(id_animal):
    adopciones = leer_adopciones()
    return any(
        a["id_animal"] == id_animal and a["estado"] == ESTADOS_ADOPCION[0]
        for a in adopciones
    )

def registrar_adopcion():
    adopciones = leer_adopciones()
    formatear_titulo("Registrar adopción")

    adoptante = seleccionar_registro_por_id(leer_adoptantes(), "adoptantes")
    if adoptante is None:
        return

    animal = seleccionar_registro_por_id(leer_animales(), "animales")
    if animal is None:
        return

    if validar_adopcion_activa(animal["id"]):
        print(f"\nEl animal #{animal['id']} ya tiene una adopción activa.")
        return

    datos_adopcion = {
        "id": incrementar_id(adopciones),
        "id_animal": animal["id"],
        "id_adoptante": adoptante["id"],
        "fecha_adopcion": obtener_fecha_hoy(),
        "seguimientos": [],
        "estado": ESTADOS_ADOPCION[0],
    }

    adopciones.append(datos_adopcion)
    guardar_registro(ARCHIVO_ADOPCIONES_RUTA, adopciones)

    print(
        f"\n¡La adopción se registró con éxito! "
        f"{nombre_desde_registro(animal)} → {nombre_desde_registro(adoptante)}."
    )

def listar_adopciones():
    adopciones = leer_adopciones()
    formatear_titulo("Lista de adopciones")

    if not adopciones:
        print("No hay adopciones cargadas. Registrá una antes de listarlas.")
        return
    
    for adopcion in adopciones:
        mostrar_adopcion(adopcion)

    print(f"\nTotal: {len(adopciones)} adopción/es.")

def buscar_adopcion():
    adopciones = leer_adopciones()
    formatear_titulo("Buscar una adopción")

    if not adopciones:
        print("No hay adopciones cargadas. Registrá una antes de buscarla.")
        return

    adopcion = seleccionar_adopcion_por_id(adopciones)
    if adopcion is None:
        return

    print("\nAdopción encontrada:")
    mostrar_adopcion(adopcion)

def agregar_nota_seguimiento():
    adopciones = leer_adopciones()
    formatear_titulo("Agregá una nota de seguimiento")

    if not adopciones:
        print("No hay adopciones cargadas. Registrá una antes de agregar una nota.")
        return

    adopcion = seleccionar_adopcion_por_id(adopciones)
    if adopcion is None:
        return

    nota = input("Ingresá la nota: ").strip()

    if not nota:
        print("La nota no puede estar vacía.")
        return

    datos_nota = {
        "fecha_seguimiento": obtener_fecha_hoy(),
        "nota_seguimiento": nota,
    }

    adopcion.setdefault("seguimientos", []).append(datos_nota)
    guardar_registro(ARCHIVO_ADOPCIONES_RUTA, adopciones)

    print(f"\n✅ Nota agregada a la adopción #{adopcion['id']}.")

def revertir_adopcion():
    adopciones = leer_adopciones()
    formatear_titulo("Revertir adopción")

    if not adopciones:
        print("No hay adopciones cargadas. Registrá una antes de revertirla.")
        return

    adopcion = seleccionar_adopcion_por_id(adopciones)
    if adopcion is None:
        return

    if adopcion["estado"] != ESTADOS_ADOPCION[0]:
        print("Esa adopción no está activa y no se puede revertir.")
        return

    adopcion["estado"] = ESTADOS_ADOPCION[1]

    guardar_registro(ARCHIVO_ADOPCIONES_RUTA, adopciones)
    print(f"\n✅ Adopción #{adopcion['id']} revertida con éxito.")
    mostrar_adopcion(adopcion)

def submenu_adopciones():

    while True:
        formatear_titulo("ADOPCIONES")
        print("  1. Registrar una nueva adopción")
        print("  2. Ver todas las adopciones concretadas")
        print("  3. Buscar una adopción")
        print("  4. Agregar una nota de seguimiento")
        print("  5. Revertir adopción")
        print("  9. Volver al menú principal")
        opcion = elegir_opcion({"1", "2", "3", "4", "5", "9"})
        if opcion == "1":
            registrar_adopcion()
        elif opcion == "2":
            listar_adopciones()
        elif opcion == "3":
            buscar_adopcion()
        elif opcion == "4":
            agregar_nota_seguimiento()
        elif opcion == "5":
            revertir_adopcion()
        elif opcion == "9":
            break