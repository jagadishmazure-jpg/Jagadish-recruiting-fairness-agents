# Limitations and known failures

- **Synthetic data only.** Two invented name pools stand in for groups. Real demographic data is sensitive, often missing and self-reported; collecting it needs consent and legal review.
- **Four-fifths rule is noisy at small n (kept visible as a test).** At 400 candidates and a 70-point cutoff, only 11 to 33 people per group are selected, so three of four jobs fall under 0.8 for the name-blind scorer with p between 0.32 and 0.38. At 4,000 they are all above 0.9. `test_known_small_sample_four_fifths_misses_visible` pins this.
- **Only names are swapped.** Real proxies include school, address, employment gaps, club memberships and writing style. A clean name swap does not prove those are clean.
- **Two groups only, no intersectional analysis.**
- **Rule-based extraction.** 100% exact here because the generator and extractor share a vocabulary; real resumes would score lower and need an evaluated extractor.
- **Redaction is pattern based.** Names are learned from the header line; a resume without a name header, or with nicknames, could leak. Use a stronger detector (see Jagadish-pii-guard) before any real use.
- **Equal selection is not the whole of fairness.** Calibration and error-rate balance need ground-truth outcomes this repo does not have.
- **The biased baseline is simulated.** Its +15 bonus is hard-coded to show detection, not measured from a real model.
