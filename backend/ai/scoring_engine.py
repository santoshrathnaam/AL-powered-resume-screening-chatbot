from typing import Dict, List, Optional
from backend.models.schemas import (
    ScoreBreakdown,
    CandidateSkillMatch,
    CandidateProfile,
    JobDescriptionData
)
from backend.config import settings

class ScoringEngine:
    def compute_score(
        self,
        profile: CandidateProfile,
        skill_matches: List[CandidateSkillMatch],
        job: JobDescriptionData,
        custom_weights: Optional[Dict[str, float]] = None,
        requirement_importance_overrides: Optional[Dict[str, str]] = None
    ) -> ScoreBreakdown:
        # Active Weights (default: Tech 35%, Exp 20%, Proj 15%, Req 10%, Edu 10%, Pref 5%, Ach 5%)
        weights = settings.DEFAULT_WEIGHTS.copy()
        if custom_weights:
            weights.update(custom_weights)

        # Normalize weights to 100%
        total_w = sum(weights.values())
        if total_w > 0:
            weights = {k: round((v / total_w) * 100.0, 2) for k, v in weights.items()}

        overrides = requirement_importance_overrides or {}

        # 1. Technical Skills Component (0 - 100)
        # Calculates weighted skill average across all requirements
        tech_scores = []
        for m in skill_matches:
            imp = overrides.get(m.skill, m.importance).lower()
            weight_mult = 1.6 if imp == "critical" else (1.1 if imp == "important" else 0.6)
            
            # Map match level to score
            if m.match_level == "Strong":
                base_s = max(m.score, 95.0)
            elif m.match_level == "Partial":
                base_s = max(m.score, 70.0)
            elif m.match_level == "Weak":
                base_s = max(m.score, 40.0)
            else:
                base_s = 0.0
            tech_scores.append((base_s, weight_mult))

        if tech_scores:
            total_weighted_tech = sum(s * w for s, w in tech_scores)
            sum_tech_weights = sum(w for _, w in tech_scores) or 1.0
            raw_tech_score = min(max(total_weighted_tech / sum_tech_weights, 0.0), 100.0)
        else:
            raw_tech_score = 65.0

        # 2. Critical Required Skills Component (focus on critical requirements)
        crit_skills = [m for m in skill_matches if overrides.get(m.skill, m.importance).lower() == "critical"]
        if crit_skills:
            crit_scores = []
            for m in crit_skills:
                if m.match_level == "Strong":
                    crit_scores.append(100.0)
                elif m.match_level == "Partial":
                    crit_scores.append(70.0)
                elif m.match_level == "Weak":
                    crit_scores.append(35.0)
                else:
                    crit_scores.append(10.0)
            raw_req_score = sum(crit_scores) / len(crit_scores)
        else:
            raw_req_score = raw_tech_score

        # 3. Preferred Skills Component (e.g. AWS, Docker)
        pref_skills = [m for m in skill_matches if overrides.get(m.skill, m.importance).lower() == "preferred"]
        if pref_skills:
            p_scores = []
            for m in pref_skills:
                if m.match_level == "Strong":
                    p_scores.append(100.0)
                elif m.match_level == "Partial":
                    p_scores.append(75.0)
                elif m.match_level == "Weak":
                    p_scores.append(40.0)
                else:
                    p_scores.append(15.0)
            raw_pref_score = sum(p_scores) / len(p_scores)
        else:
            raw_pref_score = 75.0

        # 4. Experience Component
        min_years = max(job.min_experience_years, 1.0)
        cand_years = profile.total_experience_years
        if cand_years >= min_years:
            raw_exp_score = min(90.0 + ((cand_years - min_years) * 5.0), 100.0)
        elif cand_years > 0:
            raw_exp_score = max((cand_years / min_years) * 85.0, 40.0)
        else:
            raw_exp_score = 45.0

        # 5. Projects Component
        proj_count = len(profile.projects)
        if proj_count >= 2:
            raw_proj_score = 98.0
        elif proj_count == 1:
            raw_proj_score = 85.0
        else:
            # Check if projects were described in raw_text or experience
            raw_lower = (profile.raw_text or "").lower()
            if "project" in raw_lower:
                raw_proj_score = 82.0
            else:
                raw_proj_score = 55.0

        # 6. Education Component
        raw_edu_score = 88.0
        if profile.education:
            deg = " ".join([e.degree.lower() for e in profile.education])
            if any(t in deg for t in ["master", "ms", "m.tech", "phd"]):
                raw_edu_score = 96.0
            elif any(t in deg for t in ["bachelor", "bs", "b.tech", "b.e."]):
                raw_edu_score = 90.0
            elif any(t in deg for t in ["associate", "diploma", "certificate"]):
                raw_edu_score = 78.0
        else:
            # Check raw text for degree mentions
            raw_lower = (profile.raw_text or "").lower()
            if any(t in raw_lower for t in ["master", "ms in", "m.tech", "phd"]):
                raw_edu_score = 96.0
            elif any(t in raw_lower for t in ["bachelor", "b.tech", "b.s", "bs in", "b.e"]):
                raw_edu_score = 90.0

        # 7. Achievements & Certifications Component
        ach_count = len(profile.achievements) + len(profile.certifications)
        raw_ach_score = min(75.0 + (ach_count * 12.5), 100.0)

        # 8. Calculate weighted points purely algorithmically!
        # Base weights: Tech 35%, Exp 20%, Proj 15%, Req 10%, Edu 10%, Pref 5%, Ach 5%
        tech_pts = raw_tech_score * (weights["technical_skills"] / 100.0)
        exp_pts = raw_exp_score * (weights["experience"] / 100.0)
        proj_pts = raw_proj_score * (weights["projects"] / 100.0)
        req_pts = raw_req_score * (weights["required_skills"] / 100.0)
        edu_pts = raw_edu_score * (weights["education"] / 100.0)
        pref_pts = raw_pref_score * (weights["preferred_skills"] / 100.0)
        ach_pts = raw_ach_score * (weights["achievements"] / 100.0)

        total = tech_pts + exp_pts + proj_pts + req_pts + edu_pts + pref_pts + ach_pts
        total = round(min(max(total, 0.0), 100.0), 1)

        return ScoreBreakdown(
            technical_skills=round(tech_pts, 1),
            experience=round(exp_pts, 1),
            projects=round(proj_pts, 1),
            required_skills=round(req_pts, 1),
            education=round(edu_pts, 1),
            preferred_skills=round(pref_pts, 1),
            achievements=round(ach_pts, 1),
            total=total,
            weights_used=weights
        )

scoring_engine = ScoringEngine()
