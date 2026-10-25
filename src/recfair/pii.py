"""PII redaction that runs BEFORE any scoring, logging or error message.

- Emails, phone numbers, SSN-like numbers and the header name line are replaced by tags.
- Names that recur later in the text are removed too (the header name is learned first).
- Candidate IDs are pseudonymised with a keyed HMAC (key from RECFAIR_HMAC_KEY).
- SafeError and the RedactingFilter make sure errors and logs never carry raw resume text.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
import re

EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE = re.compile(r"(?:\+?\d{1,2}[ .-]?)?\(?\d{3}\)?[ .-]?\d{3}[ .-]?\d{4}")
SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
NAME_LINE = re.compile(r"^\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\s*$", re.M)
DEV_KEY = "dev-only-key-rotate-me"


def hmac_key() -> bytes:
    return os.environ.get("RECFAIR_HMAC_KEY", DEV_KEY).encode()


def pseudonym(value: str, key: bytes | None = None) -> str:
    return "P_" + hmac.new(key or hmac_key(), value.encode(), hashlib.sha256).hexdigest()[:12]


def redact(text: str) -> tuple[str, dict[str, int]]:
    counts = {"email": 0, "phone": 0, "ssn": 0, "name": 0}
    names: list[str] = []
    m = NAME_LINE.search(text.split("\n", 1)[0] + "\n") if text else None
    if m:
        names = m.group(1).split()
    text, counts["email"] = EMAIL.subn("[EMAIL]", text)
    text, counts["ssn"] = SSN.subn("[ID]", text)
    text, counts["phone"] = PHONE.subn("[PHONE]", text)
    for nm in names:
        text, k = re.subn(rf"\b{re.escape(nm)}\b", "[NAME]", text)
        counts["name"] += k
    return text, counts


def contains_pii(text: str, names: list[str] = ()) -> bool:
    if EMAIL.search(text) or PHONE.search(text) or SSN.search(text):
        return True
    return any(re.search(rf"\b{re.escape(n)}\b", text) for n in names)


class SafeError(Exception):
    """Error whose message is redacted before it is stored, so tracebacks never leak PII."""

    def __init__(self, message: str):
        super().__init__(redact(message)[0])


class RedactingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = redact(record.getMessage())[0]
        record.args = ()
        return True


def get_logger(name: str = "recfair") -> logging.Logger:
    log = logging.getLogger(name)
    if not any(isinstance(f, RedactingFilter) for f in log.filters):
        log.addFilter(RedactingFilter())
    return log
