from pydantic import BaseModel, Field
from typing import Dict, Literal


class PredictRequest(BaseModel):
    image_data: str = Field(
        ...,
        description="Base64 encoded image string",
        min_length=1
    )

    class Config:
        schema_extra = {
            "example": {
                "image_data":
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
            }
        }


class PredictResponse(BaseModel):
    prediction: str = Field(..., description="Predicted digit")
    confidence: Dict[str, float] = Field(
        ...,
        description="Confidence scores for each possible digit"
    )

    class Config:
        schema_extra = {
            "example": {
                "prediction": "5",
                "confidence": {
                    "0": 0.01,
                    "1": 0.02,
                    "2": 0.01,
                    "3": 0.03,
                    "4": 0.01,
                    "5": 0.85,
                    "6": 0.02,
                    "7": 0.02,
                    "8": 0.02,
                    "9": 0.01
                }
            }
        }


class ErrorResponse(BaseModel):
    detail: str
    error_type: Literal["model_error", "validation_error",
                        "processing_error", "server_error"] = "server_error"
