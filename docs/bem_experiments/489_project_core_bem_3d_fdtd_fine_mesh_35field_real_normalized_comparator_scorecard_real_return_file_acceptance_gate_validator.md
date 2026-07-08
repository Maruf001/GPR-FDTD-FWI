# BEM Experiment 489: Real Return-File Acceptance-Gate Validator

Date: 2026-06-29

## Purpose

Validate the saved run `488` real return-file acceptance gate from artifacts.

## Output

```text
outputs/bem_experiments/489_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_validator
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_validator_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_validator_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           5
validation checks passed:                    5
blocking failures:                           0
acceptance-gate validation ready:            true
required real return files:                  4
accepted real return files:                  0
required real entries:                       1116
accepted real entries:                       0
required real scorecard rows:                279
accepted real scorecard rows:                0
real return packet accepted:                 false
real BEM/FDTD comparison ready:              false
GPU/HPC ready:                               false
field FWI ready:                             false
```

## Interpretation

The validator confirms that the gate is defined and still blocks all real-file,
real-value, packet-acceptance, comparison, 3D, GPU/HPC, and field-FWI
promotion.

## Decision

Use this validator as the artifact guard for run `488`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_validator.py
4 passed
```

Figure check:

```text
2753x833, dynamic range=255
```
