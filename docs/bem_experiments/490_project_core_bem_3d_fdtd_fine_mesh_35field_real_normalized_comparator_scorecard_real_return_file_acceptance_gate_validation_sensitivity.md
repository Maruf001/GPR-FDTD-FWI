# BEM Experiment 490: Real Return-File Acceptance-Gate Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `489` validator against controlled damage to the run `488`
acceptance gate.

## Output

```text
outputs/bem_experiments/490_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_validation_sensitivity_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_validation_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       35
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  34
observed failure scenarios:                  34
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 488:             true
validator rejects damaged variants:          true
real return packet accepted:                 false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

## Interpretation

The validator accepts the exact run `488` gate and rejects damaged variants for
gate-count drift, premature real-file acceptance, premature real-entry
acceptance, scorecard acceptance, packet acceptance, downstream promotion,
figure drift, and script-snapshot drift.

## Decision

Use runs `488-490` as the guarded real return-file acceptance-gate block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_validation_sensitivity.py
3 passed
```

Figure check:

```text
3761x882, dynamic range=255
```
