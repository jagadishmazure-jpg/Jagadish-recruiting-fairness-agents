# Purpose

**Problem.** A staffing firm screens hundreds of resumes per opening. Automating that saves time, but an automated screen can encode bias: if it reacts to a name, a school or a postcode, it can lower one group's chances without anyone noticing.

**What this repo shows.** A small, fully local recruiting pipeline for Brightwell Staffing (fictional) where each risk has a control you can test:

| Risk | Control in this repo |
|---|---|
| Personal data leaks into scoring, logs or errors | Redaction runs first; SafeError and a redacting log filter; audit log refuses PII |
| Score cannot be explained | Every point is tied to a written reason; reasons must add up to the score |
| Disparate impact | Selection rates by group, four-fifths rule, p-value, Wilson intervals |
| Name-based bias | Counterfactual name swap: same resume, other pool's name, measure flips |
| Automation without accountability | No release without a named human; overrides need a written reason |
| Records can be altered later | Hash-chained audit log |

**Who it is for.** Hiring managers and recruiters checking that an AI screen is fair, engineers building one, and interviewers evaluating AI Engineer / FDE candidates on responsible AI in a regulated domain.
