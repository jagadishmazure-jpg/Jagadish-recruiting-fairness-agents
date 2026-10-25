import pytest

from recfair.data import FIRST_A, FIRST_B, make_candidates, swap_name
from recfair.fairness import four_fifths, impact_ratio, name_swap, selection_rates, two_prop_p, wilson


def rates(ka, kb, n=100):
    sel = {f"a{i}": i < ka for i in range(n)} | {f"b{i}": i < kb for i in range(n)}
    groups = {f"a{i}": "A" for i in range(n)} | {f"b{i}": "B" for i in range(n)}
    return selection_rates(sel, groups)


def test_selection_rates():
    r = rates(30, 15)
    assert r["A"]["rate"] == 0.3 and r["B"]["rate"] == 0.15


def test_impact_ratio():
    assert impact_ratio(rates(30, 15)) == 0.5


@pytest.mark.parametrize("ka,kb,ok", [(50, 40, True), (50, 39, False), (10, 10, True), (20, 16, True), (20, 15, False)])
def test_four_fifths_boundary(ka, kb, ok):
    assert four_fifths(rates(ka, kb))["passes"] is ok


def test_no_one_selected_counts_as_parity():
    assert impact_ratio(rates(0, 0)) == 1.0


def test_wilson_bounds():
    lo, hi = wilson(10, 100)
    assert 0.05 < lo < 0.1 < hi < 0.18


def test_wilson_empty():
    assert wilson(0, 0) == (0.0, 0.0)


def test_rates_carry_wilson():
    assert len(rates(30, 15)["A"]["wilson95"]) == 2


def test_two_prop_p_equal():
    assert two_prop_p(20, 100, 20, 100) == 1.0


def test_two_prop_p_large_gap_significant():
    assert two_prop_p(50, 100, 10, 100) < 0.001


def test_two_prop_p_degenerate():
    assert two_prop_p(0, 100, 0, 100) == 1.0 and two_prop_p(1, 0, 1, 1) == 1.0


def test_four_fifths_reports_p():
    assert "p_value" in four_fifths(rates(30, 15))


def test_name_swap_clean():
    r = name_swap([("a", "b")] * 5, lambda s: 50.0, 40)
    assert r["passes"] and r["selection_flips"] == 0


def test_name_swap_detects_flip():
    r = name_swap([("a", "b")], lambda s: 80.0 if s == "a" else 60.0, 70)
    assert r["selection_flips"] == 1 and not r["passes"] and r["max_abs_delta"] == 20.0


def test_name_swap_score_change_without_flip_still_fails():
    r = name_swap([("a", "b")], lambda s: 90.0 if s == "a" else 85.0, 70)
    assert r["selection_flips"] == 0 and r["score_changed"] == 1 and not r["passes"]


def test_name_swap_empty():
    assert name_swap([], lambda s: 0.0, 1)["flip_rate"] == 0.0


def test_swap_changes_only_name(cands):
    c = cands[0]
    s = swap_name(c)
    assert c.first not in s and s.split("\n")[1:][:3][1:] == c.resume.split("\n")[1:][:3][1:]


def test_swap_uses_other_pool(cands):
    for c in cands[:20]:
        first = swap_name(c).split()[0]
        assert first in (FIRST_B if c.group == "A" else FIRST_A)


def test_groups_balanced():
    cs = make_candidates(400, 7)
    assert sum(c.group == "A" for c in cs) == 200


def test_data_deterministic():
    assert make_candidates(10, 3)[5].resume == make_candidates(10, 3)[5].resume


def test_name_pools_disjoint():
    assert not set(FIRST_A) & set(FIRST_B)
