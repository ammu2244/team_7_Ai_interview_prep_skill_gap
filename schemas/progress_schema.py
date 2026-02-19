from pydantic import BaseModel
from typing import List

class ProgressUpdate(BaseModel):
    completed_skills: List[str]

class ProgressResponse(BaseModel):
    user_id: int
    completed_skills: List[str]
    total_progress_percentage: float

    class Config:
        from_attributes = True
