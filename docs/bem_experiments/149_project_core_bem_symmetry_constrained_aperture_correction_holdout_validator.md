# BEM Experiment 149: Symmetry-Constrained Aperture Correction Holdout Validator

Date: 2026-06-27

## Purpose

Validate the run `148` symmetry-constrained aperture correction decision from a
consumer perspective.

Run `148` found an important split result: an even aperture-position correction
passes leave-one-receiver-out validation, but it fails the stricter
leave-one-symmetry-pair-out validation. This run checks the saved run `148`
tables and summary directly so later scripts can consume the decision without
recomputing the correction fit.

This is a CPU-only validation audit. It does not rerun FDTD, rerun BEM solvers,
compare against field data, launch GPU/HPC work, run 3D validation, or run
field FWI.

## Output

```text
outputs/bem_experiments/149_project_core_bem_symmetry_constrained_aperture_correction_holdout_validator
```

Key artifacts:

```text
data/project_core_bem_symmetry_constrained_aperture_correction_holdout_validation_checks.csv
data/project_core_bem_symmetry_constrained_aperture_correction_holdout_validator_summary.json
figures/project_core_bem_symmetry_constrained_aperture_correction_holdout_validator.png
docs/PROJECT_CORE_BEM_SYMMETRY_CONSTRAINED_APERTURE_CORRECTION_HOLDOUT_VALIDATOR.md
scripts/run_project_core_bem_symmetry_constrained_aperture_correction_holdout_validator.py
scripts/test_project_core_bem_symmetry_constrained_aperture_correction_holdout_validator.py
```

## Result

```text
validation checks:                 8
validation passes:                 8
blocking failures:                 0
source best LORO degree:           2
source best LORO relative L2:      0.06977055235365863
source best LOSPO degree:          1
source best LOSPO relative L2:     0.12895136750102182
symmetry holdout no-go valid:      true
symmetry correction promotable:    false
project-core bridge ready:         false
3D validation ready:               false
field FWI ready:                   false
GPU/HPC ready:                     false
```

Validation checks:

| Check | Status | Detail |
| --- | --- | --- |
| model_rows_nonempty | pass | 8 model rows |
| model_row_count_matches_summary | pass | 8 observed / 8 summary |
| best_loro_matches_summary | pass | degree 2 L2 0.06977055235365863 |
| loro_candidate_passes | pass | 7 receiver rows passing |
| best_lospo_matches_summary | pass | degree 1 L2 0.12895136750102182 |
| lospo_candidate_blocks_promotion | pass | 2 holdout groups passing |
| lospo_edge_pair_fails | pass | edge pair group statuses false, false |
| no_bridge_or_gpu_promotion | pass | symmetry correction, bridge, 3D, field FWI, and GPU/HPC blocked |

## Interpretation

The run `148` decision is valid. The symmetry-constrained correction passes the
easier leave-one-receiver-out check, but the stricter symmetry-pair holdout
still fails and the edge pair remains above the gate.

## Decision

Keep symmetry-constrained aperture correction, project-core comparison, 3D
validation, GPU/HPC, and field FWI blocked until the pair-holdout failure
closes or a fresh matched case validates the correction.

## Validation

Focused tests:

```text
tests/test_project_core_bem_symmetry_constrained_aperture_correction_holdout_validator.py
4 passed
```

Figure validation:

```text
project_core_bem_symmetry_constrained_aperture_correction_holdout_validator.png
2249x840, dynamic range=255
```
