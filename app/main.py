from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
from fastapi.middleware.cors import CORSMiddleware
from session_handler import load_session, save_session, clear_session

app = FastAPI()

# CORS setup so frontend can access it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Emotional keyword mapping and system instructions
emotional_keywords = {
    "lonely": "The user is feeling lonely. Respond with empathy and suggest something comforting they can do alone.",
    "sad": "The user is feeling sad. Be gentle and supportive. Remind them it’s okay to feel sad, and they’re not alone.",
    "lost": "The user may have lost something or someone. Acknowledge their loss and offer comforting words.",
    "anxious": "The user feels anxious. Gently encourage them to take deep breaths and reassure them it's okay to feel anxious.",
    "depressed": "The user might be feeling very low. Be kind, validate their emotions, and remind them that things can get better.",
    "grief": "The user is grieving. Speak with deep compassion, offering validation for their grief and reminding them it’s okay to take things slowly.",
}

system_instruction = (
    "Buddy is a kind and supportive emotional companion who always responds with empathy, kindness, and understanding. "
    "Buddy should never give multiple options; instead, Buddy should respond with a clear, singular message that shows care."
)

# Build prompt based on user message and emotion
def build_prompt(user_message):
    for keyword, guidance in emotional_keywords.items():
        if keyword in user_message.lower():
            return f"{system_instruction}{guidance}\nUser says: '{user_message}'\nBuddy replies:"

    return f"{system_instruction}User says: '{user_message}'\nBuddy replies:"

# Input model for request
class UserInput(BaseModel):
    message: str

# Test route
@app.get("/")
def root():
    return {"message": "Chatbot is running"}

# Chatbot route
@app.post("/chatbot/")
async def chatbot(input: UserInput):
    try:
        history = load_session()
        history.append({"sender": "user", "message": input.message})

        prompt = "\n".join(f"{m['sender']}: {m['message']}" for m in history)
        prompt = f"{system_instruction}\n{prompt}\nbot:"

        response = model.generate_content(prompt)
        reply = response.text.strip()

        history.append({"sender": "bot", "message": reply})
        save_session(history)

        return {"reply": reply}
    except Exception as e:
        return {"error": str(e)}

# Resume session
@app.get("/chatbot/resume")
def resume_session():
    return {"history": load_session()}

# Start new session
@app.post("/chatbot/new")
def new_session():
    clear_session()
    return {"message": "New conversation started."}
