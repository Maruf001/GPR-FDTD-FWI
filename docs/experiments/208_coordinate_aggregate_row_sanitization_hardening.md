# Experiment 208: Coordinate Aggregate Row-Sanitization Hardening

## Purpose

Harden the coordinate confidence aggregate report so raw confidence rows do not
carry non-finite optional numeric values into JSON or CSV artifacts.

## 675: Coordinate Aggregate Row-Sanitization Hardening

Output:

```text
outputs/experiments/675_coordinate_aggregate_row_sanitization_hardening
```

Command:

```text
Patch run_coordinate_confidence_aggregate.py so summary metadata and optional
numeric confidence-row fields are finite-normalized before aggregation and
serialization. Add focused regression tests.
```

Artifacts:

```text
README.md
data/coordinate_aggregate_row_sanitization_hardening.json
run_manifest.json
```

Validation:

```text
tests/test_coordinate_confidence_aggregate.py: 9 passed in 0.19 s
tests/test_coordinate_objective_diagnostic_report.py tests/test_candidate_confidence.py: 21 passed in 0.28 s
full pytest: 266 passed in 24.28 s
git diff --check: clean after run 675
```

## Interpretation

The aggregate report now writes JSON-safe nulls for unavailable optional row
numerics and sanitizes non-finite metadata such as Tx/Rx offset and frequency.

## Next Decision

Run a small aggregate CLI smoke with non-finite row values so artifact-level
JSON/CSV/plot behavior is validated.

