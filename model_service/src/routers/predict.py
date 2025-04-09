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
    import torch
    # Ensure the processed image has a batch dimension
    if processed_image.dim() == 3:
        processed_image = processed_image.unsqueeze(0)
    try:
        with torch.no_grad():
            output = model(processed_image)
            probabilities = torch.softmax(output, dim=1).squeeze(0)
            predicted_digit = int(probabilities.argmax().item())
            confidence_scores = {str(i): float(probabilities[i].item()) for i in range(probabilities.size(0))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during inference: {e}")
    return PredictResponse(prediction=str(predicted_digit), confidence=confidence_scores)
