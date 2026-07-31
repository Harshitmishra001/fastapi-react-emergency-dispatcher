from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./disaster_coordinator.db"
    INGESTION_SERVICE_DB_URL: str = "sqlite:///./ingestion.db"
    DISPATCH_SERVICE_DB_URL: str = "sqlite:///./dispatch.db"
    
    # Constraints
    RATE_LIMIT_PER_MINUTE: int = 10
    SOLVER_TIMEOUT_SECONDS: int = 5
    MAX_EVALUATION_RETRIES: int = 2

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
