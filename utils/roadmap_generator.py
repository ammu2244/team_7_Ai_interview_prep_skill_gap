"""
Roadmap generator — now powered by Gemini AI.
Delegates roadmap creation to the central AI agent for personalised, detailed learning plans.
"""

from typing import Dict, List
from utils.ai_agent import ai_generate_roadmap


def generate_roadmap(missing_skills: List[str], total_weeks: int = 4) -> List[Dict]:
    """
    Generate a structured weekly roadmap using AI, tailored to the missing skills.
    """
    return ai_generate_roadmap(missing_skills, total_weeks)
