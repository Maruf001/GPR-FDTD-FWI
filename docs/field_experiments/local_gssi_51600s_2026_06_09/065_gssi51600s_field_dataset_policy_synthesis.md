# Field Experiment 065: GSSI 51600S Dataset Policy Through Relaxed Anchor Audit

Date: 2026-06-18

## Purpose

CPU-only refresh of the dataset-level field policy after run 064 tested relaxed
late-window phase anchors for the long 015/013 profile pair.

This run does not launch FDTD, FWI, GPU kernels, 3D reconstruction, or field
geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/065_gssi51600s_field_dataset_policy_synthesis
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

Newly incorporated evidence:

```text
064 relaxed long-profile phase-anchor audit:
  relaxed picks:                    10
  low-SNR picks:                    10 / 10
  best boundary solution count:      1
  relaxed-anchor policy:             long_profile_relaxed_phase_anchor_low_snr_not_time_zero
```

Key policy metrics:

```text
survey classification:              independent_2d_line_profiles
embedded segment candidate count:    0
long pair remains:                  pattern-only QC
field FWI / 3D priority:            none
```

## Interpretation

The relaxed audit strengthens the field claim boundary. The +0.06 ns
long-profile pattern shift remains supported as pattern-only QC, but relaxed
late-window picks are not clean enough to promote profile 013 into absolute
time-zero or measured-data FWI evidence. The field dataset remains useful for
2D measured-profile QC and manuscript supplement figures, not 3D/FWI claims.

## Validation

Focused tests:

```text
tests/test_gssi_field_dataset_policy_synthesis.py tests/test_gssi_field_phase_anchor_qc.py: 4 passed
```

Figure validation:

```text
field_dataset_policy.png: 12259x835,
nonwhite=0.2570, dynamic range=255
```
