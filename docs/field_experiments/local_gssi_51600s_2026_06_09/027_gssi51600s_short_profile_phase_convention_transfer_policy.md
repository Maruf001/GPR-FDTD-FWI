# Field Experiment 027: GSSI 51600S Short-Profile Phase-Convention Transfer

Date: 2026-06-17

## Purpose

CPU-only cross-check of the 014/016 relative timing transfer across multiple
phase conventions. This tests whether the 016-minus-014 delay seen in field
experiments 024 and 025 is specific to the accepted top-envelope pick or is
also visible in independent phase landmarks.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/027_gssi51600s_short_profile_phase_convention_transfer_policy
```

Artifacts:

```text
data/short_profile_phase_convention_event_offsets.csv
data/short_profile_phase_convention_summary.csv
data/short_profile_phase_convention_transfer_summary.json
data/figure_validation.csv
figures/short_profile_phase_convention_transfer.png
run_manifest.json
```

## Inputs

```text
006_gssi51600s_phase_anchor_qc
021_gssi51600s_short_profile_stack_policy
```

Thresholds:

```text
max event-pair range per convention:      0.10 ns
max robust sigma per convention:          0.04 ns
minimum stable phase conventions:         4
max stable-convention median spread:      0.05 ns
accepted convention:                      top_envelope_35pct
```

## Result

Policy label:

```text
multi_phase_relative_time_zero_supported_qc
```

Stable phase conventions:

```text
top_envelope_35pct
signed_positive_peak
signed_negative_peak
nearest_zero_crossing
```

Summary:

```text
phase conventions tested:                 6
stable conventions:                       4
stable median offset range:               0.108055-0.127701 ns
stable median offset spread:              0.019646 ns
accepted top-envelope convention stable:  true
```

Convention table:

| Phase convention | Median 016 - 014 | Range | Stable |
| --- | ---: | ---: | --- |
| `current_cue` | 0.058939 ns | 0.117878 ns | false |
| `top_envelope_35pct` | 0.127701 ns | 0.068762 ns | true |
| `envelope_max` | 0.137525 ns | 0.127701 ns | false |
| `signed_positive_peak` | 0.117878 ns | 0.029470 ns | true |
| `signed_negative_peak` | 0.117878 ns | 0.039293 ns | true |
| `nearest_zero_crossing` | 0.108055 ns | 0.029470 ns | true |

## Interpretation

The 014/016 relative delay is not just a top-envelope artifact. All six tested
phase landmarks give positive 016-minus-014 delays, and four independent
landmarks meet the stability thresholds. This strengthens the field-data use
as relative timing/repeatability QC.

The result is still not an absolute calibrated time zero. It must not be used
as field radius, cover-depth, geometry, 3D, or FWI evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_short_profile_phase_convention_transfer_policy.py: 3 passed
```

The phase-convention figure was validated as nonblank:

```text
short_profile_phase_convention_transfer.png nonwhite=0.2685, dynamic range=255
```
