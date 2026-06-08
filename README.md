# proyectoaulaNE

## Inicio rapido

Este proyecto usa `uv` para gestionar el entorno de Python y las dependencias de analisis de datos.

### Version de Python

- Requerida: `Python 3.11` o superior.
- Validada en este proyecto: `Python 3.13.13`.

### Paso a paso con uv

1. Instala `uv` si aun no lo tienes: `pip install uv`
2. Desde la carpeta del proyecto, crea y sincroniza el entorno: `uv sync`
3. Ejecuta comandos dentro del entorno con: `uv run <comando>`

### Activar el entorno

Si quieres activar el entorno manualmente despues de `uv sync`, usa una de estas opciones:

- PowerShell: `.venv\Scripts\Activate.ps1`
- CMD: `.venv\Scripts\activate.bat`
- Git Bash: `source .venv/Scripts/activate`

### Estructura del proyecto

- `EDA.ipynb`: notebook de analisis exploratorio de datos.
- `ETLN.ipynb`: notebook de extraccion, transformacion y preparacion de datos.
- `sui_factura_promedio_consolidado.csv`: archivo consolidado listo para analisis o consumo posterior.
- `Dataset_proyecto_aula/`: carpeta con los archivos fuente mensuales en formato CSV.
- `README.md`: documentacion general del proyecto.
- `pyproject.toml`: configuracion del proyecto y dependencias administradas con `uv`.
- `uv.lock`: version congelada de las dependencias resueltas por `uv`.
- `.venv/`: entorno virtual local creado automaticamente por `uv sync`.
