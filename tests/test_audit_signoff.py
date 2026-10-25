import copy

import pytest

from recfair.audit import GENESIS, AuditLog
from recfair.pii import SafeError
from recfair.scorer import Match
from recfair.signoff import GateError, Shortlist


def log3():
    lg = AuditLog()
    for i in range(3):
        lg.append("e", {"i": i})
    return lg


def test_chain_links():
    lg = log3()
    assert lg.entries[0]["prev"] == GENESIS and lg.entries[1]["prev"] == lg.entries[0]["hash"]


def test_verify_ok():
    assert log3().verify() == (True, None)


def test_edit_detected():
    lg = log3()
    lg.entries[1]["payload"]["i"] = 9
    assert lg.verify() == (False, 1)


def test_delete_detected():
    lg = log3()
    del lg.entries[1]
    assert lg.verify()[0] is False


def test_reorder_detected():
    lg = log3()
    lg.entries[0], lg.entries[1] = lg.entries[1], lg.entries[0]
    assert lg.verify()[0] is False


def test_rehash_without_chain_detected():
    lg = log3()
    lg.entries[1]["hash"] = "f" * 64
    assert lg.verify() == (False, 1)


def test_roundtrip(tmp_path):
    lg = log3()
    lg.dump(tmp_path / "a.jsonl")
    assert AuditLog.load(tmp_path / "a.jsonl").verify() == (True, None)


def test_file_tamper_detected(tmp_path):
    lg = log3()
    p = tmp_path / "a.jsonl"
    lg.dump(p)
    p.write_text(p.read_text().replace('"i": 2', '"i": 3'))
    assert AuditLog.load(p).verify()[0] is False


def test_pii_payload_rejected():
    with pytest.raises(SafeError) as ei:
        AuditLog().append("x", {"who": "a.b@example.test"})
    assert "a.b@example.test" not in str(ei.value)


def test_empty_log_verifies():
    assert AuditLog().verify() == (True, None) and AuditLog().head == GENESIS


def good():
    return [Match("J1", "P_1", 60.0, ["required 1/1 (python) -> 60.0"])]


def sl(passes=True):
    s = Shortlist("J1", good(), AuditLog())
    s.attach_audit({"passes": passes})
    return s


def test_release_without_approval_blocked():
    with pytest.raises(GateError):
        sl().release()


def test_happy_path():
    s = sl()
    s.approve("reviewer.hr-lead")
    assert s.release() == ["P_1"] and s.state == "RELEASED"


def test_agent_cannot_approve():
    for who in ("match-agent", "audit-agent", ""):
        with pytest.raises(GateError):
            sl().approve(who)


def test_cannot_approve_before_audit():
    with pytest.raises(GateError):
        Shortlist("J1", good(), AuditLog()).approve("reviewer")


def test_failed_audit_needs_reason():
    with pytest.raises(GateError):
        sl(False).approve("reviewer")


def test_failed_audit_short_reason_rejected():
    with pytest.raises(GateError):
        sl(False).approve("reviewer", "ok")


def test_override_logged():
    s = sl(False)
    s.approve("reviewer", "ratio below line but p=0.35, name swap clean, re-audit")
    assert any(e["event"] == "shortlist.override" for e in s.log.entries)


def test_unexplained_match_blocks_approval():
    s = Shortlist("J1", [Match("J1", "P_1", 99.0, ["required 1/1 (python) -> 60.0"])], AuditLog())
    s.attach_audit({"passes": True})
    with pytest.raises(GateError):
        s.approve("reviewer")


def test_reject_blocks_release():
    s = sl()
    s.reject("reviewer", "not now")
    with pytest.raises(GateError):
        s.release()


def test_double_audit_blocked():
    with pytest.raises(GateError):
        sl().attach_audit({"passes": True})


def test_released_cannot_be_rejected():
    s = sl()
    s.approve("reviewer")
    s.release()
    with pytest.raises(GateError):
        s.reject("reviewer", "late")


def test_gate_events_chain_verifies():
    s = sl()
    s.approve("reviewer")
    s.release()
    assert s.log.verify() == (True, None) and [e["event"] for e in s.log.entries][-1] == "shortlist.released"


def test_log_copy_tamper():
    s = sl()
    t = copy.deepcopy(s.log)
    t.entries[0]["payload"]["size"] = 50
    assert t.verify() == (False, 0) and s.log.verify()[0]
