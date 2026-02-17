from pydantic import BaseModel
from typing import Optional


class VoiceChatTextRequest(BaseModel):
    """Request body when sending a text message for voice chat."""
    message: str
    user_email: Optional[str] = "anonymous"


class VoiceChatTextResponse(BaseModel):
    """Response when text→AI→text (no audio)."""
    user_text: str
    ai_response: str


class TranscriptionResponse(BaseModel):
    """Response for speech-to-text only."""
    transcribed_text: str
