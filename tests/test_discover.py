import io
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create a simulated test client that talks to our FastAPI app
client = TestClient(app)

# ====================================================================
# 1. Test Text-Based Job Search
# ====================================================================
def test_search_jobs_by_text():
    """Verify that search-text endpoint returns live & curated jobs."""
    payload = {
        "query": "Python",
        "category": "all",
        "region": "all"
    }
    response = client.post("/api/discover/search-text", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "jobs" in data
    assert "count" in data
    assert isinstance(data["jobs"], list)
    assert data["count"] >= 0


def test_search_jobs_with_category_filter():
    """Verify that filtering by category works as expected."""
    payload = {
        "query": "",
        "category": "Big Tech",
        "region": "all"
    }
    response = client.post("/api/discover/search-text", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "jobs" in data
    # Any returned job must belong to Big Tech
    for job in data["jobs"]:
        assert job.get("company_category") == "Big Tech"


# ====================================================================
# 2. Test Resume File Upload & ATS Scoring
# ====================================================================
def test_search_jobs_by_file_upload():
    """Verify that uploading a text resume extracts skills and ranks jobs."""
    # Simulate a resume document in RAM memory
    resume_content = b"""
    Experienced Software Engineer with 3 years of hands-on experience.
    Proficient in Python, FastAPI, Docker, PostgreSQL, and Git.
    Built microservices and scalable cloud solutions.
    """
    
    files = {
        "file": ("test_resume.txt", io.BytesIO(resume_content), "text/plain")
    }
    data = {
        "query": "",
        "category": "all",
        "region": "all"
    }
    
    response = client.post("/api/discover/search-file", files=files, data=data)
    
    assert response.status_code == 200
    res_data = response.json()
    assert "detected_skills" in res_data
    assert "jobs" in res_data
    
    # Verify our ATS engine detected key skills
    detected = res_data["detected_skills"]
    assert "Python" in detected or "FastAPI" in detected or "Docker" in detected
    
    # Verify jobs have ATS scores attached
    if len(res_data["jobs"]) > 0:
        first_job = res_data["jobs"][0]
        assert "ats_score" in first_job
        assert 0 <= first_job["ats_score"] <= 100


def test_search_file_unsupported_format():
    """Verify that uploading an invalid file format returns a 400 error."""
    fake_image = b"\x89PNG\r\n\x1a\n"
    files = {
        "file": ("malicious_file.png", io.BytesIO(fake_image), "image/png")
    }
    
    response = client.post("/api/discover/search-file", files=files)
    assert response.status_code == 400
    assert "Unsupported format" in response.json()["detail"]


# ====================================================================
# 3. Test Top 200 Companies Directory API
# ====================================================================
def test_get_top_companies_all():
    """Verify that the top-companies directory endpoint returns all employers."""
    response = client.get("/api/discover/top-companies")
    
    assert response.status_code == 200
    data = response.json()
    assert "companies" in data
    assert len(data["companies"]) >= 50
    
    # Verify company structure
    sample = data["companies"][0]
    assert "name" in sample
    assert "category" in sample


def test_get_top_companies_by_category():
    """Verify category filtering inside the top-companies endpoint."""
    response = client.get("/api/discover/top-companies?category=Fintech")
    
    assert response.status_code == 200
    data = response.json()
    assert "companies" in data
    
    for comp in data["companies"]:
        assert comp["category"].lower() == "fintech"