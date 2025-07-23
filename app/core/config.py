from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HF_API_TOKEN: str
    DATABASE_URL: str
    class Config:
        env_file = ".env"

settings = Settings()