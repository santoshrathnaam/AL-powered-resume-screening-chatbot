from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
import os
import shutil

from backend.config import settings
from backend.models.schemas import (
    ScreeningDashboardResponse,
    CandidateEvaluation,
    WhatIfRequest,
    ComparisonRequest,
    CandidateComparisonResponse,
    ChatRequest,
    ChatResponse
)
from backend.services.screening_service import screening_service
from backend.parsers.resume_parser import resume_parser
from backend.parsers.jd_parser import jd_parser
from backend.ai.chatbot import chatbot

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_SUBTITLE,
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "subtitle": settings.APP_SUBTITLE,
        "total_candidates": len(screening_service.raw_profiles),
        "job_title": screening_service.job.title
    }

@app.get("/api/dashboard", response_model=ScreeningDashboardResponse)
def get_dashboard():
    """Retrieve full screening dashboard data including Top 10, statistics, and weights."""
    return screening_service.get_dashboard_data()

@app.get("/api/candidate/{candidate_id}", response_model=CandidateEvaluation)
def get_candidate(candidate_id: str):
    """Retrieve in-depth candidate intelligence profile, skill breakdowns, claims, risks, and questions."""
    cands = screening_service.cached_evaluations
    # Normalize lookup: strip spaces, hash symbols, dashes, case-insensitive
    clean_target = candidate_id.lower().replace(" ", "").replace("#", "").replace("-", "")
    
    cand = next(
        (c for c in cands if c.candidate_id.lower().replace(" ", "").replace("#", "").replace("-", "") == clean_target
         or c.anonymized_id.lower().replace(" ", "").replace("#", "").replace("-", "") == clean_target
         or c.candidate_id.lower() == candidate_id.lower()
         or c.anonymized_id.lower() == candidate_id.lower()),
        None
    )
    if not cand:
        raise HTTPException(status_code=404, detail=f"Candidate '{candidate_id}' not found.")
    return cand

@app.post("/api/jd/upload", response_model=ScreeningDashboardResponse)
async def upload_job_description(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    title: Optional[str] = Form(None)
):
    """Upload new Job Description as PDF/DOCX/TXT file or paste raw text."""
    jd_text = ""
    if file:
        content = await file.read()
        jd_text = jd_parser.extract_text_from_file(file.filename, content)
    elif text:
        jd_text = text
    else:
        raise HTTPException(status_code=400, detail="Must provide either a file or plain text for Job Description.")

    if not jd_text.strip():
        raise HTTPException(status_code=400, detail="Job description text is empty.")

    screening_service.set_job_description(jd_text, custom_title=title)
    return screening_service.get_dashboard_data()

@app.post("/api/resumes/upload", response_model=ScreeningDashboardResponse)
async def upload_resumes(
    files: List[UploadFile] = File(...),
    replace: bool = Form(True)
):
    """Upload 1-20+ resumes at once as PDF/DOCX/TXT files. Defaults to screening uploaded resumes as the active pool."""
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    new_profiles = []
    base_idx = 0 if replace else len(screening_service.raw_profiles)

    for idx, f in enumerate(files):
        content = await f.read()
        text = resume_parser.extract_text_from_file(f.filename, content)
        if text.strip():
            assigned_id = f"Candidate #{base_idx + idx + 1:02d}"
            profile = resume_parser.parse_resume(text, assigned_id=assigned_id, filename=f.filename)
            new_profiles.append(profile)

    if not new_profiles:
        raise HTTPException(status_code=400, detail="Could not extract readable text from uploaded resumes. Ensure files are non-empty PDF, DOCX, or TXT.")

    screening_service.add_candidates(new_profiles, replace=replace)
    return screening_service.get_dashboard_data()

@app.post("/api/what-if", response_model=ScreeningDashboardResponse)
def what_if_simulation(request: WhatIfRequest):
    """Interactive What-If hiring simulator: dynamically modify weights or requirement importances and recalculate rankings."""
    screening_service.apply_what_if(
        weights=request.weights,
        requirement_importances=request.requirement_importances
    )
    return screening_service.get_dashboard_data()

@app.post("/api/compare", response_model=CandidateComparisonResponse)
def compare_candidates_endpoint(request: ComparisonRequest):
    """Side-by-side comparison matrix for 2-5 candidate IDs."""
    if len(request.candidate_ids) < 2:
        raise HTTPException(status_code=400, detail="Select at least 2 candidates to compare.")
    return screening_service.compare_candidates(request.candidate_ids)

@app.post("/api/chat", response_model=ChatResponse)
def chat_with_recruiter(request: ChatRequest):
    """Conversational AI Recruiter with grounded candidate context and NL filters."""
    return chatbot.process_message(
        message=request.message,
        job=screening_service.job,
        candidates=screening_service.cached_evaluations,
        active_weights=screening_service.current_weights
    )

@app.post("/api/reset-demo", response_model=ScreeningDashboardResponse)
def reset_demo():
    """Reset to the 20 benchmark demo resumes and Software Engineer JD."""
    screening_service.reset_to_demo()
    return screening_service.get_dashboard_data()

# Mount frontend dist static files if exists
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
