# BEM Experiment 151: Symmetry Calibration Design Validator

Date: 2026-06-27

## Purpose

Validate the run `150` symmetry calibration-design candidate from saved tables.

Run `150` found exactly one passing calibration design on the saved project-core
case: `edge_pair_plus_inner_pair`, degree `1`, trained on receivers `0`, `2`,
`4`, and `6` and evaluated on holdout receivers `1`, `3`, and `5`. This run
checks that result directly from the generated design table and summary.

This is a CPU-only validation audit. It does not rerun FDTD, rerun BEM solvers,
compare against field data, launch GPU/HPC work, run 3D validation, or run
field FWI.

## Output

```text
outputs/bem_experiments/151_project_core_bem_symmetry_calibration_design_validator
```

Key artifacts:

```text
data/project_core_bem_symmetry_calibration_design_validation_checks.csv
data/project_core_bem_symmetry_calibration_design_validator_summary.json
figures/project_core_bem_symmetry_calibration_design_validator.png
docs/PROJECT_CORE_BEM_SYMMETRY_CALIBRATION_DESIGN_VALIDATOR.md
scripts/run_project_core_bem_symmetry_calibration_design_validator.py
scripts/test_project_core_bem_symmetry_calibration_design_validator.py
```

## Result

```text
validation checks:                 8
validation passes:                 8
blocking failures:                 0
best passing design:               edge_pair_plus_inner_pair
best passing degree:               1
best train receivers:              0;2;4;6
best holdout receivers:            1;3;5
best holdout relative L2:          0.08334442794624965
calibration design valid:          true
candidate ready:                   true
project-core bridge ready:         false
3D validation ready:               false
field FWI ready:                   false
GPU/HPC ready:                     false
```

Validation checks:

| Check | Status | Detail |
| --- | --- | --- |
| design_rows_nonempty | pass | 28 design rows |
| row_count_matches_summary | pass | 28 observed / 28 summary |
| exactly_one_design_passes | pass | 1 passing design |
| best_passing_design_matches_summary | pass | edge_pair_plus_inner_pair degree 1 |
| best_passing_receiver_sets_match | pass | train 0;2;4;6 / holdout 1;3;5 |
| best_passing_metrics_below_gate | pass | overall 0.06410622276417251 / holdout 0.08334442794624965 |
| no_no_edge_design_passes | pass | 0 no-edge passing designs |
| no_bridge_or_gpu_promotion | pass | candidate ready, bridge/3D/field/GPU still blocked |

## Interpretation

The run `150` candidate is valid. Exactly one calibration design passes, it
uses the edge pair plus inner symmetric pair at degree `1`, and no no-edge
design passes.

## Decision

Keep `edge_pair_plus_inner_pair`, degree `1`, as the next BEM adapter
candidate. Do not promote the project-core bridge, 3D validation, GPU/HPC, or
field FWI until a fresh matched case validates it.

## Validation

Focused tests:

```text
tests/test_project_core_bem_symmetry_calibration_design_validator.py
3 passed
```

Figure validation:

```text
project_core_bem_symmetry_calibration_design_validator.png
2249x840, dynamic range=255
```
