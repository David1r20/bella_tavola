import os

import numpy as np
from fastapi import APIRouter, HTTPException
from ml.model_utils import load_model
from pydantic import BaseModel, Field

router = APIRouter()

# Configure HF_MODEL_REPO_ID no ambiente/Actions para baixar do Hugging Face.
REPO_ID = os.environ.get("HF_MODEL_REPO_ID")
_model = None


def get_model():
    global _model
    if _model is None:
        _model = load_model(REPO_ID)
    return _model


class PredictInput(BaseModel):
    valor_transacao: float = Field(gt=0)
    hora_transacao: int = Field(ge=0, le=23)
    distancia_ultima_compra: float = Field(ge=0)
    tentativas_senha: int = Field(ge=1)
    pais_diferente: int = Field(ge=0, le=1)


class PredictOutput(BaseModel):
    prediction: int
    probability: float
    label: str
    model_version: str


@router.post("/predict", response_model=PredictOutput)
async def predict(input_data: PredictInput):
    try:
        model = get_model()
        features = np.array(
            [
                [
                    input_data.valor_transacao,
                    input_data.hora_transacao,
                    input_data.distancia_ultima_compra,
                    input_data.tentativas_senha,
                    input_data.pais_diferente,
                ]
            ]
        )

        prediction = int(model.predict(features)[0])
        probability = float(model.predict_proba(features)[0][1])
        label = "fraude" if prediction == 1 else "legitimo"

        return PredictOutput(
            prediction=prediction,
            probability=round(probability, 4),
            label=label,
            model_version="local-v1" if REPO_ID is None else REPO_ID,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health():
    try:
        model = get_model()
        model.predict(np.zeros((1, 5)))
        return {"status": "ok", "model": "loaded"}
    except Exception as e:
        return {"status": "degraded", "error": str(e)}
