"""
Sidebar action creation and management
"""
import chainlit as cl
import logging
from app.constants import ACTION_TYPES
from app.utils import get_symptoms, get_user_language, get_localized_text

logger = logging.getLogger(__name__)

def create_action(name: str, value: str, label: str) -> cl.Action:
    """ Creates a single action button.
    Parameter:
        name : Unique identifier for the action
        value : Value of the action
        label : Display label shown to the user
    Returns:
        cl.Action: Created action object
    """
    return cl.Action(
        name=name,
        value=value,
        label=label,
        payload={"action": value}
    )


def create_sidebar_actions(texts: dict) -> list[cl.Action]:
    """ Creates all action buttons for sidebar.
    Parameter:
        texts : Dictionary of localized text strings
    Returns:
        list[cl.Action]: List of action objects
    """
    actions_config = [
        ("assess_symptoms", ACTION_TYPES["ASSESS"], texts["assess"]),
        ("show_summary", ACTION_TYPES["SUMMARY"], texts["summary"]),
        ("clear_symptoms", ACTION_TYPES["CLEAR"], texts["clear"])
    ]
    return [create_action(name, value, label) for name, value, label in actions_config]


async def update_sidebar_actions():
    """ Updates and displays action buttons in the sidebar.
    Creates appropriate action buttons based on the current symptom count and user's language preference.
    Raises:
        KeyError: If the language code is not supported
    """
    try:
        # Retrieve user data
        symptoms = get_symptoms()
        user_lang = get_user_language()

        unique_symptoms = list({s.strip().lower() for s in symptoms})
        symptom_count = len(unique_symptoms)

        # Get localized texts
        texts = get_localized_text(user_lang)

        # Format status message
        status_message = texts["status"].format(count=symptom_count)

        # Create actions
        actions = create_sidebar_actions(texts)

        # Send message
        await cl.Message(
            content=f"**{status_message}**",
            actions=actions,
            author="Actions"
        ).send()

    except KeyError as e:
        logger.error(f"Error: {e}")

        # Fallback to English
        user_lang = "en"
        texts = get_localized_text(user_lang)
        actions = create_sidebar_actions(texts)

        await cl.Message(
            content=f"**{texts['status'].format(count=len(get_symptoms()))}**",
            actions=actions,
            author="Actions"
        ).send()