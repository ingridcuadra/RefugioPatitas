def elegir_opcion(opciones_validas):
    while True:
        opcion = input("¿Qué querés hacer? ").strip()
        if opcion in opciones_validas:
            return opcion
        print("  Opción no válida. Probá de nuevo. 🐾")