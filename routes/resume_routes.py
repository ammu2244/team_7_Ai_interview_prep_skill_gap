from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from db import get_db
from models import User, Resume
from schemas.resume_schema import ResumeUploadResponse
from utils.jwt_handler import get_current_user
from utils.resume_parser import extract_text_from_pdf

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload", response_model=ResumeUploadResponse, status_code=201)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Upload a PDF resume, extract text, and save to DB."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    contents = await file.read()
    text = extract_text_from_pdf(contents)

    if not text.strip():
        raise HTTPException(status_code=422, detail="Could not extract text from the PDF")

    resume = Resume(user_id=current_user.id, resume_text=text)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


@router.get("/latest", response_model=ResumeUploadResponse)
def get_latest_resume(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return the most recently uploaded resume for the current user."""
    resume = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.uploaded_at.desc())
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="No resume found")
    return resume
