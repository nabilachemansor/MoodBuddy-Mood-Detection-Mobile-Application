# 🧠 Mental Health Chatbot Backend

This is a FastAPI backend using Google Gemini API. It is deployed to Render and ready to integrate with React Native.

## ✅ API Base URL
```
https://moodbuddy-mood-detection-mobile.onrender.com
```

## 📮 Endpoint

**POST /chatbot/**

Request Body (JSON):
```json
{
  "message": "I'm feeling anxious today"
}
```

Response:
```json
{
  "reply": "I'm here for you. Want to talk about what's making you anxious?"
}
```

## ⚙️ How to Use in React Native (Axios Example)

```js
import axios from 'axios';

const sendMessageToBot = async (userInput) => {
  try {
    const response = await axios.post(
      'https://your-chatbot-app.herokuapp.com/chatbot/',
      { message: userInput }
    );
    console.log('Bot reply:', response.data.reply);
    return response.data.reply;
  } catch (error) {
    console.error('Error communicating with bot:', error);
    return 'Sorry, something went wrong.';
  }
};
```

> 🔐 No Gemini key is needed on the frontend. The backend handles it securely.
