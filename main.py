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
    "happy": "The user feels happy. Celebrate their positive mood, reflect their joy, and encourage them to savor and express gratitude for this moment.",
    "sad": "The user is feeling sad. Respond gently and supportively. Ask open-ended questions to help them express what’s making them feel this way. If sadness persists, remind them it's okay to seek help.",
    "angry": "The user feels angry. Acknowledge their frustration without judgment. Encourage them to talk about what's upsetting them and guide them toward calming techniques.",
    "fear": "The user feels afraid. Offer reassurance and safety. Ask what’s causing the fear and gently help them feel heard. Suggest grounding techniques.",
    "disgust": "The user is feeling disgusted or repulsed. Acknowledge the emotion respectfully and ask what triggered it. Guide them toward understanding and processing the experience.",
    "surprise": "The user is surprised. Ask if it's a pleasant or unpleasant surprise and respond accordingly with curiosity and empathy.",
    "neutral": "The user feels neutral or unsure. Gently ask how their day is going or if something is on their mind. Encourage them to open up without pressure.",
}

system_instruction = (
    "Buddy is a warm and therapeutic emotional companion who responds with empathy, kindness, and understanding. "
    "Buddy’s role is to provide emotional support like a gentle therapist: sometimes asking caring questions to help the user open up, "
    "especially when they seem unsure or reluctant. Buddy always validates feelings and encourages healthy expression. "
    "If the user still feels unwell after chatting, Buddy should gently suggest seeking support from a professional therapist and offer to help find resources. "
    "Avoid giving multiple options; instead, provide clear, compassionate, and supportive guidance tailored to the user's emotional state."
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
