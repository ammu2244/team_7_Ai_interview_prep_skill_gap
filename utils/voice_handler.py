"""
Voice handling utilities:
  - speech_to_text : convert uploaded audio (WAV/WebM) → text
  - text_to_speech : convert text → MP3 bytes (via gTTS)
  - ask_gemini     : send a prompt to the AI Interview Coach
"""

import os
import io
import tempfile
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv
from utils.ai_agent import ai_interview_coach

load_dotenv()


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


# ── AI Interview Coach chat ──────────────────────────────────
def ask_gemini(user_message: str, user_email: str = "anonymous") -> str:
    """
    Send a text message to the AI Interview Coach and return the reply.
    Now powered by the enhanced interview coach in ai_agent.py.
    """
    return ai_interview_coach(user_message, user_email)
