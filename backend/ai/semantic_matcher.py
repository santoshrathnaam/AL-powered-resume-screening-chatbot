import re
from typing import Dict, List, Tuple, Optional
from backend.models.schemas import CandidateSkillMatch, ProjectItem, ExperienceItem

# Transferable skill graph & taxonomy
SKILL_TAXONOMY = {
    "java": {
        "equivalents": ["core java", "java 8", "java 11", "java 17", "java 21", "j2ee", "jvm", "java se", "java ee"],
        "transferable": ["kotlin", "scala", "c#", ".net"],
        "ecosystem": ["spring", "spring boot", "hibernate", "maven", "gradle", "jpa"],
        "category": "language"
    },
    "spring boot": {
        "equivalents": ["spring framework", "spring-boot", "spring mvc", "spring cloud", "spring security", "spring data"],
        "transferable": ["micronaut", "quarkus", "django", "express.js", "nest.js", "asp.net core", "fastapi"],
        "ecosystem": ["java", "hibernate", "rest api", "microservices"],
        "category": "framework"
    },
    "sql": {
        "equivalents": ["structured query language", "relational database", "rdbms", "ansi sql"],
        "transferable": ["postgresql", "mysql", "oracle", "sql server", "sqlite", "mariadb"],
        "ecosystem": ["database design", "indexing", "stored procedures", "query optimization", "pl/sql"],
        "category": "database"
    },
    "rest api": {
        "equivalents": ["restful api", "rest services", "restful web services", "rest endpoints", "api development", "rest apis", "restful"],
        "transferable": ["graphql", "grpc", "soap", "fastapi", "flask api", "api gateway"],
        "ecosystem": ["postman", "swagger", "openapi", "http methods", "json"],
        "category": "architecture"
    },
    "aws": {
        "equivalents": ["amazon web services", "aws cloud", "aws ec2", "aws s3", "aws lambda", "aws rds"],
        "transferable": ["google cloud platform", "gcp", "microsoft azure", "azure", "cloud computing", "cloud"],
        "ecosystem": ["ec2", "s3", "lambda", "ecs", "eks", "rds", "dynamodb", "cloudformation", "iam"],
        "category": "cloud"
    },
    "docker": {
        "equivalents": ["containerization", "docker containers", "dockerfile", "docker-compose", "containers"],
        "transferable": ["podman", "containerd", "kubernetes", "k8s"],
        "ecosystem": ["ci/cd", "microservices", "cloud"],
        "category": "devops"
    },
    "data structures": {
        "equivalents": ["dsa", "data structures and algorithms", "algorithms", "problem solving"],
        "transferable": ["competitive programming", "leetcode", "system design", "codeforces"],
        "ecosystem": ["arrays", "trees", "graphs", "dynamic programming"],
        "category": "cs_core"
    },
    "microservices": {
        "equivalents": ["microservice architecture", "distributed systems", "service-oriented architecture", "soa"],
        "transferable": ["event-driven architecture", "kafka", "rabbitmq"],
        "ecosystem": ["docker", "kubernetes", "api gateway"],
        "category": "architecture"
    },
    "git": {
        "equivalents": ["github", "gitlab", "version control", "vcs", "bitbucket"],
        "transferable": ["svn", "mercurial"],
        "ecosystem": ["git flow", "pr reviews", "ci/cd"],
        "category": "tool"
    },
    "python": {
        "equivalents": ["python 3", "python3", "cpython"],
        "transferable": ["ruby", "golang", "go"],
        "ecosystem": ["django", "fastapi", "flask", "pandas", "numpy", "scikit-learn"],
        "category": "language"
    }
}

