import streamlit as st
import os
from dotenv import load_dotenv
import httpx

# Local imports
from translator import detect_language, translate_to_english, translate

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Fallback for emotion detection
try:
    from emotion_detector import detect_emotion
except ImportError:
    def detect_emotion(text):
        return [("neutral", 1.0)]

# --- Response generation using OpenRouter ---
def generate_response(emotion, prompt):
    system_message = f"You are an empathetic assistant. Respond to the user's message considering the emotion: {emotion}."
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        res = httpx.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers, timeout=30)
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❗ Error fetching response: {e}"

# --- Streamlit App UI ---
st.set_page_config(page_title="Emotion-Aware Chatbot", page_icon="💬")
st.title("😊 Emotion-Aware Chatbot")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("You:", "")

if st.button("Send") and user_input.strip():
    # 🌍 Language Detection + Translation
    original_lang = detect_language(user_input)
    english_input = translate_to_english(user_input)

    # 🔍 Emotion Detection
    emotion_scores = detect_emotion(english_input)
    primary_emotion, _ = emotion_scores[0] if emotion_scores else ("neutral", 1.0)

    # 🤖 AI Response Generation
    english_response = generate_response(primary_emotion, english_input)

    # 🌐 Translate Back
    final_response = translate(english_response, target=original_lang) if original_lang != "en" else english_response

    # 💬 Update history
    st.session_state.chat_history.append({
        "user": user_input,
        "bot": final_response,
        "emotion": primary_emotion
    })

# Show chat history
if st.session_state.chat_history:
    st.markdown("### 🗨️ Conversation")
    for chat in st.session_state.chat_history[::-1]:
        st.markdown(f"**You**: {chat['user']}")
        st.markdown(f"**Bot ({chat['emotion']})**: {chat['bot']}")
        st.markdown("---")
