from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.database import init_db
from src.agent import get_chat_response

app = FastAPI(title="Elip Conversational Job Agent")

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        reply = get_chat_response(request.session_id, request.message)
        return {"agent_response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "System Online, DB and Vector Store Active."}