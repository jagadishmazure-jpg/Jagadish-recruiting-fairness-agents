# Implementation guide for adopters

1. **Write job requirements first** and check they are job-related; the scorer is only as fair as its requirements.
2. **Put redaction at the front door.** Nothing downstream should see raw resumes. Add your detector (checksums, NER) and keep a leak test on every run.
3. **Keep the score explainable.** If you swap in a learned model, keep a reason output and a test that reasons match the score.
4. **Separate protected data.** Store any self-reported demographics apart, joined only by pseudonymous ID inside the audit job.
5. **Audit every requisition.** Rates by group with intervals, the four-fifths ratio, a significance test, and counterfactual swaps (names first, then other proxies).
6. **Decide policy for small samples** before you see results: pool requisitions, or require human review with written reasons when the ratio fails.
7. **Gate on people.** A named reviewer approves; agents never do. Log every override.
8. **Keep the chain.** Anchor the latest log hash somewhere separate (e.g. a daily signed note) so the whole log cannot be rewritten.
9. **Tell candidates** an automated tool is used and how to ask for a human review.
10. **Re-run the audit** whenever requirements, cutoff or model change; CI should fail if a name swap moves any score.
