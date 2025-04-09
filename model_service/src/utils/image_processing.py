import base64
import io
from PIL import Image, ImageOps
import torchvision.transforms as transforms


def preprocess_image(
        image_data: str,
        target_size=(28, 28),
        invert_colors=True
):
    """
    Preprocess the image data from a base64 encoded string.

    Steps:
    - Decodes the base64 string to a PIL Image in grayscale.
    - Resizes the image to target_size.
    - Optionally inverts colors (useful if the drawing background is white).
    - Converts the PIL Image to tensor and normalises using MNIST mean + std.

    Returns:
        A torch.Tensor of shape (1, target_size[0], target_size[1]) suitable
        for model input.
    """
    # Decode image data from base64 and open as grayscale
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes)).convert("L")

    # Resize image to target dimensions
    image = image.resize(target_size)

    # Invert colors if necessary (MNIST digits are typically white on black bg)
    if invert_colors:
        image = ImageOps.invert(image)

    # Define transform: convert image to tensor and normalize with MNIST values
    transform_pipeline = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    tensor = transform_pipeline(image)
    return tensor
