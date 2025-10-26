"""
-- EN --
Main chat processing function that manages the state-driven medical conversation.

Workflow:
    1. Receive the user's message.
    2. Retrieve or initialize the user's memory and current state.
    3. Based on the state:
        SYMPTOM_GATHERING → Extract and collect symptoms
        If enough symptoms are collected → Transition to ASSESSMENT
        ASSESSMENT → Evaluate urgency and determine severity.
        ADVICE → Provide medical recommendations or next steps
    4. Update the state and memory with new information.
    5. Return the generated response along with current symptoms.

---------------------
** TR **
Kullanıcının mesajını işleyip, duruma (state) göre tıbbi sohbet akışını yöneten ana fonksiyon.

İş Akışı:
    1. Kullanıcı mesajını alır.
    2. Kullanıcının belleğini ve mevcut durumunu getirir veya oluşturur.
    3. State'e göre işlem yapar:
       - SYMPTOM_GATHERING → Semptomları çıkarır ve toplar.
       - Yeterli semptom varsa → ASSESSMENT aşamasına geçer.
       - ASSESSMENT → Aciliyet ve şiddet düzeyini değerlendirir.
       - ADVICE → Tıbbi öneri veya sonraki adımları sunar.
    4. State'i ve belleği günceller
    5. Üretilen yanıtı semptom bilgileriyle birlikte döndürür.
"""
import logging
from fastapi import HTTPException
from app.pydantic_models import ChatRequest, ChatResponse
from app.core.llm import create_llm
from concurrent.futures import ThreadPoolExecutor
from app.memory.memory_manager import get_or_create_user_memory, log_conversation_memory
from app.handlers.assessment_handler import should_trigger_assessment, handle_assessment, process_assessment, process_normal_conversation
from app.language.language_detector import detect_language, update_language
from app.handlers.clear_handler import handle_clear_request
executor = ThreadPoolExecutor(max_workers=3)
logger = logging.getLogger(__name__)


async def process_chat(request: ChatRequest, user_memories: dict, provider:str = None):
    """ Main chat processing function - handles both normal conversation and assessments.
        Parameters:
            request: Chat request with user data and message
            user_memories: Dictionary of all user memories
        Returns:
            ChatResponse: Response with message, symptoms, and symptom count
        Raises:
            HTTPException: If processing fails
        """
    try:
        llm = create_llm(provider=provider)

        logger.info(f"Request: name={request.name}")
        logger.info(f"Message: {request.message}")
        logger.info(f"User memories: {user_memories}")

        # Get or create user memory
        user_data = get_or_create_user_memory(user_memories, request.name)
        memory = user_data["memory"]
        state = user_data["state"]
        extracted_data = user_data["extracted_data"]

        # Check your request
        clear_response = handle_clear_request(request, user_data)
        if clear_response:
            return clear_response

        # Detect and update the language
        update_language(request, user_data)
        language = user_data["language"]
        logger.info(f"Language for {request.name}: {language}")

        # Check if assessment should be triggered
        if should_trigger_assessment(request.message) and extracted_data["symptoms"]:
            logger.info(f"Assessment triggered for {request.name}")
            return await handle_assessment(llm, request, user_data)
        else:
            # Process normal conversation
            reply = await process_normal_conversation(llm, memory, request.message, request.name, request.age, extracted_data, language)

            # Update state
            state.symptoms_collected = len(extracted_data["symptoms"])

            # Log memory
            log_conversation_memory(memory, request.name, extracted_data["symptoms"])

            return ChatResponse(
                response=reply,
                symptoms=extracted_data["symptoms"],
                symptom_count=len(extracted_data["symptoms"])
            )
    except Exception as e:
        logger.error(f"Error in process_chat: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
