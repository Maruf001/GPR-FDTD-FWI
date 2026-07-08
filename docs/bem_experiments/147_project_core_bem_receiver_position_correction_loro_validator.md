# BEM Experiment 147: Receiver-Position Correction LORO Validator

Date: 2026-06-27

## Purpose

Validate the run `146` receiver-position correction no-go result from a
consumer perspective.

Run `146` showed that a quadratic aperture-position correction improves the
leave-one-receiver-out metric but still does not pass the bridge gate. This run
checks that conclusion directly from the run `146` degree table and holdout
rows.

This is a CPU-only validation audit. It does not rerun FDTD, rerun BEM,
compare against field data, launch GPU/HPC work, run 3D validation, or run
field FWI.

## Output

```text
outputs/bem_experiments/147_project_core_bem_receiver_position_correction_loro_validator
```

Key artifacts:

```text
data/project_core_bem_receiver_position_correction_loro_validation_checks.csv
data/project_core_bem_receiver_position_correction_loro_validator_summary.json
figures/project_core_bem_receiver_position_correction_loro_validator.png
docs/PROJECT_CORE_BEM_RECEIVER_POSITION_CORRECTION_LORO_VALIDATOR.md
scripts/run_project_core_bem_receiver_position_correction_loro_validator.py
scripts/test_project_core_bem_receiver_position_correction_loro_validator.py
```

## Result

```text
validation checks:                   7
validation passes:                   7
blocking failures:                   0
source best polynomial degree:       2
source best LORO relative L2:        0.1082856299479433
receiver-position no-go valid:       true
receiver-position correction ready:  false
project-core bridge ready:           false
field FWI ready:                     false
GPU/HPC ready:                       false
```

Validation checks:

| Check | Status | Detail |
| --- | --- | --- |
| degree_rows_nonempty | pass | 4 degree rows |
| degree_count_matches_summary | pass | 4 observed / 4 summary |
| best_degree_matches_summary | pass | best degree 2 |
| best_degree_still_fails_gate | pass | best LORO L2 `0.1082856299479433` |
| no_degree_passes_gate | pass | 0 passing degrees |
| best_degree_edge_holdouts_fail | pass | edge holdout statuses false, false |
| no_bridge_or_gpu_promotion | pass | correction, bridge, 3D, field FWI, and GPU/HPC blocked |

## Interpretation

The receiver-position correction no-go is valid. Degree `2` is best but still
fails, no tested degree passes, and the best-degree edge holdouts remain above
the gate.

## Decision

Keep receiver-position correction, project-core comparison, 3D validation,
GPU/HPC escalation, and field FWI blocked from this evidence.

## Validation

Focused tests:

```text
tests/test_project_core_bem_receiver_position_correction_loro_validator.py
3 passed
```

Figure validation:

```text
project_core_bem_receiver_position_correction_loro_validator.png
2231x840, dynamic range=255
```
