# BEM Experiment 152: Symmetry Calibration Frequency Holdout Audit

Date: 2026-06-27

## Purpose

Stress-test whether the run `150`/`151` calibration candidate generalizes
across frequency.

The candidate design uses receivers `0`, `2`, `4`, and `6` with a degree `1`
even aperture correction to predict receivers `1`, `3`, and `5`. Runs `150`
and `151` validated that result when the correction is fit independently at
each frequency. This run tests a stricter condition: correction coefficients
are fit on selected frequency bins and interpolated to held-out frequency bins.

This is a CPU-only audit from saved bridge arrays. It does not rerun FDTD,
rerun BEM solvers, compare against field data, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/152_project_core_bem_symmetry_calibration_frequency_holdout_audit
```

Key artifacts:

```text
data/project_core_bem_symmetry_calibration_frequency_holdout_rows.csv
data/project_core_bem_symmetry_calibration_frequency_holdout_audit_summary.json
figures/project_core_bem_symmetry_calibration_frequency_holdout_audit.png
docs/PROJECT_CORE_BEM_SYMMETRY_CALIBRATION_FREQUENCY_HOLDOUT_AUDIT.md
scripts/run_project_core_bem_symmetry_calibration_frequency_holdout_audit.py
scripts/test_project_core_bem_symmetry_calibration_frequency_holdout_audit.py
```

## Result

```text
candidate train receivers:             0;2;4;6
candidate holdout receivers:           1;3;5
candidate spatial degree:              1
frequency holdout rows:                28
frequency holdout passing rows:        1
alternating holdout passing rows:      0
edge holdout passing rows:             1
per-frequency candidate passes:        true
frequency generalization ready:        false
project-core bridge ready:             false
3D validation ready:                   false
field FWI ready:                       false
GPU/HPC ready:                         false
```

Key frequency-holdout outcomes:

| Scheme | Best degree | Held-frequency L2 | Holdout receiver held-frequency L2 | Passes |
| --- | ---: | ---: | ---: | --- |
| even_train_odd_hold | 4 | 0.10772312141509063 | 0.08675883674934565 | false |
| odd_train_even_hold | 0 | 0.12537430746633593 | 0.11042010506672008 | false |
| low_mid_high_sparse | 2 | 0.13427096947362233 | 0.11559662500246333 | false |
| drop_low_edge | 3 | 0.0940406423099409 | 0.09363407200299485 | true |
| drop_high_edge | 4 | 0.11136718425871124 | 0.15090926362111554 | false |
| drop_both_edges | 3 | 0.10647976566066421 | 0.1230209545956325 | false |

## Interpretation

The edge-pair-plus-inner-pair candidate passes when the correction is fit
independently at each frequency. It does not pass alternating frequency
holdouts. Only one narrow edge-frequency holdout passes.

The current candidate is therefore a per-frequency adapter candidate, not a
frequency-generalized BEM/FDTD bridge.

## Decision

Keep the symmetry calibration design as a candidate only. Do not promote
project-core comparison, 3D validation, GPU/HPC, or field FWI until a
frequency-generalized correction or fresh matched case closes this gap.

## Validation

Focused tests:

```text
tests/test_project_core_bem_symmetry_calibration_frequency_holdout_audit.py
5 passed
```

Figure validation:

```text
project_core_bem_symmetry_calibration_frequency_holdout_audit.png
2896x842, dynamic range=255
```
