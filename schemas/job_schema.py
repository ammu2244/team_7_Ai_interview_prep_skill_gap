from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class JobDescriptionRequest(BaseModel):
    company_name: Optional[str] = None
    jd_text: str


class JobDescriptionResponse(BaseModel):
    id: int
    user_id: int
    company_name: Optional[str]
    jd_text: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
