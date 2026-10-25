# Real code and real output

## Redaction (src/recfair/pii.py)
```python
text, counts["email"] = EMAIL.subn("[EMAIL]", text)
text, counts["ssn"] = SSN.subn("[ID]", text)
text, counts["phone"] = PHONE.subn("[PHONE]", text)
for nm in names:
    text, k = re.subn(rf"\b{re.escape(nm)}\b", "[NAME]", text)
```
Output on a synthetic resume:
```
[NAME] [NAME]
Email: [EMAIL] | Phone: [PHONE]
Summary: engineer with 10 years of experience.
Skills: ...
Notes: [NAME] enjoys mentoring and code review.
```

## Reasons for a match (src/recfair/scorer.py)
Real reasons for the top J1 candidate in the demo run:
```
required 3/3 (python, sql, airflow) -> 60.0
nice-to-have 2/3 (dbt, aws) -> 13.3
experience 10y vs 3y minimum -> 20.0
```

## Name swap (src/recfair/fairness.py)
```python
a, b = score_fn(orig), score_fn(swapped)
changed += abs(a - b) > tol
flips += (a >= cutoff) != (b >= cutoff)
```

## `recfair demo` console output (real run)
```
J1: transparent IR=0.7222 flips=0 | baseline IR=0.2321 flips=76
J2: transparent IR=0.9167 flips=0 | baseline IR=0.2391 flips=69
J3: transparent IR=0.75 flips=0 | baseline IR=0.3509 flips=76
J4: transparent IR=0.7879 flips=0 | baseline IR=0.4127 flips=66
scale check transparent IR: {'J1': 0.9752, 'J2': 0.9545, 'J3': 0.9138, 'J4': 0.9038}
redaction leaks=0 extraction_exact=1.0 log_verified=True
```

## Measured table (generated from results.json)
<!-- BEGIN:jobs -->
| Job | Scorer | Selected A / B (of 200 each) | Impact ratio | Four-fifths | p-value | Name-swap flips (of 400) |
|---|---|---|---|---|---|---|
| J1 Data Engineer | transparent | 18 / 13 | 0.7222 | FAIL | 0.3498 | 0 |
| J1 Data Engineer | biased baseline (simulated) | 56 / 13 | 0.2321 | FAIL | 0.0 | 76 |
| J2 Platform Engineer | transparent | 12 / 11 | 0.9167 | pass | 0.8299 | 0 |
| J2 Platform Engineer | biased baseline (simulated) | 46 / 11 | 0.2391 | FAIL | 0.0 | 69 |
| J3 ML Engineer | transparent | 15 / 20 | 0.75 | FAIL | 0.3763 | 0 |
| J3 ML Engineer | biased baseline (simulated) | 57 / 20 | 0.3509 | FAIL | 0.0 | 76 |
| J4 Frontend Engineer | transparent | 33 / 26 | 0.7879 | FAIL | 0.3236 | 0 |
| J4 Frontend Engineer | biased baseline (simulated) | 63 / 26 | 0.4127 | FAIL | 0.0 | 66 |
<!-- END:jobs -->
