import hashlib
import os


def hash_password(password: str) -> str:
    """Hash a plain-text password using SHA-256 with a random salt."""
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${hashed}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a stored hash."""
    salt, stored_hash = hashed_password.split("$", 1)
    check = hashlib.sha256((salt + plain_password).encode("utf-8")).hexdigest()
    return check == stored_hash


