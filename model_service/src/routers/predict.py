from fastapi import APIRouter, Request, HTTPException
from models.prediction import PredictRequest, PredictResponse
from utils.image_processing import preprocess_image

router = APIRouter()

@router.post("/", response_model=PredictResponse)
async def predict(request_body: PredictRequest, request: Request):
    # Retrieve the loaded model from the app state
    model = request.app.state.model
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    # Preprocess the image data
    processed_image = preprocess_image(request_body.image_data)
    # TODO: Implement actual prediction using the model and processed_image
    dummy_prediction = "7"
    dummy_confidence = 0.95
    return PredictResponse(prediction=dummy_prediction, confidence=dummy_confidence)
