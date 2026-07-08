# BEM Experiment 441: 35-Field Real Normalized-Comparator Scorecard Template Validator

Date: 2026-06-29

## Purpose

Validate the non-evidence real-return scorecard template from run `440` before
using it as a future BEM/FDTD comparison handoff artifact.

## Output

```text
outputs/bem_experiments/441_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template_validator
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template_validator_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template_validator_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template_validator.png
```

## Result

```text
source template ready:              true
validation checks:                  5
validation checks passed:           5
blocking failures:                  0
scorecard template validation ready:true
scorecard template rows:            279
required real input cells:          1116
acceptance rules:                   5
template rows currently evidence:   0
real return values present:         false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

The validator confirms that the run `440` scorecard template preserves the
expected 31-by-9 receiver/frequency grid, leaves the 1116 real-return cells
blank, keeps all template rows non-evidence, and includes the required
snapshotted scripts and nonblank figure.

## Decision

Use this validator as the artifact guard for the run `440` real-return
scorecard template. Do not treat the template as real comparison evidence until
returned real BEM and FDTD values plus source hashes are supplied.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template_validator.py
8 passed
```

Figure check:

```text
2645x839, dynamic range=255
```
