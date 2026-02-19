"""
Roadmap generator — now powered by Gemini AI.
Delegates roadmap creation to the central AI agent for personalised, detailed learning plans.
"""

from typing import Dict, List
from utils.ai_agent import ai_generate_roadmap, ai_generate_projects


def generate_roadmap(missing_skills: List[str], total_weeks: int = 4) -> List[Dict]:
    """
    Generate a structured weekly roadmap using AI, tailored to the missing skills.
    """
    return ai_generate_roadmap(missing_skills, total_weeks)


def generate_mini_projects(missing_skills: List[str], count: int = 2) -> List[Dict]:
    """
    Generate a set of unique mini projects tailored to the missing skills.
    """
    return ai_generate_projects(missing_skills, count)
