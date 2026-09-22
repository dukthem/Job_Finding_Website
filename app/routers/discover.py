from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

from app.services.top_companies import get_top_companies_directory
from app.services.ats_matcher import extract_text_from_file
from app.services.job_fetcher import fetch_live_jobs, rank_jobs_by_resume

router = APIRouter(prefix="/api/discover", tags=["Discover & ATS"])

# ====================================================================
# 1. Pydantic Schema for Text-Based Search Requests
# ====================================================================
class SearchTextRequest(BaseModel):
    resume_text: Optional[str] = ""
    query: Optional[str] = ""
    category: Optional[str] = "all"
    company_type: Optional[str] = "all"
    job_type: Optional[str] = "all"
    region: Optional[str] = "all"
    experience_level: Optional[str] = "all"


# ====================================================================
# 2. Endpoint 1: Search & Match by Text Query or Pasted Resume
# ====================================================================
@router.post("/search-text")
def search_jobs_by_text(req: SearchTextRequest):
    """
    Accepts filter dropdowns and optional pasted resume text.
    Pulls matching live jobs and ranks them by ATS score!
    """
    # 1. Fetch filtered jobs using Phase 5 Sieve Engine
    matching_jobs = fetch_live_jobs(
        query=req.query,
        category=req.category,
        company_type=req.company_type,
        job_type=req.job_type,
        region=req.region,
        experience_level=req.experience_level,
        limit=50
    )

    # 2. Rank jobs against the provided resume text using Phase 4 ATS math
    ranked_jobs = rank_jobs_by_resume(
        resume_text=req.resume_text,
        jobs=matching_jobs
    )

    return {
        "count": len(ranked_jobs),
        "jobs": ranked_jobs
    }


# ====================================================================
# 3. Endpoint 2: Search & Match by Uploaded PDF / Word Resume File
# ====================================================================
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
    """
    Accepts a real uploaded resume file (.pdf, .docx, .txt).
    Extracts text in memory, fetches matching jobs, and returns ATS-ranked results!
    """
    # 1. Validate file extension
    filename = file.filename or "resume.pdf"
    if not any(filename.lower().endswith(ext) for ext in [".pdf", ".docx", ".txt"]):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload a PDF (.pdf), Word (.docx), or Text (.txt) file."
        )

    # 2. Read file bytes directly into RAM memory
    content = await file.read()

    # 3. Extract human text using Phase 4's In-Memory Parser
    resume_text = extract_text_from_file(filename, content)
    if not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from the uploaded file. Please make sure it is not an empty or password-protected document."
        )

    # 4. Fetch matching live jobs based on selected filters
    matching_jobs = fetch_live_jobs(
        query=query,
        category=category,
        company_type=company_type,
        job_type=job_type,
        region=region,
        experience_level=experience_level,
        limit=50
    )

    # 5. Score and rank matching jobs against the extracted resume text!
    ranked_jobs = rank_jobs_by_resume(
        resume_text=resume_text,
        jobs=matching_jobs
    )

    return {
        "count": len(ranked_jobs),
        "filename": filename,
        "resume_preview": resume_text[:300] + "...",
        "jobs": ranked_jobs
    }


# ====================================================================
# 4. Endpoint 3: Return the Top 200 Portals Directory
# ====================================================================
@router.get("/top-companies")
def get_top_companies(category: Optional[str] = None):
    """Returns curated Top 200 tech employers with career and recruiter links."""
    if category:
        companies = get_top_companies_by_category(category)
    else:
        companies = TOP_200_COMPANIES
    
    return {"companies": companies}
# @router.get("/top-companies")
# def get_top_companies():
#     """
#     Returns the full directory of top tech companies for the popup modal.
#     """
#     return get_top_companies_directory()