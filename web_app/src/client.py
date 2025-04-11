import requests

MODEL_SERVICE_URL = "http://localhost:8000/predict"  # Adjust URL based on model service location

def send_prediction_request(image_data: str) -> dict:
    """
    Sends a POST request with the base64-encoded image data to the model service's prediction endpoint.
    Returns the prediction result as a dictionary if the request is successful.
    In case of error, returns a dictionary with an 'error' key.
    """
    payload = {"image_data": image_data}
    try:
        response = requests.post(MODEL_SERVICE_URL, json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Return an error dictionary; you might also want to log this error.
        return {"error": f"Failed to get prediction: {e}"}
