from fastapi import APIRouter, Request, HTTPException, status, Depends
from model_service.src.models.prediction import (
    PredictRequest,
    PredictResponse,
    ErrorResponse
)
from model_service.src.utils.image_processing import preprocess_image
from model_service.src.utils.validation import validate_image_data
from typing import Any, Dict
import torch
from torch import Tensor

router = APIRouter(
    responses={
        status.HTTP_200_OK: {"model": PredictResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {"model": ErrorResponse},
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ErrorResponse},
    }
)


async def get_model(request: Request) -> Any:
    """
    Dependency to retrieve and validate the model from request state
    """
    model = request.app.state.model
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded or unavailable",
            headers={"Retry-After": "300"}
        )
    return model


@router.post(
    "/predict",
    response_model=PredictResponse,
    summary="Predict digit from image",
    description="""
    This endpoint accepts a base64-encoded image of a handwritten digit,
    runs inference using the loaded neural network model, and returns the
    predicted digit along with confidence scores for all possible digits.

    The image should be a clear, centered digit on a contrasting background
    for best results.
    """,
    status_code=status.HTTP_200_OK,
)
async def predict(
    request_body: PredictRequest,
    model: Any = Depends(get_model)
) -> PredictResponse:
    try:
        # Validate image data
        _, base64_data = validate_image_data(request_body.image_data)

        # Preprocess the image data
        processed_image: Tensor = preprocess_image(base64_data)

        # Ensure the processed image has a batch dimension
        if processed_image.dim() == 3:
            processed_image = processed_image.unsqueeze(0)

        # Get the device from the model
        device = next(model.parameters()).device
        processed_image = processed_image.to(device)

        # Run inference
        with torch.no_grad():
            output: Tensor = model(processed_image)
            probabilities: Tensor = torch.softmax(output, dim=1).squeeze(0)
            predicted_digit: int = int(probabilities.argmax().item())
            confidence_scores: Dict[str, float] = {
                str(i): float(probabilities[i].item())
                for i in range(probabilities.size(0))
            }

        return PredictResponse(
            prediction=str(predicted_digit),
            confidence=confidence_scores
        )

    except HTTPException:
        # Re-raise HTTP exceptions to preserve their status codes
        raise

    except ValueError as e:
        # Handle preprocessing errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing image: {str(e)}",
            headers={"X-Error-Type": "processing_error"}
        )

    except torch.cuda.OutOfMemoryError:
        # Handle CUDA OOM errors
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Server resource exhausted. Please try again later.",
            headers={"Retry-After": "60", "X-Error-Type": "server_error"}
        )

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during inference: {str(e)}",
            headers={"X-Error-Type": "model_error"}
        )
