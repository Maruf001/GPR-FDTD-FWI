# BEM Experiment 153: Symmetry Calibration Frequency Holdout Validator

Date: 2026-06-27

## Purpose

Validate the run `152` frequency-holdout no-go from saved tables.

Run `152` showed that the symmetry calibration candidate passes when the
correction is fit independently at each frequency, but it does not pass
alternating frequency holdouts. This run validates that conclusion directly
from the run `152` rows and summary.

This is a CPU-only validation audit. It does not rerun FDTD, rerun BEM solvers,
compare against field data, launch GPU/HPC work, run 3D validation, or run
field FWI.

## Output

```text
outputs/bem_experiments/153_project_core_bem_symmetry_calibration_frequency_holdout_validator
```

Key artifacts:

```text
data/project_core_bem_symmetry_calibration_frequency_holdout_validation_checks.csv
data/project_core_bem_symmetry_calibration_frequency_holdout_validator_summary.json
figures/project_core_bem_symmetry_calibration_frequency_holdout_validator.png
docs/PROJECT_CORE_BEM_SYMMETRY_CALIBRATION_FREQUENCY_HOLDOUT_VALIDATOR.md
scripts/run_project_core_bem_symmetry_calibration_frequency_holdout_validator.py
scripts/test_project_core_bem_symmetry_calibration_frequency_holdout_validator.py
```

## Result

```text
validation checks:                     8
validation passes:                     8
blocking failures:                     0
source frequency holdout passes:       1
source alternating holdout passes:     0
source edge holdout passes:            1
frequency holdout no-go valid:         true
per-frequency candidate passes:        true
frequency generalization ready:        false
project-core bridge ready:             false
3D validation ready:                   false
field FWI ready:                       false
GPU/HPC ready:                         false
```

Validation checks:

| Check | Status | Detail |
| --- | --- | --- |
| frequency_rows_nonempty | pass | 29 rows |
| direct_per_frequency_candidate_passes | pass | 1 direct row |
| holdout_row_count_matches_summary | pass | 28 observed / 28 summary |
| passing_holdout_count_matches_summary | pass | 1 passing holdout row |
| alternating_holdouts_do_not_pass | pass | 0 alternating passing rows |
| only_edge_holdout_passes | pass | 1 edge passing row |
| frequency_generalization_not_ready | pass | alternating frequency holdouts remain blocked |
| no_bridge_or_gpu_promotion | pass | bridge, 3D, field FWI, and GPU/HPC blocked |

## Interpretation

The run `152` frequency-holdout no-go is valid. Per-frequency calibration
passes, but alternating frequency holdouts do not, so the candidate is not
frequency-generalized.

## Decision

Keep the BEM symmetry calibration design as a per-frequency candidate only. Do
not promote project-core comparison, 3D validation, GPU/HPC, or field FWI until
frequency generalization or fresh matched validation passes.

## Validation

Focused tests:

```text
tests/test_project_core_bem_symmetry_calibration_frequency_holdout_validator.py
3 passed
```

Figure validation:

```text
project_core_bem_symmetry_calibration_frequency_holdout_validator.png
2231x840, dynamic range=255
```
