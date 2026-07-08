# BEM Experiment 614: scarep 2D CPU BEM 64-Panel Repeatability Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `613` validator by mutating the run `612` 64-panel
repeatability audit artifacts.

The sensitivity audit checks that the validator accepts the exact audit and
rejects damaged repeat rows, panel count, error thresholds, response hashes,
claim-boundary promotions, figure damage, and missing script snapshots.

This is a CPU-only artifact sensitivity audit. It does not rerun the BEM solve,
compare against project FDTD outputs, run 3D validation, launch GPU/HPC work,
run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/614_scarep_2d_cpu_bem_panel64_repeatability_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_repeatability_audit_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel64_repeatability_audit_validation_sensitivity_summary.json
figures/scarep_2d_cpu_bem_panel64_repeatability_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
cases:                              14
expected pass cases:                 1
expected fail cases:                13
actual pass cases:                   1
actual fail cases:                  13
unexpected cases:                    0
exact source passes:                 true
damaged cases rejected:              true
compared to project FDTD outputs:    false
real 3D validation ready:            false
GPU/HPC ready:                       false
field FWI ready:                     false
sensitivity ready:                   true
```

Sensitivity cases:

| Case | Expected | Actual |
| --- | --- | --- |
| exact_source | pass | pass |
| source_ready_false | fail | fail |
| repeat_row_removed | fail | fail |
| panel_damage | fail | fail |
| complex_error_damage | fail | fail |
| time_error_damage | fail | fail |
| response_hash_damage | fail | fail |
| time_hash_damage | fail | fail |
| project_fdtd_promotion | fail | fail |
| 3d_promotion | fail | fail |
| gpu_promotion | fail | fail |
| field_fwi_promotion | fail | fail |
| figure_damage | fail | fail |
| script_snapshot_damage | fail | fail |

## Interpretation

The validator rejects the failure modes that would weaken the run `612`
repeatability result. It rejects changed hashes, increased errors, wrong panel
count, and any promotion to project-FDTD, 3D, GPU/HPC, or field-FWI claims.

## Decision

Keep run `612` as a guarded 2D analytic-reference repeatability result.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_repeatability_audit.py
tests/test_scarep_2d_cpu_bem_panel64_repeatability_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel64_repeatability_audit_validation_sensitivity.py

9 passed
```

Figure validation:

```text
2284x853, dynamic range=255
```
