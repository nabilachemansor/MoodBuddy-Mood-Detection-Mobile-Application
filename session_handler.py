import json
import os

SESSION_FILE = "session.json"

def load_session():
    if not os.path.exists(SESSION_FILE):
        return []
    with open(SESSION_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_session(messages):
    with open(SESSION_FILE, "w") as f:
        json.dump(messages, f, indent=2)

def clear_session():
    with open(SESSION_FILE, "w") as f:
        json.dump([], f)
