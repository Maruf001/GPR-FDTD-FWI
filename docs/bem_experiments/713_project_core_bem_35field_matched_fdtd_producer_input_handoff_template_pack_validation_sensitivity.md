# BEM Experiment 713: Producer Input Handoff Template Pack Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `712` validator.

The sensitivity cases check whether the validator rejects damaged row shape,
filled template values, false live-file promotion, false action completion,
false exporter/FDTD/GPU readiness, damaged figures, and missing script
snapshots.

This is CPU-only validation sensitivity. It does not run FDTD, execute the
input-bound exporter, create accepted return files, run a real BEM/FDTD
comparison, launch GPU/HPC work, transfer to field evidence, or promote 3D
validation claims.

## Output

```text
outputs/bem_experiments/713_project_core_bem_35field_matched_fdtd_producer_input_handoff_template_pack_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_handoff_template_pack_validation_sensitivity_case_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_handoff_template_pack_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_handoff_template_pack_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
cases:                               15
expected pass cases:                 1
expected fail cases:                 14
actual pass cases:                   1
actual fail cases:                   14
unexpected cases:                    0
damaged cases:                       14
exporter execution ready:            false
new FDTD executed:                   false
GPU/HPC ready:                       false
```

## Interpretation

The validator accepts only the exact non-live template packet. It rejects
filled real-value cells, false live-file presence, false action completion, and
false downstream execution readiness.

## Decision

Use runs `711-713` as the guarded BEM/FDTD producer-input handoff-template
block. The next real blocker remains the two live filled matched-FDTD input
files.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_handoff_template_pack_validation_sensitivity.py
3 passed
```

Figure check:

```text
2645x853, dynamic range=255
```
