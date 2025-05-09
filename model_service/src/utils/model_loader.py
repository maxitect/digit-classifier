import os
import torch
from src.model import MNISTCNN


def load_model(model_path: str):
    """
    Load the machine learning model from the specified checkpoint.
    Returns the loaded model instance.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    try:
        # For TorchScript models use torch.jit.load instead
        if model_path.endswith('.pt'):
            model = torch.jit.load(model_path)
        else:
            # For regular PyTorch models
            model = MNISTCNN()
            model.load_state_dict(torch.load(model_path, map_location="cpu"))

        model.eval()
        return model
    except Exception as e:
        raise RuntimeError(f"Error loading model: {e}")
