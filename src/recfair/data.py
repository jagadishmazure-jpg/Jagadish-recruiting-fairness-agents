"""Synthetic candidates and jobs for Brightwell Staffing, a fictional staffing firm.

Every person here is invented. Two invented first-name pools stand in for two demographic groups
(group "A" and group "B"). Qualifications are drawn from the SAME distribution for both groups, so
any gap in selection rates comes from the scorer, not from the data.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

FIRST_A = ["Arlen", "Brisa", "Corvin", "Delphine", "Emrys", "Fenna", "Galen", "Hollis", "Isolde", "Jory"]
FIRST_B = ["Kaveh", "Liora", "Mateus", "Nadira", "Oren", "Priya", "Quillon", "Rasha", "Soren", "Tamsin"]
LAST = ["Ashgrove", "Bellwether", "Copperfield", "Dunmore", "Elsworth", "Fairhollow", "Greystone", "Hartwell", "Ironside", "Juniper"]

SKILLS = ["python", "sql", "spark", "airflow", "docker", "kubernetes", "terraform", "react", "typescript", "java", "go", "pytorch", "statistics", "dbt", "aws", "linux"]
# Aliases a resume might use for the same skill.
ALIASES = {
    "python": ["python", "py3"],
    "sql": ["sql", "postgres", "t-sql"],
    "kubernetes": ["kubernetes", "k8s"],
    "typescript": ["typescript", "ts"],
    "pytorch": ["pytorch", "torch"],
    "statistics": ["statistics", "stats"],
    "go": ["golang"],
    "aws": ["aws", "cloud infrastructure"],
}


@dataclass(frozen=True)
class Job:
    job_id: str
    title: str
    required: tuple[str, ...]
    nice: tuple[str, ...]
    min_years: int


@dataclass
class Candidate:
    cand_id: str
    group: str  # "A" or "B" - synthetic label, used ONLY by the audit, never by the scorer
    first: str
    last: str
    email: str
    phone: str
    years: int
    skills: list[str] = field(default_factory=list)
    resume: str = ""


JOBS = [
    Job("J1", "Data Engineer", ("python", "sql", "airflow"), ("spark", "dbt", "aws"), 3),
    Job("J2", "Platform Engineer", ("docker", "kubernetes", "terraform"), ("go", "linux", "aws"), 4),
    Job("J3", "ML Engineer", ("python", "pytorch", "statistics"), ("docker", "sql", "spark"), 2),
    Job("J4", "Frontend Engineer", ("react", "typescript"), ("java", "docker"), 2),
]


def _alias(rng: random.Random, skill: str) -> str:
    return rng.choice(ALIASES.get(skill, [skill]))


def render_resume(c: Candidate, rng: random.Random) -> str:
    skills = ", ".join(_alias(rng, s) for s in c.skills)
    return (
        f"{c.first} {c.last}\n"
        f"Email: {c.email} | Phone: {c.phone}\n"
        f"Summary: engineer with {c.years} years of experience.\n"
        f"Skills: {skills}\n"
        f"Notes: {c.first} enjoys mentoring and code review.\n"
    )


def make_candidates(n: int = 400, seed: int = 7) -> list[Candidate]:
    rng = random.Random(seed)
    out = []
    for i in range(n):
        group = "A" if i % 2 == 0 else "B"
        first = rng.choice(FIRST_A if group == "A" else FIRST_B)
        last = rng.choice(LAST)
        k = rng.randint(3, 8)
        skills = rng.sample(SKILLS, k)
        c = Candidate(
            cand_id=f"C{i:04d}",
            group=group,
            first=first,
            last=last,
            email=f"{first.lower()}.{last.lower()}{i}@example.test",
            phone=f"555-{rng.randint(100, 999)}-{rng.randint(1000, 9999)}",
            years=rng.randint(0, 12),
            skills=skills,
        )
        c.resume = render_resume(c, rng)
        out.append(c)
    return out


def swap_name(c: Candidate, seed: int = 0) -> str:
    """Return the resume with the name replaced by one from the OTHER pool; everything else identical."""
    rng = random.Random(f"{c.cand_id}-{seed}")
    other = rng.choice(FIRST_B if c.group == "A" else FIRST_A)
    return c.resume.replace(c.first, other)
