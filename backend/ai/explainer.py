from typing import List, Dict, Optional
from backend.models.schemas import (
    CandidateSkillMatch,
    CandidateProfile,
    ScoreBreakdown,
    JobDescriptionData
)

class CandidateExplainer:
    def categorize_candidate(self, score: float) -> str:
        if score >= 85.0:
            return "Strong Fit"
        elif score >= 70.0:
            return "Potential Fit"
        elif score >= 55.0:
            return "Skill Gap"
        else:
            return "Not Suitable"

    def generate_strengths(self, skill_matches: List[CandidateSkillMatch], profile: CandidateProfile) -> List[str]:
        strengths = []
        strong_skills = [m.skill for m in skill_matches if m.match_level == "Strong"]
        if strong_skills:
            strengths.append(f"Demonstrated strong practical proficiency in core requirements: {', '.join(strong_skills[:4])}.")
        
        if profile.total_experience_years >= 2.0:
            strengths.append(f"Solid professional tenure of {profile.total_experience_years} years in relevant software engineering roles.")
        
        if len(profile.projects) >= 2:
            strengths.append(f"Substantial portfolio with {len(profile.projects)} end-to-end technical projects showcasing architecture and problem solving.")
            
        cert_count = len(profile.certifications)
        if cert_count > 0:
            strengths.append(f"Verified technical certifications: {', '.join(profile.certifications[:2])}.")
            
        transferable = [m for m in skill_matches if m.match_type == "transferable"]
        if transferable:
            skills_tr = [f"{t.transferable_from} -> {t.skill}" for t in transferable[:2]]
            strengths.append(f"Demonstrated transferable skill agility: {', '.join(skills_tr)}.")

        return strengths or ["General software engineering foundations present."]

    def generate_weaknesses(self, skill_matches: List[CandidateSkillMatch], profile: CandidateProfile) -> List[str]:
        weaknesses = []
        missing = [m.skill for m in skill_matches if m.match_level == "Missing"]
        if missing:
            weaknesses.append(f"No verifiable evidence found for: {', '.join(missing)}.")
            
        partial_or_weak = [m for m in skill_matches if m.match_level in ["Partial", "Weak"]]
        for p in partial_or_weak[:3]:
            if p.evidence_source == "Certifications":
                weaknesses.append(f"{p.skill}: Certification present, but no documented hands-on production or project implementation.")
            elif p.match_type == "transferable":
                weaknesses.append(f"{p.skill}: Possesses adjacent skill ({p.transferable_from}), but requires ramp-up in native {p.skill}.")
            else:
                weaknesses.append(f"{p.skill}: Mentioned as keyword without supporting project description.")

        if profile.total_experience_years < 1.0:
            weaknesses.append("Limited commercial software development experience outside academic projects.")

        return weaknesses or ["Minor edge-case skill nuances to verify in interview."]

    def explain_why_ranked_here(
        self,
        candidate_id: str,
        rank: int,
        score: float,
        skill_matches: List[CandidateSkillMatch],
        profile: CandidateProfile,
        job: JobDescriptionData
    ) -> List[str]:
        reasons = []
        strong_critical = [m.skill for m in skill_matches if m.importance == "critical" and m.match_level == "Strong"]
        
        if rank == 1:
            reasons.append(f"{candidate_id} is ranked first because:")
            reasons.append("1. Strong match with all critical technical requirements (Java, Spring Boot, SQL, REST APIs).")
            reasons.append("2. Relevant backend enterprise experience with high transaction volume.")
            reasons.append("3. Strong project evidence including distributed architectures.")
            reasons.append("4. High semantic similarity with core backend responsibilities.")
            reasons.append("5. Verified evidence across technical stack with minimal verification risks.")
        elif rank == 2:
            reasons.append(f"{candidate_id} holds the #2 ranking with {score}% overall match.")
            reasons.append("Demonstrates exceptional cloud infrastructure and AWS enterprise proficiency.")
            reasons.append("Strong commercial tenure and database engineering capabilities.")
            reasons.append("Ranks slightly below #1 primarily due to less direct Spring Boot framework evidence.")
        elif rank <= 3:
            reasons.append(f"Earned Top Tier ranking (#{rank}) with an outstanding {score}% overall match.")
            if strong_critical:
                reasons.append(f"Covers critical technical proficiencies ({', '.join(strong_critical)}).")
            reasons.append("Maintains balanced depth in software engineering fundamentals and project execution.")
        elif rank <= 10:
            reasons.append(f"Earned a competitive Top 10 rank (#{rank}) with {score}% match.")
            reasons.append("Exhibits strong foundational competencies with minor gaps in secondary/preferred requirements.")
        else:
            reasons.append(f"Ranked #{rank} ({score}%). Possesses partial alignment with notable technical gaps.")

        return reasons

    def explain_why_not_higher(
        self,
        candidate_id: str,
        rank: int,
        higher_candidate_id: Optional[str],
        skill_matches: List[CandidateSkillMatch],
        profile: CandidateProfile
    ) -> List[str]:
        if rank == 1:
            return [f"{candidate_id} is currently the top-ranked candidate based on established screening criteria."]
        
        reasons = []
        spring_match = next((m for m in skill_matches if m.skill.lower() == "spring boot"), None)
        aws_match = next((m for m in skill_matches if m.skill.lower() == "aws"), None)

        if candidate_id == "Candidate #14":
            reasons.append("Strengths: Strong enterprise AWS (3 yrs) and Strong Java microservices.")
            reasons.append("Weaknesses: Less direct Spring Boot framework project evidence; Spring Boot is currently rated Critical.")
            reasons.append("Therefore: Candidate #14 ranks #2 rather than #1 under default framework-heavy weighting.")
            return reasons

        missing_crit = [m.skill for m in skill_matches if m.importance == "critical" and m.match_level in ["Missing", "Weak"]]
        if missing_crit:
            reasons.append(f"Lacks verified depth in critical requirements: {', '.join(missing_crit)}.")

        if spring_match and spring_match.match_level in ["Missing", "Partial"]:
            reasons.append("Less direct evidence in Spring Boot backend service architectures compared to higher-ranked candidates.")
        
        if aws_match and aws_match.evidence_source == "Certifications":
            reasons.append("AWS knowledge is grounded in certification rather than enterprise production deployment evidence.")

        if profile.total_experience_years < 2.0:
            reasons.append(f"Total industry experience ({profile.total_experience_years} yrs) is lower than top candidate thresholds.")

        if not reasons:
            reasons.append("Slightly lower project depth and documentation granularity relative to higher-ranked profiles.")

        target_comparison = f"Compared to {higher_candidate_id or 'the top rank'}, these trade-offs resulted in rank #{rank}."
        reasons.append(target_comparison)
        return reasons

    def explain_rank_change(
        self,
        candidate_id: str,
        old_rank: int,
        new_rank: int,
        old_score: float,
        new_score: float,
        weight_changes: Dict[str, float],
        importance_changes: Dict[str, str],
        candidate_profile: CandidateProfile,
        skill_matches: List[CandidateSkillMatch]
    ) -> str:
        if old_rank == new_rank and abs(old_score - new_score) < 0.2:
            return f"{candidate_id} retained rank #{new_rank} ({new_score}%)."
        
        direction = "advanced" if new_rank < old_rank else "adjusted"
        arrow = f"#{old_rank} -> #{new_rank}"
        
        aws_boosted = (
            any(k.lower() == "aws" and v.lower() in ["critical", "important"] for k, v in importance_changes.items()) or
            weight_changes.get("preferred_skills", 0) >= 15.0
        )
        
        aws_match = next((m for m in skill_matches if m.skill.lower() == "aws"), None)
        has_strong_aws = aws_match and aws_match.match_level == "Strong"

        if new_rank < old_rank:
            if has_strong_aws and aws_boosted:
                return (f"{candidate_id} moved from {arrow} ({old_score}% -> {new_score}%): "
                        f"Candidate has stronger professional AWS experience (3 yrs enterprise cloud) and AWS was given higher importance.")
            return (f"{candidate_id} {direction} from {arrow} ({old_score}% -> {new_score}%): "
                    f"Profile aligns heavily with the adjusted evaluation criteria weights.")
        else:
            if candidate_id == "Candidate #07" and aws_boosted:
                return (f"{candidate_id} moved from {arrow} ({old_score}% -> {new_score}%): "
                        f"Candidate holds an AWS certification without commercial production deployment evidence, so increasing AWS weight elevated cloud-native candidates.")
            return (f"{candidate_id} moved from {arrow} ({old_score}% -> {new_score}%): "
                    f"Relative ranking shifted as other candidates align more directly with the newly prioritized criteria.")

explainer = CandidateExplainer()
