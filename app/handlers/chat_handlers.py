"""
Chat event handlers
"""
import logging
import chainlit as cl
from typing import Optional
from app.constants import DEFAULT_SESSION_VALUES, MESSAGES

logger = logging.getLogger(__name__)

def extract_age_from_response(age_msg) -> Optional[str]:
    """ Extracts age string from user message response.
    Parameter:
        age_msg: User message response (dict or object)
    Returns:
        Optional[str]: Age string if found, None otherwise
    """
    if isinstance(age_msg, dict):
        return age_msg.get("output")
    elif hasattr(age_msg, "output"):
        return age_msg.output
    return None


def validate_age(age_str: Optional[str]) -> Optional[int]:
    """ Validates and converts age string to integer.
    Parameter:
        age_str (Optional[str]): Age string to validate
    Returns:
        Optional[int]: Valid age as integer, None if invalid
    """
    if not age_str or not age_str.strip().isdigit():
        return None
    return int(age_str.strip())


def initialize_user_session(name: str, age: int) -> None:
    """ Initializes user session with default values.
    Parameters:
        name: User's name
        age: User's age
    """
    cl.user_session.set("name", name)
    cl.user_session.set("age", age)
    cl.user_session.set("symptoms", DEFAULT_SESSION_VALUES["symptoms"])
    cl.user_session.set("language", DEFAULT_SESSION_VALUES["language"])
    cl.user_session.set("language_detected", DEFAULT_SESSION_VALUES["language_detected"])


async def request_user_age(name: str) -> Optional[int]:
    """ Requests and validates user's age.
    Parameter:
        name: User's name
    Returns:
        Optional[int]: Valid age if provided, None otherwise
    """
    age_msg = await cl.AskUserMessage(
        content=MESSAGES["age_prompt"].format(name=name),
        timeout=120
    ).send()

    age_str = extract_age_from_response(age_msg)
    return validate_age(age_str)
