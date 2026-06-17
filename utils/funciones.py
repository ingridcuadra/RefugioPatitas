import json, os
from datetime import date
from utils.validaciones import validar_numero_seleccionado

def incrementar_id(lista):
    if not lista:
        return 1
    return max(r["id"] for r in lista) + 1

def pedir_fecha(mensaje="Fecha"):
    print(f"\n{mensaje}")

    dia = validar_numero_seleccionado("Día: ", 1, 31)
    mes = validar_numero_seleccionado("Mes: ", 1, 12)
    anio = validar_numero_seleccionado("Año: ", 1990, 2100)
    
    fecha = date(anio, mes, dia)
    fecha_completa = fecha.strftime("%d/%m/%Y")
    return fecha_completa

def obtener_fecha_hoy():
    return date.today().strftime("%d/%m/%Y")

def leer_registros(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        return []
    with open(ruta_archivo, encoding="utf-8") as archivo:
        return json.load(archivo)

def guardar_registro(ruta_archivo, datos):
    directorio = os.path.dirname(ruta_archivo)
    if directorio:
        os.makedirs(directorio, exist_ok=True)
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

def buscar_por_id(registros):
    id_ingresado = input("Ingrese el id deseado: ").strip()
    
    if not id_ingresado.isdigit():
        print("El id ingresado no es válido")
        return []
    
    id_buscado = int(id_ingresado)
    
    return [
        registro
        for registro in registros
        if registro["id"] == id_buscado
    ]

def seleccionar_por_id(registros):
    resultados = buscar_por_id(registros)

    if not resultados:
        print("No se encontró ningún registro con ese ID.")
        return None
    return resultados[0]

def encontrar_registro_por_id(id_registros, registros):
    for registro in registros:
        match registro:
            case { "id": reg_id } if reg_id == id_registros:
                return registro
    return None 