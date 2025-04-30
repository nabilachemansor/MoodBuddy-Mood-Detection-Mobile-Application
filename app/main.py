from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
from fastapi.middleware.cors import CORSMiddleware

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
    "sad": "The user is feeling sad. Be gentle and supportive.",
    "lost": "The user may have lost something or someone. Offer comfort and acknowledge their grief.",
    "anxious": "The user feels anxious. Help them slow down and feel grounded.",
    "depressed": "The user might be feeling very low. Be kind, validate their emotions, and remind them they’re not alone.",
    "grief": "The user is grieving. Speak with compassion and let them know it’s okay to feel this way.",
}

system_instruction = "Buddy is a kind and supportive emotional companion who helps users feel better when they’re down.\n"

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
        prompt = build_prompt(input.message)
        response = model.generate_content(prompt)
        return {"reply": response.text}
    except Exception as e:
        return {"error": str(e)}
