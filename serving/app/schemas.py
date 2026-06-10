from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    anio: int = Field(..., ge=2000, le=2100)
    mes: int = Field(..., ge=1, le=12)
    segmento: str = Field(..., min_length=1)


class PredictionResponse(BaseModel):
    prediction_log: float
    prediction_cop: float


class BatchPredictionRequest(BaseModel):
    records: list[PredictionRequest] = Field(..., min_length=1)


class BatchPredictionResponse(BaseModel):
    predictions: list[PredictionResponse]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_name: str
