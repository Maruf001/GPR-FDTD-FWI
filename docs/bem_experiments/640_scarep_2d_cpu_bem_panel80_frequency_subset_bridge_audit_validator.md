# BEM Experiment 640: 80-Panel Frequency-Subset Bridge Audit Validator

Date: 2026-06-30

## Purpose

Validate run `639` as a real no-go result for the 80-panel high-frequency
candidate.

Run `639` tested whether the high-frequency panel threshold could move below
the guarded 96-panel candidate. It improved on the 64-panel default but still
failed the high-frequency-only subset. This validator checks that the result is
internally consistent, that saved arrays match the summary, and that no
project-FDTD, 3D, GPU/HPC, field-transfer, or field-FWI claim is promoted.

## Output

```text
outputs/bem_experiments/640_scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit_validator.png
scripts/
```

## Result

```text
checks:                                      6
checks passed:                              6
checks failed:                              0
panels:                                     80
frequency subsets tested:                   9
frequency subsets passing < 1e-3:           8
frequency subsets failing >= 1e-3:          1
80-panel high-band relative L2:             0.0010993149385036519
64-panel high-band relative L2:             0.001736291511432671
96-panel high-band relative L2:             0.0007600368161379071
128-panel high-band relative L2:            0.0004276569548253307
80-panel promoted:                          false
80-panel no-go validation ready:            true
project FDTD comparison ready:              false
real 3D validation ready:                   false
GPU/HPC ready:                              false
field transfer ready:                       false
field FWI ready:                            false
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | Source 80-panel no-go audit ready | pass |
| 2 | 80-panel high-frequency no-go preserved | pass |
| 3 | 80-to-96 threshold bracket preserved | pass |
| 4 | Saved arrays match summary hashes | pass |
| 5 | Claim boundary remains analytic BEM only | pass |
| 6 | Figure and scripts exist | pass |

## Interpretation

The 80-panel result is not a damaged artifact. It is a validated high-frequency
no-go:

```text
64 panels: high band fails
80 panels: high band fails
96 panels: high band passes
128 panels: stricter high-band endpoint
```

This keeps the current panel policy intact. The useful lower-cost
high-frequency candidate remains 96 panels, not 80 panels.

## Decision

Do not promote 80 panels for high-frequency work. Keep run `636` as the active
frequency-cost panel policy: 64 panels for default sweeps, 96 panels as the
lower-cost high-frequency candidate, and 128 panels as the strict endpoint.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit.py
tests/test_scarep_2d_cpu_bem_panel80_frequency_subset_bridge_audit_validator.py

6 passed
```

Figure check:

```text
2357x864, dynamic range=255
```
