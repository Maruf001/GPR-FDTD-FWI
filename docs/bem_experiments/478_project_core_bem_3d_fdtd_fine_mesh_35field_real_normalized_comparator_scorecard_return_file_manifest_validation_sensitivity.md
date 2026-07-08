# BEM Experiment 478: 35-Field Return-File Manifest Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `477` validator against controlled damage to the
return-file manifest.

## Output

```text
outputs/bem_experiments/478_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_manifest_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_manifest_validation_sensitivity_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_manifest_validation_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_manifest_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       33
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  32
observed failure scenarios:                  32
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 476:             true
validator rejects damaged variants:          true
real return files present:                   false
real return values present:                  false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field transfer ready:                        false
field FWI ready:                             false
```

The validator accepts the exact run `476` manifest and rejects damage to file
counts, file keys, per-file row counts, receiver/frequency counts, blank
templates, template hashes, downstream promotion, figure validation, and script
snapshots.

## Decision

Use runs `476-478` as the guarded BEM return-file manifest block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_manifest_validation_sensitivity.py
3 passed
```

Figure check:

```text
3617x887, dynamic range=255
```
