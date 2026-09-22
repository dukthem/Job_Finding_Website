from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.database import engine
from app import models
from app.routers import jobs, discover

# Initialize Database Tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CareerPulse API",
    description="Smart Job Application Tracker, ATS Engine & Live Job Discoverer",
    version="1.0.0"
)

# Mount Static Files (CSS, JS, Icons)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates Configuration
templates = Jinja2Templates(directory="app/templates")

# Register Backend Routers
app.include_router(jobs.router)
app.include_router(discover.router)

# Frontend Page Routes
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    """Renders the Application Tracker Dashboard."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"active_page": "dashboard"}
    )

@app.get("/discover", response_class=HTMLResponse)
def read_discover(request: Request):
    """Renders the Live Job Discovery & Resume Matcher Page."""
    return templates.TemplateResponse(
        request=request,
        name="discover.html",
        context={"active_page": "discover"}
    )