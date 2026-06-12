# Experiment 139: Optional Numeric Non-Finite Reporting Hardening

## Purpose

Make optional numeric reporting fields robust to non-finite and malformed values
in coordinate confidence aggregates and objective diagnostic reports.

## 606: Optional Numeric Non-Finite Reporting Hardening

Output:

```text
outputs/experiments/606_optional_numeric_nonfinite_reporting_hardening
```

Command:

```text
Patch optional numeric handling in run_coordinate_confidence_aggregate.py and
run_coordinate_objective_diagnostic_report.py, then add focused regressions for
non-finite and malformed values.
```

Artifacts:

```text
README.md
data/optional_numeric_nonfinite_reporting_hardening.json
run_manifest.json
```

Validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q tests/test_coordinate_objective_diagnostic_report.py tests/test_coordinate_confidence_aggregate.py
21 passed in 0.21 s

/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q
262 passed in 24.42 s

git diff --check: clean after run 606
```

## Interpretation

Optional numeric fields now degrade to missing data instead of emitting NaNs or
raising conversion errors. This keeps summary counts, figure notes, and plots
usable when legacy or sparse rows contain malformed optional metrics.

## Next Decision

Refresh the commit/PR summary and next-action queue so current local validation
points to run 606 while the run 595 archive remains the current packaged
handoff.
