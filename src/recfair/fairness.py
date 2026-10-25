"""Fairness audit: selection rates by group, the four-fifths rule, Wilson intervals and a
counterfactual name-swap check. The group label is read here and nowhere in the scorer."""

from __future__ import annotations

import math
from collections.abc import Callable


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(max(0.0, c - h), 4), round(min(1.0, c + h), 4))


def selection_rates(selected: dict[str, bool], groups: dict[str, str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for g in sorted(set(groups.values())):
        ids = [i for i, gg in groups.items() if gg == g]
        k = sum(1 for i in ids if selected.get(i, False))
        out[g] = {"n": len(ids), "selected": k, "rate": round(k / len(ids), 4) if ids else 0.0, "wilson95": wilson(k, len(ids))}
    return out


def impact_ratio(rates: dict[str, dict]) -> float:
    vals = [r["rate"] for r in rates.values()]
    hi = max(vals) if vals else 0.0
    return round(min(vals) / hi, 4) if hi > 0 else 1.0


def two_prop_p(k1: int, n1: int, k2: int, n2: int) -> float:
    """Two-sided p-value of a two-proportion z-test (normal approximation)."""
    if n1 == 0 or n2 == 0:
        return 1.0
    p = (k1 + k2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return 1.0
    z = abs(k1 / n1 - k2 / n2) / se
    return round(math.erfc(z / math.sqrt(2)), 4)


def four_fifths(rates: dict[str, dict], threshold: float = 0.8) -> dict:
    """Impact ratio against the four-fifths line, plus a significance test so small-sample noise
    is visible. The rule itself is applied strictly: `passes` is the ratio test only."""
    ir = impact_ratio(rates)
    gs = list(rates.values())
    pv = two_prop_p(gs[0]["selected"], gs[0]["n"], gs[-1]["selected"], gs[-1]["n"]) if len(gs) >= 2 else 1.0
    return {"impact_ratio": ir, "threshold": threshold, "passes": ir >= threshold, "p_value": pv}


def name_swap(pairs: list[tuple[str, str]], score_fn: Callable[[str], float], cutoff: float, tol: float = 1e-9) -> dict:
    """pairs: (original_resume, swapped_resume). Counts score changes and selection flips."""
    changed = flips = 0
    deltas = []
    for orig, swapped in pairs:
        a, b = score_fn(orig), score_fn(swapped)
        d = abs(a - b)
        deltas.append(d)
        changed += d > tol
        flips += (a >= cutoff) != (b >= cutoff)
    n = len(pairs)
    return {
        "pairs": n,
        "score_changed": changed,
        "selection_flips": flips,
        "flip_rate": round(flips / n, 4) if n else 0.0,
        "max_abs_delta": round(max(deltas), 2) if deltas else 0.0,
        "passes": flips == 0 and changed == 0,
    }
