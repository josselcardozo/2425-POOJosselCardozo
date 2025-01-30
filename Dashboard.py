import os
import subprocess
from datetime import datetime

def mostrar_codigo(ruta_script):
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r') as archivo:
            codigo = archivo.read()
            print(f"\n--- Código de {ruta_script} ---\n")
            print(codigo)
            return codigo
    except FileNotFoundError:
        print("El archivo no se encontró.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return None

def ejecutar_codigo(ruta_script):
    try:
        resultado = subprocess.run(['python', ruta_script], capture_output=True, text=True)
        print(resultado.stdout)

        with open("registro.txt", "a") as log:
            log.write(f"[{datetime.now()}] Ejecutado: {ruta_script}\n")
    except Exception as e:
        print(f"Ocurrió un error al ejecutar el código: {e}")

def mostrar_historial():
    try:
        with open("registro.txt", "r") as log:
            print("\n--- Historial de Scripts Ejecutados ---")
            print(log.read())
    except FileNotFoundError:
        print("Aún no hay registros de ejecución.")

def crear_script(ruta_sub_carpeta):
    nombre = input("Ingresa el nombre del nuevo script (sin .py): ") + ".py"
    ruta_completa = os.path.join(ruta_sub_carpeta, nombre)

    with open(ruta_completa, "w") as nuevo_script:
        nuevo_script.write("# Nuevo script creado desde el dashboard\n")
    
    print(f"Script {nombre} creado con éxito.")

def mostrar_menu():
    ruta_base = os.path.dirname(__file__)
    unidades = {'1': 'Unidad 1', '2': 'Unidad 2'}

    while True:
        print("\nMenu Principal - Dashboard")
        for key in unidades:
            print(f"{key} - {unidades[key]}")
        print("8 - Ver historial de ejecución")
        print("0 - Salir")

        eleccion = input("Elige una opción: ")
        if eleccion == '0':
            print("Saliendo del programa.")
            break
        elif eleccion == '8':
            mostrar_historial()
        elif eleccion in unidades:
            mostrar_sub_menu(os.path.join(ruta_base, unidades[eleccion]))
        else:
            print("Opción no válida.")

def mostrar_sub_menu(ruta_unidad):
    if not os.path.exists(ruta_unidad):
        print(f"La unidad {ruta_unidad} no existe.")
        return

    sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]

    while True:
        print("\nSubmenú - Selecciona una subcarpeta")
        for i, carpeta in enumerate(sub_carpetas, start=1):
            print(f"{i} - {carpeta}")
        print("0 - Regresar al menú principal")

        eleccion_carpeta = input("Elige una subcarpeta o '0' para regresar: ")
        if eleccion_carpeta == '0':
            break
        else:
            try:
                eleccion_carpeta = int(eleccion_carpeta) - 1
                if 0 <= eleccion_carpeta < len(sub_carpetas):
                    mostrar_scripts(os.path.join(ruta_unidad, sub_carpetas[eleccion_carpeta]))
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("Opción no válida. Por favor, intenta de nuevo.")

def mostrar_scripts(ruta_sub_carpeta):
    scripts = [f.name for f in os.scandir(ruta_sub_carpeta) if f.is_file() and f.name.endswith('.py')]

    if not scripts:
        print("\nNo hay scripts disponibles en esta carpeta.")
        input("Presiona Enter para regresar.")
        return

    while True:
        print("\nScripts - Selecciona un script para ver y ejecutar")
        for i, script in enumerate(scripts, start=1):
            print(f"{i} - {script}")
        print("0 - Regresar al submenú anterior")
        print("8 - Crear nuevo script")
        print("9 - Regresar al menú principal")

        eleccion_script = input("Elige un script, '0' para regresar o '9' para ir al menú principal: ")
        if eleccion_script == '0':
            break
        elif eleccion_script == '9':
            return
        elif eleccion_script == '8':
            crear_script(ruta_sub_carpeta)
        else:
            try:
                eleccion_script = int(eleccion_script) - 1
                if 0 <= eleccion_script < len(scripts):
                    ruta_script = os.path.join(ruta_sub_carpeta, scripts[eleccion_script])
                    codigo = mostrar_codigo(ruta_script)
                    if codigo:
                        ejecutar = input("¿Desea ejecutar el script? (1: Sí, 0: No): ")
                        if ejecutar == '1':
                            ejecutar_codigo(ruta_script)
                        elif ejecutar == '0':
                            print("No se ejecutó el script.")
                        else:
                            print("Opción no válida. Regresando al menú de scripts.")
                        input("\nPresiona Enter para volver al menú de scripts.")
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    mostrar_menu()
