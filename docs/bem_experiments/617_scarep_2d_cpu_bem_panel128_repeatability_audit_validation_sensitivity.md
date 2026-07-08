# BEM Experiment 617: scarep 2D CPU BEM 128-Panel Repeatability Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `616` 128-panel repeatability validator.

The sensitivity run mutates the validated repeatability artifacts in memory and
checks whether the validator rejects damaged states. The damage cases cover
source readiness, repeat-row shape, panel identity, error thresholds, response
hashes, time-B-scan hashes, project-FDTD promotion, 3D promotion, GPU/HPC
promotion, field-FWI promotion, figure damage, and missing script snapshots.

This is a CPU-only artifact sensitivity run. It does not run a new BEM solve,
compare against project FDTD outputs, run 3D validation, launch GPU/HPC work,
run field FWI, or train neural networks.

## Output

```text
outputs/bem_experiments/617_scarep_2d_cpu_bem_panel128_repeatability_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel128_repeatability_audit_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel128_repeatability_audit_validation_sensitivity_summary.json
figures/scarep_2d_cpu_bem_panel128_repeatability_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
cases:                         14
expected pass cases:            1
expected fail cases:           13
actual pass cases:              1
actual fail cases:             13
unexpected outcomes:            0
exact source passes:          true
damaged cases rejected:        true
compared to project FDTD:      false
real 3D validation ready:      false
GPU/HPC ready:                 false
field FWI ready:               false
sensitivity ready:             true
```

Sensitivity cases:

| Case | Expected | Actual |
| --- | --- | --- |
| exact source | pass | pass |
| source readiness false | fail | fail |
| repeat row removed | fail | fail |
| panel damaged | fail | fail |
| complex error damaged | fail | fail |
| time error damaged | fail | fail |
| response hash damaged | fail | fail |
| time hash damaged | fail | fail |
| project FDTD promoted | fail | fail |
| 3D promoted | fail | fail |
| GPU/HPC promoted | fail | fail |
| field FWI promoted | fail | fail |
| figure dynamic range removed | fail | fail |
| script snapshots removed | fail | fail |

## Interpretation

The validator is sensitive to the important failure modes. It accepts only the
exact 128-panel repeatability audit and rejects damaged high-accuracy errors,
hash instability, claim-boundary promotion, damaged figures, and missing
script snapshots.

## Decision

Use run `615` as a guarded 2D analytic-reference high-accuracy repeatability
result. Keep project-FDTD comparison, 3D validation, GPU/HPC, and field-FWI
claims blocked until matched comparisons are produced.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel128_repeatability_audit.py
tests/test_scarep_2d_cpu_bem_panel128_repeatability_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel128_repeatability_audit_validation_sensitivity.py

9 passed
```

Figure validation:

```text
2284x853, dynamic range=255
```
