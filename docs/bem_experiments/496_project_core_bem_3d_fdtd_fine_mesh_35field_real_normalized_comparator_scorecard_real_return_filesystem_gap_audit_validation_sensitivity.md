# BEM Experiment 496: Real Return-File Filesystem Gap-Audit Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `495` validator against controlled damage to the
filesystem gap audit.

## Output

```text
outputs/bem_experiments/496_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_validation_sensitivity_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_validation_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       22
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  21
observed failure scenarios:                  21
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 494:             true
validator rejects damaged variants:          true
real return files present:                   false
real return packet accepted:                 false
real BEM/FDTD comparison ready:              false
```

The damaged variants cover scan-count drift, real-file promotion, template or
synthetic misclassification, non-evidence promotion, downstream promotion,
figure damage, and script-snapshot damage.

## Decision

Use runs `494-496` as the guarded real-return filesystem gap-audit block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_validation_sensitivity.py
3 passed
```

Figure check:

```text
3581x921, dynamic range=255
```
