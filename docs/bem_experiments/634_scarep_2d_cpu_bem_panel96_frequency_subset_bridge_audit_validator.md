# BEM Experiment 634: 96-Panel Frequency-Subset Bridge Audit Validator

Date: 2026-06-30

## Purpose

Validate run `633`, the 96-panel scarep CPU BEM frequency-subset bridge audit.

## Output

```text
outputs/bem_experiments/634_scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit_validator.png
scripts/
```

## Result

```text
validation checks:                    6
failed checks:                        0
panels:                               96
frequency subsets:                    9
subset pass count:                    9
subset fail count:                    0
96-panel high-band relative L2:       0.0007600368161379071
64-panel high-band relative L2:       0.001736291511432671
128-panel high-band relative L2:      0.0004276569548253307
high-band improvement vs 64 panels:   2.2844834283891116x
high-band gap vs 128 panels:          1.7772114017140943x
wall time relative to 128 panels:     0.5702697635429481
project FDTD comparison ready:        false
real 3D validation ready:             false
GPU/HPC ready:                        false
field transfer ready:                 false
field FWI ready:                      false
```

All six validation checks pass:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source 96-panel bridge ready | pass |
| 2 | frequency subsets pass at 96 panels | pass |
| 3 | 96-panel high-frequency bridge and cost relation preserved | pass |
| 4 | saved arrays match summary hashes | pass |
| 5 | claim boundary remains analytic BEM only | pass |
| 6 | figure and scripts exist | pass |

## Interpretation

Run `634` validates 96 panels as a guarded lower-cost high-frequency candidate
for this two-dimensional analytic-cylinder BEM setup. The 128-panel endpoint
still gives the smaller high-band error, but 96 panels pass the current
`1e-3` high-frequency target at substantially lower wall time.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit.py
tests/test_scarep_2d_cpu_bem_panel96_frequency_subset_bridge_audit_validator.py

6 passed
```

Figure check:

```text
2357x865, dynamic range=255
```
