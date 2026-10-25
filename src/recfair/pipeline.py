"""End-to-end run: redact -> extract -> score -> shortlist -> audit -> human gate -> log."""

from __future__ import annotations

from .audit import AuditLog
from .data import JOBS, Candidate, make_candidates, swap_name
from .extract import extract
from .fairness import four_fifths, name_swap, selection_rates
from .pii import contains_pii, pseudonym, redact
from .scorer import biased_score, explained, score

CUTOFF = 70.0


def features_of(resume: str) -> dict:
    return extract(redact(resume)[0])


def run(n: int = 400, seed: int = 7) -> dict:
    cands: list[Candidate] = make_candidates(n, seed)
    log = AuditLog()
    pids = {c.cand_id: pseudonym(c.cand_id) for c in cands}
    groups = {pids[c.cand_id]: c.group for c in cands}
    red_counts = {"email": 0, "phone": 0, "ssn": 0, "name": 0}
    leaks = 0
    feats = {}
    extract_ok = 0
    for c in cands:
        red, cnt = redact(c.resume)
        for k, v in cnt.items():
            red_counts[k] += v
        leaks += contains_pii(red, [c.first, c.last, c.email, c.phone])
        f = extract(red)
        feats[pids[c.cand_id]] = f
        extract_ok += set(f["skills"]) == set(c.skills) and f["years"] == c.years
    log.append("pipeline.redacted", {"candidates": n, "leaks": leaks})
    per_job = {}
    for job in JOBS:
        fair = {c.cand_id: score(job, feats[pids[c.cand_id]], pids[c.cand_id]) for c in cands}
        biased = {c.cand_id: biased_score(job, feats[pids[c.cand_id]], pids[c.cand_id], c.resume) for c in cands}
        res = {}
        for label, ms in (("transparent", fair), ("biased_baseline_simulated", biased)):
            sel = {pids[k]: m.score >= CUTOFF for k, m in ms.items()}
            rates = selection_rates(sel, groups)
            ff = four_fifths(rates)
            if label == "transparent":
                fn = lambda r, job=job: score(job, features_of(r), "x").score  # noqa: E731
            else:
                fn = lambda r, job=job: biased_score(job, features_of(r), "x", r).score  # noqa: E731
            ns = name_swap([(c.resume, swap_name(c)) for c in cands], fn, CUTOFF)
            res[label] = {
                "rates": rates,
                "four_fifths": ff,
                "name_swap": ns,
                "explained": sum(explained(m) for m in ms.values()),
                "passes": ff["passes"] and ns["passes"],
            }
        per_job[job.job_id] = {"title": job.title, **res}
        log.append("job.audited", {"job": job.job_id, "transparent_passes": res["transparent"]["passes"], "baseline_passes": res["biased_baseline_simulated"]["passes"]})
    ok, _ = log.verify()
    return {
        "candidates": n,
        "seed": seed,
        "cutoff": CUTOFF,
        "redaction": {**red_counts, "leaks_after_redaction": leaks},
        "extraction_exact": round(extract_ok / n, 4),
        "jobs": per_job,
        "audit_log": {"entries": len(log.entries), "verified": ok},
        "_log": log,
    }
