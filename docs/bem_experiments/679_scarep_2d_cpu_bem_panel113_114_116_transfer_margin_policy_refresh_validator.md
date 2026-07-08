# BEM Experiment 679: 113/114/116 Transfer Margin Policy Refresh Validator

Date: 2026-06-30

## Purpose

Validate run `678`, the margin-aware analytic transfer panel policy.

## Output

```text
outputs/bem_experiments/679_scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh_validator.png
scripts/
```

## Result

```text
validation checks:                     5
failed checks:                         0
nearest no-go panel:                   113
minimum passing panel:                 114
guarded recommended panel:             116
minimum passing margin:                0.000015199423897917664
guarded recommended margin:            0.000049382924375243283
project FDTD comparison ready:         false
real 3D validation ready:              false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | Source policy refresh ready | pass |
| 2 | Row shape and panel set preserved | pass |
| 3 | 113/114/116 margin policy preserved | pass |
| 4 | Source validators and claim boundary preserved | pass |
| 5 | Figure and scripts exist | pass |

## Interpretation

Run `679` validates the policy split: 114 panels are the minimum pass, while
116 panels are the guarded recommendation.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh.py
tests/test_scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh_validator.py

6 passed
```

Figure check:

```text
2321x861, dynamic range=255
```
