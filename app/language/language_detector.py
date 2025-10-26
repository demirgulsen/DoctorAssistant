"""
Language detection utilities
"""
import logging
import chainlit as cl
from app.pydantic_models import ChatRequest
from app.constants import TURKISH_CHARS, TURKISH_KEYWORDS, SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)

def has_turkish_characters(text: str) -> bool:
    """ Checks if the text contains Turkish-specific characters.
    Parameter:
        text: Input text to analyze
    Returns:
        bool: True if Turkish characters are found, False otherwise
    """
    text_lower = text.lower()
    return any(char in text_lower for char in TURKISH_CHARS)


def has_turkish_keywords(text: str) -> bool:
    """ Checks if the text contains common Turkish words.
    Parameter:
        text (str): Input text to analyze
    Returns:
        bool: True if Turkish keywords are found, False otherwise
    """
    words = text.lower().split()
    return any(word in TURKISH_KEYWORDS for word in words)


def detect_language(text: str) -> str:
    """ Detects the language of the input text using character and keyword analysis.
    Currently supports Turkish and English detection. The function first checks
    for Turkish-specific characters, then for common Turkish words. If neither
    is found, defaults to English.
    Parameter:
        text: Input text to analyze
    Returns:
        str: Language code ('tr' for Turkish, 'en' for English)
    Note:
        This is a simple heuristic-based detector and may not be 100% accurate
        for short texts or mixed-language content.
    """
    if not text or not text.strip():
        return SUPPORTED_LANGUAGES["ENGLISH"]

    # Check for Turkish-specific characters
    if has_turkish_characters(text):
        return SUPPORTED_LANGUAGES["TURKISH"]

    # Check for Turkish keywords
    if has_turkish_keywords(text):
        return SUPPORTED_LANGUAGES["TURKISH"]

    # Default to English
    return SUPPORTED_LANGUAGES["ENGLISH"]


def update_language(request: ChatRequest, user_data: dict):
    """ Detects and updates user language if necessary.
    Parameters:
        request: The incoming chat request containing the user's message and optional language.
        user_data: The user's stored memory and language information.
    Return:
        None: This function updates `user_data` in place.
    """
    detected_lang = getattr(request, "language", None) or detect_language(request.message)
    current_lang = user_data.get("language", "en")

    # If there is a new language, update the memory
    if detected_lang != current_lang:
        user_data["language"] = detected_lang
        logger.info(f"Language switched for {request.name}: {current_lang} → {detected_lang}")


def get_current_language(message_content: str) -> str:
    """ Gets current language from session, updates if detected language differs. """
    detected_lang = detect_language(message_content)
    current_lang = cl.user_session.get("language", "en")

    if detected_lang and detected_lang != current_lang:
        logger.info(f"Language switched: {current_lang} → {detected_lang}")
        cl.user_session.set("language", detected_lang)
        return detected_lang

    return current_lang