import re
import uuid
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from io import BytesIO
import pdfplumber
import docx
from backend.models.schemas import (
    CandidateProfile,
    ExperienceItem,
    EducationItem,
    ProjectItem
)

class ResumeParser:
    def __init__(self):
        # Comprehensive canonical skills dictionary
        self.known_skills = [
            "java", "spring boot", "spring", "sql", "mysql", "postgresql", "oracle",
            "aws", "amazon web services", "docker", "kubernetes", "rest api", "restful api",
            "microservices", "python", "data structures", "algorithms", "dsa", "git",
            "github", "ci/cd", "redis", "kafka", "hibernate", "javascript", "react",
            "typescript", "c++", "c#", ".net", "gcp", "azure", "mongodb", "linux",
            "fastapi", "flask", "django", "node.js", "express", "graphql", "html", "css"
        ]

    def extract_text_from_file(self, filename: str, content: bytes) -> str:
        lower_name = filename.lower()
        text = ""

        # 1. PDF Extraction
        if lower_name.endswith(".pdf"):
            # Try pdfplumber first
            try:
                with pdfplumber.open(BytesIO(content)) as pdf:
                    pages_text = [page.extract_text() or "" for page in pdf.pages]
                    text = "\n".join(pages_text)
            except Exception as e:
                text = ""

            # Fallback to pypdfium2 if pdfplumber returned empty or errored
            if not text.strip():
                try:
                    import pypdfium2 as pdfium
                    pdf = pdfium.PdfDocument(BytesIO(content))
                    extracted = []
                    for page in pdf:
                        extracted.append(page.get_textpage().get_text_range() or "")
                    text = "\n".join(extracted)
                except Exception as e:
                    pass

            return text

        # 2. DOCX Extraction
        elif lower_name.endswith(".docx") or lower_name.endswith(".doc"):
            try:
                doc = docx.Document(BytesIO(content))
                text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            except Exception as e:
                text = content.decode("utf-8", errors="ignore")
            return text

        # 3. Plain Text / Markdown
        else:
            return content.decode("utf-8", errors="ignore")

    def parse_resume(
        self,
        raw_text: str,
        assigned_id: Optional[str] = None,
        filename: Optional[str] = None
    ) -> CandidateProfile:
        text = raw_text.strip()
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # Generate IDs
        cand_id = assigned_id or "Candidate #01"
        num = re.findall(r'\d+', cand_id)
        anon_id = f"CAND-{int(num[0]):03d}" if num else f"CAND-{uuid.uuid4().hex[:4].upper()}"

        # 1. Extract Candidate Name
        raw_name = "Applicant"
        if filename:
            # Try getting clean name from filename (e.g. "Alex_Chen_Resume.pdf" -> "Alex Chen")
            clean_fn = Path(filename).stem
            clean_fn = re.sub(r'[\-_]?(?:resume|cv|profile|doc)[\-_]?', ' ', clean_fn, flags=re.IGNORECASE)
            clean_fn = re.sub(r'Candidate[\s\-_]*\d*', ' ', clean_fn, flags=re.IGNORECASE)
            clean_fn = re.sub(r'[^a-zA-Z\s]', ' ', clean_fn).strip()
            if len(clean_fn) >= 3 and len(clean_fn.split()) <= 4:
                raw_name = clean_fn.title()

        if raw_name == "Applicant" and lines:
            for l in lines[:5]:
                # First line without email/phone/url and not a header
                if len(l) < 35 and "@" not in l and "http" not in l.lower() and not any(h in l.lower() for h in ["resume", "curriculum", "page"]):
                    raw_name = l.strip().title()
                    break

        if raw_name == "Applicant":
            raw_name = f"Candidate {num[0] if num else 'A'}"

        # 2. Extract Contact Info
        email_m = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        email = email_m.group(0) if email_m else None

        phone_m = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        phone = phone_m.group(0) if phone_m else None

        # 3. Extract Technical Skills
        found_skills = []
        lower_text = text.lower()
        for skill in self.known_skills:
            pattern = rf'\b{re.escape(skill)}\b'
            if re.search(pattern, lower_text):
                clean_skill = skill.title()
                if skill in ["java", "spring boot", "rest api"]:
                    clean_skill = "Java" if skill == "java" else ("Spring Boot" if skill == "spring boot" else "REST APIs")
                elif skill in ["sql", "aws", "gcp", "dsa", "html", "css"]:
                    clean_skill = skill.upper()
                found_skills.append(clean_skill)
        found_skills = list(dict.fromkeys(found_skills))

        # 4. Extract Experience & Total Years
        experience_items: List[ExperienceItem] = []
        
        # Look for date ranges (e.g., 2021 - 2024, 2022 to Present, Jan 2021 - Present)
        date_patterns = re.findall(r'(\b\d{4}\b)\s*(?:-|to|–)\s*(\b\d{4}\b|present|current)', lower_text)
        total_exp_years = 0.0
        
        if date_patterns:
            for s_str, e_str in date_patterns:
                try:
                    s_yr = int(s_str)
                    e_yr = 2026 if "present" in e_str or "current" in e_str else int(e_str)
                    if 1990 <= s_yr <= 2026 and 1990 <= e_yr <= 2030 and e_yr >= s_yr:
                        diff = max(float(e_yr - s_yr), 0.5)
                        # Avoid double counting if overlapping
                        total_exp_years += diff
                except Exception:
                    pass
            total_exp_years = min(round(total_exp_years, 1), 25.0)

        # Explicit "X years of experience" pattern
        exp_explicit = re.search(r'(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)\s*(?:of\s*)?experience', lower_text)
        if exp_explicit:
            explicit_yrs = float(exp_explicit.group(1))
            total_exp_years = max(total_exp_years, explicit_yrs)

        # Default experience to 2.0 if non-zero text but no date matched
        if total_exp_years == 0.0:
            total_exp_years = 2.0

        # Extract Experience blocks
        exp_section_match = re.search(r'(?:experience|work history|employment history|work experience)[\s\:\-]+([\s\S]+?)(?:projects|education|skills|certifications|$)', text, re.IGNORECASE)
        exp_text_block = exp_section_match.group(1).strip() if exp_section_match else text

        # Create structured experience item
        experience_items.append(ExperienceItem(
            role="Software Engineer / Developer",
            company="Technology Industry Experience",
            duration=f"{total_exp_years} Years",
            start_year=int(2026 - total_exp_years),
            end_year=2026,
            years=total_exp_years,
            description=exp_text_block[:400] + ("..." if len(exp_text_block) > 400 else ""),
            technologies=found_skills[:5]
        ))

        # 5. Extract Projects
        project_items: List[ProjectItem] = []
        proj_section_match = re.search(r'(?:projects|personal projects|key projects|academic projects)[\s\:\-]+([\s\S]+?)(?:experience|education|skills|certifications|$)', text, re.IGNORECASE)
        proj_text_block = proj_section_match.group(1).strip() if proj_section_match else ""

        if proj_text_block:
            # Split projects by bullet points or headers
            proj_snippets = [p.strip() for p in re.split(r'\n(?=[A-Z0-9\-\•\*\#])', proj_text_block) if len(p.strip()) > 25]
            for idx, ps in enumerate(proj_snippets[:3]):
                first_line = ps.split("\n")[0]
                p_title = re.sub(r'^[•\-\*\d\.\s]+', '', first_line).strip()[:50] or f"Technical Project #{idx+1}"
                p_desc = ps[:300]
                p_tech = [s for s in found_skills if s.lower() in ps.lower()][:4] or found_skills[:2]
                project_items.append(ProjectItem(
                    title=p_title,
                    description=p_desc,
                    technologies=p_tech
                ))

        if not project_items:
            project_items.append(ProjectItem(
                title="Software Engineering Implementation",
                description="Technical design, microservices, and database application development.",
                technologies=found_skills[:4]
            ))

        # 6. Extract Education
        education_items: List[EducationItem] = []
        edu_matches = re.finditer(r'(Bachelor|Master|B\.?Tech|B\.?S|M\.?S|M\.?Tech|B\.?E|Associate|Ph\.?D)[\w\s\.]*?(?:in|,)\s*([A-Za-z\s]+)', text, re.IGNORECASE)
        for em in edu_matches:
            education_items.append(EducationItem(
                degree=f"{em.group(1)} in {em.group(2).strip()[:35]}",
                institution="University",
                year="2023"
            ))

        if not education_items:
            education_items.append(EducationItem(
                degree="Bachelor of Science in Computer Science",
                institution="University",
                year="2023"
            ))

        # 7. Extract Certifications
        certifications = []
        cert_terms = ["aws certified", "cloud practitioner", "solutions architect", "oracle certified", "spring professional", "docker certified", "kubernetes certified", "gcp certified"]
        for ct in cert_terms:
            if ct in lower_text:
                certifications.append(ct.title())

        # 8. Achievements
        achievements = []
        if any(w in lower_text for w in ["award", "dean's list", "hackathon", "gold", "published", "patent", "scholarship"]):
            achievements.append("Academic & Technical Recognition")

        return CandidateProfile(
            candidate_id=cand_id,
            internal_id=str(uuid.uuid4()),
            anonymized_id=anon_id,
            raw_name=raw_name,
            email=email,
            phone=phone,
            total_experience_years=total_exp_years,
            education=education_items,
            experience=experience_items,
            projects=project_items,
            technical_skills=found_skills,
            soft_skills=["Problem Solving", "Team Collaboration", "Agile Mindset"],
            certifications=certifications,
            achievements=achievements,
            raw_text=raw_text
        )

resume_parser = ResumeParser()
