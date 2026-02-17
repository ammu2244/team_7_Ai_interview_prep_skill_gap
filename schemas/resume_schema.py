from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ResumeUploadResponse(BaseModel):
    id: int
    user_id: int
    resume_text: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
