from pydantic import BaseModel
from typing import Dict


class PredictRequest(BaseModel):
    image_data: str  # Base64 encoded image string


class PredictResponse(BaseModel):
    prediction: str
    confidence: Dict[str, float]
