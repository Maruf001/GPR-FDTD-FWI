# Experiment 143: Objective Ratio Null-Serialization Hardening

## Purpose

Serialize unavailable objective diagnostic margin ratios as JSON null instead
of numeric NaN.

## 610: Objective Ratio Null-Serialization Hardening

Output:

```text
outputs/experiments/610_objective_ratio_null_serialization_hardening
```

Command:

```text
Patch build_ratio_rows() in run_coordinate_objective_diagnostic_report.py and
update the unavailable-margin regression.
```

Artifacts:

```text
README.md
data/objective_ratio_null_serialization_hardening.json
run_manifest.json
```

Validation:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q tests/test_coordinate_objective_diagnostic_report.py tests/test_coordinate_confidence_aggregate.py
21 passed in 0.18 s

/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q
262 passed in 24.22 s

git diff --check: clean after run 610
```

## Interpretation

Unavailable objective diagnostic margin comparisons now serialize as null while
plotting and summary code continue to treat them as unavailable values.

## Next Decision

Run the objective diagnostic CLI smoke with sparse and non-finite inputs.
