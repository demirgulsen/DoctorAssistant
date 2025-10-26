"""
Symptom assessment action handlers
"""
import asyncio
import logging
import requests
from app.config import settings
from typing import Optional, Dict, Any, List
from app.pydantic_models import ChatRequest, ChatResponse
from concurrent.futures import ThreadPoolExecutor
from app.constants import ASSESSMENT_MESSAGES, TRIGGER_WORDS
from app.pydantic_models import MedicalAdvice, TriageAssessment, SymptomExtraction
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from app.handlers.response_formatter import get_response_texts, get_urgency_emoji, format_list_section

logger = logging.getLogger(__name__)
executor = ThreadPoolExecutor(max_workers=4)

def extract_symptoms(llm, user_message: str, name: str, age: int) -> SymptomExtraction:
    """ Extracts symptoms from patient message using LLM.
    Parameters:
        llm: Language model instance
        user_message (str): Patient's message content
        name (str): Patient name
        age (int): Patient age
    Return:
        SymptomExtraction: Structured symptom data
    """
    prompt = f"""Extract symptoms from this patient message.
Patient: {name}, {age} years old
Message: {user_message}

Extract:
- symptoms: list of specific symptoms mentioned
- duration: how long (if mentioned)
- severity: mild, moderate, or severe
- additional_info: any other relevant details

Return as JSON matching SymptomExtraction model.
"""
    structured_llm = llm.with_structured_output(SymptomExtraction)
    result = structured_llm.invoke(prompt)
    return result


def assess_urgency(llm, symptoms_list: list, name: str, age: int, language: str = "en") -> TriageAssessment:
    """ Assesses medical urgency based on collected symptoms.
    Paramters:
        llm: Language model instance
        symptoms_list (List[str]): List of patient symptoms
        name (str): Patient name
        age (int): Patient age
        language: current language (default: "en")
    Return:
        TriageAssessment: Urgency assessment with score and level
    """
    symptoms_text = "\n".join([f"- {s}" for s in symptoms_list])

    prompt = f"""Assess urgency for this patient. Patient: {name}, {age} years old
Symptoms:
{symptoms_text}
IMPORTANT: Respond in {"Turkish" if language == "tr" else "English"}.

Provide:
- urgency_score: 1-10 (10 is most urgent)
- urgency_level: low, medium, high, or emergency
- requires_immediate_care: true/false
- reasoning: explain your assessment

Return as JSON matching TriageAssessment model.
"""
    structured_llm = llm.with_structured_output(TriageAssessment)
    result = structured_llm.invoke(prompt)
    return result


def generate_advice(llm, assessment: TriageAssessment, symptoms_list: list, name: str, age: int, language: str = "en") -> MedicalAdvice:
    """ Generates medical advice based on urgency assessment.
    Parameters:
        llm: Language model instance
        assessment (TriageAssessment): Urgency assessment result
        symptoms_list (List[str]): List of patient symptoms
        name (str): Patient name
        age (int): Patient age
        language: current language
    Returns:
        MedicalAdvice: Structured medical recommendations and care tips
    """
    symptoms_text = "\n".join([f"- {s}" for s in symptoms_list])

    prompt = f"""You are a medical advice assistant. Generate medical advice for this patient.
    Patient: {name}, {age} years old
    Symptoms: {symptoms_text}
    Urgency Level: {assessment.urgency_level}
    Urgency Score: {assessment.urgency_score}
    
    CRITICAL INSTRUCTIONS:
    - The symptoms are in {"Turkish" if language == "tr" else "English"}
    - You MUST write ALL responses in {"Turkish" if language == "tr" else "English"}
    - Do NOT translate or interpret symptoms - use them as-is
    - recommendations, warning_signs, follow_up_timeframe, self_care_tips must ALL be in {"Turkish" if language == "tr" else "English"}

    Return **exactly one JSON object** matching the MedicalAdvice model.
    Do not add any text outside the JSON. Do not repeat items.
    """
    structured_llm = llm.with_structured_output(MedicalAdvice)
    result = structured_llm.invoke(prompt)
    return result


