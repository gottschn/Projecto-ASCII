"""Punto de entrada: maneja el flujo del programa."""
import os

from PIL import UnidentifiedImageError

import conversor
import vista


def generar_nombre_salida(ruta: str) -> str:
    """Arma el nombre del .txt a partir del nombre de la imagen."""
    nombre_base = os.path.splitext(os.path.basename(ruta))[0]
    return f"{nombre_base}_ascii.txt"


def guardar_resultado(filas: list[conversor.Fila], ruta_imagen: str) -> None:
    """Guarda el resultado en un .txt y avisa si hubo un error."""
    nombre = generar_nombre_salida(ruta_imagen)
    try:
        conversor.guardar_txt(filas, nombre)
    except OSError as error:
        vista.mostrar_error(f"No se pudo guardar el archivo: {error}")
    else:
        vista.mostrar_exito(f"Guardado como {nombre}")


def procesar_imagen(ruta: str) -> None:
    """Carga la imagen, pide las opciones, la muestra y ofrece guardarla."""
    try:
        imagen = conversor.cargar_imagen(ruta)
    except FileNotFoundError:
        vista.mostrar_error("Ese archivo no existe.")
        return
    except UnidentifiedImageError:
        vista.mostrar_error("El archivo no es una imagen válida.")
        return
    except OSError as error:
        vista.mostrar_error(f"No se pudo abrir el archivo: {error}")
        return

    ancho = vista.pedir_ancho()
    paleta = vista.pedir_paleta(conversor.PALETAS)
    con_color = vista.pedir_si_no("¿Mostrar en color?")
    invertir = vista.pedir_si_no(
        "¿Invertir claros y oscuros? (recomendado con fondo negro)"
    )

    try:
        filas = conversor.convertir(imagen, ancho, paleta, invertir)
    except (ValueError, KeyError) as error:
        vista.mostrar_error(f"No se pudo convertir la imagen: {error}")
        return

    vista.mostrar_ascii(filas, con_color)

    if vista.pedir_si_no("\n¿Guardar en un .txt?", por_defecto=False):
        guardar_resultado(filas, ruta)


def main() -> None:
    """Muestra el menú y repite hasta que el usuario escriba 'salir'."""
    vista.mostrar_titulo()
    try:
        while True:
            ruta = vista.pedir_ruta()
            if ruta.lower() == "salir":
                break
            if not ruta:
                vista.mostrar_error("No ingresaste ninguna ruta.")
                continue
            procesar_imagen(ruta)
    except (KeyboardInterrupt, EOFError):
        print()  # Ctrl+C o Ctrl+D: salimos sin mostrar el error de Python
    vista.mostrar_exito("¡Hasta luego!")


if __name__ == "__main__":
    main()
