from fastapi import FastAPI
from app.database import engine, Base
from app.routers import jobs

# 1. Automatically create database tables in SQLite on startup
Base.metadata.create_all(bind = engine)

# 2. Initialize the FastAPI app with title and metadata
app = FastAPI(title = "CareerPlus", description = "Job Application Tracker, Aggregator & ATS Keyword Matcher", version = "1.0.0")

# 3. Mount our Jobs CRUD router
app.include_router(jobs.router)

# 4. Root health-check endpoint
@app.get("/")
def root():
    return {"message": "CareerPluse API is up and running!  Visit /docs for interactive testing."}