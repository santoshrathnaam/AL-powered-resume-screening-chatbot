from typing import List
from backend.models.schemas import (
    CandidateProfile,
    ExperienceItem,
    EducationItem,
    ProjectItem
)

def get_demo_candidates() -> List[CandidateProfile]:
    candidates: List[CandidateProfile] = []

    # CANDIDATE #07 (Default Rank 1 - 94%)
    c7 = CandidateProfile(
        candidate_id="Candidate #07",
        internal_id="cand-007-uuid",
        anonymized_id="CAND-007",
        raw_name="Alex Chen",
        email="alex.chen.dev@example.com",
        phone="+1 555-0107",
        total_experience_years=2.5,
        education=[
            EducationItem(
                degree="Bachelor of Science in Computer Science",
                institution="University of Washington",
                year="2023"
            )
        ],
        experience=[
            ExperienceItem(
                role="Backend Software Engineer",
                company="Nexus Financial Systems",
                duration="2023 - Present",
                start_year=2023,
                end_year=2026,
                years=2.5,
                description="Engineered high-throughput Java microservices with Spring Boot processing 10,000 transaction events/sec. Designed normalized PostgreSQL database schemas and optimized indexing to reduce query latency by 35%. Implemented robust REST APIs with Spring Security OAuth2.",
                technologies=["Java", "Spring Boot", "SQL", "PostgreSQL", "REST APIs", "Git"]
            )
        ],
        projects=[
            ProjectItem(
                title="Distributed Order Management Platform",
                description="Architected Java Spring Boot backend with PostgreSQL database and Redis caching, featuring asynchronous REST API communication and transactional integrity.",
                technologies=["Java", "Spring Boot", "PostgreSQL", "REST APIs", "Redis"]
            ),
            ProjectItem(
                title="Algorithmic Trade Analytics Engine",
                description="Implemented custom high-performance data structures and sorting algorithms in Java 17 to analyze market ticks with sub-millisecond latencies.",
                technologies=["Java", "Data Structures", "Algorithms"]
            )
        ],
        technical_skills=["Java", "Spring Boot", "SQL", "PostgreSQL", "REST APIs", "Data Structures", "Algorithms", "Git"],
        soft_skills=["Analytical Thinking", "Cross-Functional Collaboration", "Technical Writing"],
        certifications=["AWS Certified Cloud Practitioner"],
        achievements=["ACM ICPC Regional Finalist", "Published technical article on Spring Boot performance"],
        raw_text="""Alex Chen
Backend Software Engineer | Java & Spring Boot Specialist
Email: alex.chen.dev@example.com | Phone: +1 555-0107

SUMMARY:
Results-driven Software Engineer with 2.5 years of experience developing enterprise backend microservices using Java and Spring Boot. Strong grasp of relational database optimization and RESTful API architecture.

PROFESSIONAL EXPERIENCE:
Backend Software Engineer at Nexus Financial Systems | 2023 - Present (2.5 years)
- Developed and deployed high-throughput Java microservices with Spring Boot processing 10,000 transaction events/sec.
- Designed normalized PostgreSQL database schemas and optimized indexing to reduce query latency by 35%.
- Implemented robust REST APIs with Spring Security OAuth2 and OpenAPI documentation.
- Collaborated in an agile squad conducting code reviews and CI/CD releases.

PROJECTS:
Project: Distributed Order Management Platform
Architected Java Spring Boot backend with PostgreSQL database and Redis caching, featuring asynchronous REST API communication and transactional integrity.

Project: Algorithmic Trade Analytics Engine
Implemented custom high-performance data structures and sorting algorithms in Java 17 to analyze market ticks with sub-millisecond latencies.

SKILLS:
Technical: Java, Spring Boot, SQL, PostgreSQL, REST APIs, Data Structures, Algorithms, Git, Redis
Certifications: AWS Certified Cloud Practitioner
Education: B.S. in Computer Science, University of Washington, 2023
Achievements: ACM ICPC Regional Finalist
"""
    )
    candidates.append(c7)

    # CANDIDATE #14 (Default Rank 2 - 91%, Jumps to #1 when AWS is prioritized!)
    c14 = CandidateProfile(
        candidate_id="Candidate #14",
        internal_id="cand-014-uuid",
        anonymized_id="CAND-014",
        raw_name="Marcus Vance",
        email="marcus.vance.cloud@example.com",
        phone="+1 555-0114",
        total_experience_years=3.0,
        education=[
            EducationItem(
                degree="Bachelor of Science in Software Engineering",
                institution="Purdue University",
                year="2022"
            )
        ],
        experience=[
            ExperienceItem(
                role="Cloud Software Engineer",
                company="Skyline Infrastructure Labs",
                duration="2023 - Present",
                start_year=2023,
                end_year=2026,
                years=3.0,
                description="Designed and deployed enterprise cloud infrastructure on AWS utilizing EC2, ECS, Lambda, RDS, and S3. Built Java and Spring Boot backend microservices and automated infrastructure provisioning via Terraform and Docker. Managed complex MySQL database clusters and REST API integrations.",
                technologies=["AWS", "Java", "Spring Boot", "Docker", "SQL", "MySQL", "REST APIs", "Terraform"]
            )
        ],
        projects=[
            ProjectItem(
                title="Serverless Telemetry Aggregator on AWS",
                description="Engineered an event-driven data pipeline using AWS Lambda, S3, and Amazon RDS PostgreSQL, handling over 2M records daily with automated CI/CD deployment via Docker containers.",
                technologies=["AWS", "Docker", "SQL", "Java", "REST APIs"]
            ),
            ProjectItem(
                title="Enterprise Inventory API Gateway",
                description="Developed high-availability REST APIs in Java with AWS API Gateway and RDS MySQL persistence.",
                technologies=["Java", "Spring Boot", "AWS", "SQL", "REST APIs"]
            )
        ],
        technical_skills=["AWS", "Java", "Spring Boot", "SQL", "MySQL", "Docker", "REST APIs", "Data Structures", "Terraform", "Git"],
        soft_skills=["Systems Thinking", "Agile Leadership", "Incident Management"],
        certifications=["AWS Certified Solutions Architect - Associate", "AWS Certified Developer"],
        achievements=["Led AWS Cloud Migration saving $45k annually", "Top Speaker at DevOps Meetup"],
        raw_text="""Marcus Vance
Senior Cloud Software Engineer | Enterprise AWS & Java Specialist
Email: marcus.vance.cloud@example.com | Phone: +1 555-0114

SUMMARY:
Accomplished Cloud Software Engineer with 3 years of hands-on experience designing scalable AWS cloud solutions, Dockerized microservices, and Java Spring Boot backend applications. Strong database and REST API proficiency.

EXPERIENCE:
Cloud Software Engineer at Skyline Infrastructure Labs | 2023 - Present (3 years)
- Designed and deployed enterprise cloud infrastructure on AWS utilizing EC2, ECS, Lambda, RDS, and S3.
- Built Java and Spring Boot backend microservices and automated infrastructure provisioning via Terraform and Docker.
- Managed complex MySQL database clusters and high-traffic REST API integrations.
- Optimized cloud architecture, reducing server latency by 25%.

PROJECTS:
Project: Serverless Telemetry Aggregator on AWS
Engineered an event-driven data pipeline using AWS Lambda, S3, and Amazon RDS PostgreSQL, handling over 2M records daily with automated CI/CD deployment via Docker containers.

Project: Enterprise Inventory API Gateway
Developed high-availability REST APIs in Java with AWS API Gateway and RDS MySQL persistence.

SKILLS:
Cloud: AWS (EC2, S3, RDS, Lambda, ECS, CloudWatch)
Languages & Frameworks: Java, SQL, MySQL, REST APIs, Data Structures, Docker, Git, Terraform
Certifications: AWS Certified Solutions Architect - Associate, AWS Certified Developer
Education: B.S. in Software Engineering, Purdue University, 2022
"""
    )
    candidates.append(c14)

    # CANDIDATE #03 (Rank 3 - 89%)
    c3 = CandidateProfile(
        candidate_id="Candidate #03",
        internal_id="cand-003-uuid",
        anonymized_id="CAND-003",
        raw_name="Priya Sharma",
        email="priya.sharma@example.com",
        phone="+1 555-0103",
        total_experience_years=2.0,
        education=[
            EducationItem(
                degree="Master of Science in Computer Science",
                institution="Georgia Tech",
                year="2023"
            )
        ],
        experience=[
            ExperienceItem(
                role="Backend Developer",
                company="Apex Data Corp",
                duration="2024 - Present",
                start_year=2024,
                end_year=2026,
                years=2.0,
                description="Developed Java and Spring Boot microservices with PostgreSQL backend. Integrated Google Cloud Platform (GCP) storage and created REST API endpoints.",
                technologies=["Java", "Spring Boot", "PostgreSQL", "SQL", "REST APIs", "GCP"]
            )
        ],
        projects=[
            ProjectItem(
                title="Distributed Cache Management System",
                description="Implemented distributed hash tables and caching algorithms in Java with Spring Boot REST endpoints.",
                technologies=["Java", "Spring Boot", "Data Structures", "REST APIs"]
            )
        ],
        technical_skills=["Java", "Spring Boot", "SQL", "PostgreSQL", "REST APIs", "Data Structures", "GCP", "Git"],
        soft_skills=["Collaboration", "Communication"],
        certifications=["Google Associate Cloud Engineer"],
        achievements=["Graduate Research Assistantship Award"],
        raw_text="""Priya Sharma
Backend Developer | Java, Spring Boot & Distributed Systems
Email: priya.sharma@example.com | Phone: +1 555-0103

EXPERIENCE:
Backend Developer at Apex Data Corp | 2024 - Present (2.0 years)
- Developed Java and Spring Boot microservices with PostgreSQL backend.
- Integrated Google Cloud Platform (GCP) storage and created REST API endpoints.
- Wrote extensive JUnit integration test suites.

PROJECTS:
Project: Distributed Cache Management System
Implemented distributed hash tables and caching algorithms in Java with Spring Boot REST endpoints.

SKILLS: Java, Spring Boot, SQL, PostgreSQL, REST APIs, Data Structures, GCP, Git
Education: M.S. in Computer Science, Georgia Tech, 2023
"""
    )
    candidates.append(c3)

    # CANDIDATE #18 (Rank 4 - 87%)
    c18 = CandidateProfile(
        candidate_id="Candidate #18",
        internal_id="cand-018-uuid",
        anonymized_id="CAND-018",
        raw_name="Daniel Kim",
        email="daniel.kim@example.com",
        phone="+1 555-0118",
        total_experience_years=3.5,
        education=[
            EducationItem(
                degree="Bachelor of Engineering in CS",
                institution="University of Illinois",
                year="2022"
            )
        ],
        experience=[
            ExperienceItem(
                role="Software Engineer",
                company="OmniTech Platforms",
                duration="2022 - Present",
                start_year=2022,
                end_year=2026,
                years=3.5,
                description="Built enterprise services utilizing Java and C# .NET. Containerized backend services with Docker and managed SQL Server and PostgreSQL databases with high query performance.",
                technologies=["Java", "SQL", "PostgreSQL", "Docker", "REST APIs", "Git"]
            )
        ],
        projects=[
            ProjectItem(
                title="Containerized Microservices Cluster",
                description="Packaged multi-service backend with Docker and Docker-Compose with PostgreSQL database.",
                technologies=["Docker", "Java", "SQL", "REST APIs"]
            )
        ],
        technical_skills=["Java", "SQL", "Docker", "PostgreSQL", "REST APIs", "Data Structures", "Git"],
        soft_skills=["Leadership", "Scrum"],
        certifications=["Docker Certified Associate"],
        achievements=["Company Innovation Award 2024"],
        raw_text="""Daniel Kim | Software Engineer
3.5 years experience in enterprise backend systems, Docker containerization, Java, and SQL.
Skills: Java, SQL, Docker, PostgreSQL, REST APIs, Git. B.E. CS, 2022.
"""
    )
    candidates.append(c18)

    # CANDIDATE #11 (Rank 5 - 85%)
    c11 = CandidateProfile(
        candidate_id="Candidate #11",
        internal_id="cand-011-uuid",
        anonymized_id="CAND-011",
        raw_name="Elena Rostova",
        email="elena.rostova@example.com",
        phone="+1 555-0111",
        total_experience_years=2.0,
        education=[EducationItem(degree="B.S. in CS", institution="Texas A&M", year="2023")],
        experience=[
            ExperienceItem(
                role="Junior Backend Developer",
                company="CyberPulse Systems",
                duration="2023 - Present",
                start_year=2023,
                end_year=2026,
                years=2.0,
                description="Core Java application development, algorithm design, MySQL query writing, and REST API testing.",
                technologies=["Java", "SQL", "MySQL", "REST APIs", "Data Structures"]
            )
        ],
        projects=[
            ProjectItem(
                title="Graph Algorithm Visualizer",
                description="Engineered interactive graph algorithm tool using Java and Spring Boot backend.",
                technologies=["Java", "Spring Boot", "Data Structures"]
            )
        ],
        technical_skills=["Java", "Spring Boot", "SQL", "MySQL", "Data Structures", "Algorithms", "Git"],
        soft_skills=["Problem Solving", "Detail Oriented"],
        certifications=[],
        achievements=["Dean's List 2021-2023"],
        raw_text="""Elena Rostova | Junior Backend Developer
B.S. CS Texas A&M. Skills: Java, Spring Boot, SQL, MySQL, Data Structures, Algorithms.
"""
    )
    candidates.append(c11)

    # CANDIDATE #02 (Rank 6 - 84%) - Transferable Python/FastAPI to Spring Boot
    c2 = CandidateProfile(
        candidate_id="Candidate #02",
        internal_id="cand-002-uuid",
        anonymized_id="CAND-002",
        raw_name="Jordan Reed",
        email="jordan.reed@example.com",
        phone="+1 555-0102",
        total_experience_years=3.0,
        education=[EducationItem(degree="B.S. Computer Engineering", institution="Penn State", year="2022")],
        experience=[
            ExperienceItem(
                role="Software Developer",
                company="Vector Analytics",
                duration="2023 - Present",
                start_year=2023,
                end_year=2026,
                years=3.0,
                description="Architected REST APIs in Python FastAPI and Java, integrated PostgreSQL, and deployed Docker containers.",
                technologies=["Python", "Java", "SQL", "PostgreSQL", "Docker", "REST APIs"]
            )
        ],
        projects=[
            ProjectItem(
                title="Microservices Event Hub",
                description="Developed asynchronous messaging pipeline using Docker and REST endpoints with PostgreSQL.",
                technologies=["Docker", "SQL", "REST APIs", "Java"]
            )
        ],
        technical_skills=["Python", "Java", "SQL", "PostgreSQL", "Docker", "REST APIs", "Git"],
        soft_skills=["Adaptability", "Collaboration"],
        certifications=[],
        achievements=["Hackathon First Place"],
        raw_text="""Jordan Reed | Software Developer
3 yrs experience. Python, Java, SQL, PostgreSQL, Docker, REST APIs. Transferable backend skills.
"""
    )
    candidates.append(c2)

    # CANDIDATE #09 (Rank 7 - 83%) - Date overlap risk scenario
    c9 = CandidateProfile(
        candidate_id="Candidate #09",
        internal_id="cand-009-uuid",
        anonymized_id="CAND-009",
        raw_name="Tariq Mansoor",
        email="tariq.m@example.com",
        phone="+1 555-0109",
        total_experience_years=2.5,
        education=[EducationItem(degree="B.Tech Computer Science", institution="National Institute", year="2023")],
        experience=[
            ExperienceItem(
                role="Software Engineer",
                company="Apex Solutions",
                duration="2023 - 2025",
                start_year=2023,
                end_year=2025,
                years=2.0,
                description="Java development, REST APIs, MySQL.",
                technologies=["Java", "SQL", "REST APIs"]
            ),
            ExperienceItem(
                role="Backend Consultant",
                company="Global Byte Corp",
                duration="2024 - 2026",
                start_year=2024,
                end_year=2026,
                years=2.0,
                description="Concurrent consulting role writing Java APIs and AWS integrations.",
                technologies=["Java", "AWS", "SQL"]
            )
        ],
        projects=[
            ProjectItem(
                title="Inventory System",
                description="Java and MySQL inventory tracker.",
                technologies=["Java", "SQL"]
            )
        ],
        technical_skills=["Java", "SQL", "AWS", "REST APIs", "Git"],
        soft_skills=["Multitasking"],
        certifications=[],
        achievements=[],
        raw_text="""Tariq Mansoor
Experience at Apex Solutions (2023-2025) and Global Byte Corp (2024-2026). Overlapping dates.
Java, SQL, AWS, REST APIs.
"""
    )
    candidates.append(c9)

    # CANDIDATE #16 (Rank 8 - 82%) - Strong Spring Boot, Missing AWS & Docker
    c16 = CandidateProfile(
        candidate_id="Candidate #16",
        internal_id="cand-016-uuid",
        anonymized_id="CAND-016",
        raw_name="Samantha Ray",
        email="samantha.ray@example.com",
        phone="+1 555-0116",
        total_experience_years=2.0,
        education=[EducationItem(degree="B.S. CS", institution="Rutgers", year="2023")],
        experience=[
            ExperienceItem(
                role="Java Developer",
                company="FinTech Core",
                duration="2023 - Present",
                start_year=2023,
                end_year=2026,
                years=2.0,
                description="Built Spring Boot services, SQL queries, REST endpoints.",
                technologies=["Java", "Spring Boot", "SQL", "REST APIs"]
            )
        ],
        projects=[
            ProjectItem(
                title="Billing Gateway",
                description="Spring Boot application for automated recurring billing.",
                technologies=["Java", "Spring Boot", "SQL"]
            )
        ],
        technical_skills=["Java", "Spring Boot", "SQL", "REST APIs", "Data Structures"],
        soft_skills=["Communication"],
        certifications=[],
        achievements=[],
        raw_text="""Samantha Ray | Java Developer
Spring Boot, Java, SQL, REST APIs. No cloud or docker mentioned.
"""
    )
    candidates.append(c16)

    # CANDIDATE #05 (Rank 9 - 80%) - High DSA, Junior
    c5 = CandidateProfile(
        candidate_id="Candidate #05",
        internal_id="cand-005-uuid",
        anonymized_id="CAND-005",
        raw_name="Kevin Zhang",
        email="kevin.z@example.com",
        phone="+1 555-0105",
        total_experience_years=1.5,
        education=[EducationItem(degree="B.S. Computer Science", institution="UC Berkeley", year="2024")],
        experience=[
            ExperienceItem(
                role="Associate Software Engineer",
                company="InnoWave Labs",
                duration="2024 - Present",
                start_year=2024,
                end_year=2026,
                years=1.5,
                description="Java microservice maintenance, algorithm optimization, and REST API development.",
                technologies=["Java", "Data Structures", "Algorithms", "REST APIs", "SQL"]
            )
        ],
        projects=[
            ProjectItem(
                title="Distributed Key-Value Store",
                description="Built high-speed key-value store using Java, custom hash indices, and multithreading.",
                technologies=["Java", "Data Structures", "Algorithms"]
            )
        ],
        technical_skills=["Java", "Data Structures", "Algorithms", "REST APIs", "SQL", "Git"],
        soft_skills=["Fast Learner", "Problem Solving"],
        certifications=[],
        achievements=["LeetCode Guardian Rating 2350+", "Dean's Honor List"],
        raw_text="""Kevin Zhang | Associate Software Engineer
1.5 years experience. Strong Java, Data Structures, Algorithms, REST APIs, SQL.
"""
    )
    candidates.append(c5)

    # CANDIDATE #12 (Rank 10 - 79%) - Strong Database
    c12 = CandidateProfile(
        candidate_id="Candidate #12",
        internal_id="cand-012-uuid",
        anonymized_id="CAND-012",
        raw_name="Lucas Meyer",
        email="lucas.meyer@example.com",
        phone="+1 555-0112",
        total_experience_years=3.0,
        education=[EducationItem(degree="B.S. Information Systems", institution="Ohio State", year="2022")],
        experience=[
            ExperienceItem(
                role="Database & Backend Specialist",
                company="DataMatrix Corp",
                duration="2023 - Present",
                start_year=2023,
                end_year=2026,
                years=3.0,
                description="Designed complex PostgreSQL and MySQL databases, stored procedures, and basic Java APIs.",
                technologies=["SQL", "PostgreSQL", "MySQL", "Java", "REST APIs"]
            )
        ],
        projects=[
            ProjectItem(
                title="ETL Warehouse Pipeline",
                description="Automated SQL data ingestion pipeline processing 500k rows/day.",
                technologies=["SQL", "PostgreSQL", "Java"]
            )
        ],
        technical_skills=["SQL", "PostgreSQL", "MySQL", "Java", "REST APIs", "Git"],
        soft_skills=["Organization"],
        certifications=["Oracle Database Certified Professional"],
        achievements=[],
        raw_text="""Lucas Meyer | Database & Backend Specialist
Expert in SQL, PostgreSQL, MySQL. Java, REST APIs.
"""
    )
    candidates.append(c12)

    # CANDIDATES #11 to #20 (Rank 11 - 20)
    extra_specs = [
        ("Candidate #01", "CAND-001", "Robert Davis", 2.0, ["Java", "SQL", "REST APIs"], "Potential Fit", "Good Java experience, but lacks Spring Boot and Docker depth.", 76.0),
        ("Candidate #04", "CAND-004", "Rachel Adams", 2.0, ["Java", "Spring Boot", "Git"], "Potential Fit", "Spring Boot knowledge, but lacks cloud and database indexing depth.", 74.0),
        ("Candidate #08", "CAND-008", "Chloe Bennett", 1.5, ["Java", "SQL", "Data Structures"], "Potential Fit", "Strong algorithmic skills, but limited commercial experience duration.", 71.0),
        ("Candidate #13", "CAND-013", "Vikram Patel", 1.5, ["Java", "SQL", "Docker"], "Skill Gap", "Basic Java and Docker, but missing Spring Boot enterprise frameworks.", 67.0),
        ("Candidate #17", "CAND-017", "Aiden Murphy", 1.0, ["Java", "REST APIs"], "Skill Gap", "Junior engineer with REST API basics; lacks Spring Boot and SQL.", 64.0),
        ("Candidate #10", "CAND-010", "Zoe Mitchell", 2.0, ["SQL", "Python", "Docker"], "Skill Gap", "Python backend engineer; limited direct Java experience.", 62.0),
        ("Candidate #06", "CAND-006", "Liam O'Connor", 1.0, ["Java", "Git"], "Skill Gap", "Academic background only with basic Java and git; missing frameworks.", 58.0),
        ("Candidate #15", "CAND-015", "Fatima Al-Mansoor", 0.8, ["SQL", "HTML", "JavaScript"], "Not Suitable", "Frontend and basic SQL background; lacks Java, Spring Boot, and cloud.", 54.0),
        ("Candidate #19", "CAND-019", "Carlos Gomez", 1.0, ["PHP", "MySQL"], "Not Suitable", "PHP developer looking to transition; missing Java, Spring Boot, and cloud.", 51.0),
        ("Candidate #20", "CAND-020", "Maya Lin", 0.5, ["Python", "Data Analysis"], "Not Suitable", "Data analyst profile; lacks software engineering, Java, and API design.", 47.0)
    ]

    for cid, anon, name, exp_yrs, skills, cat, notes, target_score in extra_specs:
        candidates.append(CandidateProfile(
            candidate_id=cid,
            internal_id=f"{anon.lower()}-uuid",
            anonymized_id=anon,
            raw_name=name,
            email=f"{name.lower().replace(' ', '.')}@example.com",
            phone="+1 555-0199",
            total_experience_years=exp_yrs,
            education=[EducationItem(degree="B.S. in Computer Science", institution="State University", year="2023")],
            experience=[
                ExperienceItem(
                    role="Software Associate",
                    company="Tech Horizons",
                    duration=f"2024 - Present",
                    start_year=2024,
                    end_year=2026,
                    years=exp_yrs,
                    description=f"Developed technical solutions utilizing {', '.join(skills)}.",
                    technologies=skills
                )
            ],
            projects=[
                ProjectItem(
                    title=f"{skills[0]} Application System",
                    description=f"Engineered software modules demonstrating {', '.join(skills)}.",
                    technologies=skills
                )
            ],
            technical_skills=skills,
            soft_skills=["Collaboration", "Communication"],
            certifications=[],
            achievements=[],
            raw_text=f"{name}\nExperience in {', '.join(skills)}. Total experience: {exp_yrs} years."
        ))

    return candidates
