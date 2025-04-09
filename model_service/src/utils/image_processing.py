import base64
import io
import re
from PIL import Image, ImageOps
import torchvision.transforms as transforms
import torch
from typing import Tuple


def preprocess_image(
        image_data: str,
        target_size: Tuple[int, int] = (28, 28),
        invert_colors: bool = True
) -> torch.Tensor:
    """
    Preprocess the image data from a base64 encoded string.

    Steps:
    - Extracts the base64 content if in data URI format
    - Decodes the base64 string to a PIL Image in grayscale
    - Resizes the image to target_size
    - Optionally inverts colors (useful if the drawing background is white)
    - Converts the PIL Image to tensor and normalises using MNIST mean + std

    Args:
        image_data: Base64 encoded image string, either raw or data URI format
        target_size: Tuple of (width, height) to resize the image
        invert_colors: Whether to invert the image colors

    Returns:
        A torch.Tensor of shape (1, target_size[0], target_size[1]) suitable
        for model input

    Raises:
        ValueError: If image processing fails
    """
    try:
        # Check if the image is in data URI format
        match = re.match(r'^data:image/\w+;base64,(.+)$', image_data)
        if match:
            image_data = match.group(1)

        # Decode image data from base64 and open as grayscale
        try:
            image_bytes = base64.b64decode(image_data)
        except Exception as e:
            raise ValueError(f"Failed to decode base64 image data: {str(e)}")

        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("L")
        except Exception as e:
            raise ValueError(f"Failed to open image data: {str(e)}")

        # Resize image to target dimensions
        image = image.resize(target_size)

        # Invert colors if necessary (MNIST is typically white on black bg)
        if invert_colors:
            image = ImageOps.invert(image)

        # Define transform: convert image to tensor normalise with MNIST values
        transform_pipeline = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])

        tensor = transform_pipeline(image)
        return tensor

    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"Error preprocessing image: {str(e)}")
