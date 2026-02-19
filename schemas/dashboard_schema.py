from pydantic import BaseModel
from typing import List, Optional


class DashboardResponse(BaseModel):
    user_name: str
    email: str
    xp: int
    level: int
    xp_to_next: int
    streak: int
    match_percentage: Optional[float] = None
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    total_progress_percentage: float = 0.0
    completed_skills: List[str] = []
    recent_test_scores: List[dict] = []
    earned_badges: List[int] = []
    daily_xp: dict = {}
    project_progress: List[dict] = []
