"""
Skill matcher — now powered by Gemini AI.
Delegates analysis to the central AI agent for intelligent skill extraction and comparison.
"""

from typing import Dict
from utils.ai_agent import ai_analyse_skill_gap


def analyse_skill_gap(resume_text: str, jd_text: str) -> Dict:
    """
    Compare resume skills against JD requirements using AI.
    Returns matched skills, missing skills, and match percentage.
    """
    return ai_analyse_skill_gap(resume_text, jd_text)
