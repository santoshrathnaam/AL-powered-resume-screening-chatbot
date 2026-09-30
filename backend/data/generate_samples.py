import os
from pathlib import Path
from backend.data.demo_candidates import get_demo_candidates
from backend.data.demo_jd import DEMO_JD_TEXT

def create_sample_files():
    samples_dir = Path(__file__).resolve().parent / "sample_files"
    samples_dir.mkdir(parents=True, exist_ok=True)

    # 1. Write Sample JD
    jd_file = samples_dir / "Software_Engineer_Job_Description.txt"
    jd_file.write_text(DEMO_JD_TEXT, encoding="utf-8")

    # 2. Write 20 sample resumes as TXT files
    candidates = get_demo_candidates()
    for c in candidates:
        safe_id = c.candidate_id.replace(" ", "_").replace("#", "")
        resume_file = samples_dir / f"{safe_id}_{c.raw_name.replace(' ', '_')}_Resume.txt"
        resume_file.write_text(c.raw_text or f"{c.candidate_id}\nExperience: {c.total_experience_years} years.", encoding="utf-8")

    print(f"Generated {len(candidates)} sample resumes + 1 JD file in {samples_dir}")

if __name__ == "__main__":
    create_sample_files()
