"""
Clear symptoms action handler
"""
import logging
import chainlit as cl
from typing import Optional
from app.constants import CLEAR_MESSAGES
from app.pydantic_models import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

def clear_symptoms() -> None:
    """ Clears all recorded symptoms from session."""
    cl.user_session.set("symptoms", [])


def get_clear_message(language: str) -> str:
    """ Gets localized clear confirmation message.
    Parameter:
        language (str): Language code ('en' or 'tr')
    Return:
        str: Localized message
    """
    return CLEAR_MESSAGES.get(language, CLEAR_MESSAGES["en"])


def handle_clear_request(request: ChatRequest, user_data: dict) -> Optional[ChatResponse]:
    """ Checks if user wants to clear memory and resets if needed.
    Parameters:
        request: The incoming chat request containing user message and metadata.
        user_data: The user's memory record containing extracted data and language settings.
    Returns:
        Optional[ChatResponse]: A response confirming the memory has been cleared, or None if no clear action is triggered.
    """
    clear_keywords = ["clear", "temizle", "sil", "delete"]
    if request.message.lower() in clear_keywords:
        logger.info(f"Memory cleared for {request.name}")
        user_data["extracted_data"].update({
            "symptoms": [],
            "last_assessment": None,
            "last_advice": None
        })
        response_text = "Semptomlar temizlendi." if user_data["language"] == "tr" else "Symptoms cleared."
        return ChatResponse(
            response=response_text,
            symptoms=[],
            symptom_count=0
        )
    return None
