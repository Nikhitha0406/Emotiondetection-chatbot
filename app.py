import streamlit as st
from translator import detect_language, translate_to_english, translate
from ai_generator import generate_response

# Emotion detection (fallback if not available)
try:
    from emotion_detector import detect_emotion
except ImportError:
    def detect_emotion(text):
        return [("neutral", 1.0)]

# Session state init
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Page config
st.set_page_config(page_title="Emotion-Aware Chatbot", page_icon="💬")
st.title("😊 Emotion-Aware Chatbot")

# User input
user_input = st.text_input("You:", "")

if st.button("Send") and user_input.strip():
    # 🌍 Detect and translate to English
    original_lang = detect_language(user_input)
    english_input = translate_to_english(user_input)

    # 🔍 Emotion detection
    emotion_scores = detect_emotion(english_input)
    primary_emotion, _ = emotion_scores[0] if emotion_scores else ("neutral", 1.0)

    # 🤖 AI response generation
    english_response = generate_response(primary_emotion, english_input)

    # 🌐 Translate back if needed
    final_response = translate(english_response, target=original_lang) if original_lang != "en" else english_response

    # 💬 Update chat history
    st.session_state.chat_history.append({
        "user": user_input,
        "bot": final_response,
        "emotion": primary_emotion
    })

# Display chat history
if st.session_state.chat_history:
    st.markdown("### 🗨️ Conversation")
    for chat in st.session_state.chat_history[::-1]:
        st.markdown(f"**You**: {chat['user']}")
        st.markdown(f"**Bot ({chat['emotion']})**: {chat['bot']}")
        st.markdown("---")
