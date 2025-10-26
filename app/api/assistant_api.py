"""
Doctor Assistant with Fast API
"""
import  logging
from fastapi import FastAPI, HTTPException
from app.pydantic_models import ChatRequest, ChatResponse
from app.services.chat_service import process_chat
from app.memory.memory_manager import get_memory_store
from chainlit.utils import mount_chainlit

logger = logging.getLogger(__name__)

# Start the Fast API application
app = FastAPI(title="Doctor Assistant API")

# Chatbot endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_with_doctor(request: ChatRequest):
    """ Handle chat requests between the user and the doctor assistant.
    Parameter:
        request (ChatRequest) : The incoming chat request containing the user's name, age, language, and message.
    Returns
        dict: A dictionary containing the model's response, extracted symptoms, and symptom count.
    """
    try:
        user_memories = get_memory_store()
        reply = await process_chat(request, user_memories, provider=request.provider)  # provider ekledim
        return reply

    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


mount_chainlit(app=app, target="main.py", path="/")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)