# Proyecto final - UdeM

## Informacion general

- Asignatura: `NUEVOS ENFOQUES EN INGENIERIA DE SOFTWARE II`
- Integrantes: `Juan Esteban Galvis`, `Daniela Puerta`
- Tipo de problema: regresion
- Variable objetivo: `Factura_Promedio_COP`

### Contexto del problema

Este proyecto busca construir una base analitica para un modelo predictivo de la facturacion energetica en Colombia. A partir de reportes oficiales del SUI sobre `Factura Promedio`, se realiza un proceso de ETL para consolidar la informacion y un EDA para identificar patrones, relaciones entre variables y consideraciones importantes antes de una etapa de modelado.

### Resumen del dataset

- Nombre del dataset trabajado: `sui_factura_promedio_consolidado.csv`
- Fuente original: Superintendencia de Servicios Publicos Domiciliarios, portal SUI
- Cobertura: empresas del sector electrico reportadas en el indicador `Factura Promedio`
- Periodo cubierto: enero de 2025 a marzo de 2026
- Dimensiones del consolidado: `5809` filas y `6` columnas

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

## Documentacion del dataset

### Origen de los datos

Los archivos de `Dataset_proyecto_aula/` fueron descargados desde el portal del SUI de la Superintendencia de Servicios Publicos, en el reporte comercial de energia electrica para el indicador `Factura Promedio`:

- Fuente: https://sui.superservicios.gov.co/Reportes-del-sector/Energia/Reportes-comerciales/Consolidado-energia
- Empresa: sin escogencia (todas las empresas).
- Periodo: Mensual
- Alcance disponible en este proyecto: desde `2025_01.csv` hasta `2026_03.csv`.
- Total de archivos fuente: `15`.

### Archivos fuente en `Dataset_proyecto_aula/`

La carpeta `Dataset_proyecto_aula/` contiene los reportes mensuales crudos exportados desde el SUI. Cada archivo sigue la convención `YYYY_MM.csv`, por ejemplo:

- `2025_01.csv`: reporte de enero de 2025.
- `2025_12.csv`: reporte de diciembre de 2025.
- `2026_03.csv`: reporte de marzo de 2026.

Estos archivos se leen en la ETL con codificacion `latin-1` y conservan la estructura original del portal.

### Columnas del dataset crudo mensual

Cada CSV mensual tiene `14` columnas:

