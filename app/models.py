from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key = True, index = True)
    company = Column(String(255), nullable = False, index = True)
    role = Column(String(255), nullable = False)
    location = Column(String(255), default = "Remote")
    salary = Column(String(100), nullable = True)
    status = Column(String(50), default = "Applied", index = True)
    job_url = Column(String(500), nullable = True)
    notes = Column(Text, nullable = True)
    applied_date = Column(DateTime, default = datetime.utcnow)