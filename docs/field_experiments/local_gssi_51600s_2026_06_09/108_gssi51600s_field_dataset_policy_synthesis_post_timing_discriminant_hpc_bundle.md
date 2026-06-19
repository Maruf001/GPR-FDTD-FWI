# Field Experiment 108: Dataset Policy After Timing Discriminant/HPC Bundle

Date: 2026-06-18

## Purpose

Refresh the dataset-level field policy after the publication bundle was updated
to include:

```text
105_gssi51600s_field_timing_discriminant_scorecard
106_gssi51600s_field_hpc_dimensionality_decision_card
107_gssi51600s_field_publication_claim_bundle_post_timing_discriminant_hpc
```

This is a synthesis over existing field outputs. It does not run FDTD, FWI,
GPU kernels, neural-network training, 3D inversion, or HPC jobs.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/108_gssi51600s_field_dataset_policy_synthesis_post_timing_discriminant_hpc_bundle
```

Key artifacts:

```text
data/field_dataset_policy_evidence.csv
data/field_dataset_policy_summary.json
figures/field_dataset_policy.png
```

## Result

Policy label:

```text
field_2d_qc_not_3d_or_fwi
```

Key refreshed publication fields:

```text
publication bundle rows:             22 figures / 21 claim boundaries
timing discriminant included:        true
timing discriminant policy:          field_timing_discriminant_scorecard_ready_not_absolute
timing score rows:                   4
short non-raw timing supported:      18
long short-transfer rejections:       3
timing absolute time-zero ready:     false
timing field FWI ready:              false
HPC dimensionality included:         true
HPC geometry type:                   independent_2d_line_profiles
HPC ready for 2D QC:                 true
HPC ready for 3D:                    false
HPC ready for field FWI:             false
field HPC priority:                  none
```

## Interpretation

The refreshed dataset policy keeps the measured GSSI dataset in the scoped
2D-QC role. The field side can support timing/repeatability, supported-interval
visual QC, timing-window discrimination, apparent-depth guardrails, and
explicit dimensionality/HPC boundaries. It still cannot support absolute
time-zero, calibrated cover-depth, radius recovery, measured field FWI, 3D
inversion, or synthetic-policy relabeling.

## Validation

Figure validation:

```text
field_dataset_policy.png: 12939x835,
nonwhite=0.2572, dynamic range=255
```
