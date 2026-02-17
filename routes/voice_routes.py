"""
Voice chat routes:

POST /voice/chat-audio
    Upload audio → transcribe → Gemini AI → TTS → return MP3 audio + texts

POST /voice/chat-text
    Send text → Gemini AI → TTS → return MP3 audio + texts

POST /voice/transcribe
    Upload audio → return transcribed text only

POST /voice/tts
    Send text → return MP3 audio only
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from schemas.voice_schema import VoiceChatTextRequest, VoiceChatTextResponse, TranscriptionResponse
from utils.voice_handler import speech_to_text, text_to_speech, ask_gemini
from urllib.parse import quote
import json

router = APIRouter(prefix="/voice", tags=["Voice Chat"])


# ── 1. Full voice-to-voice pipeline ──────────────────────────
@router.post("/chat-audio")
async def voice_chat_audio(
    audio: UploadFile = File(...),
    user_email: str = Form("anonymous"),
):
    """
    Full pipeline:
      1. Receive audio from user's mic
      2. Transcribe to text (STT)
      3. Send to Gemini AI
      4. Convert AI reply to audio (TTS)
      5. Return MP3 audio along with texts in headers
    """
    try:
        audio_bytes = await audio.read()
        content_type = audio.content_type or "audio/wav"

        # Step 1 — Speech to Text
        user_text = speech_to_text(audio_bytes, content_type)

        # Step 2 — Gemini AI
        ai_response = ask_gemini(user_text, user_email)

        # Step 3 — Text to Speech
        audio_reply = text_to_speech(ai_response)

        # Return audio with transcription & AI text in custom headers
        return Response(
            content=audio_reply,
            media_type="audio/mpeg",
            headers={
                "X-User-Text": quote(user_text, safe=''),
                "X-AI-Response": quote(ai_response.replace("\n", " ")[:500], safe=''),
                "Access-Control-Expose-Headers": "X-User-Text, X-AI-Response",
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice chat error: {str(e)}")


# ── 2. Text in → voice + text out ────────────────────────────
@router.post("/chat-text")
async def voice_chat_text(
    request: VoiceChatTextRequest,
):
    """
    Text pipeline:
      1. Receive text message
      2. Send to Gemini AI
      3. Convert AI reply to audio (TTS)
      4. Return MP3 audio along with AI text in headers
    """
    try:
        ai_response = ask_gemini(request.message, request.user_email)
        audio_reply = text_to_speech(ai_response)

        return Response(
            content=audio_reply,
            media_type="audio/mpeg",
            headers={
                "X-User-Text": quote(request.message, safe=''),
                "X-AI-Response": quote(ai_response.replace("\n", " ")[:500], safe=''),
                "Access-Control-Expose-Headers": "X-User-Text, X-AI-Response",
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


# ── 3. Transcribe-only (STT) ─────────────────────────────────
@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    audio: UploadFile = File(...),
):
    """Upload audio and get transcribed text back."""
    try:
        audio_bytes = await audio.read()
        content_type = audio.content_type or "audio/wav"
        text = speech_to_text(audio_bytes, content_type)
        return TranscriptionResponse(transcribed_text=text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")


# ── 4. TTS-only ──────────────────────────────────────────────
@router.post("/tts")
async def tts_only(
    text: str = Form(...),
    lang: str = Form("en"),
):
    """Convert text to speech and return MP3 audio."""
    try:
        audio_bytes = text_to_speech(text, lang)
        return Response(content=audio_bytes, media_type="audio/mpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")
