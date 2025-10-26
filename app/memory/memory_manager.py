"""
User memory and state management
"""
import copy
import logging
from typing import Dict, Any
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage
from app.pydantic_models import ConversationState
from app.core.prompt import get_system_prompt
from app.constants import DEFAULT_EXTRACTED_DATA

logger = logging.getLogger(__name__)

# Global memory dictionary
_MEMORY_STORE = {}

def get_memory_store() -> Dict[str, Dict[str, Any]]:
    """Returns the global memory store"""
    logger.info(f"Memory store returned with {len(_MEMORY_STORE)} users")
    return _MEMORY_STORE


def initialize_user_memory() -> Dict[str, Any]:
    """ Initializes user memory structure.
    Returns:
        Dict[str, Any]: User memory with conversation memory, state, and extracted data
    """
    return {
        "memory": InMemoryChatMessageHistory(),
        "state": ConversationState(),
        "extracted_data": copy.deepcopy(DEFAULT_EXTRACTED_DATA),
        "language": "en"
    }


def get_or_create_user_memory(user_memories: Dict, name: str) -> Dict[str, Any]:
    """ Gets existing user memory or creates new one.
    Parameters:
        user_memories: Dictionary of all user memories
        name: User's name
    Returns:
        Dict[str, Any]: User's memory data
    """
    if name not in user_memories:
        user_memories[name] = initialize_user_memory()
        logger.info(f"Created new memory for {name}")
    return user_memories[name]


def add_system_prompt_if_needed(memory, name: str, age: int) -> None:
    """ Adds system prompt to memory if it's the first message.
    Parameters:
        memory: Conversation memory object
        name: User's name
        age: User's age
    """
    if len(memory.messages) == 0:
        system_prompt = get_system_prompt(name, age)
        memory.add_message(HumanMessage(content=system_prompt))
        logger.info(f"System prompt added for {name}")


def log_conversation_memory(memory, name: str, symptoms: list) -> None:
    """ Logs conversation memory for debugging.
    Parameters:
        memory: Conversation memory object
        name: User's name
        symptoms: Collected symptoms
    """
    logger.info(f"\nMemory for {name}")
    for idx, m in enumerate(memory.messages, start=1):
        logger.info(f"{idx:02d}. {m.type.upper()}: {m.content[:100]}")
    logger.info(f"Collected symptoms: {symptoms}")
    print("________________________________________")