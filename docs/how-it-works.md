# How it works

1. **Generate.** `make_candidates(400, seed=7)` makes 400 people, alternating group A and B. Group A gets a first name from one invented pool, group B from another. Skills (3 to 8 of 16) and years (0 to 12) are drawn the same way for both groups, so a fair scorer should select both at similar rates.
2. **Redact.** `redact()` learns the name from the header line, then replaces emails, SSN-like IDs, phone numbers and every later mention of the name with tags. The run counts what it removed and re-checks each output for leftovers.
3. **Pseudonymise.** Candidate IDs become `P_` + 12 hex chars of an HMAC-SHA256 keyed by `RECFAIR_HMAC_KEY`.
4. **Extract.** `extract()` only accepts redacted text (it raises a redacted `SafeError` otherwise). It maps aliases like `k8s` to `kubernetes` and reads years of experience.
5. **Score.** 60 points for required skills, 20 for nice-to-haves, 20 for experience against the minimum. Each part becomes a reason line ending in its points, plus a line naming missing required skills. `explained()` checks the lines add up to the score.
6. **Audit.** For each job and each scorer: selection at score >= 70, rate per group with a Wilson 95% interval, impact ratio (lowest rate / highest rate) against 0.8, a two-proportion p-value, and a name swap: the same resume with the first name replaced by one from the other pool, rescored end to end.
7. **Gate.** A shortlist is drafted by `match-agent`, gets the audit result, then must be approved by a named human (agents are refused). If the audit failed, approval needs a written reason of at least 20 characters, which is logged. Only then can it be released, and only pseudonymous IDs leave.
8. **Log.** Every step appends `{seq, event, payload, prev, hash}`; `hash = sha256(prev, seq, event, payload)`. Editing, deleting or reordering any entry breaks `verify()`.
9. **Scale check.** The demo reruns the audit at 4,000 candidates to separate noise from real gaps.
