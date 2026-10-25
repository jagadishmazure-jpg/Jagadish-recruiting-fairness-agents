# Results (generated from results/results.json)

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

<!-- BEGIN:results -->
```json
{
  "candidates": 400,
  "seed": 7,
  "cutoff": 70.0,
  "redaction": {
    "email": 400,
    "phone": 400,
    "ssn": 0,
    "name": 1200,
    "leaks_after_redaction": 0
  },
  "extraction_exact": 1.0,
  "jobs": {
    "J1": {
      "title": "Data Engineer",
      "transparent": {
        "rates": {
          "A": {
            "n": 200,
            "selected": 18,
            "rate": 0.09,
            "wilson95": [
              0.0577,
              0.1378
            ]
          },
          "B": {
            "n": 200,
            "selected": 13,
            "rate": 0.065,
            "wilson95": [
              0.0384,
              0.108
            ]
          }
        },
        "four_fifths": {
          "impact_ratio": 0.7222,
          "threshold": 0.8,
          "passes": false,
          "p_value": 0.3498
        },
        "name_swap": {
          "pairs": 400,
          "score_changed": 0,
          "selection_flips": 0,
          "flip_rate": 0.0,
          "max_abs_delta": 0.0,
          "passes": true
        },
        "explained": 400,
        "passes": false
      },
      "biased_baseline_simulated": {
        "rates": {
          "A": {
            "n": 200,
            "selected": 56,
            "rate": 0.28,
            "wilson95": [
              0.2224,
              0.3459
            ]
          },
          "B": {
            "n": 200,
            "selected": 13,
            "rate": 0.065,
            "wilson95": [
              0.0384,
              0.108
            ]
          }
        },
        "four_fifths": {
          "impact_ratio": 0.2321,
          "threshold": 0.8,
          "passes": false,
          "p_value": 0.0
        },
        "name_swap": {
          "pairs": 400,
          "score_changed": 400,
          "selection_flips": 76,
          "flip_rate": 0.19,
          "max_abs_delta": 15.0,
          "passes": false
        },
        "explained": 400,
        "passes": false
      }
    },
    "J2": {
      "title": "Platform Engineer",
      "transparent": {
        "rates": {
          "A": {
            "n": 200,
            "selected": 12,
            "rate": 0.06,
            "wilson95": [
              0.0347,
              0.1019
            ]
          },
          "B": {
            "n": 200,
            "selected": 11,
            "rate": 0.055,
            "wilson95": [
              0.031,
              0.0958
            ]
          }
        },
        "four_fifths": {
          "impact_ratio": 0.9167,
          "threshold": 0.8,
          "passes": true,
          "p_value": 0.8299
        },
        "name_swap": {
          "pairs": 400,
          "score_changed": 0,
          "selection_flips": 0,
          "flip_rate": 0.0,
          "max_abs_delta": 0.0,
          "passes": true
        },
        "explained": 400,
        "passes": true
      },
      "biased_baseline_simulated": {
        "rates": {
          "A": {
            "n": 200,
            "selected": 46,
            "rate": 0.23,
            "wilson95": [
              0.1771,
              0.2931
            ]
          },
          "B": {
            "n": 200,
            "selected": 11,
            "rate": 0.055,
            "wilson95": [
              0.031,
              0.0958
            ]
          }
        },
        "four_fifths": {
          "impact_ratio": 0.2391,
          "threshold": 0.8,
          "passes": false,
          "p_value": 0.0
        },
        "name_swap": {
          "pairs": 400,
          "score_changed": 400,
          "selection_flips": 69,
          "flip_rate": 0.1725,
          "max_abs_delta": 15.0,
          "passes": false
        },
        "explained": 400,
        "passes": false
      }
    },
    "J3": {
      "title": "ML Engineer",
      "transparent": {
        "rates": {
          "A": {
            "n": 200,
            "selected": 15,
            "rate": 0.075,
            "wilson95": [
              0.046,
              0.12
            ]
          },
          "B": {
            "n": 200,
            "selected": 20,
            "rate": 0.1,
            "wilson95": [
              0.0657,
              0.1494
            ]
          }
        },
        "four_fifths": {
          "impact_ratio": 0.75,
          "threshold": 0.8,
          "passes": false,
          "p_value": 0.3763
        },
        "name_swap": {
          "pairs": 400,
          "score_changed": 0,
          "selection_flips": 0,
          "flip_rate": 0.0,
          "max_abs_delta": 0.0,
          "passes": true
        },
        "explained": 400,
        "passes": false
      },
      "biased_baseline_simulated": {
        "rates": {
          "A": {
            "n": 200,
            "selected": 57,
            "rate": 0.285,
            "wilson95": [
              0.2269,
              0.3512
            ]
          },
          "B": {
            "n": 200,
            "selected": 20,
            "rate": 0.1,
            "wilson95": [
              0.0657,
              0.1494
            ]
          }
        },
        "four_fifths": {
          "impact_ratio": 0.3509,
          "threshold": 0.8,
          "passes": false,
          "p_value": 0.0
        },
        "name_swap": {
          "pairs": 400,
          "score_changed": 400,
          "selection_flips": 76,
          "flip_rate": 0.19,
          "max_abs_delta": 15.0,
          "passes": false
        },
        "explained": 400,
        "passes": false
      }
    },
    "J4": {
      "title": "Frontend Engineer",
      "transparent": {
        "rates": {
          "A": {
            "n": 200,
            "selected": 33,
            "rate": 0.165,
            "wilson95": [
              0.12,
              0.2227
            ]
          },
          "B": {
            "n": 200,
            "selected": 26,
            "rate": 0.13,
            "wilson95": [
              0.0903,
              0.1837
            ]
          }
        },
        "four_fifths": {
          "impact_ratio": 0.7879,
          "threshold": 0.8,
          "passes": false,
          "p_value": 0.3236
        },
        "name_swap": {
          "pairs": 400,
          "score_changed": 0,
          "selection_flips": 0,
          "flip_rate": 0.0,
          "max_abs_delta": 0.0,
          "passes": true
        },
        "explained": 400,
        "passes": false
      },
      "biased_baseline_simulated": {
        "rates": {
          "A": {
            "n": 200,
            "selected": 63,
            "rate": 0.315,
            "wilson95": [
              0.2546,
              0.3824
            ]
          },
          "B": {
            "n": 200,
            "selected": 26,
            "rate": 0.13,
            "wilson95": [
              0.0903,
              0.1837
            ]
          }
        },
        "four_fifths": {
          "impact_ratio": 0.4127,
          "threshold": 0.8,
          "passes": false,
          "p_value": 0.0
        },
        "name_swap": {
          "pairs": 400,
          "score_changed": 400,
          "selection_flips": 66,
          "flip_rate": 0.165,
          "max_abs_delta": 15.0,
          "passes": false
        },
        "explained": 400,
        "passes": false
      }
    }
  },
  "audit_log": {
    "entries": 10,
    "verified": true
  },
  "gate": {
    "override_used": true,
    "blocked_without_approval": true,
    "released_after_approval": 5,
    "top_reasons_example": [
      "required 3/3 (python, sql, airflow) -> 60.0",
      "nice-to-have 2/3 (dbt, aws) -> 13.3",
      "experience 10y vs 3y minimum -> 20.0"
    ]
  },
  "tamper": {
    "detected_at": 2
  },
  "scale_check": {
    "candidates": 4000,
    "transparent_impact_ratio": {
      "J1": 0.9752,
      "J2": 0.9545,
      "J3": 0.9138,
      "J4": 0.9038
    },
    "baseline_impact_ratio": {
      "J1": 0.3214,
      "J2": 0.3348,
      "J3": 0.3302,
      "J4": 0.4379
    }
  }
}
```
<!-- END:results -->
