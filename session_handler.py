import json
import os

SESSION_FILE = "session.json"

def load_session():
    print(f"Loading session from {SESSION_FILE}")
    if not os.path.exists(SESSION_FILE):
        print("Session file not found. Returning empty list.")
        return []
    with open(SESSION_FILE, "r") as f:
        try:
            data = json.load(f)
            print(f"Loaded session with {len(data)} messages")
            return data
        except json.JSONDecodeError:
            print("Failed to decode JSON, returning empty list.")
            return []

def save_session(messages):
    with open(SESSION_FILE, "w") as f:
        json.dump(messages, f, indent=2)

def clear_session():
    with open(SESSION_FILE, "w") as f:
        json.dump([], f)
