import mlflow.sklearn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
model = mlflow.sklearn.load_model("model")


class Features(BaseModel):
    features: list[float]


@app.post("/predict")
def predict(body: Features):
    return {"prediction": int(model.predict([body.features])[0])}
