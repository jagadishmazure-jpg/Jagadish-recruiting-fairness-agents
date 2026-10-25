import pytest

from recfair.data import JOBS, Job
from recfair.extract import extract
from recfair.pii import redact
from recfair.scorer import biased_score, explained, score


@pytest.mark.parametrize(
    "alias,canon",
    [
        ("py3", "python"),
        ("postgres", "sql"),
        ("t-sql", "sql"),
        ("k8s", "kubernetes"),
        ("ts", "typescript"),
        ("torch", "pytorch"),
        ("stats", "statistics"),
        ("golang", "go"),
        ("cloud infrastructure", "aws"),
    ],
)
def test_alias_maps(alias, canon):
    assert canon in extract(f"Skills: {alias}")["skills"]


def test_years():
    assert extract("engineer with 7 years of experience")["years"] == 7


def test_years_missing_defaults_zero():
    assert extract("Skills: python")["years"] == 0


def test_no_substring_false_positive():
    assert "go" not in extract("Skills: mongodb, django")["skills"]


def test_extraction_exact_on_all(cands):
    for c in cands:
        f = extract(redact(c.resume)[0])
        assert set(f["skills"]) == set(c.skills) and f["years"] == c.years


J = Job("T", "Test", ("python", "sql"), ("docker",), 4)


def test_full_score():
    m = score(J, {"skills": ["python", "sql", "docker"], "years": 5}, "p")
    assert m.score == 100.0


def test_zero_score():
    assert score(J, {"skills": [], "years": 0}, "p").score == 0.0


def test_partial_score():
    assert score(J, {"skills": ["python"], "years": 2}, "p").score == 40.0


def test_missing_reason_listed():
    m = score(J, {"skills": ["python"], "years": 2}, "p")
    assert any("missing required: sql" in r for r in m.reasons)


def test_every_reason_has_points():
    m = score(J, {"skills": ["python", "docker"], "years": 9}, "p")
    assert sum("->" in r for r in m.reasons) == 3


@pytest.mark.parametrize("job", JOBS, ids=lambda j: j.job_id)
def test_all_matches_explained(job, cands):
    for c in cands[:100]:
        assert explained(score(job, extract(redact(c.resume)[0]), "p"))


def test_explained_detects_tampered_score():
    m = score(J, {"skills": ["python"], "years": 2}, "p")
    m.score += 5
    assert not explained(m)


def test_min_years_zero_full_credit():
    j = Job("Z", "Z", ("python",), (), 0)
    assert score(j, {"skills": ["python"], "years": 0}, "p").score == 80.0


def test_score_ignores_name():
    f = {"skills": ["python", "sql"], "years": 5}
    assert score(J, f, "a").score == score(J, f, "b").score


def test_biased_baseline_adds_bonus_for_pool_a():
    f = {"skills": ["python"], "years": 2}
    assert biased_score(J, f, "p", "Arlen X\n").score == 55.0
    assert biased_score(J, f, "p", "Kaveh X\n").score == 40.0


def test_biased_baseline_is_labelled():
    m = biased_score(J, {"skills": [], "years": 0}, "p", "Arlen X\n")
    assert any("SIMULATED BIAS" in r for r in m.reasons) and explained(m)


def test_biased_empty_resume():
    assert biased_score(J, {"skills": [], "years": 0}, "p", "").score == 0.0
