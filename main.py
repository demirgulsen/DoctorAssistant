import logging
import chainlit as cl
from typing import Optional
from app.actions import update_sidebar_actions
from app.authentication.auth import validate_credentials
from app.constants import (USER_ROLES, AUTH_PROVIDERS, MESSAGES, SUMMARY_MESSAGES, MAIN_MESSAGES)
from app.handlers.chat_handlers import request_user_age, initialize_user_session
from app.handlers.summary_handler import create_summary_content
from app.handlers.assessment_handler import get_assessment_texts, send_assessment_request
from app.handlers.clear_handler import clear_symptoms, get_clear_message
from app.handlers.message_handler import (validate_user_session,
                                          send_message_to_backend, process_backend_response)
from app.language.language_detector import get_current_language
from app.utils import merge_similar

logger = logging.getLogger(__name__)


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    """ Password authentication callback for Chainlit.
    Parameter:
        username (str): Provided username
        password (str): Provided password
    Returns:
        Optional[cl.User]: User object if valid, None otherwise
    """
    if validate_credentials(username, password):
        return cl.User(
            identifier=username,
            metadata={
                "role": USER_ROLES["ADMIN"],
                "provider": AUTH_PROVIDERS["CREDENTIALS"]
            }
        )
    else:
        return None


@cl.on_chat_start
async def start():
    """ Handles chat initialization when a user starts a conversation.
    Workflow:
        1. Validates user authentication
        2. Requests user's age
        3. Initializes session with user data
        4. Displays sidebar actions
    """
    # Check authentication
    user = cl.user_session.get("user")
    if not user:
        await cl.Message(content=MESSAGES["login_required"]).send()
        return
    logger.info(f"User informations: {user}")

    # Welcome message
    await cl.Message(content=MESSAGES["greeting"]).send()

    # Get user identifier
    name = getattr(user, "identifier", "User")
    logger.info(f"Chat started for user: {name}")

    # Request and validate age
    age = await request_user_age(name)
    if age is None:
        await cl.Message(content=MESSAGES["invalid_age"]).send()
        return

    logger.info(f"User age validated: {age}")

    # Initialize session
    initialize_user_session(name, age)

    # Success message
    await cl.Message(
        content=MESSAGES["success"].format(name=name)
    ).send()

    # Update sidebar
    await update_sidebar_actions()


@cl.action_callback("assess_symptoms")
async def on_assess(action: cl.Action):
    """ Handles symptom assessment when assess button is clicked.
    Workflow:
        1. Validates symptoms exist
        2. Sends assessment request to backend
        3. Displays assessment result
    Parameter:
        action (cl.Action): Action object from button click
    """
    # Get session datas
    name = cl.user_session.get("name")
    age = cl.user_session.get("age")
    symptoms = cl.user_session.get("symptoms", [])
    user_lang = cl.user_session.get("language", "en")

    texts = get_assessment_texts(user_lang)

    if not symptoms:
        await cl.Message(content=texts["no_symptoms"]).send()
        return

    # Show loading message
    loading = await cl.Message(content=texts["loading"]).send()

    try:
        symptoms_str = ", ".join(symptoms)
        trigger_message = f"değerlendir: {symptoms_str}" if user_lang == "tr" \
            else f"evaluate: {symptoms_str}"

        # Send assessment request
        response_data = await send_assessment_request(
            name,
            age,
            trigger_message,
            user_lang
        )

        # Remove loading message
        await loading.remove()

        # Display result
        if response_data and response_data.get("response"):
            await cl.Message(
                content=response_data["response"],
                author="Assessment"
            ).send()
        else:
            await cl.Message(content=texts["no_response"]).send()

    except Exception as e:
        logger.error(f"Assessment error: {str(e)}")
        await loading.remove()
        await cl.Message(content=f"Error: {str(e)}").send()


@cl.action_callback("show_summary")
async def on_summary(action: cl.Action):
    """ Displays symptom summary when summary button is clicked.
       Shows a formatted list of all recorded symptoms with total count.
    Parameter:
        action (cl.Action): Action object from button click
    """

    symptoms = cl.user_session.get("symptoms", [])
    user_lang = cl.user_session.get("language", "en")

    # Get localized texts
    texts = SUMMARY_MESSAGES.get(user_lang, SUMMARY_MESSAGES["en"])

    # Normalize: lowercase + strip
    normalized = [s.strip().lower() for s in symptoms]

    display_symptoms = merge_similar(normalized)

    # Create and send summary
    content = create_summary_content(display_symptoms, texts)

    await cl.Message(content=content, author="Summary").send()


@cl.action_callback("clear_symptoms")
async def on_clear(action: cl.Action):
    """ Clears all symptoms when clear button is clicked.
    Resets the symptoms list and updates the sidebar actions.
    Parameter:
        action (cl.Action): Action object from button click
    """
    user_lang = cl.user_session.get("language", "en")
    name = cl.user_session.get("name")
    cl.user_session.set("symptoms", [])

    # Clear symptoms
    clear_symptoms()

    if name:
        # Send memory cleanup request to the backend
        await send_message_to_backend(name, cl.user_session.get("age"), "clear" if user_lang == "en" else "temizle")

    # Send confirmation message
    message = get_clear_message(user_lang)
    await cl.Message(content=message).send()

    # Update sidebar
    await update_sidebar_actions()


@cl.on_message
async def main(message: cl.Message):
    """ Main message handler - processes user messages and sends to backend.
    Workflow:
        1. Validates user session
        2. Detects language on first message
        3. Sends message to backend
        4. Updates symptoms and displays response
    Parameter:
        message (cl.Message): User's message object
    """

    # Validate session
    name, age = validate_user_session()
    if not name or not age:
        await cl.Message(content=MAIN_MESSAGES["incomplete_info"]).send()
        return

    # Detect language
    get_current_language(message.content)

    # Show loading
    loading = await cl.Message(content=MAIN_MESSAGES["loading"]).send()
    try:
        # Send to backend
        response_data = await send_message_to_backend(name, age, message.content)

        # Remove loading
        await loading.remove()

        # Process response
        await process_backend_response(response_data)
    except Exception as e:
        logger.error(f"Message processing error: {str(e)}")
        await loading.remove()
        await cl.Message(content=f"Error: {str(e)}").send()


@cl.on_chat_resume
async def resume(thread):
    await cl.Message(content="Welcoma back! Your chat has resumed from where it stopped.").send()
