"""Lógica del programa: convierte una imagen en arte ASCII."""
from typing import BinaryIO

from PIL import Image

# Tipos usados en el módulo
Color = tuple[int, int, int]
Fila = list[tuple[str, Color]]

# Juegos de caracteres ordenados de OSCURO a CLARO
PALETAS: dict[str, str] = {
    "clasica": "@%#*+=-:. ",
    "detallada": (
        "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    ),
    "bloques": "█▓▒░ ",
}

# Los caracteres de la consola son más altos que anchos (aprox. el doble),
# así que achicamos el alto para que la imagen no salga estirada.
FACTOR_ALTO: float = 0.5


def cargar_imagen(origen: str | BinaryIO) -> Image.Image:
    """Abre la imagen y la convierte a RGB.

    Acepta una ruta (versión de consola) o un archivo ya abierto
    (versión web, la imagen subida por el usuario).
    Lanza FileNotFoundError si el archivo no existe y
    PIL.UnidentifiedImageError si el archivo no es una imagen válida.
    """
    with Image.open(origen) as imagen:
        return imagen.convert("RGB")


def redimensionar(imagen: Image.Image, ancho: int) -> Image.Image:
    """Achica la imagen al ancho pedido, manteniendo la proporción."""
    if ancho <= 0:
        raise ValueError("El ancho debe ser mayor a cero.")
    ancho_orig, alto_orig = imagen.size
    alto = int(alto_orig / ancho_orig * ancho * FACTOR_ALTO)
    return imagen.resize((ancho, max(1, alto)))


def brillo_a_caracter(brillo: int, caracteres: str) -> str:
    """Convierte un brillo (0 a 255) en un carácter de la paleta."""
    indice = brillo * len(caracteres) // 256
    return caracteres[indice]


def convertir(
    imagen: Image.Image,
    ancho: int = 100,
    paleta: str = "clasica",
    invertir: bool = False,
) -> list[Fila]:
    """Convierte la imagen en una lista de filas de (carácter, color).

    Lanza KeyError si la paleta no existe y ValueError si el ancho
    no es válido.
    """
    caracteres = PALETAS[paleta]
    if invertir:
        caracteres = caracteres[::-1]

    img = redimensionar(imagen, ancho)
    gris = img.convert("L")  # "L" = escala de grises, un valor por píxel

    filas: list[Fila] = []
    for y in range(img.height):
        fila: Fila = []
        for x in range(img.width):
            brillo = gris.getpixel((x, y))
            color = img.getpixel((x, y))  # tupla (r, g, b)
            fila.append((brillo_a_caracter(brillo, caracteres), color))
        filas.append(fila)
    return filas


def a_texto(filas: list[Fila]) -> str:
    """Une los caracteres en un solo texto, sin colores."""
    return "\n".join("".join(car for car, _ in fila) for fila in filas)


def guardar_txt(filas: list[Fila], ruta: str) -> None:
    """Guarda el resultado en un archivo de texto.

    Lanza OSError si no se puede escribir el archivo.
    """
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(a_texto(filas))
