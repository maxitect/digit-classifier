import base64
import io
from PIL import Image
from fastapi.testclient import TestClient
import pytest
from model_service.src.app import app
from unittest import mock
import torch


# Create a proper mock model that behaves more like a real PyTorch model
class MockModel(mock.MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create a dummy parameter to make next(model.parameters()) work
        self.dummy_param = torch.nn.Parameter(torch.zeros(1))

    def __call__(self, x):
        # Return a tensor with 10 outputs (one for each digit)
        return torch.tensor(
            [[0.1, 0.1, 0.1, 0.1, 0.1, 0.9, 0.1, 0.1, 0.1, 0.1]]
        )

    def to(self, device):
        # Simply return self to simulate device movement
        return self

    def parameters(self):
        # Yield the dummy parameter
        yield self.dummy_param

    def eval(self):
        # Return self for method chaining
        return self


# Create an instance of our mock model
mock_model = MockModel()

# Mock the model loading function before importing the app
with mock.patch(
    'model_service.src.utils.model_loader.load_model',
    return_value=mock_model
):

    # Explicitly set the model in app state
    app.state.model = mock_model

client = TestClient(app)


def create_test_image() -> str:
    """
    Creates a 28x28 grayscale test image, converts it to a base64 string,
    and returns a data URI.

    Usage:
        image_data = create_test_image()
    """
    # Create a white 28x28 grayscale image
    image = Image.new("L", (28, 28), color=255)
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_str}"


def test_predict_valid_image():
    """
    Test the /predict endpoint with a valid base64 image.
    Expect a 200 response with a valid prediction and confidence scores.

    Run with:
    $ pytest --maxfail=1 --disable-warnings -q
    """
    image_data = create_test_image()
    payload = {"image_data": image_data}
    response = client.post("/predict/predict", json=payload)
    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}")
    data = response.json()
    assert "prediction" in data, "Response missing 'prediction' field"
    assert "confidence" in data, "Response missing 'confidence' field"
    assert isinstance(data["confidence"], dict), (
        "'confidence' should be a dict"
    )
    assert len(data["confidence"]
               ) == 10, "Confidence scores should contain 10 entries"


def test_predict_invalid_base64():
    """
    Test the /predict endpoint with an invalid base64 string.
    Expect a 400 response indicating a processing error.
    """
    payload = {"image_data": "not_a_valid_base64_string"}
    response = client.post("/predict/predict", json=payload)
    assert response.status_code == 400, (
        f"Expected 400, got {response.status_code}"
    )
    data = response.json()
    assert "detail" in data, "Error response should contain 'detail'"


def test_predict_missing_field():
    """
    Test the /predict endpoint with a missing 'image_data' field.
    Expect a 422 Unprocessable Entity error.
    """
    payload = {}
    response = client.post("/predict/predict", json=payload)
    assert response.status_code == 422, (
        f"Expected 422, got {response.status_code}"
    )


if __name__ == "__main__":
    # To run tests manually, execute:
    # $ pytest --maxfail=1 --disable-warnings -q
    pytest.main()
