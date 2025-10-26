"""
Main message processing handler
"""
import asyncio
import logging
import chainlit as cl
from typing import Optional, Dict, Any
from app.handlers.assessment_handler import send_message
from concurrent.futures import ThreadPoolExecutor
from app.constants import MAIN_MESSAGES
from app.actions import update_sidebar_actions
from rapidfuzz import fuzz

executor = ThreadPoolExecutor(max_workers=4)
logger = logging.getLogger(__name__)

def validate_user_session() -> tuple[Optional[str], Optional[int]]:
    """ Validates user session has required information.
    Returns:
        tuple: (name, age) or (None, None) if invalid
    """
    name = cl.user_session.get("name")
    age = cl.user_session.get("age")
    return (name, age) if name and age else (None, None)


async def send_message_to_backend(name: str, age: int,
                                  content: str) -> Optional[Dict[str, Any]]:
    """ Sends message to backend API in thread pool.
    Parameters:
        name (str): User's name
        age (int): User's age
        content (str): Message content
    Returns:
        Optional: Backend response data
    """
    loop = asyncio.get_event_loop()
    language = cl.user_session.get("language", "en")
    return await loop.run_in_executor(
        executor,
        send_message,
        name,
        age,
        content,
        language
    )


def is_duplicate(symptom: str, existing: list) -> bool:
    symptom_clean = symptom.strip().lower()
    for s in existing:
        s_clean = s.strip().lower()
        # If it is more than 85% similar, it is the same number.
        if fuzz.token_sort_ratio(symptom_clean, s_clean) > 85:
            return True
    return False


def update_session_symptoms(response_data: Dict[str, Any]) -> None:
    """ Updates session with unique symptoms (case-insensitive + fuzzy match).
    Parameter:
        response_data: Backend response containing symptoms
    """
    new_symptoms = response_data.get("symptoms", [])
    existing_symptoms = cl.user_session.get("symptoms", [])
    unique_symptoms = existing_symptoms.copy()
    for s in new_symptoms:
        if not is_duplicate(s, unique_symptoms):
            unique_symptoms.append(s)

    cl.user_session.set("symptoms", unique_symptoms)


async def process_backend_response(response_data: Optional[Dict[str, Any]]) -> bool:
    """ Processes and displays backend response.
    Parameter:
        response_data: Backend response
    Return:
        bool: True if successful, False otherwise
    """
    if not response_data:
        logger.error(MAIN_MESSAGES["no_reply"])
        await cl.Message(content=MAIN_MESSAGES["no_response"]).send()
        return False

    # Get response text
    response_text = response_data.get("response", "No response available")

    # Update symptoms in session
    update_session_symptoms(response_data)

    # Send response
    await cl.Message(content=response_text, author="Doctor Assistant").send()

    # Update sidebar
    await update_sidebar_actions()

    return True
