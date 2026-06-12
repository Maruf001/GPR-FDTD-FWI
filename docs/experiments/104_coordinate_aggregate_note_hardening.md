# Experiment 104: Coordinate Aggregate Note Hardening

## Purpose

Record the reporting-code hardening found during the post-summary code review.

## 571: Coordinate Aggregate Note Hardening

Output:

```text
outputs/experiments/571_coordinate_aggregate_note_hardening
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q \
  tests/test_coordinate_objective_diagnostic_report.py \
  tests/test_coordinate_confidence_aggregate.py

/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q

git diff --check
```

Artifacts:

```text
README.md
run_manifest.json
```

Validation:

```text
focused objective/confidence tests: 17 passed in 0.20 s
full pytest: 258 passed in 24.32 s
git diff --check: clean after run 571
```

## Interpretation

The aggregate confidence figure notes now render missing maximum ambiguity
widths as `not_recorded`. This is a documentation/reporting robustness change,
not a scientific-claim or optimizer-behavior change.

## Next Decision

Refresh the commit/PR summary again because the runtime code/test surface now
includes this additional hardening and the full suite count is 258.
