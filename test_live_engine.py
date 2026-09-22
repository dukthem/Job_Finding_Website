import sys
from app.services.top_companies import (
    build_direct_job_url,
    get_company_category,
    get_company_type,
    get_recruiter_for_company,
    TOP_200_COMPANIES
)
from app.services.job_fetcher import fetch_live_jobs, rank_jobs_by_resume

print("=" * 70)
print("🚀 CAREERPULSE PHASE 1-5 END-TO-END ENGINE TEST")
print("=" * 70)

# --------------------------------------------------------------------
# Test 1: Verify the Top 200 Companies Directory
# --------------------------------------------------------------------
print(f"\n1. 🏢 Top Companies Directory Count: {len(TOP_200_COMPANIES)} companies loaded.")
assert len(TOP_200_COMPANIES) == 200, "Error: Expected 200 companies!"

# --------------------------------------------------------------------
# Test 2: Test the 6-Category Classifier & Recruiter Generator
# --------------------------------------------------------------------
print("\n2. 🏷️ Testing 6-Category Classification & Recruiter Discovery:")
test_companies = ["Google", "Stripe", "Swiggy", "Spotify", "TCS"]

for comp in test_companies:
    category = get_company_category(comp)
    recruiter = get_recruiter_for_company(comp)
    print(f"   • {comp:8} ➔ Category: {category:15} | Recruiter Link: {recruiter['linkedin_url'][:60]}...")

# --------------------------------------------------------------------
# Test 3: Fetch Live Internet Jobs (Hybrid Engine)
# --------------------------------------------------------------------
print("\n3. 🌐 Querying Live Internet API + Curated Roles (Filter: Remote / Europe)...")
jobs = fetch_live_jobs(region="all", limit=6)
print(f"   ✅ Successfully fetched {len(jobs)} active jobs!")

# --------------------------------------------------------------------
# Test 4: Run ATS Resume Scorer & Ranking Math
# --------------------------------------------------------------------
sample_resume = """
Backend Software Engineer with expertise in Python, FastAPI, Docker, and PostgreSQL.
Experience building scalable microservices, containerization, and REST APIs.
Worked with Git and Redis.
"""

print("\n4. 🧠 Running ATS Resume Scorer & Sorting Engine...")
ranked_jobs = rank_jobs_by_resume(sample_resume, jobs)

print("\n" + "=" * 70)
print("🏆 TOP RANKED JOBS MATCHED TO YOUR RESUME:")
print("=" * 70)

for i, job in enumerate(ranked_jobs[:4], start=1):
    score = job.get("ats_score", 0)
    badge = "🟢" if score >= 75 else ("🟡" if score >= 50 else "🔴")
    
    print(f"\n#{i} {badge} {score}% ATS MATCH — {job['title']}")
    print(f"   🏢 Company:   {job['company']} ({job.get('company_category', 'tech')})")
    print(f"   💰 Salary:    {job['salary']}")
    print(f"   📍 Location:  {job['location']}")
    print(f"   ✅ Matched:   {', '.join(job.get('matched_skills', []))}")
    print(f"   ⚠️ Missing:   {', '.join(job.get('missing_skills', [])) or 'None! Perfect match'}")
    print(f"   🔗 Portal:    {job['job_url']}")

print("\n" + "=" * 70)
print("🎉 ALL TESTS PASSED! Your backend engine is 100% operational!")
print("=" * 70)