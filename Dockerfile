FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md sui_factura_promedio_consolidado.csv ./
COPY serving ./serving

RUN pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    pandas \
    numpy \
    scikit-learn \
    joblib

RUN python serving/train_linear_model.py \
    --input sui_factura_promedio_consolidado.csv \
    --output serving/artifacts/linear_regression_pipeline.joblib \
    --metadata serving/artifacts/model_metadata.json

EXPOSE 8000

CMD ["uvicorn", "serving.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
