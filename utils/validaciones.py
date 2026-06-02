from datetime import date


def incrementar_id(lista):
    if not lista:
        return 1
    return max(r["id"] for r in lista) + 1



# validad que el input sea un numero entero y que este dentro de un rango de minimo y maximo
def validar_id_seleccionado(mensaje, minimo=None, maximo=None):
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



def pedir_fecha(mensaje="Fecha"):
    print(f"\n{mensaje}")

    dia = validar_id_seleccionado("Día: ", 1, 31)
    mes = validar_id_seleccionado("Mes: ", 1, 12)
    anio = validar_id_seleccionado("Año: ", 2000)

    return date(anio, mes, dia)


def confirmar(mensaje):
    respuesta = input(f"{mensaje} (s/n): ").strip().lower()
    return respuesta == "s"
