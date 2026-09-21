import re
from typing import Dict, Set, List, Tuple
import io
import pypdf
from docx import Document

# ====================================================================
# 1. Tech Skills Taxonomy (Categorized Dictionary of Modern Tech)
# ====================================================================
TECH_SKILLS_TAXONOMY: Dict[str, List[str]] = {
    "languages": [
        "python", "javascript", "typescript", "java", "c++", "c#", "go",
        "rust", "ruby", "php", "swift", "kotlin", "scala", "sql", "dart"
    ],
    "frontend": [
        "react", "vue", "angular", "next.js", "svelte", "html", "html5",
        "css", "css3", "tailwind", "bootstrap", "sass", "redux"
    ],
    "backend": [
        "fastapi", "django", "flask", "node.js", "express", "spring boot",
        "ruby on rails", "asp.net", "graphql", "rest api", "grpc", "microservices"
    ],
    "databases": [
        "postgresql", "mysql", "sqlite", "mongodb", "redis", "elasticsearch",
        "cassandra", "dynamodb", "firebase", "supabase", "mariadb", "neo4j"
    ],
    "cloud_devops": [
        "docker", "kubernetes", "aws", "gcp", "azure", "git", "github",
        "gitlab", "ci/cd", "terraform", "ansible", "linux", "nginx"
    ],
    "ai_data": [
        "machine learning", "deep learning", "artificial intelligence",
        "generative ai", "pytorch", "tensorflow", "pandas", "numpy", 
        "scikit-learn", "data science", "llm", "nlp"
    ]
}

# ====================================================================
# 2. Skill Aliases (Normalizes different spellings to 1 standard name)
# ====================================================================
SKILL_ALIASES: Dict[str, str] = {
    # Languages
    "golang": "Go",
    "js": "JavaScript",
    "ts": "TypeScript",
    "py": "Python",
    "cpp": "C++",
    
    # Frontend
    "reactjs": "React",
    "react.js": "React",
    "vuejs": "Vue",
    "vue.js": "Vue",
    "nextjs": "Next.js",
    "tailwind css": "Tailwind",
    "tailwindcss": "Tailwind",
    
    # Backend
    "nodejs": "Node.js",
    "node": "Node.js",
    "restful api": "REST API",
    "restful apis": "REST API",
    "rest apis": "REST API",
    
    # Cloud & DevOps
    "k8s": "Kubernetes",
    "amazon web services": "AWS",
    "google cloud": "GCP",
    "google cloud platform": "GCP",
    "ci cd": "CI/CD",
    "cicd": "CI/CD",
    
    # Databases
    "postgres": "PostgreSQL",
    "mongo": "MongoDB",

    # AI & Machine Learning Shortcuts
    "ai": "Artificial Intelligence",
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "ai/ml": "Machine Learning",
    "genai": "Generative AI",
    "gen ai": "Generative AI",
    "artificial intelligence": "Artificial Intelligence"
}

# ====================================================================
# 3. Canonical Display Names (Cleanly formatted titles for the UI)
# ====================================================================
CANONICAL_SKILL_NAMES: Dict[str, str] = {
    "python": "Python", "javascript": "JavaScript", "typescript": "TypeScript",
    "java": "Java", "c++": "C++", "c#": "C#", "go": "Go", "rust": "Rust",
    "sql": "SQL", "react": "React", "vue": "Vue", "angular": "Angular",
    "next.js": "Next.js", "tailwind": "Tailwind", "fastapi": "FastAPI",
    "django": "Django", "flask": "Flask", "node.js": "Node.js",
    "rest api": "REST API", "graphql": "GraphQL", "docker": "Docker",
    "kubernetes": "Kubernetes", "aws": "AWS", "gcp": "GCP", "azure": "Azure",
    "git": "Git", "ci/cd": "CI/CD", "linux": "Linux", "postgresql": "PostgreSQL",
    "mysql": "MySQL", "sqlite": "SQLite", "mongodb": "MongoDB",
    "redis": "Redis", "machine learning": "Machine Learning",
    "pytorch": "PyTorch", "tensorflow": "TensorFlow", "pandas": "Pandas",
    "llm": "LLM", "deep learning": "Deep Learning", "artificial intelligence": "Artificial Intelligence",
    "generative ai": "Generative AI", "ai": "Artificial Intelligence", "ml": "Machine Learning",
    "dl": "Deep Learning"
}

