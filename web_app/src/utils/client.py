import requests
import base64
import io
import os
from PIL import Image

MODEL_SERVICE_URL = os.environ.get(
    "MODEL_SERVICE_URL", "http://localhost:8000/predict")


def send_prediction_request(image_data) -> dict:
    """
    Sends a POST request with the base64-encoded image data to the model
    service's prediction endpoint.
    Returns the prediction result as a dictionary if the request is successful.
    In case of error, returns a dictionary with an 'error' key.
    """
    try:
        # Convert numpy array to PIL Image
        img = Image.fromarray(image_data.astype('uint8'))

        # Convert to grayscale if it's not already
        if img.mode != 'L':
            img = img.convert('L')

        # Resize to 28x28 (MNIST format)
        img = img.resize((28, 28))

        # Convert to base64 for sending over HTTP
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Send the base64 encoded image
        payload = {"image_data": img_str}
        response = requests.post(MODEL_SERVICE_URL, json=payload, timeout=5)
        response.raise_for_status()

        prediction = response.json()

        # Convert confidence values to percentages
        if "confidence" in prediction:
            prediction["confidence"] = {k: v * 100 for k, v in prediction[
                "confidence"
            ].items()}

        return prediction

    except requests.exceptions.RequestException as e:
        # Return an error dictionary
        return {
            "error": f"Failed to get prediction: {e}",
            "confidence": {},
            "prediction": "Error"
        }
    except Exception as e:
        # Handle other exceptions (like image processing errors)
        return {
            "error": f"Error processing image: {e}",
            "confidence": {},
            "prediction": "Error"
        }
