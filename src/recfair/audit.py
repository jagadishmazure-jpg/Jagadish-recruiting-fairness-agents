"""Hash-chained, append-only audit log. Each entry stores the hash of the previous entry, so
editing, deleting or reordering any line breaks verification. Payloads must be PII-free."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .pii import SafeError, contains_pii

GENESIS = "0" * 64


def _h(prev: str, seq: int, event: str, payload: dict) -> str:
    body = json.dumps({"prev": prev, "seq": seq, "event": event, "payload": payload}, sort_keys=True)
    return hashlib.sha256(body.encode()).hexdigest()


class AuditLog:
    def __init__(self) -> None:
        self.entries: list[dict] = []

    @property
    def head(self) -> str:
        return self.entries[-1]["hash"] if self.entries else GENESIS

    def append(self, event: str, payload: dict) -> dict:
        if contains_pii(json.dumps(payload)):
            raise SafeError(f"audit payload for {event} contains PII; redact first")
        seq = len(self.entries)
        e = {"seq": seq, "event": event, "payload": payload, "prev": self.head}
        e["hash"] = _h(e["prev"], seq, event, payload)
        self.entries.append(e)
        return e

    def verify(self) -> tuple[bool, int | None]:
        prev = GENESIS
        for i, e in enumerate(self.entries):
            if e.get("seq") != i or e.get("prev") != prev or e.get("hash") != _h(prev, i, e["event"], e["payload"]):
                return False, i
            prev = e["hash"]
        return True, None

    def dump(self, path: Path) -> None:
        path.write_text("".join(json.dumps(e, sort_keys=True) + "\n" for e in self.entries))

    @classmethod
    def load(cls, path: Path) -> AuditLog:
        log = cls()
        log.entries = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        return log
