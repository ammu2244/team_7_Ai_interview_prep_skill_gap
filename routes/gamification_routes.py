from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import User, ProjectProgress
import json
from utils.jwt_handler import get_current_user
from utils.streak_logic import give_badge, add_xp
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/gamification", tags=["Gamification & Projects"])

class BadgeRequest(BaseModel):
    badge_id: int

class ProjectStepUpdate(BaseModel):
    project_id: str
    completed_steps: List[int]

@router.post("/badge")
def award_badge(
    payload: BadgeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Award a badge to the current user."""
    give_badge(current_user, payload.badge_id, db)
    return {"status": "success", "earned_badges": json.loads(current_user.earned_badges)}

@router.post("/project/step")
def update_project_step(
    payload: ProjectStepUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update completed steps for a specific project."""
    project = db.query(ProjectProgress).filter(
        ProjectProgress.user_id == current_user.id,
        ProjectProgress.project_id == payload.project_id
    ).first()

    if not project:
        project = ProjectProgress(
            user_id=current_user.id,
            project_id=payload.project_id,
            completed_steps=json.dumps(payload.completed_steps)
        )
        db.add(project)
    else:
        project.completed_steps = json.dumps(payload.completed_steps)
    
    # Award minor XP for project progress
    add_xp(current_user, 20, db)
    
    db.commit()
    db.refresh(project)
    return {"status": "success", "project_id": project.project_id, "completed_steps": json.loads(project.completed_steps)}

class XPRequest(BaseModel):
    amount: int

@router.post("/add-xp")
def add_user_xp(
    payload: XPRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Manually add XP for an activity (e.g. Games)."""
    add_xp(current_user, payload.amount, db)
    db.commit()
    return {"status": "success", "total_xp": current_user.xp, "level": current_user.level}