def format_assessment_response(assessment: TriageAssessment, advice: MedicalAdvice, name: str, language: str = "en") -> str:
    """ Formats assessment result into user-friendly response.
    Creates a structured medical assessment report with urgency level,
    recommendations, warning signs, and self-care tips.
    Paramaters:
        assessment (TriageAssessment): Urgency assessment result
        advice (MedicalAdvice): Medical advice and recommendations
        name (str): Patient name
        language: current language
    Return:
        str: Formatted assessment report
    """
    texts = get_response_texts(language)
    emoji = get_urgency_emoji(assessment.urgency_level.value)

    response = f"""**📋 {texts['report_title']} - {name}**
{emoji} **{texts['urgency_level']}:** {assessment.urgency_level.value.upper()} ({texts['score']}: {assessment.urgency_score}/10)

**🤔 {texts['assessment']}:**
{assessment.reasoning}

**💊 {texts['recommendations']}:**
"""
    advice.recommendations = list(dict.fromkeys(advice.recommendations))
    advice.warning_signs = list(dict.fromkeys(advice.warning_signs))
    advice.self_care_tips = list(dict.fromkeys(advice.self_care_tips))

    # write each recommendation
    for rec in advice.recommendations:
        response += f"• {rec}\n"

    # follow-up / doctor consultation
    response += f"**⏰ {texts['doctor_consultation']}:** {advice.follow_up_timeframe}\n"

    # warning signs and self-care
    response += format_list_section(f"⚠️ {texts['warning_signs']}", advice.warning_signs)
    response += format_list_section(f"🏠 {texts['self_care']}", advice.self_care_tips)

    if assessment.requires_immediate_care:
        response += f"\n{texts['emergency']}"

    logger.info(f"Final formatted response preview:\n{response[:300]}")
    return response


def should_trigger_assessment(message: str) -> bool:
    """ Checks if message contains assessment trigger words.
    Parameter:
        message (str): User's message
    Return:
        bool: True if assessment should be triggered
    """
    message_lower = message.lower()
    return any(word in message_lower for word in TRIGGER_WORDS["assessment"])


async def process_assessment(llm, symptoms: List[str], name: str, age: int,
                             language: str = "en") -> tuple:
    """ Processes full assessment workflow: urgency evaluation and advice generation.
    Parameters:
        llm: Language model instance
        symptoms (List[str]): List of symptoms
        name (str): Patient name
        age (int): Patient age
        language (str): Current language code for response formatting
    Returns:
        tuple: (assessment, advice, formatted_response)
    """
    loop = asyncio.get_event_loop()

    # 1. Assess urgency
    try:
        assessment = await loop.run_in_executor(
            executor,
            assess_urgency,
            llm,
            symptoms,
            name,
            age,
            language
        )
    except Exception as e:
        logger.exception("assess_urgency failed")
        raise
    logger.info(f"Assessment: {assessment.urgency_level} (Score: {assessment.urgency_score})")

    # 2. Generate advice
    try:
        advice = await loop.run_in_executor(
            executor,
            generate_advice,
            llm,
            assessment,
            symptoms,
            name,
            age,
            language
        )
    except Exception as e:
        logger.exception("generate_advice failed")
        raise
    logger.info(f"Advice generated")

    # 3. Format response
    formatted_response = format_assessment_response(assessment, advice, name, language)

    return assessment, advice, formatted_response


async def extract_symptoms_async(llm, message: str, name: str, age: int,
                                 extracted_data: Dict) -> None:
    """ Extracts symptoms from message asynchronously and updates extracted data.
    Parameters:
        llm: Language model instance
        message (str): User's message
        name (str): User's name
        age (int): User's age
        extracted_data (Dict): User's extracted data dictionary
    """
    loop = asyncio.get_event_loop()

    try:
        symptoms = await loop.run_in_executor(
            executor,
            extract_symptoms,
            llm,
            message,
            name,
            age
        )
        if symptoms.symptoms:
            current_symptoms = set([s.strip().lower() for s in extracted_data.get("symptoms", [])])
            new_symptoms = [s.strip().lower() for s in symptoms.symptoms]
            unique_new = [s for s in new_symptoms if s not in current_symptoms]
            extracted_data["symptoms"].extend(unique_new)
            logger.info(f"Symptoms extracted: {symptoms.symptoms}")
        else:
            logger.info("No symptoms found in message")
    except Exception as e:
        logger.warning(f"Symptom extraction failed: {e}")


