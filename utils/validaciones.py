from datetime import date
import json, os


def incrementar_id(lista):
    if not lista:
        return 1
    return max(r["id"] for r in lista) + 1



# validad que el input sea un numero entero y que este dentro de un rango de minimo y maximo
def validar_numero_seleccionado(mensaje, minimo=None, maximo=None):
    while True:
        texto = input(mensaje).strip()
        if texto.isdigit():
            valor = int(texto)
            if minimo is not None and valor < minimo:
                print(f"  ⚠  Ingresá un número mayor o igual a {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"  ⚠  Ingresá un número menor o igual a {maximo}.")
                continue
            return valor
        print("  ⚠  Eso no es un número válido. Intentá de nuevo.")


def validar_email():
    while True:
        email = input("Email: ").strip()

        if "@" in email and "." in email:
            return email

        print("⚠ Ingresá un email válido.")


def validar_telefono():
    while True:
        telefono = input("Teléfono: ").strip()

        if telefono.isdigit() and len(telefono) >= 8:
            return telefono

        print("⚠ Ingresá un teléfono válido.")



def confirmar_accion(mensaje):
    while True:
        respuesta = input(f"{mensaje} (Si/No): ").strip().lower()

        if respuesta in ("si", "no"):
            return respuesta == "si"

        print("⚠ Ingresá 'Si' o 'No'.")


def pedir_fecha(mensaje="Fecha"):
    print(f"\n{mensaje}")

    dia = validar_numero_seleccionado("Día: ", 1, 31)
    mes = validar_numero_seleccionado("Mes: ", 1, 12)
    anio = validar_numero_seleccionado("Año: ", 2000)

    return date(anio, mes, dia)

# Retorna el modo correcto según si existe el archivo o no
def validar_archivo_existe(archivo):
    if not os.path.exists(archivo):
        return True
    else: 
        return False


