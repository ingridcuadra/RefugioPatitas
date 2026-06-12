from modulos.animales import submenu_animales
from modulos.adoptantes import submenu_adoptantes
from modulos.adopciones import submenu_adopciones
from modulos.atencion_veterinaria import submenu_atencion_veterinaria
from modulos.voluntarios_donantes import submenu_voluntarios_donantes
from utils.navegar_menu import elegir_opcion

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
        
        opcion = elegir_opcion("¿Qué querés hacer?", {"1", "2", "3", "4", "5", "0"})

        match opcion:
            case "1":
                submenu_animales()
            case "2":
                submenu_adoptantes()
            case "3":
                submenu_adopciones()
            case "4":
                submenu_atencion_veterinaria()
            case "5":
                submenu_voluntarios_donantes()
            case "0":
                print("¡Hasta pronto! 🐾")
                break

if __name__ == "__main__":
    menu_principal()