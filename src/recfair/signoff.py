"""Human sign-off gate. A shortlist moves DRAFT -> AUDITED -> APPROVED -> RELEASED.

Rules: release needs a passing fairness audit, an approval by a named human reviewer who is not
the agent that drafted it, and every entry must have reasons. A failed audit can only be
overridden by a reviewer with a written justification (logged)."""

from __future__ import annotations

from dataclasses import dataclass, field

from .audit import AuditLog
from .scorer import Match, explained

AGENT_IDS = {"match-agent", "audit-agent"}


class GateError(Exception):
    pass


@dataclass
class Shortlist:
    job_id: str
    matches: list[Match]
    log: AuditLog
    state: str = "DRAFT"
    audit: dict | None = None
    approver: str | None = None
    notes: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.log.append("shortlist.drafted", {"job": self.job_id, "size": len(self.matches), "by": "match-agent"})

    def attach_audit(self, audit: dict) -> None:
        if self.state != "DRAFT":
            raise GateError(f"cannot audit in state {self.state}")
        self.audit = audit
        self.state = "AUDITED"
        self.log.append("shortlist.audited", {"job": self.job_id, "passes": audit["passes"]})

    def approve(self, reviewer: str, override_reason: str | None = None) -> None:
        if self.state != "AUDITED":
            raise GateError(f"cannot approve in state {self.state}")
        if not reviewer or reviewer in AGENT_IDS:
            raise GateError("approval must come from a named human reviewer, not an agent")
        if not all(explained(m) for m in self.matches):
            raise GateError("every match needs reasons that add up to its score")
        if not self.audit["passes"]:
            if not override_reason or len(override_reason.strip()) < 20:
                raise GateError("fairness audit failed; a written override reason (20+ chars) is required")
            self.notes.append(override_reason)
            self.log.append("shortlist.override", {"job": self.job_id, "reviewer": reviewer, "reason": override_reason})
        self.approver = reviewer
        self.state = "APPROVED"
        self.log.append("shortlist.approved", {"job": self.job_id, "reviewer": reviewer})

    def reject(self, reviewer: str, reason: str) -> None:
        if self.state in ("RELEASED",):
            raise GateError("already released")
        self.state = "REJECTED"
        self.log.append("shortlist.rejected", {"job": self.job_id, "reviewer": reviewer, "reason": reason})

    def release(self) -> list[str]:
        if self.state != "APPROVED":
            raise GateError(f"cannot release in state {self.state}; human approval required")
        self.state = "RELEASED"
        self.log.append("shortlist.released", {"job": self.job_id, "ids": [m.pid for m in self.matches]})
        return [m.pid for m in self.matches]
