"""
Medical assessment response formatting utilities
"""
from typing import List, Dict
from app.constants import URGENCY_EMOJI, ASSESSMENT_RESPONSE_TEXTS

def get_response_texts(language: str) -> Dict[str, str]:
    """ Gets localized texts for response formatting.
    Parameter:
        language: Language code ('en' or 'tr')
    Return:
        Dict[str, str]: Localized text dictionary
    """
    return ASSESSMENT_RESPONSE_TEXTS.get(language, ASSESSMENT_RESPONSE_TEXTS["en"])


def get_urgency_emoji(urgency_level: str) -> str:
    """ Gets emoji for urgency level.
    Parameter:
        urgency_level: Urgency level value
    Returns:
        str: Corresponding emoji
    """
    return URGENCY_EMOJI.get(urgency_level, "⚪")


def format_list_section(title: str, items: List[str], prefix: str = "•") -> str:
    """ Formats a list section with title and items.
    Parameters:
        title: Section title
        items: List of items
        prefix: Prefix for each item (default: "•")
    Returns:
        str: Formatted section string
    """
    if not items:
        return ""

    section = f"\n**{title}:**\n"
    for item in items:
        section += f"{prefix} {item}\n"
    return section
