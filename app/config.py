import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """ Application configuration settings.
    Contains all API, LLM, and server configuration parameters.
    Uses Pydantic BaseSettings for environment variable support.
    """
    load_dotenv()

    # API Configuration
    API_TITLE: str = "Doctor Assistant API"

    # LLM Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")  # "groq" or "ollama"

    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

    # for local development
    # Ollama config
    OLLAMA_MODEL: str = "qwen2.5:3b"
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # Backend API Configuration
    API_URL: str = os.getenv("API_URL", "http://localhost:8002/chat")   # FastAPI server address and endpoint


settings = Settings()


# Alternative models
# ***  groq  ***
# llama-3.1-8b-instant
# llama-3.3-70b-versatile
# qwen/qwen3-32b

# ***  ollama  ***
# qwen2.5:3b
# llama3.1:8b  # 1. good structured output
# mistral:7b   # 2. good medical information
# qwen2.5:7b   # 3. good structured output
# llama3.2:3b
