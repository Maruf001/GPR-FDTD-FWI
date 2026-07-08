# BEM Experiment 611: scarep 2D CPU BEM Panel Accuracy-Cost Policy Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `610` validator by mutating the run `609` panel
accuracy/cost policy artifacts.

The sensitivity audit checks that the validator accepts the exact policy and
rejects damaged panel choices, threshold counts, convergence metrics,
claim-boundary promotions, figure damage, and missing script snapshots.

This is a CPU-only artifact sensitivity audit. It does not rerun the BEM solve,
compare against project FDTD outputs, run 3D validation, launch GPU/HPC work,
run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/611_scarep_2d_cpu_bem_panel_accuracy_cost_policy_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel_accuracy_cost_policy_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel_accuracy_cost_policy_validation_sensitivity_summary.json
figures/scarep_2d_cpu_bem_panel_accuracy_cost_policy_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
cases:                              17
expected pass cases:                 1
expected fail cases:                16
actual pass cases:                   1
actual fail cases:                  16
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
| policy_ready_false | fail | fail |
| threshold_row_removed | fail | fail |
| threshold_count_damage | fail | fail |
| repeat_panel_damage | fail | fail |
| high_accuracy_panel_damage | fail | fail |
| strict_threshold_promoted | fail | fail |
| panel_values_damage | fail | fail |
| complex_order_damage | fail | fail |
| time_order_damage | fail | fail |
| wall_ratio_damage | fail | fail |
| project_fdtd_promotion | fail | fail |
| 3d_validation_promotion | fail | fail |
| gpu_hpc_promotion | fail | fail |
| field_fwi_promotion | fail | fail |
| figure_damage | fail | fail |
| script_snapshot_damage | fail | fail |

## Interpretation

The validator rejects the key failure modes. In particular, it rejects an
attempt to make 32 panels the repeat-sweep default for the `1e-3` target,
rejects an attempt to use 64 panels as the high-accuracy endpoint, rejects a
false `1e-4` success, and rejects promotion to project-FDTD comparison, 3D
validation, GPU/HPC, or field FWI.

## Decision

Keep the scarep panel policy as a 2D BEM numerical validation policy until a
matched project-FDTD comparison is produced and accepted.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel_accuracy_cost_policy_validator.py
tests/test_scarep_2d_cpu_bem_panel_accuracy_cost_policy_validation_sensitivity.py

6 passed
```

Figure validation:

```text
2284x857, dynamic range=255
```
