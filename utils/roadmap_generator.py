from typing import Dict, List

# Pre-built resource suggestions per skill
SKILL_RESOURCES: Dict[str, str] = {
    "python": "https://docs.python.org/3/tutorial/",
    "java": "https://dev.java/learn/",
    "javascript": "https://javascript.info/",
    "react": "https://react.dev/learn",
    "node.js": "https://nodejs.org/en/docs/guides",
    "sql": "https://www.w3schools.com/sql/",
    "docker": "https://docs.docker.com/get-started/",
    "aws": "https://aws.amazon.com/getting-started/",
    "machine learning": "https://developers.google.com/machine-learning/crash-course",
    "data structures": "https://www.geeksforgeeks.org/data-structures/",
    "algorithms": "https://www.geeksforgeeks.org/fundamentals-of-algorithms/",
    "system design": "https://github.com/donnemartin/system-design-primer",
}


def generate_roadmap(missing_skills: List[str], total_weeks: int = 4) -> List[Dict]:
    """
    Generate a structured weekly roadmap based on the missing skills.
    Distributes skills evenly across the given number of weeks.
    """
    if not missing_skills:
        return [{
            "week": 1,
            "title": "You're all set!",
            "skills": [],
            "notes": "Your resume already covers the JD requirements. Keep practising!",
            "resources": [],
        }]

    # Distribute skills across weeks
    skills_per_week = max(1, len(missing_skills) // total_weeks)
    roadmap: List[Dict] = []

    for week_num in range(1, total_weeks + 1):
        start = (week_num - 1) * skills_per_week
        if week_num == total_weeks:
            week_skills = missing_skills[start:]
        else:
            week_skills = missing_skills[start:start + skills_per_week]

        if not week_skills:
            continue

        resources = [
            {"skill": s, "url": SKILL_RESOURCES.get(s, f"https://www.google.com/search?q=learn+{s.replace(' ', '+')}")}
            for s in week_skills
        ]

        roadmap.append({
            "week": week_num,
            "title": f"Week {week_num}: {', '.join(s.title() for s in week_skills)}",
            "skills": week_skills,
            "notes": f"Focus on learning and practising: {', '.join(week_skills)}.",
            "resources": resources,
        })

    return roadmap
