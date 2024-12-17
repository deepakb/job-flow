from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Job Flow API"
    
    # Firebase Settings
    FIREBASE_CREDENTIALS: Optional[str] = None
    FIREBASE_WEB_API_KEY: Optional[str] = None
    
    # OpenAI Settings
    OPENAI_API_KEY: Optional[str] = None
    
    # Security Settings
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]  # Update with actual origins in production
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