| Columna                | Descripcion                                                                                                                                            |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Empresa`              | Nombre de la empresa prestadora reportada en el SUI.                                                                                                   |
| `Variable Calculada`   | Tipo de indicador reportado en la fila. En los archivos crudos aparecen filas de contexto y la ETL conserva solo las que contienen `factura promedio`. |
| `Estrato 1`            | Valor de factura promedio para usuarios residenciales de estrato 1.                                                                                    |
| `Estrato 2`            | Valor de factura promedio para usuarios residenciales de estrato 2.                                                                                    |
| `Estrato 3`            | Valor de factura promedio para usuarios residenciales de estrato 3.                                                                                    |
| `Estrato 4`            | Valor de factura promedio para usuarios residenciales de estrato 4.                                                                                    |
| `Estrato 5`            | Valor de factura promedio para usuarios residenciales de estrato 5.                                                                                    |
| `Estrato 6`            | Valor de factura promedio para usuarios residenciales de estrato 6.                                                                                    |
| `Total Residencial`    | Promedio agregado para el segmento residencial.                                                                                                        |
| `Industrial`           | Factura promedio para el segmento industrial.                                                                                                          |
| `Comercial`            | Factura promedio para el segmento comercial.                                                                                                           |
| `Oficial`              | Factura promedio para entidades oficiales.                                                                                                             |
| `Otros`                | Factura promedio para otros tipos de usuario.                                                                                                          |
| `Total No Residencial` | Promedio agregado para los segmentos no residenciales.                                                                                                 |

### Valores y observaciones del dataset crudo

- En `Variable Calculada` aparecen valores como `factura promedio`, pero tambien filas con etiquetas como `2025`, `enero` o `urbano`; esas filas no representan observaciones finales y son descartadas en la ETL.
- Los valores faltantes del reporte original pueden venir como `ND`, `N/D`, `-` o vacios.
- Cada fila util del dataset crudo representa una empresa en un mes, con varias columnas de segmentos en formato ancho.

### Transformacion aplicada en `ETLN.ipynb`

El notebook `ETLN.ipynb` construye `sui_factura_promedio_consolidado.csv` aplicando estos pasos:

1. Lee todos los archivos de `Dataset_proyecto_aula/` en orden cronologico.
2. Extrae `Anio` y `Mes` desde el nombre del archivo, por ejemplo `2025_01.csv`.
3. Filtra solo las filas donde `Variable Calculada` contiene `factura promedio`.
4. Elimina filas sin empresa valida.
5. Normaliza el nombre de `Empresa` pasandolo a mayusculas y quitando espacios sobrantes.
6. Convierte a numerico las columnas de segmentos; los marcadores `ND`, `N/D`, `-` y vacios pasan a nulos.
7. Reestructura el archivo de formato ancho a formato largo usando una fila por empresa, periodo y segmento.
8. Elimina registros con `Factura_Promedio_COP` nula.
9. Concatena todos los meses y exporta el consolidado en `utf-8-sig`.

### Archivo consolidado final

El archivo `sui_factura_promedio_consolidado.csv` es la salida final de la ETL y contiene `5809` registros con `6` columnas:

| Columna                | Descripcion                                                   |
| ---------------------- | ------------------------------------------------------------- |
| `Empresa`              | Nombre de la empresa normalizado en mayusculas.               |
| `Anio`                 | Anio del reporte extraido desde el nombre del archivo fuente. |
| `Mes`                  | Numero de mes del reporte fuente.                             |
| `Periodo`              | Periodo en formato `YYYY-MM`.                                 |
| `Segmento`             | Segmento del mercado al que pertenece la observacion.         |
| `Factura_Promedio_COP` | Valor numerico de la factura promedio en pesos colombianos.   |

### Segmentos presentes en el consolidado

Los valores observados en la columna `Segmento` son:

- `Estrato 1`
- `Estrato 2`
- `Estrato 3`
- `Estrato 4`
- `Estrato 5`
- `Estrato 6`
- `Total Residencial`
- `Industrial`
- `Comercial`
- `Oficial`
- `Otros`
- `Total No Residencial`

### Diferencia entre el crudo y el consolidado

- Los archivos crudos mensuales estan en formato ancho: una empresa por fila y una columna por segmento.
- El consolidado final esta en formato largo: una fila por `Empresa` + `Periodo` + `Segmento`.
- El consolidado ya excluye filas de encabezado o contexto del SUI y conserva solo observaciones utiles para analisis.
- El consolidado deja la variable de interes lista para visualizacion, agregacion y modelado: `Factura_Promedio_COP`.

## Hallazgos del EDA y consideraciones para modelado

### Hallazgos principales

- El dataset consolidado no presenta valores nulos ni registros duplicados despues del ETL, por lo que queda en una condicion adecuada para analisis descriptivo y preparacion de modelado.
- `Factura_Promedio_COP` tiene una distribucion fuertemente asimetrica hacia la derecha, con outliers altos que elevan la media general.
- Los segmentos no residenciales, especialmente `Industrial`, concentran los valores promedio mas altos y la mayor dispersion.
- `Empresa` y `Segmento` son las variables con mayor relacion con la facturacion promedio, mientras que `Mes` y `Anio` tienen una relacion mucho mas debil.
- La correlacion lineal y los scatterplots muestran que no existe una tendencia temporal simple que explique por si sola el comportamiento de la facturacion.
- Existe un caso puntual de valor negativo que debe revisarse antes de cualquier etapa predictiva.

### Consideraciones para modelado

- La variable objetivo del futuro modelo es `Factura_Promedio_COP`, por lo que el problema se aborda como regresion.
- `Periodo` es una variable redundante respecto a `Anio` y `Mes`, por lo que no deberia usarse al mismo tiempo que ambas en un mismo modelo.
- `Segmento` es una variable categorica apta para codificacion posterior, por ejemplo con `one-hot encoding`.
- `Empresa` requiere un tratamiento especial por su alta cardinalidad; aplicar `one-hot encoding` de forma directa no seria la mejor opcion sin evaluacion previa.
- `Total Residencial` y `Total No Residencial` son categorias agregadas del SUI, no segmentos base. Se conservaron en el EDA para respetar la estructura original de la fuente, pero para un modelo enfocado en segmentos especificos convendria excluirlos.
- Dada la asimetria del target, conviene evaluar transformaciones del objetivo o enfoques robustos antes del entrenamiento.

### Cierre metodologico

El EDA permite concluir que el comportamiento de la facturacion promedio depende mas de diferencias entre empresas y segmentos que de una evolucion temporal lineal. Por eso, un primer modelo deberia priorizar variables de negocio como `Segmento` y `Empresa`, tratar con cuidado la alta cardinalidad, revisar el caso atipico negativo y considerar una version del dataset sin categorias agregadas para obtener un problema de modelado mas limpio y coherente.
