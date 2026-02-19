import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import User, TestResult
from schemas.test_schema import (
    TestRequest,
    TestGenerateResponse,
    QuestionOut,
    SubmitTestRequest,
    SubmitTestResponse,
    QuestionResult,
    TestResultResponse,
)
from utils.jwt_handler import get_current_user
from utils.test_generator import generate_test_questions
from utils.streak_logic import add_xp, update_streak, XP_PER_TEST

router = APIRouter(prefix="/test", tags=["Mock Tests"])

# In-memory store for active tests (test_id -> list of full question dicts)
_active_tests: dict[str, list[dict]] = {}


@router.post("/generate", response_model=TestGenerateResponse)
def generate_test(
    payload: TestRequest,
    current_user: User = Depends(get_current_user),
):
    """Generate MCQ questions for a skill.
    Returns questions WITHOUT correct answers — user must submit answers to /test/check."""
    questions = generate_test_questions(payload.skill_name, payload.num_questions)

    # Create a unique test ID and store the full questions (with answers) server-side
    test_id = str(uuid.uuid4())
    _active_tests[test_id] = questions

    # Return questions WITHOUT correct_answer or explanation
    questions_out = [
        QuestionOut(id=i, question=q["question"], options=q["options"])
        for i, q in enumerate(questions)
    ]

    return TestGenerateResponse(
        test_id=test_id,
        skill_name=payload.skill_name,
        questions=questions_out,
    )


@router.post("/check", response_model=SubmitTestResponse)
def check_answers(
    payload: SubmitTestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit your answers and get right/wrong results for each question."""
    if payload.test_id not in _active_tests:
        raise HTTPException(status_code=404, detail="Test not found or already submitted")

    full_questions = _active_tests.pop(payload.test_id)  # remove after checking
    total = len(full_questions)
    correct_count = 0
    results = []

    for ans in payload.answers:
        if ans.question_id < 0 or ans.question_id >= total:
            continue

        q = full_questions[ans.question_id]
        is_correct = ans.selected_answer.strip().lower() == q["correct_answer"].strip().lower()
        if is_correct:
            correct_count += 1

        results.append(QuestionResult(
            question_id=ans.question_id,
            question=q["question"],
            selected_answer=ans.selected_answer,
            correct_answer=q["correct_answer"],
            is_correct=is_correct,
            explanation=q.get("explanation"),
        ))

    score = round((correct_count / total) * 100, 2) if total > 0 else 0.0

    # Save result to DB
    test_result = TestResult(
        user_id=current_user.id,
        skill_name=payload.skill_name,
        score=score,
    )
    db.add(test_result)
    db.commit()
    db.refresh(test_result)

    # Award XP and update streak
    add_xp(current_user, XP_PER_TEST, db)
    update_streak(current_user, db)

    return SubmitTestResponse(
        skill_name=payload.skill_name,
        total_questions=total,
        correct_count=correct_count,
        score=score,
        results=results,
    )


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
