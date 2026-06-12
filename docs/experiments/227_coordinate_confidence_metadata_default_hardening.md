# Experiment 227: Coordinate Confidence Metadata/Default Hardening

## Purpose

Fix remaining JSON-safety edges found during lightweight self-review of the
coordinate confidence reporting hardening.

## 694: Coordinate Confidence Metadata/Default Hardening

Output:

```text
outputs/experiments/694_coordinate_confidence_metadata_default_hardening
```

Command:

```text
Patch candidate-confidence metadata serialization and aggregate default Tx/Rx
offset validation; add focused regression tests.
```

Artifacts:

```text
README.md
data/coordinate_confidence_metadata_default_hardening.json
run_manifest.json
```

Validation:

```text
candidate/aggregate focused tests: 19 passed in 0.20 s
objective diagnostic tests: 13 passed in 0.28 s
full pytest: 268 passed in 24.43 s
git diff --check: clean after run 694
```

## Interpretation

The aggregate CLI now rejects non-finite or negative default Tx/Rx offsets
before row enrichment, and shared candidate-confidence rows null non-finite
numeric metadata before serialization.

## Next Decision

Run an aggregate CLI negative smoke with non-finite/default Tx/Rx values so
argument-level behavior is validated outside unit tests.

