# Risk notes

## EU AI Act
AI used to recruit or select people, filter applications or evaluate candidates is listed as **high-risk** (Annex III, employment). For a real deployment that means, in our summary:

| Obligation (high-risk) | What this repo has | Gap for real use |
|---|---|---|
| Risk management across the lifecycle | Threat model, limitations, audit per run | Formal process and sign-offs |
| Data governance, bias examination | Synthetic balanced data, fairness audit | Real-data representativeness study |
| Technical documentation | These docs, model card | Conformity-format file |
| Record keeping / logging | Hash-chained audit log | Retention policy, secure storage |
| Transparency to deployers | Reasons per score, model card | Instructions for use |
| Human oversight | Mandatory named approver, written override | Reviewer training, workload limits |
| Accuracy, robustness, cybersecurity | Tests, tamper detection, CI security | Real-world accuracy validation |

Candidates should also be told an AI system is used, and emotion recognition in the workplace is prohibited; this repo does neither.

## US practice
The four-fifths rule is a rule of thumb from US federal selection guidelines for spotting adverse impact, not a legal safe harbour. Some cities require independent bias audits of automated hiring tools and notice to candidates. This repo shows the measurement, not legal compliance.

## NIST AI RMF mapping
Govern: owner, gate, override log. Map: purpose and limitations. Measure: impact ratio, p-value, name swap, extraction accuracy. Manage: block-or-override gate, re-audit at next intake.

## GDPR
Resume data is personal data; automated decisions with significant effect need human involvement, which the gate enforces. Pseudonymisation is still personal data.
