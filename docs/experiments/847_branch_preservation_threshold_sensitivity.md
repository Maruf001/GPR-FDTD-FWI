# Experiment 847: Branch-Preservation Threshold Sensitivity

Date: 2026-06-18

## Purpose

Sweep branch-preservation absolute and relative misfit-gap thresholds over the
saved coordinate optimizer candidate surfaces. This tests whether the proposed
0.01 absolute / 10% relative preservation rule is a reasonable manuscript
policy rather than a single arbitrary cutoff.

This is CPU-only analysis of saved candidate CSVs. It does not run FDTD, FWI,
GPU kernels, field work, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/096_local_2d_branch_preservation_threshold_sensitivity
```

Key artifacts:

```text
data/local_2d_branch_preservation_threshold_sensitivity_summary.json
data/local_2d_branch_preservation_threshold_sensitivity_rows.csv
data/local_2d_branch_preservation_threshold_sensitivity_gates.csv
data/figure_validation.csv
figures/local_2d_branch_preservation_threshold_sensitivity.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         local_2d_branch_preservation_threshold_sensitivity_cpu_no_gpu
threshold combinations:               25
default cutoff:                       abs=0.01, rel=0.10
default recovered count:              13
default mean extra candidates/step:    4.598
max recovered count:                  14
most efficient max-recovery cutoff:   abs=0.01, rel=0.20
max-recovery mean extra/step:          6.317
default recovers max count:           false
default threshold policy ready:       true
broad GPU queue ready:                false
detector-seeded FWI ready:            false
gpu priority:                         none
```

Important tradeoff points:

```text
abs=0.005, rel=0.02: recovers 10/17 with 0.582 extra candidates/step
abs=0.010, rel=0.10: recovers 13/17 with 4.598 extra candidates/step
abs=0.010, rel=0.20: recovers 14/17 with 6.317 extra candidates/step
abs=0.020, rel=0.20: recovers 14/17 with 8.764 extra candidates/step
```

## Interpretation

Run `096` supports the 0.01 / 10% preservation window as a useful balanced
policy. It does not recover the maximum possible count in the tested grid, but
the single extra recovery from relaxing to 20% relative tolerance costs about
37% more retained candidates per step. A much tighter 0.005 / 2% rule is
cheaper but loses three of the default-rule recoveries.

The paper-safe wording is therefore:

```text
We retain near-tie lateral branches under a bounded 0.01 absolute / 10%
relative objective-gap rule. This recovers most archive missed truth-lateral
near-ties while keeping the branch fanout bounded; looser thresholds recover
only one additional missed branch in the tested grid at materially higher
candidate-retention cost.
```

This remains CPU-side policy evidence. It does not authorize a broad GPU queue
or detector-seeded FWI.

## Validation

Focused test for the new threshold-sensitivity script:

```text
tests/test_local_2d_branch_preservation_threshold_sensitivity.py
3 passed
```

Focused detector/field regression:

```text
69 passed
```

Full suite:

```text
884 passed
```

Figure validation:

```text
local_2d_branch_preservation_threshold_sensitivity.png: 2227x903,
nonwhite=0.6313, dynamic range=255
```
