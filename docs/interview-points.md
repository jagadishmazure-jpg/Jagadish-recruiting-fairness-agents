# Interview points

- Why redact first: it limits what any later step can learn, and it protects logs and errors, which are often forgotten.
- Why a rule scorer: easy to explain, easy to audit; a learned model must beat it and keep reasons.
- Four-fifths in practice: at n=400 a fair scorer failed it on 3 of 4 jobs from noise (p about 0.35); at n=4,000 all were above 0.9. Pair the ratio with a significance test and intervals, and decide small-sample policy up front.
- Counterfactual name swap catches what aggregate rates hide: the simulated biased baseline flipped 66 to 76 of 400 decisions per job.
- Human oversight that is real: named approver, agents refused, written override, all logged.
- Hash chain vs database audit table: cheap tamper evidence; anchor the head hash elsewhere.
- EU AI Act: recruitment AI is high-risk; map each obligation to a control and name the gaps honestly.
