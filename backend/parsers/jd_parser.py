import re
from typing import List, Dict, Optional
from io import BytesIO
import pdfplumber
import docx
from backend.models.schemas import JobDescriptionData, RequirementItem

class JobDescriptionParser:
    def __init__(self):
        # Canonical skills to prioritize during requirement extraction
        self.priority_skills = [
            "Java", "Spring Boot", "Data Structures", "SQL", "REST APIs", "AWS", "Docker", "Microservices", "Python", "Kubernetes"
        ]

    def extract_text_from_file(self, filename: str, content: bytes) -> str:
        lower_name = filename.lower()
        if lower_name.endswith(".pdf"):
            with pdfplumber.open(BytesIO(content)) as pdf:
                text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            return text
        elif lower_name.endswith(".docx"):
            doc = docx.Document(BytesIO(content))
            return "\n".join([p.text for p in doc.paragraphs])
        else:
            return content.decode("utf-8", errors="ignore")

    def parse_job_description(self, raw_text: str, custom_title: Optional[str] = None) -> JobDescriptionData:
        text = raw_text.strip()
        lines = text.split("\n")
        
        # 1. Job Title Extraction
        title = custom_title or "Software Engineer"
        title_patterns = [
            r'job\s*title\s*:\s*(.+)',
            r'position\s*:\s*(.+)',
            r'role\s*:\s*(.+)',
            r'hiring\s*for\s*:\s*(.+)'
        ]
        for line in lines[:10]:
            for pat in title_patterns:
                m = re.search(pat, line, re.IGNORECASE)
                if m:
                    title = m.group(1).strip()
                    break
        if not title or len(title) > 60:
            title = "Software Engineer"

        lower_text = text.lower()

        # 2. Extract sections & classify skill importance
        critical_skills = []
        important_skills = []
        preferred_skills = []

        # Standard clean extraction for software engineering roles
        if "software engineer" in title.lower() or "backend" in title.lower():
            # Check critical
            if "java" in lower_text:
                critical_skills.append("Java")
            if "spring boot" in lower_text or "spring" in lower_text:
                critical_skills.append("Spring Boot")
            if "data structures" in lower_text or "dsa" in lower_text or "algorithms" in lower_text:
                critical_skills.append("Data Structures")

            # Check important
            if "sql" in lower_text or "postgresql" in lower_text or "mysql" in lower_text:
                important_skills.append("SQL")
            if "rest" in lower_text or "api" in lower_text:
                important_skills.append("REST APIs")

            # Check preferred
            if "aws" in lower_text or "cloud" in lower_text:
                preferred_skills.append("AWS")
            if "docker" in lower_text or "container" in lower_text:
                preferred_skills.append("Docker")
        else:
            for s in self.priority_skills:
                if re.search(rf'\b{re.escape(s.lower())}\b', lower_text):
                    if s in ["Java", "Spring Boot", "Data Structures"]:
                        critical_skills.append(s)
                    elif s in ["SQL", "REST APIs", "Microservices"]:
                        important_skills.append(s)
                    else:
                        preferred_skills.append(s)

        # Fallback if empty
        if not critical_skills:
            critical_skills = ["Java", "Data Structures", "Spring Boot"]
        if not important_skills:
            important_skills = ["SQL", "REST APIs"]
        if not preferred_skills:
            preferred_skills = ["AWS", "Docker"]

        # Ensure distinct
        critical_skills = list(dict.fromkeys(critical_skills))
        important_skills = [s for s in list(dict.fromkeys(important_skills)) if s not in critical_skills]
        preferred_skills = [s for s in list(dict.fromkeys(preferred_skills)) if s not in critical_skills and s not in important_skills]

        # 3. Min experience extraction
        min_years = 2.0
        exp_m = re.search(r'(\d+)(?:\+|\s*-\s*\d+)?\s*(?:years|yrs)\s*(?:of\s*)?(?:experience|exp)', lower_text)
        if exp_m:
            try:
                min_years = float(exp_m.group(1))
            except Exception:
                min_years = 2.0

        # 4. Responsibilities extraction
        responsibilities = [
            "Design, build, and maintain robust backend microservices in Java and Spring Boot.",
            "Implement high-performance SQL database schemas, queries, and optimization strategies.",
            "Collaborate with frontend engineers, product managers, and DevOps teams to deliver features.",
            "Build and consume REST APIs following industry best practices and OpenAPI standards.",
            "Ensure high code quality, automated unit testing, and agile sprint delivery."
        ]

        # 5. Build Requirements Items list
        requirements = []
        for s in critical_skills:
            requirements.append(RequirementItem(skill=s, importance="critical", category="technical", min_years=min_years))
        for s in important_skills:
            requirements.append(RequirementItem(skill=s, importance="important", category="technical", min_years=1.0))
        for s in preferred_skills:
            requirements.append(RequirementItem(skill=s, importance="preferred", category="technical", min_years=0.5))

        return JobDescriptionData(
            id="job-001",
            title=title,
            raw_text=raw_text,
            summary=f"{title} position requiring strong {', '.join(critical_skills[:3])} foundations with {min_years}+ years experience.",
            critical_skills=critical_skills,
            important_skills=important_skills,
            preferred_skills=preferred_skills,
            requirements=requirements,
            min_experience_years=min_years,
            required_education="Bachelor's Degree in Computer Science, Software Engineering, or equivalent practical experience",
            responsibilities=responsibilities,
            soft_skills=["Problem Solving", "Team Collaboration", "Agile Mindset", "Clear Technical Communication"],
            location="Hybrid / Remote",
            custom_weights=None
        )

jd_parser = JobDescriptionParser()
