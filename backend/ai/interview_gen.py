from typing import List
from backend.models.schemas import (
    InterviewQuestion,
    InterviewReadiness,
    CandidateProfile,
    CandidateSkillMatch,
    ClaimVerification,
    JobDescriptionData
)

class InterviewGenerator:
    def generate_questions(
        self,
        profile: CandidateProfile,
        skill_matches: List[CandidateSkillMatch],
        claims: List[ClaimVerification],
        job: JobDescriptionData
    ) -> List[InterviewQuestion]:
        questions: List[InterviewQuestion] = []
        q_id = 1

        # 1. High Priority Verification Questions (Claims & Evidence gaps)
        for claim in claims:
            if claim.status in ["Insufficient evidence", "Requires interview verification"]:
                questions.append(InterviewQuestion(
                    id=f"Q-{q_id}",
                    category="Claim Verification",
                    priority="High",
                    question=f"Regarding your claim: '{claim.claim}' — could you walk through your hands-on implementation details, architecture, and exact tools used?",
                    context_reason=claim.recommendation,
                    suggested_evaluation="Assess whether the candidate exhibits deep hands-on command or merely conceptual familiarity."
                ))
                q_id += 1

        # 2. High/Medium Priority Technical Questions (Core skills)
        strong_skills = [m for m in skill_matches if m.match_level == "Strong"]
        for match in strong_skills[:3]:
            skill_name = match.skill
            if skill_name.lower() == "java":
                questions.append(InterviewQuestion(
                    id=f"Q-{q_id}",
                    category="Technical",
                    priority="High",
                    question="How do you handle memory management, garbage collection tuning (G1/ZGC), and thread concurrency in high-throughput Java applications?",
                    context_reason=f"Candidate demonstrates strong Java background ({match.evidence_snippet[:50]}...).",
                    suggested_evaluation="Evaluate candidate's understanding of JVM internals, concurrency primitives, and production diagnostics."
                ))
            elif skill_name.lower() == "spring boot":
                questions.append(InterviewQuestion(
                    id=f"Q-{q_id}",
                    category="Technical",
                    priority="High",
                    question="Describe how you structure REST API microservices in Spring Boot, including security (JWT/OAuth2), transaction propagation, and error handling.",
                    context_reason="Spring Boot is a critical requirement for this role.",
                    suggested_evaluation="Look for clear layered architecture (controller, service, repository, DTO) and resilient exception handling."
                ))
            elif skill_name.lower() == "sql":
                questions.append(InterviewQuestion(
                    id=f"Q-{q_id}",
                    category="Technical",
                    priority="Medium",
                    question="When a complex SQL query begins causing lock contention and high latency under heavy load, how do you diagnose and optimize it using EXPLAIN plans and indexing?",
                    context_reason="Candidate has proven database and SQL experience.",
                    suggested_evaluation="Candidate should discuss B-tree indexes, composite indexes, query execution plans, and transaction isolation levels."
                ))
            elif skill_name.lower() == "aws":
                questions.append(InterviewQuestion(
                    id=f"Q-{q_id}",
                    category="Technical",
                    priority="High",
                    question="Which AWS managed services (EC2, ECS, Lambda, RDS, S3) have you personally provisioned and configured in production or testing environments?",
                    context_reason="Validate hands-on cloud architecture competencies.",
                    suggested_evaluation="Evaluate practical infrastructure deployment experience vs. console-only familiarity."
                ))
            q_id += 1

        # 3. Project-Specific Questions
        if profile.projects:
            top_proj = profile.projects[0]
            questions.append(InterviewQuestion(
                id=f"Q-{q_id}",
                category="Project",
                priority="High",
                question=f"In your project '{top_proj.title}', what was the single biggest architectural challenge or technical roadblock you faced, and how did you resolve it?",
                context_reason=f"Candidate's primary highlighted project is {top_proj.title}.",
                suggested_evaluation="Check for problem-solving depth, systematic debugging, and individual ownership."
            ))
            q_id += 1

        # 4. JD-Specific Architectural Question
        questions.append(InterviewQuestion(
            id=f"Q-{q_id}",
            category="JD-Specific",
            priority="Medium",
            question=f"For our {job.title} position, how would you design a scalable, fault-tolerant backend system that handles peak traffic surges without service degradation?",
            context_reason=f"Directly assesses suitability for {job.title} role responsibilities.",
            suggested_evaluation="Look for mention of caching (Redis), asynchronous messaging (Kafka/RabbitMQ), circuit breakers, and rate limiting."
        ))
        q_id += 1

        # 5. Behavioral Question
        questions.append(InterviewQuestion(
            id=f"Q-{q_id}",
            category="Behavioral",
            priority="Low",
            question="Tell us about a situation where you had a strong technical disagreement with a peer or team lead regarding an architecture or implementation choice. How did you navigate it?",
            context_reason="Evaluates collaborative teamwork and communication under technical ambiguity.",
            suggested_evaluation="Listen for empathy, data-driven reasoning, openness to trade-offs, and alignment with business goals."
        ))

        return questions

    def assess_readiness(
        self,
        overall_score: float,
        profile: CandidateProfile,
        skill_matches: List[CandidateSkillMatch],
        claims: List[ClaimVerification]
    ) -> InterviewReadiness:
        # Technical Strength calculation
        strong_count = sum(1 for m in skill_matches if m.match_level == "Strong")
        total_skills = max(len(skill_matches), 1)
        tech_strength = min(round((strong_count / total_skills) * 100.0 + 15.0, 1), 98.0)

        # Experience Fit
        exp_fit = min(round((profile.total_experience_years / 2.5) * 85.0 + 10.0, 1), 96.0)

        # Project Relevance
        proj_rel = 92.0 if len(profile.projects) >= 2 else (80.0 if profile.projects else 50.0)

        # Evidence Confidence
        unsupported = sum(1 for c in claims if c.status in ["Insufficient evidence", "Requires interview verification"])
        evidence_conf = max(94.0 - (unsupported * 12.0), 55.0)

        # Risk Level
        if unsupported >= 2 or overall_score < 65.0:
            risk_level = "High"
            readiness = "Low"
        elif unsupported == 1 or overall_score < 80.0:
            risk_level = "Moderate"
            readiness = "Moderate"
        else:
            risk_level = "Low"
            readiness = "High"

        explanation = (
            f"Candidate presents {readiness.upper()} interview readiness. "
            f"Technical competencies stand at {tech_strength}%, backed by {evidence_conf}% evidence confidence. "
            f"{'Candidate exhibits verified project implementation depth with minimal verification concerns.' if risk_level == 'Low' else 'Specific technical claims require structured verification during interview.'}"
        )

        return InterviewReadiness(
            overall_readiness=readiness,
            overall_score=overall_score,
            technical_strength=tech_strength,
            experience_fit=exp_fit,
            project_relevance=proj_rel,
            evidence_confidence=evidence_conf,
            risk_level=risk_level,
            explanation=explanation
        )

interview_gen = InterviewGenerator()
