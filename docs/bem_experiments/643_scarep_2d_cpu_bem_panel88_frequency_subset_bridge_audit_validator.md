# BEM Experiment 643: 88-Panel Frequency-Subset Bridge Audit Validator

Date: 2026-06-30

## Purpose

Validate run `642` as a guarded positive high-frequency bridge result.

Run `642` showed that 88 panels pass all nine frequency subsets on the scarep
analytic-cylinder scan. This validator checks source readiness, the all-subset
pass, the 80-to-88-to-96 threshold bracket, saved-array hashes, figure output,
script snapshots, and downstream claim boundaries.

## Output

```text
outputs/bem_experiments/643_scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit_validator.png
scripts/
```

## Result

```text
checks:                                      6
checks passed:                              6
checks failed:                              0
panels:                                     88
frequency subsets tested:                   9
frequency subsets passing < 1e-3:           9
frequency subsets failing >= 1e-3:          0
88-panel high-band relative L2:             0.0009060002386797175
80-panel high-band relative L2:             0.0010993149385036519
96-panel high-band relative L2:             0.0007600368161379071
128-panel high-band relative L2:            0.0004276569548253307
88-panel promoted high-frequency candidate: true
88-panel validation ready:                  true
project FDTD comparison ready:              false
real 3D validation ready:                   false
GPU/HPC ready:                              false
field transfer ready:                       false
field FWI ready:                            false
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | Source 88-panel bridge audit ready | pass |
| 2 | 88-panel all-subset pass preserved | pass |
| 3 | 80-to-88-to-96 threshold bracket preserved | pass |
| 4 | Saved arrays match summary hashes | pass |
| 5 | Claim boundary remains analytic BEM only | pass |
| 6 | Figure and scripts exist | pass |

## Interpretation

The 88-panel result is now validated as a guarded lower-cost high-frequency
candidate for the analytic-cylinder BEM setting:

```text
64 panels: high band fails
80 panels: high band fails
88 panels: high band passes
96 panels: high band passes
128 panels: strict high-band endpoint
```

The promotion is limited to the scarep analytic-cylinder BEM policy. It is not
a project-FDTD comparison, 3D validation, GPU/HPC result, field-transfer
result, or field-FWI result.

## Decision

Promote 88 panels as the lower-cost high-frequency candidate after sensitivity
hardening. Keep 128 panels as the strict endpoint.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit.py
tests/test_scarep_2d_cpu_bem_panel88_frequency_subset_bridge_audit_validator.py

6 passed
```

Figure check:

```text
2357x864, dynamic range=255
```
