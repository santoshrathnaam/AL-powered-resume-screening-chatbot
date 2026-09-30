from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class RequirementItem(BaseModel):
    skill: str
    importance: str = "important"  # "critical", "important", "preferred"
    category: Optional[str] = "technical"
    min_years: Optional[float] = 0.0
    context: Optional[str] = ""

class JobDescriptionData(BaseModel):
    id: str = "job-001"
    title: str
    raw_text: str
    summary: Optional[str] = ""
    critical_skills: List[str] = []
    important_skills: List[str] = []
    preferred_skills: List[str] = []
    requirements: List[RequirementItem] = []
    min_experience_years: float = 0.0
    required_education: str = "Bachelor's Degree in Computer Science or related field"
    responsibilities: List[str] = []
    soft_skills: List[str] = []
    location: Optional[str] = "Remote / Hybrid"
    custom_weights: Optional[Dict[str, float]] = None

class CandidateSkillMatch(BaseModel):
    skill: str
    importance: str = "important"  # "critical", "important", "preferred"
    match_level: str = "Missing"   # "Strong", "Partial", "Weak", "Missing"
    match_type: str = "none"       # "exact", "semantic", "transferable", "none"
    score: float = 0.0             # 0 - 100
    confidence: float = 85.0       # 0 - 100%
    evidence_snippet: str = "No direct evidence found in resume"
    evidence_source: str = ""      # "Projects", "Work Experience", "Certifications", etc.
    transferable_from: Optional[str] = None
    note: Optional[str] = ""

class ClaimVerification(BaseModel):
    claim: str
    evidence_found: str
    professional_usage_demonstrated: bool = True
    confidence: str = "High"       # "High", "Moderate", "Low"
    status: str = "Verified"       # "Verified", "Insufficient evidence", "Requires interview verification"
    recommendation: str

class ConsistencyRisk(BaseModel):
    type: str                      # "employment_overlap", "vague_description", "unsupported_claim", "date_gap"
    severity: str = "Low"          # "Low", "Medium", "High"
    title: str
    description: str
    recommendation: str

class ScoreBreakdown(BaseModel):
    technical_skills: float = 0.0
    experience: float = 0.0
    projects: float = 0.0
    required_skills: float = 0.0
    education: float = 0.0
    preferred_skills: float = 0.0
    achievements: float = 0.0
    total: float = 0.0
    weights_used: Dict[str, float] = {}

class InterviewQuestion(BaseModel):
    id: str
    category: str                  # "Technical", "Resume Verification", "JD-Specific", "Project", "Behavioral", "Claim Verification"
    priority: str = "Medium"       # "High", "Medium", "Low"
    question: str
    context_reason: str
    suggested_evaluation: str

class InterviewReadiness(BaseModel):
    overall_readiness: str = "High"  # "High", "Moderate", "Low"
    overall_score: float = 85.0
    technical_strength: float = 85.0
    experience_fit: float = 80.0
    project_relevance: float = 90.0
    evidence_confidence: float = 88.0
    risk_level: str = "Low"          # "Low", "Moderate", "High"
    explanation: str = ""

class ExperienceItem(BaseModel):
    role: str
    company: str
    duration: str
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    years: float = 0.0
    description: str
    technologies: List[str] = []

class EducationItem(BaseModel):
    degree: str
    institution: str
    year: str
    grade: Optional[str] = ""

class ProjectItem(BaseModel):
    title: str
    description: str
    technologies: List[str] = []
    link: Optional[str] = ""

class CandidateProfile(BaseModel):
    candidate_id: str             # e.g., "Candidate #07"
    internal_id: str              # UUID
    anonymized_id: str            # "CAND-007"
    raw_name: str                 # Hidden during bias-free evaluation
    email: Optional[str] = None
    phone: Optional[str] = None
    total_experience_years: float = 0.0
    education: List[EducationItem] = []
    experience: List[ExperienceItem] = []
    projects: List[ProjectItem] = []
    technical_skills: List[str] = []
    soft_skills: List[str] = []
    certifications: List[str] = []
    achievements: List[str] = []
    raw_text: Optional[str] = ""

class CandidateEvaluation(BaseModel):
    candidate_id: str             # "Candidate #07"
    anonymized_id: str            # "CAND-007"
    rank: int
    previous_rank: Optional[int] = None
    overall_score: float          # 0 - 100
    previous_score: Optional[float] = None
    category: str                 # "Strong Fit", "Potential Fit", "Skill Gap", "Not Suitable"
    score_breakdown: ScoreBreakdown
    skill_matches: List[CandidateSkillMatch] = []
    strengths: List[str] = []
    weaknesses: List[str] = []
    missing_skills: List[str] = []
    transferable_skills: List[str] = []
    claims: List[ClaimVerification] = []
    risks: List[ConsistencyRisk] = []
    why_this_candidate: List[str] = []
    why_not_higher: List[str] = []
    interview_readiness: InterviewReadiness
    interview_questions: List[InterviewQuestion] = []
    rank_change_reason: Optional[str] = ""
    profile: Optional[CandidateProfile] = None

class ScreeningDashboardResponse(BaseModel):
    job: JobDescriptionData
    total_resumes: int
    top_10: List[CandidateEvaluation]
    all_candidates: List[CandidateEvaluation]
    statistics: Dict[str, Any]
    weights: Dict[str, float]
    version: int = 1
    ranking_history_notes: List[str] = []

class WhatIfRequest(BaseModel):
    weights: Optional[Dict[str, float]] = None
    requirement_importances: Optional[Dict[str, str]] = None  # { "AWS": "critical", "Java": "critical" }

class ComparisonRequest(BaseModel):
    candidate_ids: List[str]

class ComparisonMatrixItem(BaseModel):
    criteria: str
    category: str  # "skill", "experience", "education", "overall"
    scores: Dict[str, Any]  # { "Candidate #07": "Strong (3 projects)", "Candidate #14": "Partial" }
    highest_candidate: Optional[str] = None
    notes: Optional[str] = None

class CandidateComparisonResponse(BaseModel):
    candidates: List[CandidateEvaluation]
    matrix: List[ComparisonMatrixItem]
    summary: str
    key_differentiators: List[str]

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    response: str
    suggested_followups: List[str] = []
    relevant_candidates: List[str] = []
    applied_filters: Optional[Dict[str, Any]] = None
