from pydantic import BaseModel


class PredictRequest(BaseModel):
    image_data: str  # Base64 encoded image string


class PredictResponse(BaseModel):
    prediction: str
    confidence: float
