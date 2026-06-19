# Experiment 813: Synthetic Objective-Threshold Sensitivity

Date: 2026-06-17

## Purpose

CPU-only threshold-sensitivity audit for the known-acquisition target2 close14
x-resolution caveat identified by experiments 811 and 812. This tests whether
the close14 target2 near ties are robust under tighter ambiguity thresholds or
only default-threshold edge cases.

This run does not launch FDTD, FWI, GPU kernels, or new inversion experiments.

## Output

```text
outputs/experiments/1291_synthetic_objective_threshold_sensitivity
```

Artifacts:

```text
data/synthetic_objective_threshold_sensitivity_rows.csv
data/synthetic_objective_threshold_sensitivity_summary.json
data/figure_validation.csv
figures/synthetic_objective_threshold_sensitivity.png
run_manifest.json
```

## Result

Policy label:

```text
close14_target2_objective_threshold_sensitivity_source5_persistent_cpu_no_gpu
```

Summary:

```text
family:                               target2_close14
geometry delta:                       x
default-scale row count:              102
near ties at 0.5x threshold:            2
near ties at 0.75x threshold:           2
near ties at 1.0x threshold:            4
near ties at 1.25x threshold:          48
source5 Tx/Rx45 near ties at 0.5x:      2
source5 Tx/Rx45 near ties at 1.0x:      2
source4 Tx/Rx45 default edge count:     1
source7 Tx/Rx45 default edge count:     1
source4 Tx/Rx50 default near ties:      0
source4 Tx/Rx50 near ties at 1.25x:    38
gpu priority:                          none_now
```

The source5 / Tx/Rx=45 mm near ties persist even at a 0.5x ambiguity threshold,
with gap-to-threshold ratios around 0.20-0.29. The source4 and source7
Tx/Rx=45 mm default near ties are edge cases. Tx/Rx=50 mm is clean at the
default threshold, but becomes sensitive under looser thresholds.

## Interpretation

This supports a narrower future question: if a synthetic GPU probe is later
needed, it should target source5 / Tx/Rx=45 mm target2 close14 x-resolution
after the objective threshold is fixed. It does not justify broad GPU sweeps,
target1 reruns, or close50 reruns.

## Validation

Focused tests:

```text
tests/test_synthetic_objective_threshold_sensitivity.py: 3 passed
```

Figure validation:

```text
synthetic_objective_threshold_sensitivity.png: 2569x903,
nonwhite=0.1376, dynamic range=255
```
