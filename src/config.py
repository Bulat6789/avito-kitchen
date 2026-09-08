from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    RESTAURANT_API_URL: str = "http://restaurant-example:8001"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()