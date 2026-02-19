from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# --- Questions shown to user (NO answer revealed) ---
class QuestionOut(BaseModel):
    """Question as shown to the user — no correct_answer or explanation."""
    id: int
    question: str
    options: List[str]


# --- Full question with answer (used internally) ---
class QuestionFull(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None


class TestRequest(BaseModel):
    skill_name: str
    num_questions: int = 5


class TestGenerateResponse(BaseModel):
    """Response to the user — questions WITHOUT answers."""
    test_id: str
    skill_name: str
    questions: List[QuestionOut]


# --- User submits answers ---
class AnswerItem(BaseModel):
    question_id: int
    selected_answer: str


class SubmitTestRequest(BaseModel):
    test_id: str
    skill_name: str
    answers: List[AnswerItem]


# --- Result for each question ---
class QuestionResult(BaseModel):
    question_id: int
    question: str
    selected_answer: str
    correct_answer: str
    is_correct: bool
    explanation: Optional[str] = None


class SubmitTestResponse(BaseModel):
    skill_name: str
    total_questions: int
    correct_count: int
    score: float
    results: List[QuestionResult]


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
