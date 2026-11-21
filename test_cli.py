from src.agent import get_chat_response

print("Sending prompt to Gemini...")
try:
    response = get_chat_response("test_session", "Show me remote jobs paying over 70k")
    print("\n[SUCCESS] Agent Response:\n", response)
except Exception as e:
    print("\n[ERROR]", e)