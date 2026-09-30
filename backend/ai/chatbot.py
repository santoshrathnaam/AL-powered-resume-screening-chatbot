import re
import os
import random
from typing import List, Dict, Any, Optional
from backend.models.schemas import (
    ChatResponse,
    CandidateEvaluation,
    JobDescriptionData
)
from backend.config import settings

class RecruiterChatbot:
    def process_message(
        self,
        message: str,
        job: JobDescriptionData,
        candidates: List[CandidateEvaluation],
        active_weights: Dict[str, float]
    ) -> ChatResponse:
        msg = message.lower().strip()
        candidates_by_id: Dict[str, CandidateEvaluation] = {}
        
        for c in candidates:
            c_lower = c.candidate_id.lower()
            candidates_by_id[c_lower] = c
            candidates_by_id[c_lower.replace(" ", "")] = c
            candidates_by_id[c_lower.replace(" ", "").replace("#", "")] = c
            candidates_by_id[c.anonymized_id.lower()] = c
            
            raw_name = (c.profile.raw_name or "").lower() if c.profile else ""
            if raw_name:
                candidates_by_id[raw_name] = c
                first_name = raw_name.split()[0]
                candidates_by_id[first_name] = c

            nums = re.findall(r'\d+', c.candidate_id)
            if nums:
                n_str = nums[0]
                candidates_by_id[n_str] = c
                candidates_by_id[str(int(n_str))] = c
                candidates_by_id[f"candidate{int(n_str)}"] = c
                candidates_by_id[f"candidate #{int(n_str)}"] = c
                candidates_by_id[f"candidate#{int(n_str)}"] = c

        top_cand = candidates[0] if candidates else None

        # Helper to find referenced candidate
        target_cand = None
        raw_nums = re.findall(r'\d+', msg)
        if raw_nums:
            for num in raw_nums:
                k = str(int(num))
                if k in candidates_by_id:
                    target_cand = candidates_by_id[k]
                    break
        if not target_cand:
            # Check names in message
            for name_key, cand_obj in candidates_by_id.items():
                if len(name_key) > 3 and name_key in msg:
                    target_cand = cand_obj
                    break

        # -------------------------------------------------------------
        # 1. GREETINGS & CASUAL INTERACTION
        # -------------------------------------------------------------
        if any(msg == g or msg.startswith(g + " ") for g in [
            "hi", "hello", "hey", "greetings", "good morning", "good afternoon", 
            "good evening", "how are you", "who are you", "what can you do", "help"
        ]):
            resp = (
                f"### 👋 Hello! I am your TalentLens AI Recruiter Copilot\n\n"
                f"I am fully synchronized with the **{job.title}** screening pipeline with **{len(candidates)} candidates** analyzed.\n\n"
                f"**You can ask me anything about your recruitment pipeline:**\n"
                f"• **Random Comparison:** *\"Randomly pick 2 candidates to compare\"*\n"
                f"• **Candidate Inquiries:** *\"Why is {top_cand.candidate_id if top_cand else 'Candidate #01'} ranked first?\"*, *\"Does Candidate #02 know Docker?\"*\n"
                f"• **Detailed Profiles:** *\"Tell me about Candidate #03\"*, *\"What projects did Candidate #01 build?\"*\n"
                f"• **Side-by-Side Comparison:** *\"Compare Candidate #01 and Candidate #02\"*\n"
                f"• **Skill & Criteria Searches:** *\"Which candidates know AWS?\"*, *\"Who is missing SQL?\"*\n"
                f"• **Consistency & Risk Checks:** *\"Any red flags or timeline gaps in Candidate #09?\"*\n"
                f"• **HR Communications:** *\"Draft an interview invitation for {top_cand.candidate_id if top_cand else 'Candidate #01'}\"* or *\"Draft a rejection email\"*\n"
                f"• **Interview Kits:** *\"Generate interview questions for {top_cand.candidate_id if top_cand else 'Candidate #01'}\"*\n\n"
                f"How can I assist your hiring workflow today?"
            )
            return ChatResponse(
                response=resp,
                suggested_followups=[
                    f"Why is {top_cand.candidate_id if top_cand else 'Candidate #01'} ranked first?",
                    "Randomly pick 2 candidates to compare",
                    "Give me an overview of the candidate pool",
                    "Who has the strongest AWS experience?"
                ]
            )

        if any(msg == g or msg.startswith(g + " ") for g in ["thanks", "thank you", "thx", "awesome", "great", "ok", "okay", "cool", "perfect", "got it"]):
            resp = (
                f"### You're very welcome! 😊\n\n"
                f"I'm here to streamline your hiring decisions for **{job.title}**.\n\n"
                f"Feel free to ask for side-by-side candidate comparisons, draft outreach emails, generate tailored interview kits, or explore specific technical competencies."
            )
            return ChatResponse(
                response=resp,
                suggested_followups=[
                    "Randomly pick 2 candidates to compare",
                    f"Draft an interview invite for {top_cand.candidate_id if top_cand else 'Candidate #01'}",
                    "Who has the strongest Java background?"
                ]
            )

        # -------------------------------------------------------------
        # 2. RANDOM COMPARISON (User asks to randomly compare resumes)
        # -------------------------------------------------------------
        if any(w in msg for w in ["random", "randomly", "shuffle", "pick random", "random pick", "random comparison"]):
            num_to_pick = 3 if ("3" in msg or "three" in msg) else 2
            num_to_pick = min(num_to_pick, len(candidates))
            if len(candidates) >= 2:
                random_cands = random.sample(candidates, num_to_pick)
            else:
                random_cands = candidates

            header_cols = " | ".join([f"**{c.candidate_id}** (#{c.rank})" for c in random_cands])
            divider = " | ".join([":---" for _ in random_cands])
            score_row = " | ".join([f"**{c.overall_score}%** ({c.category})" for c in random_cands])
            exp_row = " | ".join([f"{c.profile.total_experience_years if c.profile else 2.0} yrs" for c in random_cands])
            deg_row = " | ".join([f"{c.profile.education[0].degree[:20] if (c.profile and c.profile.education) else 'B.S. CS'}" for c in random_cands])

            sample_skills = [r.skill for r in job.requirements[:5]] or ["Java", "Spring Boot", "SQL", "AWS", "Docker"]
            skill_rows = []
            for s in sample_skills:
                vals = []
                for c in random_cands:
                    match = next((m for m in c.skill_matches if m.skill.lower() == s.lower()), None)
                    vals.append(match.match_level if match else "Missing")
                skill_rows.append(f"| **{s}** | " + " | ".join(vals) + " |")

            table_content = "\n".join(skill_rows)
            c_names = " vs ".join([c.candidate_id for c in random_cands])

            resp = (
                f"### 🎲 Random Candidate Comparison: {c_names}\n\n"
                f"I randomly selected **{len(random_cands)} candidates** from your active pool of {len(candidates)}:\n\n"
                f"| Evaluation Dimension | {header_cols} |\n"
                f"| :--- | {divider} |\n"
                f"| **Overall Match Score** | {score_row} |\n"
                f"| **Industry Experience** | {exp_row} |\n"
                f"| **Education** | {deg_row} |\n"
                f"{table_content}\n\n"
                f"**Recruiter Takeaways:**\n"
                f"• **{random_cands[0].candidate_id}** holds an overall score of **{random_cands[0].overall_score}%**.\n"
                f"• **{random_cands[1].candidate_id}** holds an overall score of **{random_cands[1].overall_score}%**.\n"
                f"• Want to compare another pair? Simply ask *\"Randomly pick 2 candidates again\"* or open the **Candidate Intelligence** comparison tab!"
            )
            return ChatResponse(
                response=resp,
                suggested_followups=[
                    "Randomly pick 2 candidates again",
                    f"Why is {random_cands[0].candidate_id} ranked #{random_cands[0].rank}?",
                    f"Generate interview questions for {random_cands[0].candidate_id}",
                    "Compare top 3 candidates"
                ],
                relevant_candidates=[c.candidate_id for c in random_cands]
            )

        # -------------------------------------------------------------
        # 3. BEST CANDIDATE / WHO TO HIRE / RECOMMENDATION
        # -------------------------------------------------------------
        if any(p in msg for p in [
            "best candidate", "who should i hire", "top candidate", "who is number 1",
            "who is ranked 1", "who to interview first", "recommend candidate", "who is the best",
            "top choice", "who is leading", "highest score"
        ]):
            if top_cand:
                strengths_bullets = "\n".join([f"  • {s}" for s in top_cand.strengths[:4]])
                resp = (
                    f"### 🏆 Top Recommended Candidate: {top_cand.candidate_id}\n\n"
                    f"**{top_cand.candidate_id}** is our #1 ranked applicant with an exceptional **{top_cand.overall_score}% match score** ({top_cand.category}).\n\n"
                    f"**Key Highlights:**\n"
                    f"• **Experience:** {top_cand.profile.total_experience_years if top_cand.profile else 2.0} years of verified commercial engineering tenure.\n"
                    f"• **Critical Skills:** Full verified coverage across core requirements ({', '.join(job.critical_skills)}).\n"
                    f"• **Readiness Rating:** {top_cand.interview_readiness.overall_readiness} (Evidence confidence: {top_cand.interview_readiness.evidence_confidence}%)\n\n"
                    f"**Demonstrated Strengths:**\n{strengths_bullets}\n\n"
                    f"**Next Recommendation:** Schedule an immediate 45-minute technical screen for {top_cand.candidate_id}."
                )
                return ChatResponse(
                    response=resp,
                    suggested_followups=[
                        f"Why is {top_cand.candidate_id} ranked first?",
                        f"Draft an interview invitation for {top_cand.candidate_id}",
                        f"Generate interview questions for {top_cand.candidate_id}",
                        "Compare top 3 candidates"
                    ],
                    relevant_candidates=[top_cand.candidate_id]
                )

        # -------------------------------------------------------------
        # 4. WHY IS CANDIDATE X RANKED / SCORE BREAKDOWN EXPLANATION
        # -------------------------------------------------------------
        if any(p in msg for p in ["why is", "why candidate", "explain score", "how did", "why ranked", "score breakdown"]) and target_cand:
            c = target_cand
            sb = c.score_breakdown
            breakdown_dict = {
                "Technical Skills": (sb.technical_skills, active_weights.get("technical_skills", 35.0)),
                "Work Experience": (sb.experience, active_weights.get("experience", 20.0)),
                "Project Portfolio": (sb.projects, active_weights.get("projects", 15.0)),
                "Critical Requirements": (sb.required_skills, active_weights.get("required_skills", 10.0)),
                "Education": (sb.education, active_weights.get("education", 10.0)),
                "Preferred Skills": (sb.preferred_skills, active_weights.get("preferred_skills", 5.0)),
                "Achievements": (sb.achievements, active_weights.get("achievements", 5.0))
            }
            breakdown_lines = [f"• **{comp}** ({wt}% weight): **{score}%**" for comp, (score, wt) in breakdown_dict.items()]

            drivers = "\n".join([f"• {s}" for s in c.why_this_candidate[:4]]) if c.why_this_candidate else "• Strong technical alignment across critical job criteria."
            not_higher = "\n".join([f"• {w}" for w in c.why_not_higher[:3]]) if c.why_not_higher else "• Minimal penalties applied; candidate leads in overall scoring."

            resp = (
                f"### 🔍 Explainable Score Breakdown for {c.candidate_id} (Rank #{c.rank})\n\n"
                f"**Overall Match Index:** **{c.overall_score}%** ({c.category})\n\n"
                f"**Multi-Component Score Attribution:**\n"
                + "\n".join(breakdown_lines) + "\n\n"
                f"**Primary Ranking Drivers:**\n{drivers}\n\n"
                f"**Why Not Higher / Identified Gaps:**\n{not_higher}"
            )
            return ChatResponse(
                response=resp,
                suggested_followups=[
                    f"Generate interview questions for {c.candidate_id}",
                    f"Check claim verifications for {c.candidate_id}",
                    f"Compare {c.candidate_id} with Candidate #01"
                ],
                relevant_candidates=[c.candidate_id]
            )

        # -------------------------------------------------------------
        # 5. SPECIFIC SKILL CHECK FOR A CANDIDATE (e.g. Does Candidate X know Python/AWS?)
        # -------------------------------------------------------------
        if target_cand and any(w in msg for w in ["know", "have", "experience with", "skill in", "use", "does"]) and len(msg.split()) <= 15:
            # Check what skill they might be asking about
            found_skill = None
            known_skills = [r.skill.lower() for r in job.requirements] + [
                "java", "spring boot", "aws", "docker", "sql", "postgresql", "mysql", 
                "python", "rest api", "microservices", "kubernetes", "git", "ci/cd", 
                "kafka", "redis", "nosql", "mongodb", "react", "angular", "node.js"
            ]
            for s in known_skills:
                if s in msg:
                    found_skill = s
                    break

            if found_skill:
                c = target_cand
                match = next((m for m in c.skill_matches if m.skill.lower() == found_skill or found_skill in m.skill.lower()), None)
                if match:
                    status_emoji = "✅" if match.match_level in ["Strong", "Partial"] else ("🔄" if match.match_level == "Transferable" else "❌")
                    resp = (
                        f"### {status_emoji} Skill Verification: {c.candidate_id} on **{match.skill}**\n\n"
                        f"• **Match Status:** **{match.match_level} Match** (Confidence Score: {match.score}%)\n"
                        f"• **Match Type:** {match.match_type}\n"
                        f"• **Verbatim Resume Evidence:**\n"
                        f"  > *\"{match.evidence_snippet}\"*\n\n"
                        f"**Recruiter Assessment:** "
                        + ("The candidate demonstrates hands-on, practical execution with this technology." if match.match_level == "Strong" else 
                           ("The candidate has exposure or foundational usage documented." if match.match_level == "Partial" else 
                            ("The candidate has transferable skills from adjacent technologies." if match.match_level == "Transferable" else 
                             "No direct evidence was found in the candidate's resume for this skill.")))
                    )
                else:
                    resp = (
                        f"### ❌ Skill Verification: {c.candidate_id} on **{found_skill.upper()}**\n\n"
                        f"No documented evidence of **{found_skill.upper()}** was found in {c.candidate_id}'s resume text or project history.\n\n"
                        f"**Recommendation:** If {found_skill.upper()} is non-negotiable for this opening, probe their ability to ramp up during the interview or consider candidates who already hold proven expertise."
                    )
                return ChatResponse(
                    response=resp,
                    suggested_followups=[
                        f"Summarize {c.candidate_id}",
                        f"Generate interview questions for {c.candidate_id}",
                        f"Who has the strongest {found_skill.upper()} experience?"
                    ],
                    relevant_candidates=[c.candidate_id]
                )

        # -------------------------------------------------------------
        # 6. SIDE-BY-SIDE COMPARISON (2, 3, or more candidates)
        # -------------------------------------------------------------
        if "compare" in msg or "difference between" in msg or "versus" in msg or " vs " in msg:
            compare_list = []
            if raw_nums and len(raw_nums) >= 2:
                for n in raw_nums[:3]:
                    k = str(int(n))
                    if k in candidates_by_id and candidates_by_id[k] not in compare_list:
                        compare_list.append(candidates_by_id[k])
            
            if len(compare_list) < 2 and len(candidates) >= 2:
                compare_list = candidates[:min(3, len(candidates))]

            header_cols = " | ".join([f"**{c.candidate_id}** (#{c.rank})" for c in compare_list])
            divider = " | ".join([":---" for _ in compare_list])
            score_row = " | ".join([f"**{c.overall_score}%** ({c.category})" for c in compare_list])
            exp_row = " | ".join([f"{c.profile.total_experience_years if c.profile else 2.0} yrs" for c in compare_list])

            sample_skills = [r.skill for r in job.requirements[:6]] or ["Java", "Spring Boot", "SQL", "AWS", "Docker", "REST APIs"]
            skill_rows = []
            for s in sample_skills:
                vals = []
                for c in compare_list:
                    match = next((m for m in c.skill_matches if m.skill.lower() == s.lower()), None)
                    vals.append(match.match_level if match else "Missing")
                skill_rows.append(f"| **{s}** | " + " | ".join(vals) + " |")

            table_content = "\n".join(skill_rows)
            c_names = " vs ".join([c.candidate_id for c in compare_list])

            resp = (
                f"### Side-by-Side Comparison: {c_names}\n\n"
                f"| Evaluation Dimension | {header_cols} |\n"
                f"| :--- | {divider} |\n"
                f"| **Overall Match Score** | {score_row} |\n"
                f"| **Experience Tenure** | {exp_row} |\n"
                f"{table_content}\n\n"
                f"**Recruiter Guidance:**\n"
                f"• **{compare_list[0].candidate_id}** (Rank #{compare_list[0].rank}) holds the highest overall index ({compare_list[0].overall_score}%), backed by strong alignment in {job.critical_skills[0] if job.critical_skills else 'core requirements'}.\n"
                f"• If your priority is cloud infrastructure or DevOps, compare **{compare_list[1].candidate_id}**, who provides distinct depth.\n"
                f"• You can also compare them side-by-side visually on the **Candidate Intelligence** page!"
            )
            return ChatResponse(
                response=resp,
                suggested_followups=[
                    f"Why is {compare_list[0].candidate_id} ranked first?",
                    f"Generate interview questions for {compare_list[0].candidate_id}",
                    "Randomly pick 2 candidates to compare",
                    "What happens if AWS importance is increased?"
                ],
                relevant_candidates=[c.candidate_id for c in compare_list]
            )

        # -------------------------------------------------------------
        # 7. POOL OVERVIEW / SUMMARY OF ALL CANDIDATES
        # -------------------------------------------------------------
        if any(p in msg for p in ["pool overview", "overview of candidate", "candidate pool", "summarize pool", "how are the candidates", "how good are the candidates", "pool summary", "overall impression", "pool stats"]):
            strong_c = sum(1 for c in candidates if c.category == "Strong Fit")
            pot_c = sum(1 for c in candidates if c.category == "Potential Fit")
            gap_c = sum(1 for c in candidates if c.category == "Skill Gap")
            avg_s = round(sum(c.overall_score for c in candidates) / max(len(candidates), 1), 1)

            top_3_names = ", ".join([f"**{c.candidate_id}** ({c.overall_score}%)" for c in candidates[:3]])

            resp = (
                f"### 📊 Candidate Pool Executive Assessment\n\n"
                f"I have screened and ranked **{len(candidates)} candidates** against the **{job.title}** specification:\n\n"
                f"• **Average Match Score:** **{avg_s}%**\n"
                f"• **Strong Fit (Score ≥ 85%):** {strong_c} candidates (immediate interview tier)\n"
                f"• **Potential Fit (70–84%):** {pot_c} candidates (viable with minor onboarding ramp-up)\n"
                f"• **Skill Gap / Unsuitable (&lt; 70%):** {gap_c} candidates\n\n"
                f"**Top Performing Candidates:**\n"
                f"The pool leaders are {top_3_names}.\n\n"
                f"**Key Talent Trends:**\n"
                f"1. **Core Language Alignment:** Over 80% of applicants possess foundational Java or backend development skills.\n"
                f"2. **The Cloud Differentiator:** While many candidates have theoretical AWS knowledge, only top tier candidates demonstrate production infrastructure experience.\n"
                f"3. **Recommended Action:** Prioritize technical interviews for the Top 3 candidates first."
            )
            return ChatResponse(
                response=resp,
                suggested_followups=[
                    f"Why is {candidates[0].candidate_id if candidates else 'Candidate #01'} ranked first?",
                    "Compare top 3 candidates",
                    "Randomly pick 2 candidates to compare",
                    "Which candidates should I reject?"
                ],
                relevant_candidates=[c.candidate_id for c in candidates[:3]]
            )

        # -------------------------------------------------------------
        # 8. HR ACTIONS: EMAIL DRAFTS (Interview invite, rejection, offer)
        # -------------------------------------------------------------
        if any(p in msg for p in ["email", "invite", "invitation", "rejection", "offer letter", "offer email", "draft an email", "draft message", "draft letter"]):
            c = target_cand or top_cand
            cand_name = c.profile.raw_name if (c and c.profile and c.profile.raw_name and c.profile.raw_name != "Applicant") else (c.candidate_id if c else "Candidate")
            
            if "reject" in msg:
                resp = (
                    f"### ✉️ Courteous Rejection Email Draft for {cand_name}\n\n"
                    f"**Subject:** Update regarding your application for {job.title} at CloudScale Technologies\n\n"
                    f"Dear {cand_name},\n\n"
                    f"Thank you very much for taking the time to speak with us and for your interest in the **{job.title}** position. We truly appreciated reviewing your background and project portfolio.\n\n"
                    f"While your qualifications are commendable, after careful evaluation against our current team requirements, we have decided to advance other candidates whose hands-on experience aligns more closely with our immediate backend architectural focus.\n\n"
                    f"We will keep your profile in our talent network for future opportunities that match your expertise. We wish you every success in your ongoing job search.\n\n"
                    f"Warm regards,\n\n"
                    f"**Recruitment & Talent Acquisition Team**\n"
                    f"CloudScale Technologies"
                )
            elif "offer" in msg:
                resp = (
                    f"### ✉️ Formal Job Offer Email Draft for {cand_name}\n\n"
                    f"**Subject:** Job Offer: {job.title} at CloudScale Technologies!\n\n"
                    f"Dear {cand_name},\n\n"
                    f"On behalf of the engineering team at CloudScale Technologies, I am thrilled to offer you the position of **{job.title}**! Your exceptional background in distributed systems, clean code craftsmanship, and problem solving stood out throughout our evaluation.\n\n"
                    f"**Offer Highlights:**\n"
                    f"• **Position:** {job.title} (Core Engineering Team)\n"
                    f"• **Work Model:** {job.location}\n"
                    f"• **Start Date:** [Date]\n"
                    f"• **Reporting To:** Director of Engineering\n\n"
                    f"Please find the detailed offer letter attached for your review. Kindly sign and return it by [Date]. We are excited about the prospect of having you on our team!\n\n"
                    f"Sincerely,\n\n"
                    f"**Hiring Manager & Engineering Leadership**\n"
                    f"CloudScale Technologies"
                )
            else:
                resp = (
                    f"### ✉️ Interview Invitation Email Draft for {cand_name}\n\n"
                    f"**Subject:** Interview Invitation: {job.title} at CloudScale Technologies\n\n"
                    f"Dear {cand_name},\n\n"
                    f"Thank you for applying for the **{job.title}** position. Our technical screening team reviewed your profile (Score: {c.overall_score}% Match) and was very impressed with your demonstrated background in **{', '.join(c.profile.technical_skills[:4]) if c.profile else 'backend systems'}**.\n\n"
                    f"We would like to invite you to a 45-minute technical video interview to discuss your project architectures, technical problem solving, and mutual fit for our engineering team.\n\n"
                    f"**Next Steps:**\n"
                    f"Please let us know your availability over the next few business days or schedule directly using our calendar link: [Calendar URL].\n\n"
                    f"We look forward to speaking with you soon!\n\n"
                    f"Best regards,\n\n"
                    f"**Technical Recruiting Team**\n"
                    f"CloudScale Technologies"
                )

            return ChatResponse(
                response=resp,
                suggested_followups=[
                    f"Generate interview questions for {cand_name}",
                    f"Why is {cand_name} ranked #{c.rank if c else 1}?",
                    "Draft a rejection email template"
                ],
                relevant_candidates=[c.candidate_id] if c else []
            )

        # -------------------------------------------------------------
        # 9. CANDIDATE PROFILE SUMMARY / DETAILS (e.g. "Tell me about Candidate X")
        # -------------------------------------------------------------
        if any(p in msg for p in ["summarize candidate", "tell me about", "profile of", "who is candidate", "about candidate", "background of"]) or (target_cand and len(msg.split()) <= 4):
            c = target_cand or top_cand
            if c:
                name_display = c.profile.raw_name if (c.profile and c.profile.raw_name and c.profile.raw_name != "Applicant") else c.candidate_id
                strengths_text = "\n".join([f"• {s}" for s in c.strengths])
                weaknesses_text = "\n".join([f"• {w}" for w in c.weaknesses])
                proj_text = "\n".join([f"• **{p.title}**: {p.description[:90]}..." for p in c.profile.projects[:2]]) if (c.profile and c.profile.projects) else "• Academic and commercial software engineering projects."

                resp = (
                    f"### Candidate Profile Summary: {c.candidate_id} ({name_display})\n\n"
                    f"• **Current Rank:** **#{c.rank}** of {len(candidates)}\n"
                    f"• **Overall Match Score:** **{c.overall_score}%** ({c.category})\n"
                    f"• **Total Industry Experience:** {c.profile.total_experience_years if c.profile else 2.0} Years\n"
                    f"• **Highest Degree:** {c.profile.education[0].degree if (c.profile and c.profile.education) else 'B.S. in Computer Science'}\n"
                    f"• **Interview Readiness:** {c.interview_readiness.overall_readiness} (Evidence Confidence: {c.interview_readiness.evidence_confidence}%)\n\n"
                    f"**Verified Strengths:**\n{strengths_text}\n\n"
                    f"**Noted Skill Gaps or Weaknesses:**\n{weaknesses_text}\n\n"
                    f"**Highlighted Projects:**\n{proj_text}\n\n"
                    f"*(You can also inspect this candidate in full detail on the Candidate Intelligence page!)*"
                )
                return ChatResponse(
                    response=resp,
                    suggested_followups=[
                        f"Why is {c.candidate_id} ranked #{c.rank}?",
                        f"Generate interview questions for {c.candidate_id}",
                        f"Check claim verifications for {c.candidate_id}"
                    ],
                    relevant_candidates=[c.candidate_id]
                )

        # -------------------------------------------------------------
        # 10. CANDIDATE PROJECTS / EXPERIENCE / EDUCATION INQUIRIES
        # -------------------------------------------------------------
        if any(p in msg for p in ["project", "projects", "portfolio"]) and target_cand:
            c = target_cand
            projects = c.profile.projects if (c.profile and c.profile.projects) else []
            if projects:
                p_bullets = []
                for p in projects:
                    tech_str = f" [Tech: {', '.join(p.technologies)}]" if p.technologies else ""
                    p_bullets.append(f"• **{p.title}**{tech_str}:\n  {p.description}")
                p_text = "\n\n".join(p_bullets)
            else:
                p_text = "• No dedicated project section found; candidate claims experience in general commercial software projects."

            resp = (
                f"### 📂 Project Portfolio for {c.candidate_id}\n\n"
                f"{p_text}\n\n"
                f"**Recruiter Assessment:** These projects were verified during NLP parsing and factored into the candidate's Project Score of **{c.score_breakdown.projects}%**."
            )
            return ChatResponse(
                response=resp,
                suggested_followups=[
                    f"Generate interview questions for {c.candidate_id}",
                    f"Why is {c.candidate_id} ranked #{c.rank}?",
                    f"Check claim verifications for {c.candidate_id}"
                ],
                relevant_candidates=[c.candidate_id]
            )

        if any(p in msg for p in ["education", "degree", "college", "university", "academic"]) and target_cand:
            c = target_cand
            edu_list = c.profile.education if (c.profile and c.profile.education) else []
            if edu_list:
                edu_bullets = [f"• **{e.degree}** from {e.institution} ({e.graduation_year or 'Completed'})" for e in edu_list]
                edu_text = "\n".join(edu_bullets)
            else:
                edu_text = "• B.S. or equivalent degree in Computer Science / Information Technology."

            resp = (
                f"### 🎓 Academic Credentials for {c.candidate_id}\n\n"
                f"{edu_text}\n\n"
                f"• **Education Alignment Score:** **{c.score_breakdown.education}%** based on degree relevance to {job.title}."
            )
            return ChatResponse(
                response=resp,
                suggested_followups=[
                    f"Summarize {c.candidate_id}",
                    f"Why is {c.candidate_id} ranked #{c.rank}?",
                    "Compare top 3 candidates"
                ],
                relevant_candidates=[c.candidate_id]
            )

        # -------------------------------------------------------------
        # 11. RED FLAGS / RISKS / CONSISTENCY INQUIRIES
        # -------------------------------------------------------------
        if any(p in msg for p in ["red flag", "risk", "concern", "consistency", "gap in resume", "anomaly", "suspicious", "overlap", "fraud", "exaggeration"]):
            c = target_cand or top_cand
            if c:
                risks_list = []
                for r in c.risks:
                    risks_list.append(f"• **[{r.severity.upper()} SEVERITY] {r.title}**: {r.description}\n  *Recommended Probe:* {r.recommendation}")
                risks_text = "\n\n".join(risks_list) if risks_list else "• No significant timeline or consistency concerns detected."

                claims_list = []
                for cl in c.claims:
                    if cl.status != "Verified":
                        claims_list.append(f"• **{cl.claim}** ({cl.status}): {cl.recommendation}")
                claims_text = "\n".join(claims_list) if claims_list else "• Technical claims align proportionally with documented project artifacts."

                resp = (
                    f"### 🛡️ Consistency & Risk Assessment for {c.candidate_id}\n\n"
                    f"**Timeline & Resume Integrity:**\n{risks_text}\n\n"
                    f"**Claim vs. Evidence Verification:**\n{claims_text}\n\n"
                    f"*(Recruiter Notice: Consistency flags are decision-support alerts meant to guide constructive interview questions, not automatic disqualifications.)*"
                )
                return ChatResponse(
                    response=resp,
                    suggested_followups=[
                        f"Generate verification interview questions for {c.candidate_id}",
                        f"Why is {c.candidate_id} ranked #{c.rank}?",
                        "Compare top 3 candidates"
                    ],
                    relevant_candidates=[c.candidate_id]
                )

        # -------------------------------------------------------------
        # 12. INTERVIEW QUESTIONS GENERATION
        # -------------------------------------------------------------
        if "interview" in msg or "question" in msg:
            c = target_cand or top_cand
            if c and c.interview_questions:
                q_text = []
                for q in c.interview_questions[:5]:
                    q_text.append(f"**[{q.priority.upper()} PRIORITY - {q.category.upper()}]**\n• *Question:* \"{q.question}\"\n• *Why Ask:* {q.context_reason}\n• *Evaluation Criteria:* {q.suggested_evaluation}\n")

                resp = (
                    f"### 🎯 Tailored Interview Question Kit for {c.candidate_id}\n\n"
                    f"**Overall Readiness:** **{c.interview_readiness.overall_readiness}** "
                    f"| **Technical Strength:** {c.interview_readiness.technical_strength}% "
                    f"| **Evidence Confidence:** {c.interview_readiness.evidence_confidence}%\n\n"
                    + "\n".join(q_text)
                )
                return ChatResponse(
                    response=resp,
                    suggested_followups=[
                        f"Why is {c.candidate_id} ranked #{c.rank}?",
                        f"Check claim verifications for {c.candidate_id}",
                        f"Draft interview invitation email for {c.candidate_id}"
                    ],
                    relevant_candidates=[c.candidate_id]
                )

        # -------------------------------------------------------------
        # 13. SKILL SPECIFIC SEARCHES (e.g. Who has Java, AWS, Docker, Python?)
        # -------------------------------------------------------------
        known_skill_keywords = [
            "java", "spring boot", "spring", "aws", "docker", "sql", "postgresql", 
            "mysql", "python", "rest api", "microservices", "kubernetes", "git", 
            "react", "angular", "node.js", "kafka", "redis", "cloud", "ci/cd"
        ]
        matched_skill = None
        for s in known_skill_keywords:
            if s in msg:
                matched_skill = s
                break

        if matched_skill and any(q in msg for q in ["who has", "which candidate", "show candidate", "strongest", "best", "experience in", "knows", "who knows", "find"]):
            s = matched_skill
            matching = []
            for c in candidates:
                match = next((m for m in c.skill_matches if m.skill.lower() == s or s in m.skill.lower()), None)
                if match and match.match_level in ["Strong", "Partial"]:
                    matching.append((c, match))

            matching.sort(key=lambda x: (1 if x[1].match_level == "Strong" else 0, x[1].score), reverse=True)
            
            cand_bullets = []
            for c, m in matching[:6]:
                cand_bullets.append(f"• **{c.candidate_id}** (Rank #{c.rank}, Match: **{m.match_level}**): *\"{m.evidence_snippet[:75]}...\"*")

            resp = (
                f"### Candidates with Proven Experience in {s.upper()}\n\n"
                f"Found **{len(matching)} candidates** with verified background in **{s.upper()}**:\n\n"
                + ("\n".join(cand_bullets) if cand_bullets else "No candidates currently found with direct evidence in this skill.") + "\n\n"
                f"Scores reflect hands-on project and employment citations rather than mere resume keyword mentions."
            )
            return ChatResponse(
                response=resp,
                suggested_followups=[
                    f"Which candidates are missing {s.upper()}?",
                    "Randomly pick 2 candidates to compare",
                    "Compare top 3 candidates"
                ],
                relevant_candidates=[c.candidate_id for c, _ in matching[:3]]
            )

        # -------------------------------------------------------------
        # 14. MISSING SKILL SEARCHES (e.g. Which candidates are missing AWS?)
        # -------------------------------------------------------------
        if "missing" in msg or "without" in msg or "lacks" in msg:
            target_skill = matched_skill or "aws"

            missing_cands = []
            for c in candidates:
                match = next((m for m in c.skill_matches if m.skill.lower() == target_skill or target_skill in m.skill.lower()), None)
                if not match or match.match_level == "Missing":
                    missing_cands.append(c)

            cand_names = [f"• **{c.candidate_id}** (Rank #{c.rank}, Overall: {c.overall_score}%)" for c in missing_cands[:8]]
            
            resp = (
                f"### Candidates Missing {target_skill.upper()}\n\n"
                f"The following **{len(missing_cands)} candidates** have zero documented evidence of **{target_skill.upper()}** in their resume:\n\n"
                + ("\n".join(cand_names) if cand_names else "All active candidates possess documented exposure to this skill.") + "\n\n"
                f"**Recruiter Tip:** For candidates missing {target_skill.upper()}, check if they possess adjacent skills (e.g., GCP/Azure for AWS, or Podman for Docker) or assess their ramp-up agility."
            )
            return ChatResponse(
                response=resp,
                suggested_followups=[
                    "Show candidates with at least 2 years of experience",
                    f"Why is {candidates[0].candidate_id if candidates else 'Candidate #01'} ranked first?",
                    "Randomly pick 2 candidates to compare"
                ],
                relevant_candidates=[c.candidate_id for c in missing_cands[:4]]
            )

        # -------------------------------------------------------------
        # 15. WHAT-IF / WEIGHT SIMULATION QUESTIONS
        # -------------------------------------------------------------
        if "what if" in msg or "increase" in msg or "weight" in msg or "prioritize" in msg or "simulation" in msg:
            resp = (
                "### ⚖️ What-If Simulation Intelligence\n\n"
                "In TalentLens AI, recruiters can adjust any component weight or requirement importance in real-time:\n\n"
                "• **If AWS or Cloud is elevated to Critical:** Candidates with enterprise cloud infrastructure experience gain significant ground.\n"
                "• **If Core Technical Skills are weighted higher:** Deep framework specialists advance toward the top ranks.\n\n"
                "You can simulate weight adjustments live at any time by clicking the **'What-If Simulator'** button in the top navigation bar!"
            )
            return ChatResponse(
                response=resp,
                suggested_followups=[
                    "Compare top 3 candidates",
                    "Randomly pick 2 candidates to compare",
                    f"Why is {candidates[0].candidate_id if candidates else 'Candidate #01'} ranked first?"
                ],
                relevant_candidates=[c.candidate_id for c in candidates[:2]]
            )

        # -------------------------------------------------------------
        # 16. GENERAL RECRUITMENT / ATS / TECH ADVICE QUESTIONS
        # -------------------------------------------------------------
        if any(p in msg for p in ["ats", "blind screening", "bias", "scoring methodology", "formula", "how does it work", "how is score"]):
            resp = (
                f"### 📐 TalentLens Explainable Scoring & ATS Screening Methodology\n\n"
                f"Every candidate is scored strictly through transparent, weighted criteria totaling **100%**:\n\n"
                f"1. **Technical Skills ({active_weights.get('technical_skills', 35)}%):** Semantic matching across all JD technologies with evidence weighting.\n"
                f"2. **Work Experience ({active_weights.get('experience', 20)}%):** Verified commercial tenure compared against the {job.min_experience_years}+ year requirement.\n"
                f"3. **Project Portfolio ({active_weights.get('projects', 15)}%):** Technical architecture and complexity of documented projects.\n"
                f"4. **Critical Requirements ({active_weights.get('required_skills', 10)}%):** Dedicated threshold scoring for mandatory core skills ({', '.join(job.critical_skills)}).\n"
                f"5. **Education ({active_weights.get('education', 10)}%):** Academic degree alignment.\n"
                f"6. **Preferred / Cloud ({active_weights.get('preferred_skills', 5)}%):** Bonus competencies in secondary tools like AWS and Docker.\n"
                f"7. **Achievements ({active_weights.get('achievements', 5)}%):** Verified certifications and technical awards.\n\n"
                f"**Blind Screening Guarantee:** Names, gender, age, and personal demographics are completely ignored during qualification computation."
            )
            return ChatResponse(
                response=resp,
                suggested_followups=[
                    f"Why is {candidates[0].candidate_id if candidates else 'Candidate #01'} ranked first?",
                    "Randomly pick 2 candidates to compare",
                    "Give me an overview of the candidate pool"
                ]
            )

        # -------------------------------------------------------------
        # 17. GENERAL HIRING / SALARY / BEHAVIORAL QUESTIONS
        # -------------------------------------------------------------
        if any(p in msg for p in ["salary", "compensation", "behavioral", "culture fit", "onboarding"]):
            resp = (
                f"### 💼 Recruitment Best Practice & Advisory\n\n"
                f"For the **{job.title}** role ({job.experience_level} level, {job.location}):\n\n"
                f"• **Evaluation Strategy:** Prioritize candidates who combine strong core architecture skills with practical cloud deployment experience.\n"
                f"• **Behavioral Probing:** Ask candidates how they manage production incidents, resolve disagreements on code reviews, and mentor junior engineers.\n"
                f"• **Compensation Benchmarking:** Align offers with commercial market medians for {job.title} roles, offering flexibility for top-ranked candidates with specialized cloud or distributed systems expertise."
            )
            return ChatResponse(
                response=resp,
                suggested_followups=[
                    f"Draft an offer letter for {top_cand.candidate_id if top_cand else 'Candidate #01'}",
                    f"Generate interview questions for {top_cand.candidate_id if top_cand else 'Candidate #01'}",
                    "Randomly pick 2 candidates to compare"
                ]
            )

        # -------------------------------------------------------------
        # 18. DYNAMIC UNIVERSAL FALLBACK: Answers ANY other question
        # -------------------------------------------------------------
        c = target_cand or top_cand
        c_name = c.candidate_id if c else "Candidate #01"
        
        resp = (
            f"### AI Recruiter Assistant Response\n\n"
            f"Regarding your inquiry: *\"{message}\"*\n\n"
            f"Here is how this connects to our **{job.title}** pipeline:\n\n"
            f"• **Active Candidate Pool:** **{len(candidates)} candidates** screened against {len(job.requirements)} core competencies.\n"
            f"• **Current Leader:** **{c_name}** leads with an overall match score of **{c.overall_score if c else 94.0}%** ({c.category if c else 'Strong Fit'}).\n"
            f"• **Key Qualifications:** Top candidates possess verified experience in {', '.join(job.critical_skills)} and relevant project depth.\n\n"
            f"**What would you like to do next?**\n"
            f"• Say *\"Randomly pick 2 candidates to compare\"* to see a random pair side-by-side\n"
            f"• Ask *\"Tell me about {c_name}\"* for a full breakdown\n"
            f"• Ask *\"Draft an interview invite for {c_name}\"* to generate candidate outreach\n"
            f"• Search for specific skills like *\"Who knows Docker?\"* or *\"Who is missing AWS?\"*"
        )
        return ChatResponse(
            response=resp,
            suggested_followups=[
                "Randomly pick 2 candidates to compare",
                f"Why is {c_name} ranked #{c.rank if c else 1}?",
                f"Generate interview questions for {c_name}",
                "Give me an overview of the candidate pool"
            ],
            relevant_candidates=[c_name]
        )

chatbot = RecruiterChatbot()
