"""
Voice handling utilities:
  - speech_to_text : convert uploaded audio (WAV/WebM) → text
  - text_to_speech : convert text → MP3 bytes (via gTTS)
  - ask_gemini     : send a prompt to Gemini and get a text reply
"""

import os
import io
import tempfile
import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# ── Gemini setup ──────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

_model = genai.GenerativeModel("gemini-3-flash-preview")

SYSTEM_PROMPT = (
    "You are an AI Interview Preparation Assistant. "
    "Help the user practise for job interviews, answer technical questions, "
    "give feedback on their answers, and suggest improvements. "
    "Keep replies concise and spoken-friendly (the user hears your answer). "
    "Use simple language suitable for text-to-speech."
)

# Store per-user chat sessions in memory (swap for DB/Redis in prod)
_chat_sessions: dict[str, object] = {}


def _get_chat(user_email: str):
    """Return (or create) a Gemini chat session for this user."""
    if user_email not in _chat_sessions:
        _chat_sessions[user_email] = _model.start_chat(
            history=[{"role": "user", "parts": [SYSTEM_PROMPT]},
                     {"role": "model", "parts": ["Understood! I'm ready to help you prepare for your interviews. Go ahead and ask me anything."]}]
        )
    return _chat_sessions[user_email]


# ── Speech-to-Text ────────────────────────────────────────────
def speech_to_text(audio_bytes: bytes, content_type: str = "audio/wav") -> str:
    """
    Convert raw audio bytes to text using Google Web Speech API
    (free, no key required — uses the SpeechRecognition library).
    Accepts WAV or WebM audio.
    """
    recognizer = sr.Recognizer()

    # Write bytes to a temp file so SpeechRecognition can read it
    suffix = ".wav" if "wav" in content_type else ".webm"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        with sr.AudioFile(tmp_path) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text
    finally:
        os.unlink(tmp_path)


# ── Text-to-Speech ────────────────────────────────────────────
def text_to_speech(text: str, lang: str = "en") -> bytes:
    """Convert text → MP3 audio bytes using Google TTS."""
    tts = gTTS(text=text, lang=lang, slow=False)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()


# ── Gemini AI chat ────────────────────────────────────────────
def ask_gemini(user_message: str, user_email: str = "anonymous") -> str:
    """Send a text message to Gemini and return the model's reply."""
    chat = _get_chat(user_email)
    response = chat.send_message(user_message)
    return response.text
