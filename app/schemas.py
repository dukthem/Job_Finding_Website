from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# 1. Base Schema (Fields shared across create and response)
class JobBase(BaseModel):
    company: str
    role: str
    location: Optional[str] = "Remote"
    salary: Optional[str] = None
    status: Optional[str] = "Applied"
    job_url: Optional[str] = None
    notes: Optional[str] = None

# 2. Schema for CREATING a job (inherits everything from JobBase)
class JobCreate(JobBase):
    pass

# 3. Schema for UPDATING a job (everything is optional)
class JobUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    status: Optional[str] = None
    job_url: Optional[str] = None
    notes: Optional[str] = None

# 4. Schema for RETURNING a job to the browser (includes id & date)
class JobResponse(JobBase):
    id: int
    applied_date: datetime

    model_config = ConfigDict(from_attributes=True)