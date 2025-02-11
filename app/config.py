import os
from dotenv import load_dotenv
from functools import lru_cache
from pydantic_settings import BaseSettings

# Explicitly load .env file
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)


class Settings(BaseSettings):
    AUTH0_DOMAIN: str
    AUTH0_API_AUDIENCE: str
    AUTH0_ISSUER: str
    AUTH0_ALGORITHMS: str
    REDIS_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    # scope: str  # Add if needed
    REDIS_HOST: str  # Add if needed
    REDIS_PORT: int  # Add if needed
    REDIS_PASSWORD: str  # Add if needed
    DATABASE_URL: str
    AFRICASTALKING_API_KEY: str
    AFRICASTALKING_USERNAME: str  # Add if needed

    class Config:
        env_file = ".env"  # Load environment variables from .env file


@lru_cache()
def get_settings():
    return Settings()
