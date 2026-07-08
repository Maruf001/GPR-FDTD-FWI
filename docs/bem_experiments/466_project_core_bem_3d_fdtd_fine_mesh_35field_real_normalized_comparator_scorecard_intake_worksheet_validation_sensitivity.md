# BEM Experiment 466: 35-Field Scorecard Intake Worksheet Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `465` validator with controlled damage to worksheet counts,
row completion state, requirement schema, storage precision, downstream states,
figure validation, and script snapshots.

## Output

```text
outputs/bem_experiments/466_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet_validation_sensitivity_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet_validation_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                      40
expected passes:                            1
observed passes:                            1
expected failures:                          39
observed failures:                          39
unexpected outcomes:                        0
validation sensitivity ready:               true
validator accepts exact run 464:            true
validator rejects damaged variants:         true
real return values present:                 false
real BEM/FDTD comparison ready:             false
3D validation ready:                        false
GPU/HPC ready:                              false
field transfer ready:                       false
field FWI ready:                            false
```

## Decision

Use runs `464-466` as the guarded non-evidence 35-field normalized-comparator
scorecard intake worksheet block. It does not promote BEM/FDTD comparison
evidence; it defines the required real-return fields.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet_validation_sensitivity.py
3 passed
```

Figure check:

```text
3653x919, dynamic range=255
```
