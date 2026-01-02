from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # LLM
    LLM_BASE_URL: str = "https://api.openai.com/v1"
    LLM_API_KEY: str = "test_key"
    LLM_MODEL_TEXT: str = "gpt-4-turbo-preview"
    LLM_MODEL_VISION: str = "gpt-4-vision-preview"
    
    # Storage
    STORAGE_PATH: str = "./storage"
    UPLOAD_PATH: str = "./storage/uploads"
    DOCUMENT_PATH: str = "./storage/documents"
    
    # Security
    SECRET_KEY: str = "dev-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # Pricing
    TAX_PERCENT: float = 5.0
    CONTINGENCY_PERCENT: float = 10.0
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

