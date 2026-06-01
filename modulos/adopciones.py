import datetime

from utils.formatear_texto import formatear_titulo
from utils.navegar_menu import elegir_opcion
from utils.validaciones import incrementar_id, validar_id_seleccionado
from modulos.animales import animales
from modulos.adoptantes import adoptantes

adopciones = []
estado = ("Activa", "Revertida")

def _nombre_registro(registro):
    return registro.get("nombre") or registro.get("nombre_completo") or "sin nombre"

def _seleccionar_por_id(lista, tipo):
    if not lista:
        print(f"  No hay {tipo} cargados. Registralos antes en su módulo.")
        return None

    print(f"\n  {tipo.capitalize()} disponibles:")
    for registro in lista:
        print(f"    ID #{registro['id']} — {_nombre_registro(registro)}")

    id_elegido = validar_id_seleccionado("  Ingresá el ID: ", minimo=1)
    registro = next((r for r in lista if r["id"] == id_elegido), None)
    if registro is None:
        print("  ID no encontrado.")
    return registro

def _animal_con_adopcion_activa(id_animal):
    return any(
        a["id_animal"] == id_animal and a["estado"] == estado[0]
        for a in adopciones
    )

def registrar_adopcion():
    formatear_titulo("Registrar adopción")

    adoptante = _seleccionar_por_id(adoptantes, "adoptantes")
    if adoptante is None:
        return

    animal = _seleccionar_por_id(animales, "animales")
    if animal is None:
        return

    if _animal_con_adopcion_activa(animal["id"]):
        print(f"  El animal #{animal['id']} ya tiene una adopción activa.")
        return

    datos_adopcion = {
        "id": incrementar_id(adopciones),
        "id_animal": animal["id"],
        "id_adoptante": adoptante["id"],
        "fecha_adopcion": datetime.datetime.now(),
        "seguimientos": [],
        "estado": estado[0],
    }

    adopciones.append(datos_adopcion)
    print(
        f"\n  Adopción #{datos_adopcion['id']} registrada: "
        f"{_nombre_registro(animal)} → {_nombre_registro(adoptante)}."
    )

def listar_adopciones():
    print("listar adopciones")

def buscar_adopcion():
    print("buscar adopción")

def agregar_nota_seguimiento():
    nota = input(f"Ingrese una nota nota")
    fecha_hora = datetime.datetime.now()
    datos_nota = {
        "fecha_seguimiento": fecha_hora,
        "nota_seguimiento": nota
    }
    print("agregar nota de seguimiento")

def revertir_adopcion():
    print("revertir adopción")

def submenu_adopciones():
    while True:
        formatear_titulo("Adopciones")
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