async def process_normal_conversation(llm, memory, message: str, name: str,
                                      age: int, extracted_data: Dict, language) -> str:
    """ Processes normal conversation flow with symptom extraction.
    Parameters:
        llm: Language model instance
        memory: Conversation memory
        message (str): User's message
        name (str): User's name
        age (int): User's age
        extracted_data (Dict): User's extracted data
        language (str): Current language code for response formatting
    Return:
        str: AI response
    """
    memory.add_message(HumanMessage(content=message, additional_kwargs={"language": language}))
    language_instruction = SystemMessage(
        content=f"CRITICAL: You MUST respond in {'Turkish' if language == 'tr' else 'English'}. "
                f"Ignore the language of previous messages. Current language is: {language}"
    )
    messages_with_instruction = [language_instruction] + memory.messages

    for idx, msg in enumerate(memory.messages):
        print(f"{idx}. {msg.type}: {msg.content[:100]}")

    reply = llm.invoke(messages_with_instruction )
    reply_text = reply.content if hasattr(reply, 'content') else str(reply)
    memory.add_message(AIMessage(content=reply_text))

    # Extract symptoms in background
    await extract_symptoms_async(llm, message, name, age, extracted_data)

    return reply_text


def get_assessment_texts(language: str) -> Dict[str, str]:
    """ Retrieves assessment messages for specified language.
    Parameter:
        language (str): Language code ('en' or 'tr')
    Return:
        Dict[str, str]: Dictionary of localized messages
    """
    return ASSESSMENT_MESSAGES.get(language, ASSESSMENT_MESSAGES["en"])


async def send_assessment_request(name: str, age: int, command: str, language: str = "en") -> Optional[Dict[str, Any]]:
    """ Sends assessment request to backend in a thread pool.
    Parameters:
        name (str): User's name
        age (int): User's age
        command (str): Assessment command
        language: current language code
    Return:
        Optional[Dict[str, Any]]: Backend response data
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor,
        send_message,
        name,
        age,
        command,
        language
    )


def send_message(name: str, age: int, user_msg: str, language: str = "en") -> dict:
    """ Sends user message to FastAPI backend and returns the response.
    Handles all HTTP errors, timeouts, and connection issues gracefully.
    Returns a standardized response format in all cases.
    Parameters:
        name: User's name
        age: User's age
        user_msg: User's message text
        language: current language code
    Returns:
        Dictionary containing:
            - response: AI response or error message
            - symptoms: List of extracted symptoms
            - symptom_count: Number of symptoms found
    """
    # Prepare API request payload (JSON format)
    payload = {
        "name": name,
        "age": age,
        "message": user_msg,
        "language": language,
        "provider": "groq"
    }
    try:
        # Send POST request to API endpoint
        res = requests.post(settings.API_URL, json=payload, timeout=100)
        if res.status_code == 200:
            data=res.json()
            return {
                "response": data.get("response", "No response"),
                "symptoms": data.get("symptoms", []),
                "symptom_count": data.get("symptom_count", 0)
            }
        else:
            return {
                "response": f"Error: {res.status_code} - {res.text}",
                "symptoms": [],
                "symptom_count": 0
            }
    except requests.exceptions.Timeout:
        return {"response": "Request timed out. Please try again.", "symptoms": [], "symptom_count": 0}
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error: {e.response.text}")
        return {"response": f"Server error: {e.response.status_code}", "symptoms": [], "symptom_count": 0}
    except requests.exceptions.RequestException as e:
        logger.error(f"Connection error: {e}")
        return {"response": f"Connection error: {str(e)}", "symptoms": [], "symptom_count": 0}



async def handle_assessment(llm, request: ChatRequest, user_data: dict) -> ChatResponse:
    """ Processes the assessment step when enough symptoms are gathered.
    Parameters:
        llm: The active language model instance (e.g., ChatGroq or ChatOllama).
        request: The user's chat request including name, age, and message.
        user_data: The user's memory data containing extracted symptoms and language.
    Returns:
        ChatResponse: The model's assessment response, with cleared symptom list.
    """
    extracted_data = user_data["extracted_data"]
    language = user_data["language"]

    extracted_data["symptoms"] = list(dict.fromkeys(extracted_data["symptoms"]))[-20:]
    assessment, advice, reply = await process_assessment(
        llm,
        extracted_data["symptoms"],
        request.name,
        request.age,
        language
    )
    extracted_data.update({
        "last_assessment": assessment,
        "last_advice": advice,
        "symptoms": []
    })
    return ChatResponse(response=reply, symptoms=[], symptom_count=0)
