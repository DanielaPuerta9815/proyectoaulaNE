from fastapi import FastAPI, HTTPException

from serving.app.model_service import load_model_bundle, predict
from serving.app.schemas import (
    BatchPredictionRequest,
    BatchPredictionResponse,
    HealthResponse,
    PredictionRequest,
    PredictionResponse,
)


app = FastAPI(
    title="Factura Promedio API",
    description="API REST para predecir Factura_Promedio_COP usando Linear Regression.",
    version="1.0.0",
)


@app.on_event("startup")
def startup_check() -> None:
    load_model_bundle()


@app.get("/", tags=["Info"])
def root() -> dict:
    return {
        "message": "Factura Promedio API activa",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health() -> HealthResponse:
    try:
        _, metadata = load_model_bundle()
        model_name = metadata.get("model", "LinearRegression")
        return HealthResponse(status="ok", model_loaded=True, model_name=model_name)
    except Exception:
        return HealthResponse(status="error", model_loaded=False, model_name="unknown")


@app.post("/predict", response_model=PredictionResponse, tags=["Predicciones"])
def predict_one(payload: PredictionRequest) -> PredictionResponse:
    try:
        records = [payload.model_dump()]
        prediction_log, prediction_cop = predict(records)
        return PredictionResponse(
            prediction_log=float(prediction_log[0]),
            prediction_cop=float(prediction_cop[0]),
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post(
    "/predict-batch",
    response_model=BatchPredictionResponse,
    tags=["Predicciones"],
)
def predict_batch(payload: BatchPredictionRequest) -> BatchPredictionResponse:
    try:
        records = [item.model_dump() for item in payload.records]
        prediction_log, prediction_cop = predict(records)

        predictions = [
            PredictionResponse(
                prediction_log=float(log_val),
                prediction_cop=float(cop_val),
            )
            for log_val, cop_val in zip(prediction_log, prediction_cop)
        ]

        return BatchPredictionResponse(predictions=predictions)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
