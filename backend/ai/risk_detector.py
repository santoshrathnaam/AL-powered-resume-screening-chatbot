import re
from typing import List
from backend.models.schemas import ConsistencyRisk, CandidateProfile, CandidateSkillMatch

class RiskDetector:
    def detect_risks(
        self,
        profile: CandidateProfile,
        skill_matches: List[CandidateSkillMatch]
    ) -> List[ConsistencyRisk]:
        risks: List[ConsistencyRisk] = []
        raw_text = profile.raw_text or ""

        # 1. Check for overlapping full-time employment
        exp_list = profile.experience
        if len(exp_list) >= 2:
            years = []
            for e in exp_list:
                if e.start_year and e.end_year:
                    years.append((e.start_year, e.end_year, e.role, e.company))
            for i in range(len(years)):
                for j in range(i + 1, len(years)):
                    y1_s, y1_e, r1, c1 = years[i]
                    y2_s, y2_e, r2, c2 = years[j]
                    # Check overlap of full-time roles
                    if max(y1_s, y2_s) < min(y1_e, y2_e):
                        risks.append(ConsistencyRisk(
                            type="employment_overlap",
                            severity="Medium",
                            title="Overlapping Employment Dates",
                            description=f"Listed concurrent dates between {r1} at {c1} ({y1_s}–{y1_e}) and {r2} at {c2} ({y2_s}–{y2_e}).",
                            recommendation="Clarify whether roles were concurrent consulting, freelance, or full-time during interview."
                        ))

        # 2. Check for vague project descriptions
        for proj in profile.projects:
            desc = proj.description.lower()
            if len(desc) < 30 or any(phrase in desc for phrase in ["worked on various", "assisted team", "responsible for tasks", "general maintenance"]):
                risks.append(ConsistencyRisk(
                    type="vague_description",
                    severity="Low",
                    title="Vague Project Contribution",
                    description=f"Project '{proj.title}' provides minimal technical specificity ({proj.description[:60]}...).",
                    recommendation="Request candidate to delineate their exact individual architectural contributions versus team responsibilities."
                ))

        # 3. Check for skills with zero evidence
        weak_or_missing_crit = [m.skill for m in skill_matches if m.importance == "critical" and m.match_level in ["Missing", "Weak"]]
        if weak_or_missing_crit:
            risks.append(ConsistencyRisk(
                type="critical_skill_gap",
                severity="High" if len(weak_or_missing_crit) > 1 else "Medium",
                title="Critical Requirement Gap",
                description=f"Critical role requirements missing or unsubstantiated in resume: {', '.join(weak_or_missing_crit)}.",
                recommendation="Evaluate whether candidate possesses rapid ramp-up potential or transferable foundational skills."
            ))

        # 4. Check for employment gap (> 1.5 years)
        if len(exp_list) >= 2:
            sorted_exp = sorted([e for e in exp_list if e.start_year and e.end_year], key=lambda x: x.start_year)
            for k in range(len(sorted_exp) - 1):
                gap = sorted_exp[k+1].start_year - sorted_exp[k].end_year
                if gap > 1:
                    risks.append(ConsistencyRisk(
                        type="date_gap",
                        severity="Low",
                        title="Employment Timeline Gap",
                        description=f"{gap}-year interval detected between {sorted_exp[k].company} and {sorted_exp[k+1].company}.",
                        recommendation="Neutral verification: Inquire constructively about professional development or education during this period."
                    ))

        if not risks:
            risks.append(ConsistencyRisk(
                type="clean_profile",
                severity="Low",
                title="No Consistency Anomaly Detected",
                description="Employment timeline, project narratives, and technical credentials align coherently.",
                recommendation="Standard structured interview questions apply."
            ))

        return risks

risk_detector = RiskDetector()
