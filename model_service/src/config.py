from pydantic import BaseSettings


class Settings(BaseSettings):
    model_path: str = "model_service/model/checkpoint.pth"

    class Config:
        env_file = ".env"


settings = Settings()
