def incrementar_id(lista):
    if not lista:
        return 1
    return max(r["id"] for r in lista) + 1

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