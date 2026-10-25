# ADR 0001: Start with a transparent rule scorer

Status: accepted. Context: hiring is high-risk and decisions must be explainable. Decision: a weighted rule score whose reasons sum to the number; any learned model later must beat it on the same audit and still emit reasons. Consequence: less nuance, much easier review.
