from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application-specific settings
    secret_key: str #= "default_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # MongoDB configuration
    mongo_username: str  # Will load from .env
    mongo_password: str  # Will load from .env
    db_name: str = "cognitive_project"
    collection_name: str = "user_data"

    genai_api_key: str # Will load from .env

    @property
    def database_url(self) -> str:
        return (
            f"mongodb+srv://{self.mongo_username}:{self.mongo_password}"
            f"@cluster0.3rx4l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        )

    class Config:
        env_file = ".env"

# Instantiate settings
settings = Settings()
