# Model card: Brightwell transparent match scorer v0.1

| Field | Value |
|---|---|
| Type | Deterministic weighted rule score, not a learned model |
| Inputs | Redacted resume text -> skills set, years of experience; job requirements |
| Output | Score 0-100 with reason lines; shortlist candidate if >= 70 |
| Intended use | Rank synthetic candidates in a demo of a human-reviewed screen |
| Out of scope | Automated rejection; any use on real people without legal review, notice and validation |
| Protected attributes | Not used; group labels only enter the audit |
| Training data | None (rules). Evaluation data: 400 synthetic candidates, seed 7; scale check 4,000 |
| Owner | Portfolio demo by Jagadish Meduri |

## Evaluation (measured, synthetic)
<!-- BEGIN:headline -->
| What | Measured (synthetic data, seed 7) |
|---|---|
| Candidates | 400 (scale check 4000) |
| PII redacted before scoring | 400 emails, 400 phones, 1200 name mentions; 0 left |
| Skills + years extracted exactly | 100.0% |
| Transparent scorer impact ratio, n=400 | J1 0.7222, J2 0.9167, J3 0.75, J4 0.7879 |
| Transparent scorer impact ratio, n=4000 | J1 0.9752, J2 0.9545, J3 0.9138, J4 0.9038 |
| Biased baseline (simulated) impact ratio, n=4000 | J1 0.3214, J2 0.3348, J3 0.3302, J4 0.4379 |
| Name-swap selection flips, transparent / baseline | J1 0 / 76, J2 0 / 69, J3 0 / 76, J4 0 / 66 |
| Release without human approval | blocked = True; override with written reason used = True |
| Audit log | 10 entries, chain verified = True; edited entry detected at seq 2 |
| Tests | 122 |
<!-- END:headline -->

## Ethical considerations
Rules can still discriminate if the requirements themselves are biased (for example, inflated year minimums). Requirements should be job-related and reviewed. Humans make the decision; the score is an aid.

## Caveats
See [limitations.md](limitations.md).
