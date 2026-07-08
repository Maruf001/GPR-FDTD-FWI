# BEM Experiment 652: 82-Panel Frequency-Subset Bridge Audit Validator

Date: 2026-06-30

## Purpose

Validate run `651` as a real no-go result for the 82-panel high-frequency
candidate.

Run `651` tested whether the threshold could move below the narrow 84-panel
pass. It improved on 80 panels but still failed the high-frequency-only subset.
This validator checks that the no-go result is internally consistent, that
saved arrays match the summary, and that no project-FDTD, 3D, GPU/HPC,
field-transfer, or field-FWI claim is promoted.

## Output

```text
outputs/bem_experiments/652_scarep_2d_cpu_bem_panel82_frequency_subset_bridge_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel82_frequency_subset_bridge_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel82_frequency_subset_bridge_audit_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel82_frequency_subset_bridge_audit_validator.png
scripts/
```

## Result

```text
checks:                                      6
checks passed:                              6
checks failed:                              0
panels:                                     82
frequency subsets tested:                   9
frequency subsets passing < 1e-3:           8
frequency subsets failing >= 1e-3:          1
82-panel high-band relative L2:             0.001045485149014675
96-panel high-band relative L2:             0.0007600368161379071
128-panel high-band relative L2:            0.0004276569548253307
82-panel promoted:                          false
82-panel no-go validation ready:            true
project FDTD comparison ready:              false
real 3D validation ready:                   false
GPU/HPC ready:                              false
field transfer ready:                       false
field FWI ready:                            false
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | Source 82-panel no-go audit ready | pass |
| 2 | 82-panel high-frequency no-go preserved | pass |
| 3 | 82-to-96 threshold bracket preserved | pass |
| 4 | Saved arrays match summary hashes | pass |
| 5 | Claim boundary remains analytic BEM only | pass |
| 6 | Figure and scripts exist | pass |

## Interpretation

The 82-panel result is not a damaged artifact. It is a validated
high-frequency no-go:

```text
80 panels: high band fails
82 panels: high band fails
84 panels: high band passes narrowly
88 panels: high band passes
96 panels: high band passes
128 panels: strict endpoint
```

## Decision

Do not promote 82 panels for high-frequency work. Use it as the no-go lower
side of the 82/84 threshold bracket.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel82_frequency_subset_bridge_audit.py
tests/test_scarep_2d_cpu_bem_panel82_frequency_subset_bridge_audit_validator.py

6 passed
```

Figure check:

```text
2357x864, dynamic range=255
```
