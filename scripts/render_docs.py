"""Write measured numbers into README.md and docs/*.md from results/results.json.

python scripts/render_docs.py          # rewrite generated blocks
python scripts/render_docs.py --check  # CI: fail if docs drifted from results.json or the test count
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import count_tests  # noqa: E402


def blocks(r: dict, tests: int) -> dict[str, str]:
    rows = ["| Job | Scorer | Selected A / B (of 200 each) | Impact ratio | Four-fifths | p-value | Name-swap flips (of 400) |", "|---|---|---|---|---|---|---|"]
    for j, v in r["jobs"].items():
        for label, name in (("transparent", "transparent"), ("biased_baseline_simulated", "biased baseline (simulated)")):
            x = v[label]
            a, b = x["rates"]["A"]["selected"], x["rates"]["B"]["selected"]
            ff = x["four_fifths"]
            verdict = "pass" if ff["passes"] else "FAIL"
            rows.append(f"| {j} {v['title']} | {name} | {a} / {b} | {ff['impact_ratio']} | {verdict} | {ff['p_value']} | {x['name_swap']['selection_flips']} |")
    sc = r["scale_check"]
    red = r["redaction"]
    summ = [
        f"| What | Measured (synthetic data, seed {r['seed']}) |",
        "|---|---|",
        f"| Candidates | {r['candidates']} (scale check {sc['candidates']}) |",
        f"| PII redacted before scoring | {red['email']} emails, {red['phone']} phones, {red['name']} name mentions; {red['leaks_after_redaction']} left |",
        f"| Skills + years extracted exactly | {r['extraction_exact'] * 100:.1f}% |",
        f"| Transparent scorer impact ratio, n={r['candidates']} | "
        + ", ".join(f"{j} {v['transparent']['four_fifths']['impact_ratio']}" for j, v in r["jobs"].items())
        + " |",
        f"| Transparent scorer impact ratio, n={sc['candidates']} | " + ", ".join(f"{j} {v}" for j, v in sc["transparent_impact_ratio"].items()) + " |",
        f"| Biased baseline (simulated) impact ratio, n={sc['candidates']} | " + ", ".join(f"{j} {v}" for j, v in sc["baseline_impact_ratio"].items()) + " |",
        "| Name-swap selection flips, transparent / baseline | "
        + ", ".join(
            f"{j} {v['transparent']['name_swap']['selection_flips']} / {v['biased_baseline_simulated']['name_swap']['selection_flips']}" for j, v in r["jobs"].items()
        )
        + " |",
        f"| Release without human approval | blocked = {r['gate']['blocked_without_approval']}; override with written reason used = {r['gate']['override_used']} |",
        f"| Audit log | {r['audit_log']['entries']} entries, chain verified = {r['audit_log']['verified']}; edited entry detected at seq {r['tamper']['detected_at']} |",
        f"| Tests | {tests} |",
    ]
    return {"headline": "\n".join(summ), "jobs": "\n".join(rows), "tests": f"**{tests} tests**", "results": "```json\n" + json.dumps(r, indent=2) + "\n```"}


def apply(text: str, bl: dict[str, str]) -> str:
    for k, v in bl.items():
        text = re.sub(rf"(<!-- BEGIN:{k} -->\n).*?(<!-- END:{k} -->)", lambda m, v=v: m.group(1) + v + "\n" + m.group(2), text, flags=re.S)
    return text


def main() -> int:
    r = json.loads((ROOT / "results/results.json").read_text())
    bl = blocks(r, count_tests.count())
    bad = []
    for f in [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]:
        old = f.read_text()
        new = apply(old, bl)
        if new != old:
            if "--check" in sys.argv:
                bad.append(f.name)
            else:
                f.write_text(new)
    if bad:
        print("out of date:", ", ".join(bad), "- run: python scripts/render_docs.py")
        return 1
    print("docs match results.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
