import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import User, SkillAnalysis
from utils.jwt_handler import get_current_user
from utils.roadmap_generator import generate_roadmap

router = APIRouter(prefix="/roadmap", tags=["AI Roadmap"])


@router.get("/")
def get_roadmap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate an AI-based weekly roadmap from the user's latest skill analysis.
    """
    analysis = (
        db.query(SkillAnalysis)
        .filter(SkillAnalysis.user_id == current_user.id)
        .order_by(SkillAnalysis.id.desc())
        .first()
    )
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Run a skill-gap analysis first (POST /analysis/jd then GET /analysis/skill-gap)",
        )

    missing_skills = json.loads(analysis.missing_skills) if analysis.missing_skills else []
    roadmap = generate_roadmap(missing_skills)

    return {
        "user_id": current_user.id,
        "match_percentage": analysis.match_percentage,
        "roadmap": roadmap,
    }
