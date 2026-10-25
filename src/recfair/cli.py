"""recfair demo [--n 400] [--seed 7] [--out results]"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .board import draw
from .data import JOBS
from .pipeline import run
from .signoff import GateError, Shortlist


def demo(n: int, seed: int, out: Path, scale_n: int = 4000) -> dict:
    r = run(n, seed)
    log = r.pop("_log")
    # Human gate demo on job J1 using the transparent scorer's top 5.
    from .data import make_candidates
    from .pii import pseudonym
    from .pipeline import features_of
    from .scorer import score

    cands = make_candidates(n, seed)
    job = JOBS[0]
    top = sorted((score(job, features_of(c.resume), pseudonym(c.cand_id)) for c in cands), key=lambda m: -m.score)[:5]
    sl = Shortlist(job.job_id, top, log)
    sl.attach_audit({"passes": r["jobs"][job.job_id]["transparent"]["passes"]})
    try:
        sl.release()
        blocked = False
    except GateError:
        blocked = True
    ff = r["jobs"][job.job_id]["transparent"]["four_fifths"]
    reason = None
    if not sl.audit["passes"]:
        reason = f"impact ratio {ff['impact_ratio']} below 0.8 but p={ff['p_value']} (not significant); name-swap clean; re-audit at next intake"
    sl.approve("reviewer.hr-lead", override_reason=reason)
    released = sl.release()
    r["gate"] = {
        "override_used": reason is not None,
        "blocked_without_approval": blocked,
        "released_after_approval": len(released),
        "top_reasons_example": top[0].reasons,
    }
    # Tamper demo on a copy.
    import copy

    t = copy.deepcopy(log)
    t.entries[2]["payload"]["leaks"] = 999
    r["tamper"] = {"detected_at": t.verify()[1]}
    ok, _ = log.verify()
    r["audit_log"] = {"entries": len(log.entries), "verified": ok}
    big = run(scale_n, seed)
    big.pop("_log")
    r["scale_check"] = {
        "candidates": scale_n,
        "transparent_impact_ratio": {j: v["transparent"]["four_fifths"]["impact_ratio"] for j, v in big["jobs"].items()},
        "baseline_impact_ratio": {j: v["biased_baseline_simulated"]["four_fifths"]["impact_ratio"] for j, v in big["jobs"].items()},
    }
    out.mkdir(parents=True, exist_ok=True)
    log.dump(out / "audit_log.jsonl")
    (out / "results.json").write_text(json.dumps(r, indent=2) + "\n")
    return r


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="recfair")
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("demo")
    d.add_argument("--n", type=int, default=400)
    d.add_argument("--seed", type=int, default=7)
    d.add_argument("--out", type=Path, default=Path("results"))
    d.add_argument("--board", action="store_true")
    d.add_argument("--scale-n", type=int, default=4000)
    a = ap.parse_args(argv)
    r = demo(a.n, a.seed, a.out, a.scale_n)
    if a.board:
        draw(r, a.out / "evidence_board.png")
    for j, v in r["jobs"].items():
        t, b = v["transparent"], v["biased_baseline_simulated"]
        tt = f"transparent IR={t['four_fifths']['impact_ratio']} flips={t['name_swap']['selection_flips']}"
        bb = f"baseline IR={b['four_fifths']['impact_ratio']} flips={b['name_swap']['selection_flips']}"
        print(f"{j}: {tt} | {bb}")
    print("scale check transparent IR:", r["scale_check"]["transparent_impact_ratio"])
    print(f"redaction leaks={r['redaction']['leaks_after_redaction']} extraction_exact={r['extraction_exact']} log_verified={r['audit_log']['verified']}")
    return 0
