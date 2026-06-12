# Experiment 196: Candidate Confidence Row-Sanitization Hardening

## Purpose

Harden flattened candidate-confidence rows so non-finite optional numeric
fields are serialized as missing/null values.

## 663: Candidate Confidence Row-Sanitization Hardening

Output:

```text
outputs/experiments/663_candidate_confidence_row_sanitization_hardening
```

Command:

```text
Patch inversion/candidate_confidence.py so summarize_case_confidence() nulls
non-finite optional numeric fields and competing-geometry comparison tolerates
malformed x/z fields. Add focused regression tests.
```

Artifacts:

```text
README.md
data/candidate_confidence_row_sanitization_hardening.json
run_manifest.json
```

Validation:

```text
tests/test_candidate_confidence.py: 8 passed in 0.02 s
tests/test_coordinate_objective_diagnostic_report.py tests/test_coordinate_confidence_aggregate.py: 22 passed in 0.29 s
full pytest: 266 passed in 24.35 s
git diff --check: clean after run 663
```

## Interpretation

The candidate-confidence helper now emits JSON-safe nulls for unavailable
optional numerics and no longer risks NaN/inf values leaking into downstream
report JSON or CSV artifacts.

## Next Decision

Refresh commit-preparation and next-action queue pointers so local validation
points to run 663.