# ====================================================================
# 4. Document Text Extraction Engine (PDF & DOCX Parsers)
# ====================================================================

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts raw text from a PDF file in-memory using pypdf.
    """
    text_chunks: List[str] = []
    try:
        pdf_stream = io.BytesIO(file_bytes)
        reader = pypdf.PdfReader(pdf_stream)
        
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)
                
        return "\n".join(text_chunks)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""


def extract_text_from_docx(file_bytes: bytes) -> str:
    """
    Extracts raw text from a Word (.docx) file in-memory.
    Scans both normal paragraphs AND tables!
    """
    text_chunks: List[str] = []
    try:
        docx_stream = io.BytesIO(file_bytes)
        doc = Document(docx_stream)
        
        # 1. Read normal paragraphs
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_chunks.append(paragraph.text.strip())
                
        # 2. Read text inside tables (resumes often use tables for skills!)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        text_chunks.append(cell.text.strip())
                        
        return "\n".join(text_chunks)
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return ""


def extract_text_from_file(filename: str, file_bytes: bytes) -> str:
    """
    Universal dispatcher: automatically detects file type by extension
    and uses the appropriate parser!
    """
    lower_name = filename.lower()
    
    if lower_name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif lower_name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    elif lower_name.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
    else:
        return ""

# ====================================================================
# 5. Skill Normalization & Extraction Engine
# ====================================================================

def normalize_skill(raw_skill: str) -> str:
    """
    Normalizes any skill variation (e.g. 'k8s', 'nodejs', 'fastapi')
    into its canonical display title (e.g. 'Kubernetes', 'Node.js', 'FastAPI').
    """
    clean = raw_skill.strip().lower()
    
    # 1. Check if it's an alias (e.g., 'k8s' -> 'Kubernetes', 'ml' -> 'Machine Learning')
    if clean in SKILL_ALIASES:
        return SKILL_ALIASES[clean]
        
    # 2. Check canonical display dictionary (e.g., 'fastapi' -> 'FastAPI')
    if clean in CANONICAL_SKILL_NAMES:
        return CANONICAL_SKILL_NAMES[clean]
        
    # 3. Default fallback: capitalize each word nicely
    return raw_skill.strip().title()


def extract_skills_from_text(text: str) -> Set[str]:
    """
    Scans messy text (resume or job description) using word-boundary regex
    and returns a clean, deduplicated Set of recognized technical skills.
    """
    if not text:
        return set()
        
    found_skills: Set[str] = set()
    
    # Compile a master list of all known skills to search for
    all_target_skills: Set[str] = set()
    
    # Add skills from our 6 taxonomy categories
    for category_skills in TECH_SKILLS_TAXONOMY.values():
        all_target_skills.update(category_skills)
        
    # Add all informal aliases (k8s, ml, ai, etc.)
    all_target_skills.update(SKILL_ALIASES.keys())
    
    # Scan text for each skill using word boundaries
    for skill_term in all_target_skills:
        # Escapes special characters like C++, Next.js, C#
        escaped_term = re.escape(skill_term)
        
        # Word-boundary pattern: ensures we match whole words, not substrings!
        pattern = rf"(?i)\b{escaped_term}\b"
        
        if re.search(pattern, text):
            # Normalize to canonical name and add to our Set
            canonical_name = normalize_skill(skill_term)
            found_skills.add(canonical_name)
            
    return found_skills

# ====================================================================
# 6. ATS Scoring & Skills Gap Analysis Formula
# ====================================================================

def calculate_ats_score(resume_text: str, job_description: str) -> Dict:
    """
    Compares a candidate's resume against a job description.
    Calculates:
      - Match Score (0 to 100%)
      - Matched Skills (intersection)
      - Missing Skills (gap)
      - Actionable recommendation for the applicant
    """
    # 1. Extract skills from both texts
    resume_skills: Set[str] = extract_skills_from_text(resume_text)
    job_skills: Set[str] = extract_skills_from_text(job_description)
    
    # Edge Case: If the job description lists zero technical skills
    if not job_skills:
        score = 80 if resume_skills else 50
        return {
            "score": score,
            "matched_skills": sorted(list(resume_skills)),
            "missing_skills": [],
            "resume_skills": sorted(list(resume_skills)),
            "job_skills": [],
            "recommendation": "The job description does not specify exact technical keywords. Ensure your resume highlights your strongest projects."
        }
        
    # 2. Set Theory Math: Intersection and Difference
    matched_skills: Set[str] = resume_skills.intersection(job_skills)
    missing_skills: Set[str] = job_skills.difference(resume_skills)
    
    # 3. Calculate percentage (capped at 100%)
    match_ratio = len(matched_skills) / len(job_skills)
    score = min(100, round(match_ratio * 100))
    
    # 4. Generate intelligent, actionable recommendations
    if score >= 80:
        recommendation = "🌟 Outstanding ATS Match! Your resume contains almost all required technical keywords."
    elif score >= 50:
        recommendation = f"⚠️ Moderate Match. Consider adding missing keywords like: {', '.join(sorted(list(missing_skills))[:3])}."
    else:
        recommendation = f"❌ Low ATS Match. Critical keywords missing from your resume: {', '.join(sorted(list(missing_skills))[:4])}."
        
    return {
        "score": score,
        "matched_skills": sorted(list(matched_skills)),
        "missing_skills": sorted(list(missing_skills)),
        "resume_skills": sorted(list(resume_skills)),
        "job_skills": sorted(list(job_skills)),
        "recommendation": recommendation
    }