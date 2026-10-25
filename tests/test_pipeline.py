import json

import pytest

from recfair.cli import demo, main

JOBS = ["J1", "J2", "J3", "J4"]


def test_no_leaks(result):
    assert result["redaction"]["leaks_after_redaction"] == 0


def test_extraction_exact(result):
    assert result["extraction_exact"] == 1.0


@pytest.mark.parametrize("j", JOBS)
def test_transparent_name_swap_clean(result, j):
    assert result["jobs"][j]["transparent"]["name_swap"]["passes"]


@pytest.mark.parametrize("j", JOBS)
def test_baseline_name_swap_caught(result, j):
    assert result["jobs"][j]["biased_baseline_simulated"]["name_swap"]["selection_flips"] > 0


@pytest.mark.parametrize("j", JOBS)
def test_baseline_fails_four_fifths(result, j):
    assert not result["jobs"][j]["biased_baseline_simulated"]["four_fifths"]["passes"]


@pytest.mark.parametrize("j", JOBS)
def test_baseline_gap_significant(result, j):
    assert result["jobs"][j]["biased_baseline_simulated"]["four_fifths"]["p_value"] < 0.01


@pytest.mark.parametrize("j", JOBS)
def test_transparent_gap_not_significant(result, j):
    # Known behaviour kept visible: at n=400 some transparent ratios dip under 0.8 from noise alone.
    assert result["jobs"][j]["transparent"]["four_fifths"]["p_value"] > 0.05


def test_known_small_sample_four_fifths_misses_visible(result):
    fails = [j for j in JOBS if not result["jobs"][j]["transparent"]["four_fifths"]["passes"]]
    assert fails == ["J1", "J3", "J4"]


def test_all_explained(result):
    for j in JOBS:
        assert result["jobs"][j]["transparent"]["explained"] == 400


def test_log_verified(result):
    assert result["audit_log"]["verified"]


def test_demo_end_to_end(tmp_path):
    r = demo(200, 7, tmp_path, scale_n=400)
    assert r["gate"]["blocked_without_approval"] and r["gate"]["released_after_approval"] == 5
    assert r["tamper"]["detected_at"] == 2
    assert (tmp_path / "audit_log.jsonl").exists()
    assert json.loads((tmp_path / "results.json").read_text())["candidates"] == 200


def test_outputs_have_no_pii(tmp_path):
    demo(200, 7, tmp_path, scale_n=200)
    text = (tmp_path / "results.json").read_text() + (tmp_path / "audit_log.jsonl").read_text()
    assert "@example.test" not in text and "555-" not in text


def test_cli_board(tmp_path, capsys):
    assert main(["demo", "--n", "100", "--scale-n", "100", "--out", str(tmp_path), "--board"]) == 0
    assert (tmp_path / "evidence_board.png").stat().st_size > 10000 and "J1:" in capsys.readouterr().out
