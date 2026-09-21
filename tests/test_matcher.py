import pytest
from app.services.ats_matcher import (
    extract_skills_from_text,
    normalize_skill,
    calculate_ats_score
)

# ====================================================================
# Test 1: Verify Skill Extraction & Normalization
# ====================================================================
def test_skill_extraction_and_aliases():
    sample_resume = """
    Software Engineer with 3 years of experience.
    Proficient in Python, FastAPI, Docker, and k8s.
    Built scalable microservices and worked with PostgreSQL.
    """
    
    skills = extract_skills_from_text(sample_resume)
    
    # 1. Verify skills were detected
    assert "Python" in skills
    assert "FastAPI" in skills
    assert "Docker" in skills
    assert "PostgreSQL" in skills
    
    # 2. Verify that 'k8s' was converted to 'Kubernetes'
    assert "Kubernetes" in skills
    
    # 3. Verify normal words were NOT falsely tagged as skills
    assert "Software" not in skills
    assert "Experience" not in skills


# ====================================================================
# Test 2: Verify Modern AI/ML Shortcuts (Your Feature!)
# ====================================================================
def test_ai_ml_shortcuts():
    sample_text = "Experienced in machine learning, AI, ML, PyTorch, and GenAI."
    
    skills = extract_skills_from_text(sample_text)
    
    assert "Machine Learning" in skills
    assert "Artificial Intelligence" in skills
    assert "PyTorch" in skills
    assert "Generative AI" in skills


# ====================================================================
# Test 3: Verify the Exact Mathematical ATS Score
# ====================================================================
def test_ats_scoring_exact_math():
    job_description = """
    We are looking for a Senior Backend Engineer.
    Required Tech Stack:
    - Python
    - FastAPI
    - Docker
    - AWS
    """
    # Total job skills required = 4 (Python, FastAPI, Docker, AWS)
    
    candidate_resume = """
    Backend developer skilled in Python, FastAPI, and Git.
    """
    # Candidate matches: Python, FastAPI (2 skills)
    # Expected Score: 2 / 4 = 50%
    
    result = calculate_ats_score(
        resume_text=candidate_resume, 
        job_description=job_description
    )
    
    # Verify score is exactly 50%
    assert result["score"] == 50
    
    # Verify matched skills
    assert "Python" in result["matched_skills"]
    assert "FastAPI" in result["matched_skills"]
    
    # Verify missing skills
    assert "AWS" in result["missing_skills"]
    assert "Docker" in result["missing_skills"]


# ====================================================================
# Test 4: Verify Defensive Coding (Vague Job Description)
# ====================================================================
def test_vague_job_description_does_not_crash():
    vague_job = "Looking for a fast learner who loves problem solving and team collaboration."
    resume = "Python and Docker developer."
    
    # Must NOT crash with ZeroDivisionError!
    result = calculate_ats_score(resume_text=resume, job_description=vague_job)
    
    assert result["score"] > 0
    assert "recommendation" in result