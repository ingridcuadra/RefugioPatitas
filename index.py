from modulos.animales import submenu_animales
from modulos.adoptantes import submenu_adoptantes
from modulos.adopciones import submenu_adopciones
from modulos.atencion_veterinaria import submenu_atencion_veterinaria
from modulos.voluntarios_donantes import submenu_voluntarios_donantes

def menu_principal():
    while True:
        print("\n" + "═"*51)
        print("  🐾 REFUGIO PATITAS DEL LITORAL 🐾  ")
        print("═"*51)
        print("  1. Animales del refugio")
        print("  2. Familias adoptantes")
        print("  3. Adopciones")
        print("  4. Atención veterinaria")
        print("  5. Voluntarios y donantes")
        print("  0. Salir")
        print("═"*51)
        
        opcion = input("¿Qué querés hacer? ").strip()
        
        if opcion == "1":
            submenu_animales()
        elif opcion == "2":
            submenu_adoptantes()
        elif opcion == "3":
            submenu_adopciones()
        elif opcion == "4":
            submenu_atencion_veterinaria()
        elif opcion == "5":
            submenu_voluntarios_donantes()
        elif opcion == "0":
            print("Salir")
            break
        else:
            print("  Opción no válida. Probá de nuevo. 🐾")

if __name__ == "__main__":
    menu_principal()