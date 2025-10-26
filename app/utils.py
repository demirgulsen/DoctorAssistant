"""
Utility helper functions
"""
import chainlit as cl
from difflib import SequenceMatcher
from app.constants import SIDEBAR_TEXTS

def get_user_language() -> str:
    """ Retrieves the user's language preference from session.
    Returns:
        str: Language code (default: 'en')
    """
    return cl.user_session.get("language", "en")


def get_symptoms() -> list:
    """ Retrieves the list of recorded symptoms from session.
    Returns:
        list: List of symptoms
    """
    return cl.user_session.get("symptoms", [])


def get_localized_text(lang: str) -> dict:
    """ Retrieves localized texts for the specified language.
    Parameter:
        lang (str): Language code ('tr' or 'en')
    Returns:
        dict: Dictionary of localized text strings
    Raises:
        KeyError: If the language code is not supported
    """
    if lang not in SIDEBAR_TEXTS:
        raise KeyError(f"Unsupported language: {lang}")
    return SIDEBAR_TEXTS[lang]


def merge_similar(symptoms: list[str], threshold: float = 0.8) -> list[str]:
    """ Merge similar symptom strings based on a similarity threshold.
    Parameters:
        symptoms: The list of extracted symptom strings.
        threshold: The similarity ratio (0–1) above which two symptoms are considered duplicates.
                   Default is 0.8.
    Returns: A list of unique or merged symptom strings with near-duplicates removed.
    """
    merged = []
    for s in symptoms:
        found = False
        for m in merged:
            if SequenceMatcher(None, s, m).ratio() >= threshold:
                found = True
                break
        if not found:
            merged.append(s)
    return merged
