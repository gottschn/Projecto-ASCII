"""Versión web del generador: servidor Flask que reutiliza conversor.py."""
from flask import Flask, render_template, request
from markupsafe import Markup, escape
from PIL import UnidentifiedImageError

import conversor

# Opciones fijas: la web solo pide la imagen
ANCHO = 120
PALETA = "clasica"
INVERTIR = True  # el resultado se muestra sobre fondo negro
TAMANIO_MAX_MB = 5

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = TAMANIO_MAX_MB * 1024 * 1024


def filas_a_html(filas: list[conversor.Fila]) -> Markup:
    """Convierte las filas en HTML, con un <span> de color por carácter."""
    lineas = []
    for fila in filas:
        linea = "".join(
            f'<span style="color: rgb({r},{g},{b})">{escape(car)}</span>'
            for car, (r, g, b) in fila
        )
        lineas.append(linea)
    return Markup("\n".join(lineas))


@app.route("/", methods=["GET", "POST"])
def inicio() -> str:
    """Muestra el formulario y, si se subió una imagen, el resultado."""
    if request.method == "GET":
        return render_template("index.html")

    archivo = request.files.get("imagen")
    if archivo is None or archivo.filename == "":
        return render_template("index.html", error="No elegiste ninguna imagen.")

    try:
        imagen = conversor.cargar_imagen(archivo.stream)
        filas = conversor.convertir(imagen, ANCHO, PALETA, INVERTIR)
    except UnidentifiedImageError:
        return render_template("index.html",
                               error="El archivo no es una imagen válida.")
    except OSError:
        return render_template("index.html",
                               error="No se pudo leer la imagen.")

    return render_template(
        "index.html",
        resultado=filas_a_html(filas),
        texto=conversor.a_texto(filas),
        nombre=archivo.filename.rsplit(".", 1)[0] + "_ascii.txt",
    )


@app.errorhandler(413)
def archivo_muy_grande(error: Exception) -> tuple[str, int]:
    """Avisa cuando la imagen supera el tamaño máximo permitido."""
    mensaje = f"La imagen pesa más de {TAMANIO_MAX_MB} MB."
    return render_template("index.html", error=mensaje), 413


if __name__ == "__main__":
    app.run(debug=True)
