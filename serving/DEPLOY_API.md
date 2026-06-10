# Despliegue de API REST con FastAPI y Docker

## Objetivo

Servir predicciones de `Factura_Promedio_COP` con una API REST en FastAPI usando el mejor modelo de `MODELS.ipynb`: `Linear Regression`.

## Estructura creada

- `serving/train_linear_model.py`: entrena y serializa el modelo para serving.
- `serving/app/main.py`: API FastAPI.
- `serving/app/model_service.py`: carga del modelo y prediccion.
- `serving/app/schemas.py`: contratos de entrada y salida.
- `serving/artifacts/`: artefactos del modelo (`.joblib` y metadata).
- `Dockerfile`: empaquetado de la API en contenedor.
- `.dockerignore`: reduce contexto de build.

## 1. Preparar dependencias localmente

Si usas `uv`:

```bash
uv sync
```

## 2. Entrenar y exportar el modelo

Ejecuta desde la raiz del proyecto:

```bash
uv run python serving/train_linear_model.py
```

Esto genera:

- `serving/artifacts/linear_regression_pipeline.joblib`
- `serving/artifacts/model_metadata.json`

## 3. Ejecutar la API local (sin Docker)

```bash
uv run uvicorn serving.app.main:app --reload --host 0.0.0.0 --port 8000
```

Prueba rapida:

- Swagger: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

## 4. Probar endpoint de prediccion

### Endpoint unico

`POST /predict`

Ejemplo:

```json
{
  "anio": 2026,
  "mes": 3,
  "segmento": "Estrato 3"
}
```

Respuesta esperada (ejemplo de forma):

```json
{
  "prediction_log": 12.34,
  "prediction_cop": 228000.12
}
```

### Endpoint batch

`POST /predict-batch`

```json
{
  "records": [
    {
      "anio": 2026,
      "mes": 3,
      "segmento": "Estrato 3"
    },
    {
      "anio": 2026,
      "mes": 3,
      "segmento": "Industrial"
    }
  ]
}
```

## 5. Construir y ejecutar con Docker

### Build

```bash
docker build -t factura-promedio-api:1.0.0 .
```

### Run

```bash
docker run --rm -p 8000:8000 factura-promedio-api:1.0.0
```

La API quedara disponible en:

- `http://localhost:8000`
- `http://localhost:8000/docs`

## 6. Flujo recomendado de despliegue

1. Actualizar dataset consolidado.
2. Reentrenar con `serving/train_linear_model.py`.
3. Ejecutar pruebas basicas de API (`/health`, `/predict`).
4. Construir imagen Docker versionada.
5. Publicar imagen en registro (Docker Hub, GHCR, ECR, etc.).
6. Desplegar contenedor en el entorno objetivo.

## Notas tecnicas

- El target se modela con transformacion `log1p` y se revierte con `expm1` al responder.
- Se excluyen `Total Residencial` y `Total No Residencial` para alinear el enfoque del notebook.
- Si llega un segmento no visto en entrenamiento, `OneHotEncoder(handle_unknown="ignore")` evita fallo y permite inferencia.
