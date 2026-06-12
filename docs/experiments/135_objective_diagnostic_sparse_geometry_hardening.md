# Experiment 135: Objective Diagnostic Sparse-Geometry Hardening

## Purpose

Close the sparse-diagnostic reporting gap adjacent to run 584 by making
objective diagnostic enrichment and ratio rows tolerate missing best-candidate
geometry.

## 602: Objective Diagnostic Sparse-Geometry Hardening

Output:

```text
outputs/experiments/602_objective_diagnostic_sparse_geometry_hardening
```

Command:

```text
Patch run_coordinate_objective_diagnostic_report.py and add a regression test
for objective_diagnostic_rows with missing best geometry.
```

Artifacts:

```text
README.md
data/objective_diagnostic_sparse_geometry_hardening.json
run_manifest.json
```

Validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q tests/test_coordinate_objective_diagnostic_report.py tests/test_coordinate_confidence_aggregate.py
19 passed in 0.19 s

/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q
260 passed in 24.15 s

git diff --check: clean after run 602
```

## Interpretation

The diagnostic reporter now distinguishes "geometry comparison unavailable"
from "variant changed geometry." Sparse or malformed diagnostic rows preserve
missing geometry as null, emit null absolute-error values, and avoid conversion
exceptions.

## Next Decision

Refresh the commit/PR summary and next-action queue so current local validation
points to run 602 while the run 595 archive remains the current packaged
handoff.
