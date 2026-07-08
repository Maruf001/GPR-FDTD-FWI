# BEM Experiment 638: 64/96/128 Frequency-Cost Panel Policy Refresh Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `637` validator for the refreshed run `636` panel policy.

The audit checks whether the validator rejects damaged policy roles,
high-frequency threshold/cost relations, downstream claim promotion, figure
damage, and missing script snapshots.

## Output

```text
outputs/bem_experiments/638_scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:              true
sensitivity cases:                   25
expected pass cases:                 1
expected fail cases:                 24
actual pass cases:                   1
actual fail cases:                   24
unexpected outcomes:                 0
exact source passes:                 true
damaged cases rejected:              true
policy-role damage rejected:         true
high-frequency damage rejected:      true
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
| Source readiness and row shape | 2 | rejected |
| 64/96/128 policy-role and count drift | 9 | rejected |
| High-frequency threshold, cost, and role flags | 6 | rejected |
| Project FDTD, 3D, GPU/HPC, field transfer, and field FWI promotion | 5 | rejected |
| Figure and script artifacts | 2 | rejected |

## Interpretation

Run `638` hardens the refreshed panel policy. The exact run `636` policy is
accepted by the run `637` validator, while all damaged variants fail. The
current guarded policy remains:

```text
64 panels: receiver-line and broad/low/mid sweeps
96 panels: lower-cost high-frequency candidate
128 panels: strict high-frequency endpoint
```

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh.py
tests/test_scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh_validator.py
tests/test_scarep_2d_cpu_bem_panel64_96_128_frequency_cost_policy_refresh_validation_sensitivity.py

9 passed
```

Figure check:

```text
2752x886, dynamic range=255
```
