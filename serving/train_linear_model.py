import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def build_training_dataframe(input_csv: Path) -> pd.DataFrame:
    df = pd.read_csv(input_csv)
    df.columns = df.columns.str.lower().str.replace(" ", "_", regex=False)

    required_columns = ["anio", "mes", "segmento", "factura_promedio_cop"]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas requeridas en el CSV: {missing}")

    df = df[required_columns].copy()

    df["factura_promedio_cop"] = (
        df["factura_promedio_cop"]
        .where(df["factura_promedio_cop"] >= 0, np.nan)
    )

    segmentos_totales = ["Total Residencial", "Total No Residencial"]
    df = df[~df["segmento"].isin(segmentos_totales)].copy()
    df = df.dropna(subset=["factura_promedio_cop", "segmento", "anio", "mes"]).copy()

    return df


def train_pipeline(df: pd.DataFrame) -> Pipeline:
    x = df[["anio", "mes", "segmento"]].copy()
    y = np.log1p(df["factura_promedio_cop"].values)

    preprocess = ColumnTransformer(
        transformers=[
            ("segmento_ohe", OneHotEncoder(handle_unknown="ignore"), ["segmento"]),
        ],
        remainder="passthrough",
    )

    pipeline = Pipeline(
        steps=[
            ("preprocess", preprocess),
            ("regressor", LinearRegression()),
        ]
    )

    pipeline.fit(x, y)
    return pipeline


def save_artifacts(model: Pipeline, df: pd.DataFrame, output_model: Path, output_meta: Path) -> None:
    output_model.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, output_model)

    metadata = {
        "model": "LinearRegression",
        "target": "factura_promedio_cop",
        "target_transform": "log1p",
        "features": ["anio", "mes", "segmento"],
        "excluded_segments": ["Total Residencial", "Total No Residencial"],
        "training_rows": int(len(df)),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    output_meta.write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Entrena y serializa Linear Regression para serving")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("sui_factura_promedio_consolidado.csv"),
        help="Ruta al CSV consolidado",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("serving/artifacts/linear_regression_pipeline.joblib"),
        help="Ruta de salida del modelo serializado",
    )
    parser.add_argument(
        "--metadata",
        type=Path,
        default=Path("serving/artifacts/model_metadata.json"),
        help="Ruta de salida del metadata JSON",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = build_training_dataframe(args.input)
    model = train_pipeline(df)
    save_artifacts(model, df, args.output, args.metadata)

    print(f"Modelo guardado en: {args.output}")
    print(f"Metadata guardada en: {args.metadata}")
    print(f"Filas de entrenamiento usadas: {len(df)}")


if __name__ == "__main__":
    main()
