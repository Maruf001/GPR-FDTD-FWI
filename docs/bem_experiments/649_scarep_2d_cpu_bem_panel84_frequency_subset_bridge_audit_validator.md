# BEM Experiment 649: 84-Panel Frequency-Subset Bridge Audit Validator

Date: 2026-06-30

## Purpose

Validate run `648`, the 84-panel high-frequency bridge audit.

Run `648` showed that 84 panels pass all nine frequency subsets, but with a
narrow high-band margin below the `1e-3` target. This validator checks source
readiness, the all-subset pass, the 80-to-84-to-96 threshold bracket, saved
array hashes, figure output, script snapshots, and downstream claim boundaries.

## Output

```text
outputs/bem_experiments/649_scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit_validator.png
scripts/
```

## Result

```text
checks:                                      6
checks passed:                              6
checks failed:                              0
panels:                                     84
frequency subsets tested:                   9
frequency subsets passing < 1e-3:           9
frequency subsets failing >= 1e-3:          0
84-panel high-band relative L2:             0.000995562585853498
80-panel high-band relative L2:             0.0010993149385036519
96-panel high-band relative L2:             0.0007600368161379071
128-panel high-band relative L2:            0.0004276569548253307
84-panel promoted high-frequency candidate: true
84-panel validation ready:                  true
project FDTD comparison ready:              false
real 3D validation ready:                   false
GPU/HPC ready:                              false
field transfer ready:                       false
field FWI ready:                            false
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | Source 84-panel bridge audit ready | pass |
| 2 | 84-panel all-subset pass preserved | pass |
| 3 | 80-to-84-to-96 threshold bracket preserved | pass |
| 4 | Saved arrays match summary hashes | pass |
| 5 | Claim boundary remains analytic BEM only | pass |
| 6 | Figure and scripts exist | pass |

## Interpretation

The 84-panel result is validated as a narrow-margin analytic-cylinder BEM
candidate:

```text
80 panels: high band fails
84 panels: high band passes at 0.000995562585853498
88 panels: high band passes at 0.0009060002386797175
96 panels: high band passes at 0.0007600368161379071
128 panels: strict endpoint
```

Because the 84-panel margin is small, this result still needs sensitivity
hardening before replacing the active run `645` policy.

## Decision

Treat 84 panels as the current narrow-margin lower-cost candidate after
sensitivity hardening. Keep downstream project-FDTD, 3D, GPU/HPC,
field-transfer, and field-FWI claims blocked.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit.py
tests/test_scarep_2d_cpu_bem_panel84_frequency_subset_bridge_audit_validator.py

6 passed
```

Figure check:

```text
2357x864, dynamic range=255
```
