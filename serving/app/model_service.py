import json
from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np
import pandas as pd


ARTIFACT_DIR = Path(__file__).resolve().parent.parent / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "linear_regression_pipeline.joblib"
METADATA_PATH = ARTIFACT_DIR / "model_metadata.json"


@lru_cache(maxsize=1)
def load_model_bundle() -> tuple[object, dict]:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "No se encontro el modelo serializado. Ejecuta serving/train_linear_model.py primero."
        )

    model = joblib.load(MODEL_PATH)
    metadata = {}

    if METADATA_PATH.exists():
        metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))

    return model, metadata


def predict(records: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    model, _ = load_model_bundle()
    features = pd.DataFrame(records, columns=["anio", "mes", "segmento"])

    prediction_log = model.predict(features)
    prediction_cop = np.expm1(prediction_log)
    prediction_cop = np.maximum(prediction_cop, 0.0)

    return prediction_log, prediction_cop