class SemanticMatcher:
    def __init__(self):
        pass

    def normalize(self, text: str) -> str:
        if not text:
            return ""
        return re.sub(r'[^a-zA-Z0-9\s\+\#\.]', ' ', text.lower()).strip()

    def find_evidence_in_text(self, target_term: str, text_corpus: List[str]) -> Tuple[bool, str]:
        """Finds if a term occurs in text and extracts the supporting sentence or snippet."""
        clean_target = self.normalize(target_term)
        pattern = re.compile(rf'\b{re.escape(clean_target)}\b', re.IGNORECASE)
        
        for text in text_corpus:
            if not text:
                continue
            # Split by line breaks, periods, or bullets
            sentences = re.split(r'[\.\n\r;\•\-\*\t]', text)
            for sentence in sentences:
                cleaned_sent = sentence.strip()
                if len(cleaned_sent) > 8 and pattern.search(cleaned_sent):
                    # Clean snippet
                    return True, cleaned_sent[:150]
        return False, ""

    def evaluate_skill(
        self,
        skill_req: str,
        importance: str,
        resume_skills: List[str],
        experience_items: List[ExperienceItem],
        project_items: List[ProjectItem],
        certifications: List[str],
        raw_text: str = ""
    ) -> CandidateSkillMatch:
        normalized_skill = self.normalize(skill_req)
        
        # Build text corpuses
        exp_texts = [f"{e.role} at {e.company} ({e.duration}): {e.description} " + " ".join(e.technologies) for e in experience_items]
        proj_texts = [f"{p.title}: {p.description} " + " ".join(p.technologies) for p in project_items]
        cert_texts = certifications
        resume_skill_norms = [self.normalize(s) for s in resume_skills]

        # 1. Exact Match Check
        direct_in_skills = any(normalized_skill == s or normalized_skill in s.split() for s in resume_skill_norms)
        
        found_in_proj, proj_evidence = self.find_evidence_in_text(normalized_skill, proj_texts)
        found_in_exp, exp_evidence = self.find_evidence_in_text(normalized_skill, exp_texts)
        found_in_cert, cert_evidence = self.find_evidence_in_text(normalized_skill, cert_texts)

        # Look up taxonomy
        tax_entry = SKILL_TAXONOMY.get(normalized_skill, {})
        equivalents = tax_entry.get("equivalents", [])
        transferables = tax_entry.get("transferable", [])
        ecosystem = tax_entry.get("ecosystem", [])

        # Check equivalents in text
        found_equiv_proj = False
        equiv_evidence = ""
        for eq in equivalents:
            has_eq, eq_ev = self.find_evidence_in_text(eq, exp_texts + proj_texts)
            if has_eq:
                found_equiv_proj = True
                equiv_evidence = eq_ev
                break

        # Check raw text for exact or equivalent skill
        found_in_raw, raw_evidence = False, ""
        if not found_in_exp and not found_in_proj and not found_equiv_proj:
            found_in_raw, raw_evidence = self.find_evidence_in_text(normalized_skill, [raw_text])
            if not found_in_raw:
                for eq in equivalents:
                    found_in_raw, raw_evidence = self.find_evidence_in_text(eq, [raw_text])
                    if found_in_raw:
                        break

        # Check transferables
        found_trans = False
        trans_source = ""
        trans_evidence = ""
        for tr in transferables:
            has_tr, tr_ev = self.find_evidence_in_text(tr, exp_texts + proj_texts + cert_texts + [raw_text])
            if not has_tr:
                has_tr = any(tr == s for s in resume_skill_norms)
                if has_tr:
                    tr_ev = f"Listed in skills: {tr}"
            if has_tr:
                found_trans = True
                trans_source = tr
                trans_evidence = tr_ev
                break

        # Check if raw evidence shows action/work
        has_action_context = False
        if found_in_raw and raw_evidence:
            action_verbs = ["developed", "built", "engineered", "implemented", "managed", "designed", "created", "worked on", "experience with", "using", "utilized", "architected"]
            has_action_context = any(v in raw_evidence.lower() for v in action_verbs)

        # Scoring & Evidence Assignment
        if found_in_exp:
            score = 96.0
            level = "Strong"
            match_type = "exact"
            confidence = 94.0
            evidence = exp_evidence
            source = "Work Experience"
            note = f"Demonstrated in professional role with hands-on responsibilities."
        elif found_in_proj:
            score = 92.0
            level = "Strong"
            match_type = "exact"
            confidence = 90.0
            evidence = proj_evidence
            source = "Projects"
            note = f"Demonstrated in technical project implementation."
        elif found_equiv_proj:
            score = 90.0
            level = "Strong"
            match_type = "semantic"
            confidence = 88.0
            evidence = equiv_evidence
            source = "Semantic Equivalence"
            note = f"Strong semantic match via equivalent technology pattern."
        elif found_in_raw and has_action_context:
            score = 88.0
            level = "Strong"
            match_type = "exact"
            confidence = 86.0
            evidence = raw_evidence
            source = "Work Context"
            note = f"Demonstrated with active implementation verbs in resume text."
        elif direct_in_skills and found_in_cert:
            score = 70.0
            level = "Partial"
            match_type = "exact"
            confidence = 72.0
            evidence = f"Certified ({cert_evidence}); listed in skills."
            source = "Certifications"
            note = f"Certification found, but professional usage is not explicitly detailed."
        elif found_in_cert:
            score = 65.0
            level = "Partial"
            match_type = "exact"
            confidence = 68.0
            evidence = f"Certified: {cert_evidence}."
            source = "Certifications"
            note = f"Theoretical / certification grounding without verified production deployments."
        elif found_trans:
            score = 65.0
            level = "Partial"
            match_type = "transferable"
            confidence = 75.0
            evidence = f"Transferable skill verified: {trans_source.upper()} ({trans_evidence})"
            source = "Transferable Skill"
            note = f"Candidate utilizes {trans_source.title()}, which shares conceptual architecture with {skill_req}."
        elif found_in_raw:
            score = 60.0
            level = "Partial"
            match_type = "semantic"
            confidence = 65.0
            evidence = raw_evidence
            source = "Resume Text"
            note = f"Mentioned in resume context: '{raw_evidence[:60]}...'."
        elif direct_in_skills:
            score = 45.0
            level = "Weak"
            match_type = "exact"
            confidence = 50.0
            evidence = f"Keyword '{skill_req}' listed in resume skills section."
            source = "Resume Keywords"
            note = f"Mentioned in skills list without supporting implementation details."
        else:
            score = 0.0
            level = "Missing"
            match_type = "none"
            confidence = 95.0
            evidence = "No direct or transferable evidence found anywhere in the resume."
            source = "None"
            note = f"Candidate lacks documented experience with {skill_req}."

        return CandidateSkillMatch(
            skill=skill_req,
            importance=importance,
            match_level=level,
            match_type=match_type,
            score=score,
            confidence=confidence,
            evidence_snippet=evidence,
            evidence_source=source,
            transferable_from=trans_source if found_trans else None,
            note=note
        )

semantic_matcher = SemanticMatcher()
