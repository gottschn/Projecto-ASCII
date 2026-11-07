"""Vista: todo lo que se muestra o se pide en la consola."""
from collections.abc import Iterable

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.text import Text

from conversor import Fila

console = Console()


def mostrar_titulo() -> None:
    """Muestra el título del programa dentro de un recuadro."""
    console.print(Panel.fit(
        "[bold cyan]Generador de ASCII Art[/]\n"
        "Convertí cualquier imagen en texto",
        border_style="cyan",
    ))


def pedir_ruta() -> str:
    """Pide la ruta de la imagen y le quita espacios y comillas."""
    respuesta = Prompt.ask("\n[bold]Ruta de la imagen[/] (o 'salir')")
    return respuesta.strip().strip('"')


def pedir_ancho() -> int:
    """Pide el ancho en caracteres y lo limita al tamaño de la consola.

    IntPrompt vuelve a preguntar solo si se ingresa algo que no es número.
    """
    maximo = console.width
    ancho = IntPrompt.ask(
        f"Ancho en caracteres (entre 10 y {maximo})",
        default=min(100, maximo),
    )
    return max(10, min(ancho, maximo))


def pedir_paleta(opciones: Iterable[str]) -> str:
    """Pide una paleta de la lista; rechaza opciones que no existen."""
    return Prompt.ask("Paleta", choices=list(opciones), default="clasica")


def pedir_si_no(pregunta: str, por_defecto: bool = True) -> bool:
    """Hace una pregunta de sí o no y devuelve la respuesta."""
    return Confirm.ask(pregunta, default=por_defecto)


def mostrar_ascii(filas: list[Fila], con_color: bool) -> None:
    """Imprime el arte ASCII, con o sin los colores originales."""
    console.print()
    for fila in filas:
        linea = Text()
        for car, (r, g, b) in fila:
            if con_color:
                linea.append(car, style=f"rgb({r},{g},{b})")
            else:
                linea.append(car)
        console.print(linea, no_wrap=True, overflow="crop")


def mostrar_exito(mensaje: str) -> None:
    """Muestra un mensaje de éxito en verde."""
    console.print(f"[green]✔ {mensaje}[/]")


def mostrar_error(mensaje: str) -> None:
    """Muestra un mensaje de error en rojo."""
    console.print(f"[bold red]✘ {mensaje}[/]")
