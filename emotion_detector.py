# emotion_detector.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")  # Ensure .env has: HF_API_KEY=your_token_here

def detect_emotion(text):
    API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": text}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        predictions = response.json()[0]
        return [(item['label'].lower(), round(item['score'], 4)) for item in predictions]
    except Exception as e:
        print("HF API error:", e)
        return [("neutral", 1.0)]
