# BEM Experiment 647: 64/88/96/128 Frequency-Cost Policy Refresh Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `646` validator for the refreshed scarep 2D CPU BEM panel
policy.

Run `646` validated the current policy: 64 panels for default sweeps, 80 panels
as a no-go lower bound, 88 panels as the lower-cost high-frequency candidate,
96 panels as a validated reference, and 128 panels as the strict endpoint. This
run damages the policy artifact one case at a time to verify that role drift,
threshold drift, downstream claim promotion, figure damage, and missing script
snapshots are rejected.

## Output

```text
outputs/bem_experiments/647_scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                   true
cases tested:                             33
expected pass cases:                      1
expected fail cases:                      32
actual pass cases:                        1
actual fail cases:                        32
unexpected outcomes:                      0
exact source passes:                      true
damaged cases rejected:                   true
policy-role damage rejected:              true
high-frequency damage rejected:           true
claim-promotion cases rejected:           true
validation sensitivity ready:             true
project FDTD comparison ready:            false
real 3D validation ready:                 false
GPU/HPC ready:                            false
field transfer ready:                     false
field FWI ready:                          false
```

Sensitivity classes:

| Class | Cases | Outcome |
| --- | ---: | --- |
| Exact source | 1 | accepted |
| Source readiness and row shape | 2 | rejected |
| Policy-role drift | 13 | rejected |
| High-frequency threshold or cost drift | 10 | rejected |
| Downstream claim promotion | 5 | rejected |
| Figure or script damage | 2 | rejected |

## Interpretation

The refreshed policy is guarded against accidental role drift. The exact
run `646` source is accepted, while all damaged policy, threshold, and claim
states are rejected.

## Decision

Keep run `646` as the validator guard for the current scarep analytic-cylinder
64/88/96/128 policy.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh.py
tests/test_scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh_validator.py
tests/test_scarep_2d_cpu_bem_panel64_88_96_128_frequency_cost_policy_refresh_validation_sensitivity.py

9 passed
```

Figure check:

```text
3004x885, dynamic range=255
```
