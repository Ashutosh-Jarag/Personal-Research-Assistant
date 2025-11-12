"""
Configuration management using Pydantic Settings
This centralizes all our app settings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    Pydantic automatically reads from .env file
    """
    
    # API Keys
    GOOGLE_API_KEY: str
    TAVILY_API_KEY: Optional[str] = None
    LANGSMITH_API_KEY: Optional[str] = None
    
    # LangSmith Configuration
    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_PROJECT: str = "research-assistant"
    
    # Application Settings
    APP_NAME: str = "AI Research Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./database/research.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a global settings instance
settings = Settings()