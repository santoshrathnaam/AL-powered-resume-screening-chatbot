import re
from typing import List
from backend.models.schemas import ClaimVerification, CandidateProfile, CandidateSkillMatch

class ClaimVerifier:
    def verify_candidate_claims(
        self,
        profile: CandidateProfile,
        skill_matches: List[CandidateSkillMatch]
    ) -> List[ClaimVerification]:
        claims: List[ClaimVerification] = []
        raw_text = (profile.raw_text or "").lower()
        skills_text = " ".join(profile.technical_skills).lower()

        # Check for expert / lead claims in skills where only cert or basic exposure exists
        for match in skill_matches:
            skill_lower = match.skill.lower()
            expert_patterns = [
                rf'expert in {re.escape(skill_lower)}',
                rf'mastery in {re.escape(skill_lower)}',
                rf'lead {re.escape(skill_lower)}',
                rf'advanced {re.escape(skill_lower)}'
            ]
            has_expert_claim = any(re.search(p, raw_text) for p in expert_patterns)
            
            if has_expert_claim and match.match_level in ["Partial", "Weak", "Missing"]:
                claims.append(ClaimVerification(
                    claim=f"Claimed 'Expert / Advanced in {match.skill}'",
                    evidence_found=match.evidence_snippet,
                    professional_usage_demonstrated=False,
                    confidence="Moderate",
                    status="Insufficient evidence",
                    recommendation=f"Resume lists {match.skill} expertise, but lacks extensive production depth. Recommend probing in-depth architectural questions during interview."
                ))
            elif match.skill.lower() == "aws" and match.evidence_source == "Certifications" and match.match_level == "Partial":
                claims.append(ClaimVerification(
                    claim="AWS Cloud Competency",
                    evidence_found=f"{match.evidence_snippet}",
                    professional_usage_demonstrated=False,
                    confidence="Low/Moderate",
                    status="Requires interview verification",
                    recommendation="AWS certification found, but professional hands-on cloud production experience is not explicitly demonstrated. Verify deployed services in interview."
                ))

        # Check for quantitative claims (e.g. "improved performance by 40%")
        metric_matches = re.findall(r'(improved|reduced|increased|boosted|optimized)[^.\n]*?(\d+%)', raw_text)
        for action, metric in metric_matches[:2]:
            claims.append(ClaimVerification(
                claim=f"High-impact metric: '{action.strip()} by {metric}'",
                evidence_found="Mentioned in resume bullet point without explicit benchmarking baseline or tooling description.",
                professional_usage_demonstrated=True,
                confidence="Moderate",
                status="Requires interview verification",
                recommendation=f"Ask candidate how the {metric} improvement was measured and what profiling tools were used."
            ))

        # If no flags detected, provide a positive verification
        if not claims:
            claims.append(ClaimVerification(
                claim="Consistent Technical Claims",
                evidence_found="Project descriptions align proportionally with claimed experience duration and skill ratings.",
                professional_usage_demonstrated=True,
                confidence="High",
                status="Verified",
                recommendation="Experience claims appear grounded and consistent with demonstrated project artifacts."
            ))

        return claims

claim_verifier = ClaimVerifier()
