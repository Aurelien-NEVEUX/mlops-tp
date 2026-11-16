# syntax=docker/dockerfile:1
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ARG MLFLOW_TRACKING_URI
COPY fetch_model.py .
RUN --mount=type=secret,id=dagshub_user \
    --mount=type=secret,id=dagshub_token \
    MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI \
    MLFLOW_TRACKING_USERNAME=$(cat /run/secrets/dagshub_user) \
    MLFLOW_TRACKING_PASSWORD=$(cat /run/secrets/dagshub_token) \
    python fetch_model.py

COPY main.py .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
