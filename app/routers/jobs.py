from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import JobApplication
from app.schemas import JobCreate, JobUpdate, JobResponse

# Create router with a common URL prefix and Swagger tag
router = APIRouter(prefix = "/api/jobs", tags = ["Jobs"])

# 1. CREATE: Add a new job application
@router.post("/", response_model = JobResponse, status_code = status.HTTP_201_CREATED)
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    db_job = JobApplication(**job_data.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

# 2. READ ALL: Get all jobs (with optional filter by status)
@router.get("/", response_model = List[JobResponse])
def get_all_jobs(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(JobApplication)
    if status and status != "all":
        query = query.filter(JobApplication.status.ilike(status))
    return query.order_by(JobApplication.applied_date.desc()).all()

# 3. READ ONE: Get a single job by its ID
@router.get("/{job_id}", response_model = JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobApplication).filter(JobApplication.id == job_id).first()
    if not job:
        raise HTTPException(status_code = 404, detail = "Job application not found")
    return job

# 4. UPDATE: Modify an existing job's status or details
@router.put("/{job_id}", response_model = JobResponse)
def update_job(job_id: int, job_data: JobUpdate, db: Session = Depends(get_db)):
    job = db.query(JobApplication).filter(JobApplication.id == job_id).first()
    if not job:
        raise HTTPException(status_code = 404, detail = "Job application not found")
    
    # Only update the fields the user actually sent
    update_fields = job_data.model_dump(exclude_unset = True)
    for key, value in update_fields.items():
        setattr(job, key, value)
        
    db.commit()
    db.refresh(job)
    return job

# 5. DELETE: Remove a job application
@router.delete("/{job_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobApplication).filter(JobApplication.id == job_id).first()
    if not job:
        raise HTTPException(status_code = 404, detail = "Job application not found")
    
    db.delete(job)
    db.commit()
    return None