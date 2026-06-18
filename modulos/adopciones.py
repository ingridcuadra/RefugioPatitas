from utils.formatear_texto import formatear_titulo, agregar_separador
from utils.navegar_menu import elegir_opcion
from utils.validaciones import validar_numero_seleccionado
from utils.funciones import incrementar_id, obtener_fecha_hoy, leer_registros, guardar_registro, seleccionar_por_id
from modulos.animales import animales, cambiar_estado_animal
from modulos.adoptantes import adoptantes

ARCHIVO_ADOPCIONES_RUTA = "archivos/adopciones.json"
ESTADOS_ADOPCION = ("Activa", "Revertida")
adopciones = leer_registros(ARCHIVO_ADOPCIONES_RUTA)

def nombre_desde_registro(registro):
    if registro is None:
        return "Sin nombre"
    return registro.get("nombre") or registro.get("nombre_completo") or "Sin nombre"

def nombre_por_id(id_registro, registros):
    registro = next((r for r in registros if r["id"] == id_registro), None)
    return nombre_desde_registro(registro)

def mostrar_adopcion(adopcion):
    nombre_animal = nombre_por_id(adopcion["id_animal"], animales)
    nombre_adoptante = nombre_por_id(adopcion["id_adoptante"], adoptantes)
    cantidad_seguimientos = len(adopcion.get("seguimientos", []))
    elementos_lista = 'nota' if cantidad_seguimientos == 1 else 'notas'
    
    print(
        f"Adopción #{adopcion['id']} — {nombre_animal} → {nombre_adoptante} "
        f"| {adopcion['estado']} | {adopcion['fecha_adopcion']} "
        f"| {cantidad_seguimientos} {elementos_lista} de seguimiento."
    )

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
    
    agregar_separador()
    return registro_encontrado

def registrar_adopcion():
    formatear_titulo("Registrar adopción")

    adoptante = seleccionar_registro_por_id(adoptantes, "adoptantes")
    if adoptante is None:
        return
    
    animales_en_adopcion = [
        a for a in animales
        if a["estado"] == "en_adopcion"
    ]

    if not animales_en_adopcion:
        print("\nNo hay animales en adopción. Cambiá el estado en el módulo 'Animales del refugio'.")
        return

    animal = seleccionar_registro_por_id(animales_en_adopcion, "animales")
    if animal is None:
        return
    
    id_animal = animal["id"]

    datos_adopcion = {
        "id": incrementar_id(adopciones),
        "id_animal": id_animal,
        "id_adoptante": adoptante["id"],
        "fecha_adopcion": obtener_fecha_hoy(),
        "seguimientos": [],
        "estado": ESTADOS_ADOPCION[0],
    }

    adopciones.append(datos_adopcion)
    guardar_registro(ARCHIVO_ADOPCIONES_RUTA, adopciones)
    cambiar_estado_animal(id_animal, 2)

    print(
        f"\n✅ ¡La adopción se registró con éxito!"
        f"\n{nombre_desde_registro(animal)} → {nombre_desde_registro(adoptante)}."
    )

def listar_adopciones():
    formatear_titulo("Lista de adopciones")

    if not adopciones:
        print("No hay adopciones cargadas.")
        return
    
    for adopcion in adopciones:
        mostrar_adopcion(adopcion)

    elementos_lista = 'adopción' if len(adopciones) == 1 else 'adopciones'
    print(f"\nTotal: {len(adopciones)} {elementos_lista}.")

def buscar_adopcion():
    formatear_titulo("Buscar una adopción")

    if not adopciones:
        print("No hay adopciones cargadas.")
        return

    adopcion = seleccionar_por_id(adopciones)
    if adopcion is None:
        return

    print("\nAdopción encontrada:")
    mostrar_adopcion(adopcion)

def agregar_nota_seguimiento():
    formatear_titulo("Agregá una nota de seguimiento")

    if not adopciones:
        print("Aún no hay adopciones registradas. Registrá una antes de agregar una nota de seguimiento.")
        return

    adopcion = seleccionar_por_id(adopciones)
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
    formatear_titulo("Revertir adopción")

    if not adopciones:
        print("No hay adopciones cargadas. Registrá una antes de intentar revertirla.")
        return

    adopcion = seleccionar_por_id(adopciones)
    if adopcion is None:
        return

    if adopcion["estado"] != ESTADOS_ADOPCION[0]:
        print("Esa adopción no está activa. No se puede revertir.")
        return

    adopcion["estado"] = ESTADOS_ADOPCION[1]
    id_animal = adopcion["id_animal"]

    guardar_registro(ARCHIVO_ADOPCIONES_RUTA, adopciones)
    cambiar_estado_animal(id_animal, 1)
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
        opcion = elegir_opcion("¿Qué querés hacer?", {"1", "2", "3", "4", "5", "9"})
        match opcion:
            case "1":
                registrar_adopcion()
            case "2":
                listar_adopciones()
            case "3":
                buscar_adopcion()
            case "4":
                agregar_nota_seguimiento()
            case "5":
                revertir_adopcion()
            case "9":
                break