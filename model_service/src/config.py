from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_path: str = "model_service/src/exported_model.pt"

    class Config:
        env_file = ".env"


settings = Settings()
