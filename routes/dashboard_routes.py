import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import User, SkillAnalysis, Progress, TestResult
from schemas.dashboard_schema import DashboardResponse
from utils.jwt_handler import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return a summary dashboard for the current user."""

    # Latest skill analysis
    analysis = (
        db.query(SkillAnalysis)
        .filter(SkillAnalysis.user_id == current_user.id)
        .order_by(SkillAnalysis.id.desc())
        .first()
    )

    matched_skills = json.loads(analysis.matched_skills) if analysis and analysis.matched_skills else []
    missing_skills = json.loads(analysis.missing_skills) if analysis and analysis.missing_skills else []
    match_percentage = analysis.match_percentage if analysis else None

    # Latest progress
    progress = (
        db.query(Progress)
        .filter(Progress.user_id == current_user.id)
        .order_by(Progress.id.desc())
        .first()
    )
    completed_skills = json.loads(progress.completed_skills) if progress and progress.completed_skills else []
    total_progress = progress.total_progress_percentage if progress else 0.0

    # Recent test scores (last 10)
    recent_tests = (
        db.query(TestResult)
        .filter(TestResult.user_id == current_user.id)
        .order_by(TestResult.taken_at.desc())
        .limit(10)
        .all()
    )
    recent_test_scores = [
        {"skill_name": t.skill_name, "score": t.score, "taken_at": str(t.taken_at)}
        for t in recent_tests
    ]

    return DashboardResponse(
        user_name=current_user.name,
        email=current_user.email,
        xp=current_user.xp,
        streak=current_user.streak,
        match_percentage=match_percentage,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        total_progress_percentage=total_progress,
        completed_skills=completed_skills,
        recent_test_scores=recent_test_scores,
    )
