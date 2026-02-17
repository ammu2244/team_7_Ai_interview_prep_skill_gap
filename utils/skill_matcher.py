import re
from typing import Dict, List

# Common technical skills to look for (expandable list)
KNOWN_SKILLS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "ruby", "php",
    "swift", "kotlin", "r", "scala", "sql", "nosql", "html", "css",
    "react", "angular", "vue", "next.js", "node.js", "express", "django", "flask", "fastapi",
    "spring", "spring boot", ".net",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins", "ci/cd",
    "git", "linux", "rest api", "graphql", "microservices",
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
    "pandas", "numpy", "scikit-learn",
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "firebase",
    "data structures", "algorithms", "system design", "oop",
    "agile", "scrum", "jira", "communication", "leadership", "teamwork", "problem solving",
]


def _extract_skills(text: str) -> List[str]:
    """Extract known skills from a block of text."""
    text_lower = text.lower()
    found = []
    for skill in KNOWN_SKILLS:
        # Use word-boundary-aware matching
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill)
    return sorted(set(found))


def analyse_skill_gap(resume_text: str, jd_text: str) -> Dict:
    """
    Compare resume skills against JD requirements.
    Returns matched skills, missing skills, and match percentage.
    """
    resume_skills = _extract_skills(resume_text)
    jd_skills = _extract_skills(jd_text)

    if not jd_skills:
        return {
            "matched_skills": resume_skills,
            "missing_skills": [],
            "match_percentage": 100.0,
        }

    matched = [s for s in jd_skills if s in resume_skills]
    missing = [s for s in jd_skills if s not in resume_skills]
    match_pct = round((len(matched) / len(jd_skills)) * 100, 2)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "match_percentage": match_pct,
    }
