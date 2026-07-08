# BEM Experiment 442: 35-Field Real Normalized-Comparator Scorecard Template Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `441` validator for the non-evidence real-return scorecard
template from run `440`.

## Output

```text
outputs/bem_experiments/442_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template_validation_sensitivity_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template_validation_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template_validation_sensitivity.png
```

## Result

```text
scenarios:                          24
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         23
observed failure scenarios:         23
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 440:    true
validator rejects damaged variants: true
real return values present:         false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

The damaged variants cover source/template readiness drift, row-count drift,
receiver/frequency count drift, removed scorecard rows, filled real-return
cells, filled generated-score cells, evidence promotion, acceptance-rule drift,
downstream promotion, blank or undersized figures, and missing script
snapshots.

## Decision

Use runs `440-442` as the guarded non-evidence real-return scorecard-template
block for future paired BEM/FDTD exports. The branch is ready to receive real
returned values and hashes, but it is still not real comparison evidence.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template_validator.py
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_template_validation_sensitivity.py
11 passed
```

Figure check:

```text
3581x890, dynamic range=255
```
