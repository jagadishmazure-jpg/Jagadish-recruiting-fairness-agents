import logging

import pytest

from recfair.extract import extract
from recfair.pii import SafeError, contains_pii, get_logger, pseudonym, redact

SAMPLE = "Arlen Ashgrove\nEmail: arlen.ashgrove1@example.test | Phone: 555-123-4567\nSSN 123-45-6789\nNotes: Arlen likes code review.\n"


def test_email_redacted():
    assert "@" not in redact(SAMPLE)[0]


def test_phone_redacted():
    assert "555-123-4567" not in redact(SAMPLE)[0]


def test_ssn_redacted():
    assert "123-45-6789" not in redact(SAMPLE)[0]


def test_header_name_and_repeats_redacted():
    out, c = redact(SAMPLE)
    assert "Arlen" not in out and "Ashgrove" not in out and c["name"] == 3


def test_counts():
    _, c = redact(SAMPLE)
    assert c["email"] == 1 and c["phone"] == 1 and c["ssn"] == 1


@pytest.mark.parametrize("phone", ["555-123-4567", "(555) 123-4567", "555.123.4567", "+1 555 123 4567"])
def test_phone_formats(phone):
    assert "[PHONE]" in redact(f"x\ncall {phone}")[0]


def test_empty_text():
    assert redact("") == ("", {"email": 0, "phone": 0, "ssn": 0, "name": 0})


def test_contains_pii_detects_names():
    assert contains_pii("hello Kaveh", ["Kaveh"]) and not contains_pii("hello there", ["Kaveh"])


def test_all_synthetic_resumes_clean_after_redaction(cands):
    for c in cands:
        assert not contains_pii(redact(c.resume)[0], [c.first, c.last, c.email, c.phone])


def test_pseudonym_stable_and_keyed():
    assert pseudonym("C1", b"k1") == pseudonym("C1", b"k1") != pseudonym("C1", b"k2")


def test_pseudonym_env_key(monkeypatch):
    a = pseudonym("C1")
    monkeypatch.setenv("RECFAIR_HMAC_KEY", "rotated")
    assert pseudonym("C1") != a


def test_pseudonym_hides_id():
    assert "C1" not in pseudonym("C1") and pseudonym("C1").startswith("P_")


def test_safe_error_redacts_message():
    e = SafeError("bad row for jory.dunmore@example.test 555-222-3333")
    assert "@" not in str(e) and "555-222-3333" not in str(e)


def test_extract_refuses_unredacted_and_error_is_clean():
    with pytest.raises(SafeError) as ei:
        extract("Email: a.b@example.test skills python")
    assert "a.b@example.test" not in str(ei.value)


def test_logger_redacts(caplog):
    log = get_logger("recfair.test")
    with caplog.at_level(logging.INFO, logger="recfair.test"):
        log.info("candidate %s phone %s", "x.y@example.test", "555-999-0000")
    assert "x.y@example.test" not in caplog.text and "555-999-0000" not in caplog.text and "[EMAIL]" in caplog.text


def test_logger_filter_added_once():
    log = get_logger("recfair.once")
    get_logger("recfair.once")
    assert len(log.filters) == 1
