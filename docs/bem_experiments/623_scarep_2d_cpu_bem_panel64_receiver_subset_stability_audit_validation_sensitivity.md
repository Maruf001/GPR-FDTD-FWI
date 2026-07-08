# BEM Experiment 623: scarep 2D CPU BEM 64-Panel Receiver-Subset Stability Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `622` receiver-subset stability validator.

The sensitivity run mutates the run `621` artifacts in memory and checks
whether the validator rejects damaged source readiness, subset design, error
thresholds, pass counts, saved array hashes, array shapes, claim-boundary
promotion, figure damage, and missing script snapshots.

This is a CPU-only artifact sensitivity run. It does not rerun BEM solves,
compare against project FDTD outputs, run 3D validation, launch GPU/HPC work,
transfer to field work, run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/623_scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit_validation_sensitivity_summary.json
figures/scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
cases:                         19
expected pass cases:            1
expected fail cases:           18
actual pass cases:              1
actual fail cases:             18
unexpected outcomes:            0
exact source passes:          true
damaged cases rejected:       true
compared to project FDTD:     false
real 3D validation ready:     false
GPU/HPC ready:                false
field transfer ready:         false
field FWI ready:              false
sensitivity ready:            true
```

Damage cases cover row removal, subset-name damage, scan-index damage, scan
count damage, complex-error threshold failure, time-B-scan threshold failure,
pass-count damage, response-hash damage, time-B-scan hash damage, array-shape
damage, project-FDTD promotion, 3D promotion, GPU/HPC promotion, field-transfer
promotion, field-FWI promotion, figure damage, and missing script snapshots.

## Interpretation

The validator is sensitive to the failure modes that would undermine the
receiver-subset stability result. It accepts only the exact run `621` artifacts
and rejects damaged design, error, array, claim-boundary, figure, and script
states.

## Decision

Keep run `622` as the validator guard for run `621`.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit.py
tests/test_scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel64_receiver_subset_stability_audit_validation_sensitivity.py

10 passed
```

Figure validation:

```text
2500x868, dynamic range=255
```
