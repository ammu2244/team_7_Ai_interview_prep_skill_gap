from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    xp: int
    level: int
    xp_to_next: int
    streak: int
    earned_badges: str = "[]"
    daily_xp: str = "{}"

    class Config:
        from_attributes = True
