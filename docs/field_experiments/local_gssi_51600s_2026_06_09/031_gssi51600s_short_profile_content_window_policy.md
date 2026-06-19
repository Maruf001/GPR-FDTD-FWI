# Field Experiment 031: GSSI 51600S Short-Profile Content Window Policy

Date: 2026-06-17

## Purpose

CPU-only content-QC reduction for the aligned short-profile pair 014/016. This
run separates repeat-backed stack-content windows from timing-only field cues
using the short-profile stack from experiment 021 and the bootstrap timing
policy from experiment 029.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/031_gssi51600s_short_profile_content_window_policy
```

Artifacts:

```text
data/short_profile_content_windows.csv
data/short_profile_event_content_classification.csv
data/short_profile_content_window_policy_summary.json
data/figure_validation.csv
figures/short_profile_content_window_policy.png
run_manifest.json
```

## Inputs

```text
021_gssi51600s_short_profile_stack_policy
029_gssi51600s_short_profile_timing_bootstrap_policy
```

## Result

Policy label:

```text
repeat_content_windows_limited_qc
```

Summary:

```text
stable content windows:                 2
event pairs:                            3
content-backed event pairs:             2
timing-only event pairs:                1
content-backed event fraction:          0.667
max content anchor distance:            9.999 mm
max timing residual to bootstrap median: 0.058939 ns
max content-backed timing residual:      0.009823 ns
```

Content windows:

| Window | Center | Nearest event pair | Event distance | Peak stack z |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 396.627 mm | 2 | 6.666 mm | 10.2020 |
| 2 | 703.263 mm | 3 | 9.999 mm | 10.9257 |

Event classification:

| Pair | Reference x | Content label | Timing residual to bootstrap median |
| ---: | ---: | --- | ---: |
| 1 | 129.987 mm | `timing_only_no_stable_content_anchor` | +0.058939 ns |
| 2 | 403.293 mm | `repeat_content_anchor` | -0.009823 ns |
| 3 | 693.264 mm | `repeat_content_anchor` | +0.009823 ns |

## Interpretation

The short 014/016 pair has two repeatable profile-content windows, but not all
timing picks are equal content evidence. Event pair 1 remains timing-only: it
does not sit near a stable stack-content anchor and falls outside the bootstrap
CI envelope used by this reducer. Event pairs 2 and 3 are the better candidates
for later field-to-synthetic visual comparison because they are both
content-backed and close to the bootstrap timing median.

This remains field profile QC only. It should not be used as field radius,
cover-depth, geometry, 3D, or FWI evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_short_profile_content_window_policy.py: 4 passed
```

The content-window figure was validated as nonblank:

```text
short_profile_content_window_policy.png nonwhite=0.1185, dynamic range=255
```
