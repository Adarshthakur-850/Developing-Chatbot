from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine.response_engine import ChatBotEngine
from memory import chat_memory

app = FastAPI(title="Context-Aware Chatbot API")
engine = ChatBotEngine()

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response_data = engine.generate_response(request.session_id, request.message)
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{session_id}")
def get_history(session_id: str):
    return chat_memory.get_history(session_id)
