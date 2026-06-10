# Proyecto final - UdeM

## Informacion general

- Asignatura: `NUEVOS ENFOQUES EN INGENIERIA DE SOFTWARE II`
- Integrantes: `Juan Esteban Galvis Bedoya`, `Daniela Puerta Mesa`
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

## API de prediccion (FastAPI + Docker)

Se agrego una implementacion de serving basada en el mejor modelo de `MODELS.ipynb` (`Linear Regression`).

Guia completa de instalacion, entrenamiento, despliegue y uso:

- `serving/DEPLOY_API.md`

### Que hace la API

La API expone un modelo de regresion lineal para estimar `Factura_Promedio_COP` a partir de:

- `anio`
- `mes`
- `segmento`

Incluye endpoints de salud (`/health`), prediccion unitaria (`/predict`) y prediccion por lotes (`/predict-batch`).

### Input y output de la API

Input para `POST /predict`:

```json
{
  "anio": 2026,
  "mes": 3,
  "segmento": "Estrato 3"
}
```

Output de `POST /predict`:

```json
{
  "prediction_log": 11.9348,
  "prediction_cop": 152492.43
}
```

- `prediction_log`: prediccion en escala logaritmica (`log1p`).
- `prediction_cop`: prediccion final en COP (escala original).

### Comandos para crear modelo, ejecutar API y probar

Todos los comandos se ejecutan desde la carpeta raiz del proyecto.

1. Crear entorno virtual (sin uv):

```bash
python -m venv .venv
```

2. Activar entorno:

- PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

- CMD:

```bat
.venv\Scripts\activate.bat
```

- Git Bash:

```bash
source .venv/Scripts/activate
```

3. Instalar dependencias:

```bash
python -m pip install --upgrade pip
pip install fastapi "uvicorn[standard]" pandas numpy scikit-learn joblib mlflow matplotlib seaborn ipykernel
```

4. Entrenar y serializar modelo:

```bash
python serving/train_linear_model.py
```

5. Ejecutar API:

```bash
python -m uvicorn serving.app.main:app --host 0.0.0.0 --port 8000 --reload
```

6. Probar salud con curl:

```bash
curl -X GET "http://127.0.0.1:8000/health"
```

7. Probar prediccion unitaria con curl:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
	-H "Content-Type: application/json" \
	-d '{"anio": 2026, "mes": 3, "segmento": "Estrato 3"}'
```

8. Probar prediccion batch con curl:

```bash
curl -X POST "http://127.0.0.1:8000/predict-batch" \
	-H "Content-Type: application/json" \
	-d '{"records":[{"anio":2026,"mes":3,"segmento":"Estrato 3"},{"anio":2026,"mes":3,"segmento":"Industrial"}]}'
```

9. Probar por interfaz Swagger:

- `http://127.0.0.1:8000/docs`

### Archivos dentro de serving

- `serving/train_linear_model.py`: entrena el modelo Linear Regression y genera artefactos para inferencia.
- `serving/DEPLOY_API.md`: guia de instalacion, despliegue y uso de la API.
- `serving/app/main.py`: define la app FastAPI y los endpoints REST.
- `serving/app/model_service.py`: carga el modelo serializado y ejecuta predicciones.
- `serving/app/schemas.py`: define validaciones de entrada y formato de respuesta.
- `serving/artifacts/.gitkeep`: mantiene la carpeta de artefactos en el repositorio.
- `serving/artifacts/*.joblib`: modelo entrenado serializado (generado en runtime).
- `serving/artifacts/*.json`: metadata del modelo (generada en runtime).

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
8. Elimina registros con `Factura_Promedio_COP` nula y reporta cuantos se descartan en cantidad y porcentaje.
9. Concatena todos los meses y exporta el consolidado en `utf-8-sig`.

En el paso 8, la ETL detecta `11436` registros en formato largo antes de la limpieza y elimina `5627` observaciones con `Factura_Promedio_COP` faltante, equivalentes al `49.20%` del total transformado. Esta decision se justifica porque `Factura_Promedio_COP` es la variable objetivo reportada directamente por el SUI: imputar esos faltantes introduciria valores artificiales en el target, distorsionaria comparaciones entre empresas y segmentos y mezclaria observaciones reales con supuestos. Como los marcadores originales (`ND`, `N/D`, `-` y vacios) representan dato no reportado o no disponible, el criterio mas conservador para el EDA y para un modelado posterior es conservar solo registros efectivamente reportados.

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

