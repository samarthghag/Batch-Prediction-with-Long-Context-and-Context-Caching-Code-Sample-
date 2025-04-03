import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # API Configuration
    google_api_key: str = os.getenv("google_api_key", "")
    
    # Model Configuration
    MODEL_NAME: str = "gemini-1.5-pro"
    MAX_TOKENS: int = 2048
    TEMPERATURE: float = 0.7
    
    # Batch Processing Configuration
    BATCH_SIZE: int = 5
    MAX_RETRIES: int = 3
    
    # Context Configuration
    MAX_CONTEXT_LENGTH: int = 30000  # Maximum context length in characters
    CHUNK_OVERLAP: int = 500  # Overlap between chunks in characters
    
    # Cache Configuration
    CACHE_TTL: int = 3600  # Cache time-to-live in seconds
    
    class Config:
        env_file = ".env"

settings = Settings() 