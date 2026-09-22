from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

from app.services.top_companies import TOP_200_COMPANIES, get_top_companies_directory
from app.services.ats_matcher import extract_text_from_file, extract_skills_from_text
from app.services.job_fetcher import fetch_live_jobs, rank_jobs_by_resume

router = APIRouter(prefix="/api/discover", tags=["Discover & ATS"])

class SearchTextRequest(BaseModel):
    resume_text: Optional[str] = ""
    query: Optional[str] = ""
    category: Optional[str] = "all"
    company_type: Optional[str] = "all"
    job_type: Optional[str] = "all"
    region: Optional[str] = "all"
    experience_level: Optional[str] = "all"

@router.post("/search-text")
def search_jobs_by_text(req: SearchTextRequest):
    """Pulls matching live jobs and ranks them by ATS score."""
    matching_jobs = fetch_live_jobs(
        query=req.query,
        category=req.category,
        company_type=req.company_type,
        job_type=req.job_type,
        region=req.region,
        experience_level=req.experience_level,
        limit=50
    )

    ranked_jobs = rank_jobs_by_resume(
        resume_text=req.resume_text or "",
        jobs=matching_jobs
    )

    # Extract detected skills if resume text was passed
    detected_skills = []
    if req.resume_text and req.resume_text.strip():
        detected_skills = list(extract_skills_from_text(req.resume_text))

    return {
        "count": len(ranked_jobs),
        "detected_skills": detected_skills,
        "jobs": ranked_jobs
    }

@router.post("/search-file")
async def search_jobs_by_file(
    file: UploadFile = File(...),
    query: Optional[str] = Form(""),
    category: Optional[str] = Form("all"),
    company_type: Optional[str] = Form("all"),
    job_type: Optional[str] = Form("all"),
    region: Optional[str] = Form("all"),
    experience_level: Optional[str] = Form("all")
):
    """Accepts uploaded resume, extracts skills in memory, and ranks jobs."""
    filename = file.filename or "resume.pdf"
    if not any(filename.lower().endswith(ext) for ext in [".pdf", ".docx", ".doc", ".txt"]):
        raise HTTPException(
            status_code=400,
            detail="Unsupported format. Please upload PDF, Word (.docx), or Text (.txt)."
        )

    content = await file.read()
    resume_text = extract_text_from_file(filename, content)

    if not resume_text or not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text. Please ensure document is not empty or password protected."
        )

    matching_jobs = fetch_live_jobs(
        query=query,
        category=category,
        company_type=company_type,
        job_type=job_type,
        region=region,
        experience_level=experience_level,
        limit=50
    )

    ranked_jobs = rank_jobs_by_resume(
        resume_text=resume_text,
        jobs=matching_jobs
    )

    detected_skills = list(extract_skills_from_text(resume_text))

    return {
        "count": len(ranked_jobs),
        "filename": filename,
        "detected_skills": detected_skills,
        "jobs": ranked_jobs
    }

@router.get("/top-companies")
def get_top_companies(category: Optional[str] = None):
    """Returns the top tech companies directory for the modal."""
    companies = TOP_200_COMPANIES
    if category and category.lower() != "all":
        companies = [c for c in companies if c.get("category", "").lower() == category.lower()]
    return {"companies": companies}