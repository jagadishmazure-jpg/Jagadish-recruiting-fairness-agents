"""Skills extraction from REDACTED resume text. Refuses text that still holds PII."""

from __future__ import annotations

import re

from .data import ALIASES, SKILLS
from .pii import EMAIL, PHONE, SafeError

_LOOKUP: dict[str, str] = {s: s for s in SKILLS}
for canon, alts in ALIASES.items():
    for a in alts:
        _LOOKUP[a] = canon
YEARS = re.compile(r"(\d{1,2})\s+years?")


def extract(redacted: str) -> dict:
    if EMAIL.search(redacted) or PHONE.search(redacted):
        raise SafeError("extract() got unredacted text: " + redacted[:80])
    low = redacted.lower()
    found = set()
    for alias, canon in sorted(_LOOKUP.items(), key=lambda kv: -len(kv[0])):
        if re.search(rf"(?<![\w-]){re.escape(alias)}(?![\w-])", low):
            found.add(canon)
    m = YEARS.search(low)
    return {"skills": sorted(found), "years": int(m.group(1)) if m else 0}
