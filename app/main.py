from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import engine, Base
from app.routers import jobs

# 1. Automatically create database tables in SQLite on startup
Base.metadata.create_all(bind = engine)

# 2. Initialize the FastAPI app with title and metadata
app = FastAPI(title = "CareerPlus", description = "Job Application Tracker, Aggregator & ATS Keyword Matcher", version = "1.0.0")

# 3. Mount the static folder (makes /static/js/app.js accessible to the browser)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 4. Tell Jinja2 where our HTML templates live
templates = Jinja2Templates(directory="app/templates")

# 5. Mount our Jobs CRUD router
app.include_router(jobs.router)

# 6. Root health-check endpoint
@app.get("/")
def home_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
    # return templates.TemplateResponse("index.html", {"request": request})
# def root():
#     return {"message": "CareerPluse API is up and running!  Visit /docs for interactive testing."}