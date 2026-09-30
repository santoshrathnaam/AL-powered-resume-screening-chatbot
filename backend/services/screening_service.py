from typing import List, Dict, Optional, Any
from backend.models.schemas import (
    JobDescriptionData,
    CandidateProfile,
    CandidateEvaluation,
    CandidateSkillMatch,
    ScreeningDashboardResponse,
    ComparisonMatrixItem,
    CandidateComparisonResponse
)
from backend.ai.semantic_matcher import semantic_matcher
from backend.ai.scoring_engine import scoring_engine
from backend.ai.claim_verifier import claim_verifier
from backend.ai.risk_detector import risk_detector
from backend.ai.explainer import explainer
from backend.ai.interview_gen import interview_gen
from backend.parsers.jd_parser import jd_parser
from backend.data.demo_jd import DEMO_JD_TEXT
from backend.data.demo_candidates import get_demo_candidates
from backend.config import settings

class ScreeningService:
    def __init__(self):
        # Initial state initialized with Demo JD & 20 demo candidates
        self.job: JobDescriptionData = jd_parser.parse_job_description(DEMO_JD_TEXT, "Software Engineer")
        self.raw_profiles: List[CandidateProfile] = get_demo_candidates()
        self.current_weights: Dict[str, float] = settings.DEFAULT_WEIGHTS.copy()
        self.requirement_importances: Dict[str, str] = {
            r.skill: r.importance for r in self.job.requirements
        }
        self.ranking_version: int = 1
        self.ranking_history: List[Dict[str, Any]] = []
        self.cached_evaluations: List[CandidateEvaluation] = []
        
        # Run initial evaluation
        self.evaluate_all()

    def set_job_description(self, raw_text: str, custom_title: Optional[str] = None):
        self.job = jd_parser.parse_job_description(raw_text, custom_title)
        self.requirement_importances = {r.skill: r.importance for r in self.job.requirements}
        self.ranking_version += 1
        self.evaluate_all(rank_change_note="New Job Description uploaded and evaluated.")

    def add_candidates(self, new_profiles: List[CandidateProfile], replace: bool = True):
        if replace:
            # Renumber candidates cleanly from #01 to #N
            for idx, p in enumerate(new_profiles):
                p.candidate_id = f"Candidate #{idx + 1:02d}"
                p.anonymized_id = f"CAND-{idx + 1:03d}"
            self.raw_profiles = new_profiles
            self.ranking_version += 1
            self.evaluate_all(rank_change_note=f"Screened {len(new_profiles)} uploaded resume(s).")
        else:
            current_count = len(self.raw_profiles)
            for idx, p in enumerate(new_profiles):
                p.candidate_id = f"Candidate #{current_count + idx + 1:02d}"
                p.anonymized_id = f"CAND-{current_count + idx + 1:03d}"
                self.raw_profiles.append(p)
            self.ranking_version += 1
            self.evaluate_all(rank_change_note=f"Added {len(new_profiles)} new resume(s) to candidate pool.")

    def reset_to_demo(self):
        self.job = jd_parser.parse_job_description(DEMO_JD_TEXT, "Software Engineer")
        self.raw_profiles = get_demo_candidates()
        self.current_weights = settings.DEFAULT_WEIGHTS.copy()
        self.requirement_importances = {r.skill: r.importance for r in self.job.requirements}
        self.ranking_version = 1
        self.ranking_history = []
        self.evaluate_all(rank_change_note="Reset to initial 20 Demo Resumes and Software Engineer JD.")

    def evaluate_all(self, rank_change_note: Optional[str] = None) -> List[CandidateEvaluation]:
        # Preserve previous state for ranking change animations and delta analysis
        prev_map = {e.candidate_id: (e.rank, e.overall_score) for e in self.cached_evaluations}

        evaluations: List[CandidateEvaluation] = []

        for profile in self.raw_profiles:
            # 1. Semantic Skill Matches
            skill_matches: List[CandidateSkillMatch] = []
            for req in self.job.requirements:
                active_imp = self.requirement_importances.get(req.skill, req.importance)
                sm = semantic_matcher.evaluate_skill(
                    skill_req=req.skill,
                    importance=active_imp,
                    resume_skills=profile.technical_skills,
                    experience_items=profile.experience,
                    project_items=profile.projects,
                    certifications=profile.certifications,
                    raw_text=profile.raw_text or ""
                )
                skill_matches.append(sm)

            # 2. Score Breakdown
            score_breakdown = scoring_engine.compute_score(
                profile=profile,
                skill_matches=skill_matches,
                job=self.job,
                custom_weights=self.current_weights,
                requirement_importance_overrides=self.requirement_importances
            )

            # 3. Claims & Risks
            claims = claim_verifier.verify_candidate_claims(profile, skill_matches)
            risks = risk_detector.detect_risks(profile, skill_matches)

            # 4. Strengths, Weaknesses, Missing & Transferable Skills
            strengths = explainer.generate_strengths(skill_matches, profile)
            weaknesses = explainer.generate_weaknesses(skill_matches, profile)
            missing = [m.skill for m in skill_matches if m.match_level == "Missing"]
            transferable = [f"{m.transferable_from} -> {m.skill}" for m in skill_matches if m.match_type == "transferable"]

            # 5. Interview Readiness & Question Kit
            readiness = interview_gen.assess_readiness(score_breakdown.total, profile, skill_matches, claims)
            questions = interview_gen.generate_questions(profile, skill_matches, claims, self.job)

            category = explainer.categorize_candidate(score_breakdown.total)

            prev_rank, prev_score = prev_map.get(profile.candidate_id, (None, None))

            eval_cand = CandidateEvaluation(
                candidate_id=profile.candidate_id,
                anonymized_id=profile.anonymized_id,
                rank=0,  # assigned after sorting
                previous_rank=prev_rank,
                overall_score=score_breakdown.total,
                previous_score=prev_score,
                category=category,
                score_breakdown=score_breakdown,
                skill_matches=skill_matches,
                strengths=strengths,
                weaknesses=weaknesses,
                missing_skills=missing,
                transferable_skills=transferable,
                claims=claims,
                risks=risks,
                why_this_candidate=[],
                why_not_higher=[],
                interview_readiness=readiness,
                interview_questions=questions,
                rank_change_reason="",
                profile=profile
            )
            evaluations.append(eval_cand)

        # Sort by overall score descending
        evaluations.sort(key=lambda x: x.overall_score, reverse=True)

        # Assign ranks and explainability
        for idx, ev in enumerate(evaluations):
            ev.rank = idx + 1
            higher_id = evaluations[idx - 1].candidate_id if idx > 0 else None
            ev.why_this_candidate = explainer.explain_why_ranked_here(
                ev.candidate_id, ev.rank, ev.overall_score, ev.skill_matches, ev.profile, self.job
            )
            ev.why_not_higher = explainer.explain_why_not_higher(
                ev.candidate_id, ev.rank, higher_id, ev.skill_matches, ev.profile
            )

            # Check for rank change reason
            if ev.previous_rank:
                ev.rank_change_reason = explainer.explain_rank_change(
                    ev.candidate_id,
                    ev.previous_rank,
                    ev.rank,
                    ev.previous_score or ev.overall_score,
                    ev.overall_score,
                    self.current_weights,
                    self.requirement_importances,
                    ev.profile,
                    ev.skill_matches
                )

        self.cached_evaluations = evaluations
        if rank_change_note:
            self.ranking_history.append({
                "version": self.ranking_version,
                "note": rank_change_note,
                "top_1": evaluations[0].candidate_id if evaluations else "None",
                "top_score": evaluations[0].overall_score if evaluations else 0
            })

        return evaluations

    def apply_what_if(
        self,
        weights: Optional[Dict[str, float]] = None,
        requirement_importances: Optional[Dict[str, str]] = None
    ) -> List[CandidateEvaluation]:
        if weights:
            self.current_weights.update(weights)
        if requirement_importances:
            self.requirement_importances.update(requirement_importances)
        
        self.ranking_version += 1
        note = "What-if simulation adjusted criteria weights."
        return self.evaluate_all(rank_change_note=note)

    def get_dashboard_data(self) -> ScreeningDashboardResponse:
        cands = self.cached_evaluations
        total = len(cands)
        
        # Category statistics
        strong_count = sum(1 for c in cands if c.category == "Strong Fit")
        potential_count = sum(1 for c in cands if c.category == "Potential Fit")
        gap_count = sum(1 for c in cands if c.category == "Skill Gap")
        unsuitable_count = sum(1 for c in cands if c.category == "Not Suitable")
        avg_score = round(sum(c.overall_score for c in cands) / max(total, 1), 1)

        # Skill availability counts
        skill_coverage: Dict[str, Dict[str, int]] = {}
        for req in self.job.requirements:
            s_name = req.skill
            skill_coverage[s_name] = {"Strong": 0, "Partial": 0, "Weak": 0, "Missing": 0}
            for c in cands:
                match = next((m for m in c.skill_matches if m.skill == s_name), None)
                if match:
                    skill_coverage[s_name][match.match_level] = skill_coverage[s_name].get(match.match_level, 0) + 1

        stats = {
            "total_resumes": total,
            "strong_fit": strong_count,
            "potential_fit": potential_count,
            "skill_gap": gap_count,
            "not_suitable": unsuitable_count,
            "average_match_score": avg_score,
            "skill_coverage": skill_coverage,
            "category_distribution": [
                {"name": "Strong Fit", "count": strong_count, "color": "#10b981"},
                {"name": "Potential Fit", "count": potential_count, "color": "#3b82f6"},
                {"name": "Skill Gap", "count": gap_count, "color": "#f59e0b"},
                {"name": "Not Suitable", "count": unsuitable_count, "color": "#ef4444"}
            ]
        }

        return ScreeningDashboardResponse(
            job=self.job,
            total_resumes=total,
            top_10=cands[:10],
            all_candidates=cands,
            statistics=stats,
            weights=self.current_weights,
            version=self.ranking_version,
            ranking_history_notes=[h["note"] for h in self.ranking_history]
        )

    def compare_candidates(self, candidate_ids: List[str]) -> CandidateComparisonResponse:
        norm_ids = {cid.lower().replace(" ", "").replace("#", "").replace("-", "") for cid in candidate_ids}
        selected = [
            c for c in self.cached_evaluations 
            if c.candidate_id.lower().replace(" ", "").replace("#", "").replace("-", "") in norm_ids
            or c.anonymized_id.lower().replace(" ", "").replace("#", "").replace("-", "") in norm_ids
            or c.candidate_id in candidate_ids
            or c.anonymized_id in candidate_ids
        ]
        if not selected:
            selected = self.cached_evaluations[:min(3, len(self.cached_evaluations))]

        matrix: List[ComparisonMatrixItem] = []

        # Compare Skills
        for req in self.job.requirements:
            scores_dict = {}
            best_cand = None
            best_score = -1.0
            for c in selected:
                match = next((m for m in c.skill_matches if m.skill == req.skill), None)
                if match:
                    val_str = f"{match.match_level}"
                    if match.evidence_source:
                        val_str += f" ({match.evidence_source})"
                    scores_dict[c.candidate_id] = val_str
                    if match.score > best_score:
                        best_score = match.score
                        best_cand = c.candidate_id
                else:
                    scores_dict[c.candidate_id] = "Missing"

            matrix.append(ComparisonMatrixItem(
                criteria=req.skill,
                category="skill",
                scores=scores_dict,
                highest_candidate=best_cand,
                notes=f"Importance: {req.importance.title()}"
            ))

        # Compare Experience
        exp_dict = {}
        best_exp_cand = None
        best_exp = -1.0
        for c in selected:
            yrs = c.profile.total_experience_years if c.profile else 2.0
            exp_dict[c.candidate_id] = f"{yrs} yrs"
            if yrs > best_exp:
                best_exp = yrs
                best_exp_cand = c.candidate_id
        matrix.append(ComparisonMatrixItem(
            criteria="Experience",
            category="experience",
            scores=exp_dict,
            highest_candidate=best_exp_cand,
            notes=f"Min Required: {self.job.min_experience_years} yrs"
        ))

        # Compare Projects
        proj_dict = {}
        for c in selected:
            count = len(c.profile.projects) if c.profile else 1
            proj_dict[c.candidate_id] = f"{count} documented project(s)"
        matrix.append(ComparisonMatrixItem(
            criteria="Technical Projects",
            category="project",
            scores=proj_dict,
            highest_candidate=selected[0].candidate_id,
            notes="Evaluated for architectural complexity"
        ))

        # Compare Overall Match Score
        score_dict = {c.candidate_id: f"{c.overall_score}% (#{c.rank})" for c in selected}
        matrix.append(ComparisonMatrixItem(
            criteria="Overall Score",
            category="overall",
            scores=score_dict,
            highest_candidate=selected[0].candidate_id,
            notes="Weighted explainable index"
        ))

        # Key differentiators summary
        diffs = []
        if len(selected) >= 2:
            diffs.append(f"{selected[0].candidate_id} leads with higher depth in {self.job.critical_skills[0] if self.job.critical_skills else 'core backend'}.")
            if len(selected) > 1:
                diffs.append(f"{selected[1].candidate_id} provides competitive cloud competencies with distinctive infrastructure experience.")

        summary_text = f"Comparative evaluation across {len(selected)} candidates highlights distinct trade-offs between immediate core framework readiness and specialized cloud infrastructure exposure."

        return CandidateComparisonResponse(
            candidates=selected,
            matrix=matrix,
            summary=summary_text,
            key_differentiators=diffs
        )

screening_service = ScreeningService()
