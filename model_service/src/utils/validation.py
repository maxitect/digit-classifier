import base64
import re
from fastapi import HTTPException, status
from typing import Tuple


def validate_image_data(image_data: str) -> Tuple[str, str]:
    """
    Validates the format and content of the image data.

    Args:
        image_data: Base64 encoded image string

    Returns:
        Tuple containing image format and base64 data

    Raises:
        HTTPException: If validation fails
    """
    if not image_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image data is required"
        )

    # Check for data URI format (data:image/format;base64,...)
    pattern = r'^data:image/(\w+);base64,(.+)$'
    match = re.match(pattern, image_data)

    if not match:
        # Try with just raw base64 data
        try:
            base64.b64decode(image_data)
            return "unknown", image_data
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image data format. "
                       "Expected base64 encoded image data"
            )

    image_format, base64_data = match.groups()

    # Validate supported image formats
    if image_format.lower() not in ["jpeg", "jpg", "png"]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(f"Unsupported image format: {image_format}. "
                    "Supported formats: JPEG, PNG")
        )

    # Validate base64 encoding and size
    try:
        decoded_data = base64.b64decode(base64_data)
        if len(decoded_data) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Image size exceeds the 10MB limit"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid base64 encoding"
        )

    return image_format, base64_data
