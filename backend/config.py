import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
(UPLOADS_DIR / "resumes").mkdir(exist_ok=True)
(UPLOADS_DIR / "jds").mkdir(exist_ok=True)

class Settings(BaseSettings):
    APP_NAME: str = "TalentLens AI — Explainable AI Recruitment Assistant"
    APP_SUBTITLE: str = "Evidence-Based Resume Screening, Candidate Ranking & Interview Intelligence"
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/talentlens.db"
    
    # Default component weights (percentages totaling 100%)
    DEFAULT_WEIGHTS: dict = {
        "technical_skills": 35.0,
        "experience": 20.0,
        "projects": 15.0,
        "required_skills": 10.0,
        "education": 10.0,
        "preferred_skills": 5.0,
        "achievements": 5.0
    }
    
    # Requirement importance multipliers for skill scoring
    IMPORTANCE_WEIGHTS: dict = {
        "critical": 1.5,
        "important": 1.0,
        "preferred": 0.6
    }
    
    # Bias-aware settings
    ANONYMIZE_PROFILES: bool = True
    
    # Optional LLM keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    class Config:
        env_file = ".env"

settings = Settings()
