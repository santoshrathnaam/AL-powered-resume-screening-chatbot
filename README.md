# TalentLens AI — Explainable AI Recruitment Assistant
### Evidence-Based Resume Screening, Candidate Ranking & Interview Intelligence

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141+-green.svg)
![React](https://img.shields.io/badge/React-18+-61dafb.svg)
![Vite](https://img.shields.io/badge/Vite-5+-yellow.svg)

---

## 📌 Executive Summary
**TalentLens AI** is an explainable AI recruitment and screening platform engineered for hiring teams to screen batches of 15–20+ resumes against specific Job Descriptions (JDs), rank the Top 10 candidates, provide transparent evidence-based scoring, identify skill gaps and resume risks, run interactive What-If hiring simulations, and generate personalized interview questions with interview-readiness assessments.

Unlike black-box keyword matchers, **TalentLens AI provides verifiable citations from the resume for every score calculation**, respects protected demographics through **bias-aware screening**, and allows HR to interactively simulate hiring priorities.

---

## 🚀 Key Differentiators & Capabilities

1. **Explainable AI & Evidence Extraction**:
   - Every score is traceable back to quoted snippets in the candidate's projects, experience, or certifications.
   - Transparent score breakdown (Technical Skills 35%, Experience 20%, Projects 15%, Critical Requirements 10%, Education 10%, Preferred/Cloud 5%, Achievements 5%).
2. **Semantic Skill Matching & Transferable Skill Detection**:
   - Goes beyond exact keyword matching (e.g., PostgreSQL/MySQL → SQL; FastAPI/Flask → REST APIs; GCP/Azure → AWS).
   - Distinguishes *Exact Match*, *Strong Semantic Match*, *Partial/Transferable Match*, *Weak Match*, and *Missing*.
3. **Bias-Aware Blind Screening**:
   - Redacts names, gender, photo, age, and address during technical qualification scoring.
   - Uses anonymized candidate IDs (e.g. `Candidate #07` / `CAND-007`) to eliminate demographic bias.
4. **What-If Hiring Simulator**:
   - HR can adjust criteria weights and requirement importance (e.g. promoting AWS from Preferred to Critical).
   - Dynamic live recalculation displaying *Previous Rank → New Rank*, *Score Deltas*, and explicit reasons for ranking shifts.
5. **Resume Consistency & Risk Detector**:
   - Identifies overlapping concurrent employment dates, multi-year timeline gaps, and vague project descriptions.
6. **Claim vs. Evidence Verification**:
   - Flags exaggerated claims (e.g., "Expert in AWS" when only an entry-level certificate is listed without hands-on production deployments).
7. **AI Recruiter Conversational Copilot**:
   - Natural language assistant grounded solely on verified candidate data (no hallucinations).
   - Answers inquiries like: *"Why is Candidate #07 ranked first?"*, *"Compare Candidate #07 and #14"*, *"Show candidates missing AWS"*, or natural language filters like *"Candidates with >= 2 years experience"*.
8. **Interview Readiness Assessment & Question Generator**:
   - Generates prioritized questions categorized into: *Technical*, *Resume Verification*, *JD-Specific*, *Project*, *Behavioral*, and *Claim Verification*.
   - Assigns priority badges (*High*, *Medium*, *Low*) and scoring evaluation criteria.

---

## 🏗️ Architecture & Project Structure

```
Ai powered resume chatbot/
├── backend/
│   ├── main.py                  # FastAPI application entry point & API endpoints
│   ├── config.py                # App configuration, weights, and directory paths
│   ├── models/
│   │   └── schemas.py           # Pydantic data schemas & contracts
│   ├── parsers/
│   │   ├── jd_parser.py         # Job description parser & requirement classifier
│   │   └── resume_parser.py     # PDF/DOCX/TXT resume parser with bias anonymization
│   ├── ai/
│   │   ├── semantic_matcher.py  # Semantic matching & transferable skill graph
│   │   ├── scoring_engine.py    # Multi-component explainable scoring engine
│   │   ├── claim_verifier.py    # Resume claim vs. evidence verification
│   │   ├── risk_detector.py     # Consistency, date overlap & gap detection
│   │   ├── explainer.py         # Why this candidate & Why not higher rationale
│   │   ├── interview_gen.py     # Interview questions & readiness scoring
│   │   └── chatbot.py           # Conversational HR recruiter engine
│   ├── services/
│   │   └── screening_service.py # Orchestrates end-to-end screening pipeline
│   └── data/
│       ├── demo_jd.py           # Benchmark Software Engineer Job Description
│       ├── demo_candidates.py   # 20 realistic benchmark candidate profiles
│       ├── generate_samples.py  # Script generating sample resume TXT files
│       └── sample_files/        # 20 ready-to-test resume files + sample JD
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx               # Navigation bar & blind screening toggle
│   │   │   ├── DisclaimerBanner.jsx     # HR decision-support disclaimer banner
│   │   │   ├── WhatIfModal.jsx          # Interactive hiring simulation modal
│   │   │   ├── ComparisonModal.jsx      # Side-by-side candidate comparison matrix
│   │   │   ├── JobUploadModal.jsx       # JD upload & paste text modal
│   │   │   └── ResumeUploadModal.jsx    # Batch 15-20 resume upload modal
│   │   ├── pages/
│   │   │   ├── DashboardPage.jsx        # Page 1: JD summary, stats, Top 10, table
│   │   │   ├── CandidateDetailPage.jsx  # Page 2: In-depth candidate intelligence
│   │   │   └── AiRecruiterPage.jsx      # Page 3: Conversational HR chatbot
│   │   ├── App.jsx                      # App root router & state manager
│   │   └── index.css                    # Design system (glassmorphism & dark mode)
│   ├── dist/                            # Production bundle served by FastAPI
│   └── package.json
├── run.ps1                      # 1-Click PowerShell launcher
├── run.bat                      # 1-Click Windows batch launcher
└── README.md
```

---

## 💻 Quick Start & Running Locally

### Prerequisites
- Python 3.10+
- Node.js 18+ (already bundled in production build in `frontend/dist/`)

### 1-Click Launch (Recommended)
Run the PowerShell script:
```powershell
.\run.ps1
```
Or execute the batch file:
```cmd
run.bat
```
The server will start at:
👉 **http://127.0.0.1:8000**

---

## 🎯 Step-by-Step Demonstration Scenario

For your college major project review, hackathon demo, or technical interview:

1. **Explore the HR Dashboard (Page 1)**:
   - Notice the **Software Engineer** JD with extracted **Critical Requirements** (Java, Data Structures, Spring Boot), **Important Skills** (SQL, REST APIs), and **Preferred** (AWS, Docker).
   - Review the **Statistics Cards** (20 Resumes analyzed, Strong Fit: 7, Potential Fit: 8, Skill Gap: 3, Not Suitable: 2).
   - Inspect the **Top 10 Leaderboard**: Candidate #07 is ranked **#1 (94.4%)** and Candidate #14 is **#2 (92.2%)**.

2. **Inspect Candidate Intelligence (Page 2)**:
   - Click on **Candidate #07**:
     - *Skill Match & Evidence*: Strong Java, Spring Boot, SQL, REST APIs with verbatim project citations. Partial AWS (Certification only, no production exposure). Missing Docker.
     - *Explainability*: Read *"Why Rank #1?"* and the detailed score breakdown.
     - *Claim Verification*: Notice the flag on AWS certification requiring interview verification.
     - *Interview Readiness*: High readiness, evidence confidence, and customized high-priority interview questions.

3. **Run What-If Hiring Simulation (Prompt Section 47)**:
   - Click **What-If Simulator** in the navbar.
   - Switch **AWS (Cloud)** from `PREFERRED` to `CRITICAL` (or select the *Cloud First* preset).
   - Click **Simulate & Recalculate Rankings**:
     - **Candidate #14 moves from #2 → #1 (96.7%)!**
     - **Candidate #07 drops from #1 → #2 (89.5%)!**
     - Reason displayed: *"Candidate #14 has stronger professional AWS experience (3 yrs enterprise cloud) and AWS was given higher importance."*

4. **Chat with AI Recruiter (Page 3)**:
   - Switch to the **AI Recruiter** tab.
   - Click the prompt: *"Why is Candidate #07 ranked first?"* → Receive an evidence-backed rationale.
   - Ask: *"Compare Candidate #07 and Candidate #14"* → Receive a side-by-side comparison matrix with differentiators.
   - Ask: *"Who has the strongest Java experience?"* or *"Which candidates are missing AWS?"*.
   - Ask: *"Generate interview questions for Candidate #14"*.

5. **Test Custom Uploads**:
   - Click **Batch Resume Upload** and select files from `backend/data/sample_files/` to see real-time parsing and screening of fresh resumes!

---

## ⚖️ Ethical AI & HR Disclaimer
> **Important:** TalentLens AI provides algorithmic decision-support recommendations. In adherence to employment regulations and responsible AI ethics, AI assessments must never serve as the sole determinant for employment decisions. Human recruiters retain ultimate oversight.
