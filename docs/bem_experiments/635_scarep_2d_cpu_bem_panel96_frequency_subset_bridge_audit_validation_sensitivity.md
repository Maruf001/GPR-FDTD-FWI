# BEM Experiment 635: 96-Panel Frequency-Subset Bridge Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `634` validator for the run `633` 96-panel
frequency-subset bridge audit.

The audit checks whether the validator rejects damaged source readiness,
frequency-subset shape, high-frequency boundary, cost relation, saved-array
hashes, claim-boundary, figure, and script states.

## Output

```text
outputs/bem_experiments/635_scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:              true
sensitivity cases:                   22
expected pass cases:                 1
expected fail cases:                 21
actual pass cases:                   1
actual fail cases:                   21
unexpected outcomes:                 0
exact source passes:                 true
damaged cases rejected:              true
bridge-boundary damage rejected:     true
array damage rejected:               true
claim-promotion cases rejected:      true
project FDTD comparison ready:       false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

Damage groups:

| Group | Damaged states | Result |
| --- | ---: | --- |
| Source readiness and subset shape | 5 | rejected |
| 64/96/128 high-band and cost relation | 6 | rejected |
| Saved arrays and hashes | 3 | rejected |
| Project FDTD, 3D, GPU/HPC, field transfer, and field FWI promotion | 5 | rejected |
| Figure and script artifacts | 2 | rejected |

## Interpretation

Run `635` hardens the 96-panel bridge result. The exact run `633` artifact is
accepted by the run `634` validator, while all damaged variants fail. This
supports using 96 panels as the current lower-cost high-frequency candidate for
the scarep analytic-cylinder BEM setup, while 128 panels remains the stricter
endpoint.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit.py
tests/test_scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit_validation_sensitivity.py

9 passed
```

Figure check:

```text
2680x884, dynamic range=255
```
