# Field Experiment 029: GSSI 51600S Short-Profile Timing Bootstrap

Date: 2026-06-17

## Purpose

CPU-only bootstrap uncertainty analysis for the 014/016 short-profile relative
timing offset. This uses the stable phase-convention event offsets from field
experiment 027 and estimates the uncertainty of the relative 016-minus-014
delay under cell, phase-convention-cluster, and event-pair-cluster resampling.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/029_gssi51600s_short_profile_timing_bootstrap_policy
```

Artifacts:

```text
data/short_profile_stable_phase_offsets.csv
data/short_profile_timing_bootstrap_summary.csv
data/short_profile_timing_bootstrap_policy_summary.json
data/figure_validation.csv
figures/short_profile_timing_bootstrap.png
run_manifest.json
```

## Inputs

```text
027_gssi51600s_short_profile_phase_convention_transfer_policy
```

Bootstrap settings:

```text
iterations:             20000
alpha:                  0.05
random seed:            20260617
minimum CI lower bound: 0.09 ns
maximum CI width:       0.05 ns
stable conventions:     4 minimum
```

## Result

Policy label:

```text
bootstrap_relative_time_zero_supported_qc
```

Summary:

```text
stable offsets:                12
stable phase conventions:      4
observed median offset:        0.117878 ns
minimum bootstrap CI lower:    0.108055 ns
maximum bootstrap CI upper:    0.147348 ns
maximum bootstrap CI width:    0.039293 ns
```

Bootstrap intervals:

| Method | Observed median | 95% CI lower | 95% CI upper | CI width |
| --- | ---: | ---: | ---: | ---: |
| cell | 0.117878 ns | 0.108055 ns | 0.132613 ns | 0.024558 ns |
| phase-convention cluster | 0.117878 ns | 0.108055 ns | 0.127701 ns | 0.019646 ns |
| event-pair cluster | 0.117878 ns | 0.108055 ns | 0.147348 ns | 0.039293 ns |

## Interpretation

The relative 014/016 delay remains positive and tightly bounded under several
small-sample resampling views. This strengthens the field timing/repeatability
claim with an uncertainty interval instead of only point estimates.

This is still relative timing QC only. It is not an absolute calibrated time
zero and must not be used as field radius, cover-depth, geometry, 3D, or FWI
evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_short_profile_timing_bootstrap_policy.py: 3 passed
```

The bootstrap figure was validated as nonblank:

```text
short_profile_timing_bootstrap.png nonwhite=0.0503, dynamic range=255
```
