import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    checkpoints_dir: str = os.environ.get(
        "CHECKPOINTS_DIR", "src/checkpoints/")
    model_path: str = os.environ.get(
        "MODEL_PATH", "model_service/src/best_model.pth")
    model_path: str = os.environ.get(
        "EXPORT_MODEL_PATH", "src/exported_model.pt")

    class Config:
        env_file = ".env"


settings = Settings()
