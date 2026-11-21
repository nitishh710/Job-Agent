import os
import google.generativeai as genai
from src.tools import agent_tools

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Use flash for fast tool calling
model = genai.GenerativeModel(
    model_name='gemini-3.5-flash-lite',
    tools=agent_tools,
    system_instruction=(
        "You are an AI job matching assistant. Help users find jobs by analyzing their requests. "
        "Use the provided tools to query the database. "
        "Always summarize the findings naturally to the user."
    )
)

# In a production app, we would store chats in Redis/Postgres per user.
# For the PoC, we keep an in-memory dictionary of chat sessions.
chat_sessions = {}

def get_chat_response(session_id: str, user_message: str) -> str:
    if session_id not in chat_sessions:
        chat_sessions[session_id] = model.start_chat(enable_automatic_function_calling=True)
        
    chat = chat_sessions[session_id]
    response = chat.send_message(user_message)
    
    return response.text