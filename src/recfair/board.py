"""Evidence board PNG built from results.json (real run, synthetic data)."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def draw(r: dict, out: Path, tests: int | None = None) -> Path:
    jobs = r["jobs"]
    ids = list(jobs)
    fig, ax = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("Recruiting fairness agents - evidence board (synthetic candidates, measured run)", fontsize=14, weight="bold")
    w = 0.2
    for k, (label, col) in enumerate((("transparent", "#2a7"), ("biased_baseline_simulated", "#c44"))):
        for g, off in (("A", -w / 2), ("B", w / 2)):
            vals = [jobs[j][label]["rates"][g]["rate"] for j in ids]
            ax[0, 0].bar([i + off + k * 2 * w - w for i in range(len(ids))], vals, w, color=col, alpha=1 if g == "A" else 0.55, label=f"{label} group {g}")
    ax[0, 0].set_xticks(range(len(ids)), [f"{j} {jobs[j]['title']}" for j in ids], fontsize=8)
    ax[0, 0].set_title("Selection rate by group (cutoff {:.0f})".format(r["cutoff"]))
    ax[0, 0].legend(fontsize=7)
    for label, col, m in (("transparent", "#2a7", "o"), ("biased_baseline_simulated", "#c44", "s")):
        ax[0, 1].plot(ids, [jobs[j][label]["four_fifths"]["impact_ratio"] for j in ids], m + "-", color=col, label=label)
    ax[0, 1].axhline(0.8, ls="--", color="k", label="four-fifths line 0.8")
    ax[0, 1].set_ylim(0, 1.15)
    ax[0, 1].set_title("Impact ratio (min rate / max rate)")
    ax[0, 1].legend(fontsize=8)
    x = range(len(ids))
    ax[1, 0].bar([i - 0.2 for i in x], [jobs[j]["transparent"]["name_swap"]["selection_flips"] for j in ids], 0.4, color="#2a7", label="transparent")
    ax[1, 0].bar(
        [i + 0.2 for i in x], [jobs[j]["biased_baseline_simulated"]["name_swap"]["selection_flips"] for j in ids], 0.4, color="#c44", label="biased baseline (simulated)"
    )
    ax[1, 0].set_xticks(list(x), ids)
    ax[1, 0].set_title(f"Name-swap selection flips (of {r['candidates']} pairs per job)")
    ax[1, 0].legend(fontsize=8)
    ax[1, 1].axis("off")
    red = r["redaction"]
    lines = [
        f"Candidates: {r['candidates']} synthetic (seed {r['seed']})",
        f"Redacted: {red['email']} emails, {red['phone']} phones, {red['name']} names",
        f"PII left after redaction: {red['leaks_after_redaction']}",
        f"Skills+years extracted exactly: {r['extraction_exact'] * 100:.1f}%",
        f"Audit log: {r['audit_log']['entries']} entries, chain verified={r['audit_log']['verified']}",
        f"Tamper test detected: {r.get('tamper', {}).get('detected_at')}",
        f"Gate: release without human approval blocked={r.get('gate', {}).get('blocked_without_approval')}",
    ]
    sc = r.get("scale_check")
    if sc:
        lines.append(f"Scale check n={sc['candidates']}: transparent IR " + ", ".join(f"{k}={v}" for k, v in sc["transparent_impact_ratio"].items()))
    lines.append(f"p-values (n={r['candidates']}): " + ", ".join(f"{j}={v['transparent']['four_fifths']['p_value']}" for j, v in jobs.items()))
    if tests is not None:
        lines.append(f"Tests: {tests}")
    ax[1, 1].text(0, 1, "\n".join(lines), va="top", family="monospace", fontsize=10)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=110)
    plt.close(fig)
    return out
