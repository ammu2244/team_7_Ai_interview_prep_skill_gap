from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import User, TestResult
from schemas.test_schema import (
    TestRequest,
    TestGenerateResponse,
    SubmitAnswerRequest,
    TestResultResponse,
)
from utils.jwt_handler import get_current_user
from utils.test_generator import generate_test_questions
from utils.streak_logic import add_xp, update_streak, XP_PER_TEST

router = APIRouter(prefix="/test", tags=["Mock Tests"])


@router.post("/generate", response_model=TestGenerateResponse)
def generate_test(
    payload: TestRequest,
    current_user: User = Depends(get_current_user),
):
    """Generate mock-interview questions for a given skill."""
    questions = generate_test_questions(payload.skill_name, payload.num_questions)
    return TestGenerateResponse(skill_name=payload.skill_name, questions=questions)


@router.post("/submit", response_model=TestResultResponse, status_code=201)
def submit_test(
    payload: SubmitAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit test score for a skill and record the result."""
    result = TestResult(
        user_id=current_user.id,
        skill_name=payload.skill_name,
        score=payload.score,
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    # Award XP and update streak
    add_xp(current_user, XP_PER_TEST, db)
    update_streak(current_user, db)

    return result


@router.get("/history", response_model=list[TestResultResponse])
def get_test_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return all test results for the current user."""
    results = (
        db.query(TestResult)
        .filter(TestResult.user_id == current_user.id)
        .order_by(TestResult.taken_at.desc())
        .all()
    )
    return results
