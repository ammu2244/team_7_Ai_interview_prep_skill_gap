import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import User

XP_PER_TEST = 10
XP_PER_ANALYSIS = 5


def update_streak(user: User, db: Session) -> None:
    """
    Update the user's streak.
    Call this whenever the user performs a daily activity (test, analysis, etc.).
    If the user was active yesterday, increment streak; otherwise reset to 1.
    """
    today = datetime.utcnow().date()
    last_active = user.created_at.date()  # simplified – use a dedicated field in production

    if (today - last_active) == timedelta(days=1):
        user.streak += 1
    elif (today - last_active) > timedelta(days=1):
        user.streak = 1
    # If same day, do nothing

    db.commit()
    db.refresh(user)


def add_xp(user: User, points: int, db: Session) -> None:
    """Add XP to the user's profile and handle leveling."""
    today = datetime.utcnow().date().isoformat()
    
    # Update Daily XP
    daily_xp_data = json.loads(user.daily_xp) if user.daily_xp else {}
    daily_xp_data[today] = daily_xp_data.get(today, 0) + points
    user.daily_xp = json.dumps(daily_xp_data)

    # Add XP and Level Up
    user.xp += points
    while user.xp >= user.xp_to_next:
        user.xp -= user.xp_to_next
        user.level += 1
        user.xp_to_next += 500  # Progression difficulty increase
        
    db.commit()
    db.refresh(user)


def give_badge(user: User, badge_id: int, db: Session) -> None:
    """Award a badge to the user if they don't have it."""
    badges = json.loads(user.earned_badges) if user.earned_badges else []
    if badge_id not in badges:
        badges.append(badge_id)
        user.earned_badges = json.dumps(badges)
        db.commit()
        db.refresh(user)
