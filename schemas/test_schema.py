from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Question(BaseModel):
    question: str
    options: List[str]
    correct_answer: str


class TestRequest(BaseModel):
    skill_name: str
    num_questions: int = 5


class TestGenerateResponse(BaseModel):
    skill_name: str
    questions: List[Question]


class SubmitAnswerRequest(BaseModel):
    skill_name: str
    score: float


class TestResultResponse(BaseModel):
    id: int
    user_id: int
    skill_name: str
    score: float
    taken_at: datetime

    class Config:
        from_attributes = True
