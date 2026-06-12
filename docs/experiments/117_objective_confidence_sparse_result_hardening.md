# Experiment 117: Objective Confidence Sparse-Result Hardening

## Purpose

Harden the objective diagnostic report against sparse saved objective-result
metadata that lacks a complete top-candidate x/z/r geometry.

## 584: Objective Confidence Sparse-Result Hardening

Output:

```text
outputs/experiments/584_objective_confidence_sparse_result_hardening
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
data/objective_confidence_sparse_result_hardening.json
run_manifest.json
```

Validation:

```text
focused objective/confidence tests: 18 passed in 0.19 s
full pytest: 259 passed in 24.01 s
git diff --check: clean after run 584
```

## Interpretation

Objective confidence rows now tolerate sparse metadata by emitting `None`
geometry-error fields and a plain false `is_truth_geometry` flag when best
x/z/r values are unavailable. This prevents a reporting crash without changing
objective selection, scientific claims, or the current archive.

## Next Decision

Refresh the current next-action queue so run 584 becomes the local validation
checkpoint after the run 580 packaged archive.