- El consolidado final contiene `5809` registros, `52` empresas y `12` segmentos reportados entre enero de 2025 y marzo de 2026.
- Despues del ETL, el dataset no presenta valores nulos ni registros duplicados, lo que lo deja en una condicion adecuada para analisis descriptivo y preparacion de modelado.
- La distribucion de `Factura_Promedio_COP` es fuertemente asimetrica hacia la derecha: la media queda muy por encima de la mediana y existen outliers altos que arrastran el promedio general.
- Los segmentos no residenciales, especialmente `Industrial`, concentran los valores promedio mas altos y la mayor dispersion. Ademas, `Total No Residencial` debe interpretarse con cuidado porque corresponde a una categoria agregada del SUI y no a un segmento base.
- `Empresa` y `Segmento` son las variables con mayor relacion con la facturacion promedio, mientras que `Mes` y `Anio` muestran una relacion mucho mas debil.
- El comportamiento temporal presenta fluctuaciones entre periodos, pero la correlacion lineal y los scatterplots muestran que no existe una tendencia uniforme simple que explique por si sola el comportamiento de la facturacion.
- Se detecta un caso puntual con valor negativo en octubre de 2025 para la empresa `ELECTRIFICADORA DE SANTANDER S.A. E.S.P.` en el segmento `Otros`, que conviene revisar antes de cualquier etapa predictiva.

### Interpretacion general

El EDA muestra que el dataset no debe leerse como una sola poblacion homogenea. Las diferencias entre segmentos son amplias y, si se analiza solo el promedio global, se puede perder la lectura real del comportamiento de usuarios residenciales frente a usuarios no residenciales. Por eso, los analisis por segmento y por empresa resultan mas informativos que una unica medida agregada.

Tambien se observa que una parte importante de la asimetria proviene de un conjunto reducido de empresas con facturas promedio muy superiores al resto. Esto hace recomendable complementar la media con mediana, percentiles o visualizaciones segmentadas cuando se quieran comunicar resultados o comparar periodos.

### Consideraciones para modelado

- La variable objetivo del futuro modelo es `Factura_Promedio_COP`, por lo que el problema se aborda como regresion.
- `Periodo` es una variable redundante respecto a `Anio` y `Mes`, por lo que no deberia usarse al mismo tiempo que ambas en un mismo modelo.
- `Segmento` es una variable categorica apta para codificacion posterior, por ejemplo con `one-hot encoding`.
- `Empresa` requiere un tratamiento especial por su alta cardinalidad; aplicar `one-hot encoding` de forma directa no seria la mejor opcion sin evaluacion previa.
- `Total Residencial` y `Total No Residencial` son categorias agregadas del SUI, no segmentos base. Se conservaron en el EDA para respetar la estructura original de la fuente, pero para un modelo enfocado en segmentos especificos convendria excluirlos.
- Dada la asimetria del target, conviene evaluar transformaciones del objetivo o enfoques robustos antes del entrenamiento.

### Consideraciones interesantes del ETL

- El ETL filtra unicamente las filas de `factura promedio`, eliminando filas de contexto incluidas por el reporte original del SUI, como etiquetas de anio, mes o cobertura.
- Los nombres de empresa se normalizan a mayusculas y se limpian espacios, lo que facilita agrupaciones y comparaciones consistentes.
- Los valores faltantes originales (`ND`, `N/D`, `-` o vacios) se convierten a nulos y luego se excluyen en la salida final. En total se descartan `5627` registros, equivalentes al `49.20%` de los `11436` registros generados en formato largo antes de la limpieza.
- La exclusion de esos faltantes se mantiene de forma deliberada: al tratarse de la variable objetivo reportada por la fuente, imputarla introduciria facturas artificiales y sesgaria el analisis descriptivo y cualquier modelo posterior.
- La transformacion de formato ancho a largo permite comparar periodos y segmentos de forma mucho mas simple en pandas y en visualizaciones.
- La diferencia en el numero de registros por segmento no necesariamente implica errores del ETL; en muchos casos refleja que no todas las empresas reportan datos validos para todos los segmentos en todos los meses.
- Cada fila del consolidado representa un promedio reportado por empresa, periodo y segmento, no una factura individual. Esa diferencia es importante para evitar interpretaciones equivocadas sobre el nivel de detalle del dato.

### Cierre metodologico

El EDA permite concluir que el comportamiento de la facturacion promedio depende mas de diferencias entre empresas y segmentos que de una evolucion temporal lineal. Por eso, un primer modelo deberia priorizar variables de negocio como `Segmento` y `Empresa`, tratar con cuidado la alta cardinalidad, revisar el caso atipico negativo y considerar una version del dataset sin categorias agregadas para obtener un problema de modelado mas limpio y coherente.
