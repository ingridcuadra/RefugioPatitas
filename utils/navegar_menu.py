def elegir_opcion(mensaje, opciones_validas):
    while True:
        opcion = input(f"{mensaje} ").strip()
        if opcion in opciones_validas:
            return opcion
        print("  Opción no válida. Probá de nuevo. 🐾")