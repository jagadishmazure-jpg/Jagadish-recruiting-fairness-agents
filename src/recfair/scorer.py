"""Transparent match scorer. Every point in the score is tied to a written reason.

score = 60 * (required skills matched / required)
      + 20 * (nice-to-have matched / nice-to-have)
      + 20 * min(years / min_years, 1)       (20 if min_years == 0)

`biased_score` is a deliberately flawed SIMULATED baseline: it reads the raw resume and adds a
bonus when the first name is from pool A, standing in for a model that learned a name proxy.
It exists only so the audit can show it catches bias. It is never used for a real shortlist.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .data import FIRST_A, Job


@dataclass
class Match:
    job_id: str
    pid: str
    score: float
    reasons: list[str] = field(default_factory=list)


def score(job: Job, features: dict, pid: str) -> Match:
    have = set(features["skills"])
    req = [s for s in job.required if s in have]
    nice = [s for s in job.nice if s in have]
    missing = [s for s in job.required if s not in have]
    r_pts = 60 * len(req) / len(job.required)
    n_pts = 20 * len(nice) / len(job.nice) if job.nice else 0.0
    y_ratio = 1.0 if job.min_years == 0 else min(features["years"] / job.min_years, 1.0)
    y_pts = 20 * y_ratio
    reasons = [
        f"required {len(req)}/{len(job.required)} ({', '.join(req) or 'none'}) -> {r_pts:.1f}",
        f"nice-to-have {len(nice)}/{len(job.nice)} ({', '.join(nice) or 'none'}) -> {n_pts:.1f}",
        f"experience {features['years']}y vs {job.min_years}y minimum -> {y_pts:.1f}",
    ]
    if missing:
        reasons.append(f"missing required: {', '.join(missing)}")
    total = round(r_pts + n_pts + y_pts, 2)
    return Match(job.job_id, pid, total, reasons)


def biased_score(job: Job, features: dict, pid: str, raw_resume: str) -> Match:
    m = score(job, features, pid)
    first = raw_resume.split()[0] if raw_resume.split() else ""
    if first in FIRST_A:
        m.score = round(m.score + 15, 2)
        m.reasons.append("SIMULATED BIAS: +15 name-proxy bonus")
    return m


def explained(m: Match) -> bool:
    """A match is explained when the reasons add up to the score (within rounding)."""
    pts = 0.0
    for r in m.reasons:
        if "->" in r:
            pts += float(r.rsplit("->", 1)[1])
        elif r.startswith("SIMULATED BIAS"):
            pts += 15
    return abs(pts - m.score) < 0.11
