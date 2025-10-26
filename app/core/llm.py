import logging
from langchain_community.chat_models import ChatOllama
from langchain_groq import ChatGroq
from app.config import settings

logger = logging.getLogger(__name__)

def create_llm(provider=None):
    """ Create LLM based on configured provider.
    Parameter:
        provider (str, optional): Override default provider ("groq" or "ollama")
    Return:
        ChatOllama or ChatGroq instance
    """
    provider = provider or settings.LLM_PROVIDER

    # local
    if provider == "ollama":
        logger.info(f"Initializing ChatOllama - Model: {settings.OLLAMA_MODEL}")
        return ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.1,
            timeout=60
        )

    elif provider == "groq":
        logger.info(f"Initializing ChatGroq - Model: {settings.GROQ_MODEL}")
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        return ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=0.1,
            timeout=90,
            max_retries=2
        )
    else:
        raise ValueError(f"Unknown LLM provider: {provider}. Use 'groq' or 'ollama'")
