# Field Experiment 056: GSSI 51600S Dataset Policy Through Long Shift Sensitivity

Date: 2026-06-17

## Purpose

CPU-only dataset-level field policy refresh after the long-profile shift-scan
sensitivity check in field experiment 055.

This run does not launch FDTD, FWI, GPU kernels, 3D reconstruction, or field
geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/056_gssi51600s_field_dataset_policy_synthesis
```

Artifacts:

```text
data/field_dataset_policy_evidence.csv
data/field_dataset_policy_summary.json
data/figure_validation.csv
figures/field_dataset_policy.png
run_manifest.json
```

## Result

Policy label:

```text
field_2d_qc_not_3d_or_fwi
```

Key added evidence:

| Evidence | Status | Key metric | Limitation |
| --- | --- | ---: | --- |
| Long-pair pattern shift sensitivity | `long_profile_pattern_shift_window_robust_rejects_short_transfer` | best offset spread 0.000 ns | pattern-shift stability only |

Current field-data statement:

```text
The long 015/013 pair has a robust pattern-only +0.06 ns shift across the
tested shallow windows, while the inherited 014/016 short-pair offset is
negative in every window. The local GSSI dataset remains 2D line-profile
timing/QC evidence, not a 3D survey or measured-data FWI benchmark.
```

## Validation

Focused tests:

```text
tests/test_gssi_field_long_profile_shift_scan_sensitivity.py
tests/test_gssi_field_dataset_policy_synthesis.py
```

The dataset policy figure was validated as nonblank:

```text
field_dataset_policy.png: 11579x835,
nonwhite=0.2588, dynamic range=255
```
