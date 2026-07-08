# BEM Experiment 625: 64-Panel Frequency-Subset Stability Audit Validator

Date: 2026-06-30

## Purpose

Validate run `624`, which tested whether the 64-panel two-dimensional CPU BEM
default remains accurate under different frequency subsets.

Run `624` found a useful boundary: the full, low, and mid bands pass the
`1e-3` relative-error target, but the high-frequency-only 2.08-3.00 GHz subset
does not. This validator checks that the saved artifact preserves that boundary
and does not promote it into project FDTD, field, GPU/HPC, or three-dimensional
evidence.

## Output

```text
outputs/bem_experiments/625_scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit_validator.png
scripts/
```

## Result

```text
validation checks:                                5
failed checks:                                    0
frequency subsets:                                9
passing frequency subsets below 1e-3:             8
failing frequency subsets:                        1
full-band relative L2:                            0.0007053747139208217
mid-band relative L2:                             0.0009503011515443673
high-band relative L2:                            0.001736291511432671
high-band exceeds 1e-3:                           true
high-frequency-only needs endpoint confirmation:  true
project FDTD comparison ready:                    false
real 3D validation ready:                         false
GPU/HPC ready:                                    false
field transfer ready:                             false
field FWI ready:                                  false
```

All five validation checks pass:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source frequency-subset audit ready | pass |
| 2 | frequency subset rows preserve design | pass |
| 3 | high-frequency boundary is preserved | pass |
| 4 | claim boundary remains analytic 2D only | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

The run `624` frequency-subset finding is now guarded as a stable BEM artifact.
The 64-panel default is acceptable for broad-band, low-band, and mid-band
analytic-cylinder checks, but it is not enough for a claim based only on the
2.08-3.00 GHz band under the `1e-3` target.

This supports a practical BEM policy:

```text
Use 64 panels for cheaper broad/low/mid-band receiver-line sweeps.
Use the 128-panel endpoint, or a dedicated high-frequency confirmation, when a
claim depends on the high-frequency-only band.
```

The result remains internal to the two-dimensional scarep analytic-cylinder BEM
validation problem. It is not a project FDTD comparison, not a field-data result,
not a three-dimensional Maxwell validation, and not a GPU/HPC readiness result.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit.py
tests/test_scarep_2d_cpu_bem_panel64_frequency_subset_stability_audit_validator.py

6 passed
```

Figure check:

```text
2285x839, dynamic range=255
```
