"""
Application configuration settings.

This module manages all configuration settings for the application, including:
- Environment variables
- API keys and credentials
- Database settings
- Service configurations
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional, List
import os
from pathlib import Path

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        PROJECT_NAME: Name of the application
        VERSION: Application version
        DEBUG: Debug mode flag
        
        # API Settings
        API_V1_STR: API version prefix
        SECRET_KEY: Secret key for JWT encoding
        ACCESS_TOKEN_EXPIRE_MINUTES: JWT token expiration time
        
        # Firebase Settings
        FIREBASE_CREDENTIALS: Path to Firebase service account JSON
        FIREBASE_WEB_API_KEY: Firebase Web API key
        
        # OpenAI Settings
        OPENAI_API_KEY: OpenAI API key
        OPENAI_MODEL: GPT model to use
        OPENAI_MAX_TOKENS: Maximum tokens per request
        
        # Database Settings
        DATABASE_URL: Database connection URL
        
        # CORS Settings
        BACKEND_CORS_ORIGINS: List of allowed origins for CORS
        
        # File Storage Settings
        UPLOAD_DIR: Directory for file uploads
        MAX_UPLOAD_SIZE: Maximum file upload size in bytes
    """
    
    # Application Settings
    PROJECT_NAME: str = "Job Flow API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Firebase Settings
    FIREBASE_CREDENTIALS: Path
    FIREBASE_WEB_API_KEY: str
    
    # OpenAI Settings
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_MAX_TOKENS: int = 2000
    
    # Database Settings
    DATABASE_URL: Optional[str] = None
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # File Storage Settings
    UPLOAD_DIR: Path = Path("uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        """Configuration for the settings class."""
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        """Initialize settings with environment variables."""
        super().__init__(**kwargs)
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        self._validate_settings()
    
    def _validate_settings(self):
        """Validate that all required settings are properly configured."""
        required_settings = [
            ('SECRET_KEY', "Secret key is required for JWT encoding"),
            ('FIREBASE_CREDENTIALS', "Firebase credentials file path is required"),
            ('FIREBASE_WEB_API_KEY', "Firebase Web API key is required"),
            ('OPENAI_API_KEY', "OpenAI API key is required")
        ]
        
        for setting, message in required_settings:
            if not getattr(self, setting):
                raise ValueError(f"Missing required setting: {message}")
        
        if not self.FIREBASE_CREDENTIALS.exists():
            raise ValueError(f"Firebase credentials file not found at: {self.FIREBASE_CREDENTIALS}")

@lru_cache()
def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()

# Create a global settings instance
settings = get_settings()
