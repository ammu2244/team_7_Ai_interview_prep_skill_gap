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
    """Add XP to the user's profile."""
    user.xp += points
    db.commit()
    db.refresh(user)
