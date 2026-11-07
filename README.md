# Generador de ASCII Art

Programa de consola que convierte cualquier imagen (JPG, PNG, etc.) en arte ASCII.
Permite elegir el ancho, la paleta de caracteres, mostrar el resultado con los
colores originales de la imagen y guardarlo en un archivo `.txt`.

## Librerías utilizadas

- **[Pillow](https://pypi.org/project/pillow/)**: abre, redimensiona y pasa a escala de grises la imagen.
- **[Rich](https://pypi.org/project/rich/)**: muestra el menú, valida las entradas y pinta el ASCII en color.

## Estructura del proyecto

```
ascii_art/
├── main.py           # Punto de entrada y flujo del programa
├── conversor.py      # Lógica: convierte la imagen en caracteres
├── vista.py          # Interfaz de consola (entradas y salidas)
├── requirements.txt  # Dependencias
├── README.md
└── .gitignore
```

## Instalación

1. Clonar o descargar el proyecto y entrar a la carpeta:
   ```
   cd ascii_art
   ```
2. Crear el entorno virtual:
   ```
   python -m venv .venv
   ```
3. Activarlo:
   - Windows: `.venv\Scripts\activate`
   - Linux / macOS: `source .venv/bin/activate`
4. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Ejecución

Con el entorno virtual activado:

```
python main.py
```

El programa pide:

1. La ruta de la imagen (o `salir` para terminar).
2. El ancho en caracteres.
3. La paleta: `clasica`, `detallada` o `bloques`.
4. Si se muestra en color.
5. Si se invierten claros y oscuros (recomendado con la consola en fondo negro).
6. Si se guarda el resultado en un `.txt`.

## Cómo funciona

Cada píxel de la imagen achicada se reemplaza por un carácter según su brillo
(de 0 a 255): los píxeles oscuros reciben caracteres densos como `@` y los
claros, caracteres livianos como `.` o un espacio. Como los caracteres de la
consola son más altos que anchos, el alto de la imagen se reduce a la mitad
para que no salga estirada.

## Integrantes

- Nombre Apellido
- Nombre Apellido
- Nombre Apellido
