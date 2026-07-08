# Field Experiment 080: Cue-Spacing Context Audit

Date: 2026-06-18

## Purpose

Summarize measured reflector-cue spacing in the local GSSI 51600S profiles so
the field dataset can be described honestly in a manuscript context. This is a
CPU-only field-data context audit. It does not launch FDTD, FWI, GPU kernels,
3D inversion, radius recovery, cover-depth recovery, or synthetic relabeling.

## Outputs

```text
093_gssi51600s_field_cue_spacing_context_audit
094_gssi51600s_field_cue_spacing_sensitivity_audit
095_gssi51600s_field_publication_claim_bundle_post_cue_spacing_context
096_gssi51600s_field_dataset_policy_synthesis_post_cue_spacing_bundle
```

Key artifacts:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/093_gssi51600s_field_cue_spacing_context_audit/data/field_cue_spacing_context_summary.json
outputs/field_experiments/local_gssi_51600s_2026_06_09/093_gssi51600s_field_cue_spacing_context_audit/data/field_cue_spacing_profile_context.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/093_gssi51600s_field_cue_spacing_context_audit/data/field_cue_spacing_pair_context.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/093_gssi51600s_field_cue_spacing_context_audit/figures/field_cue_spacing_context_audit.png
outputs/field_experiments/local_gssi_51600s_2026_06_09/094_gssi51600s_field_cue_spacing_sensitivity_audit/data/field_cue_spacing_threshold_sensitivity_summary.json
outputs/field_experiments/local_gssi_51600s_2026_06_09/094_gssi51600s_field_cue_spacing_sensitivity_audit/data/field_cue_spacing_threshold_sensitivity_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/094_gssi51600s_field_cue_spacing_sensitivity_audit/figures/field_cue_spacing_threshold_sensitivity.png
outputs/field_experiments/local_gssi_51600s_2026_06_09/095_gssi51600s_field_publication_claim_bundle_post_cue_spacing_context/data/field_publication_figure_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/095_gssi51600s_field_publication_claim_bundle_post_cue_spacing_context/data/field_publication_claim_boundaries.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/096_gssi51600s_field_dataset_policy_synthesis_post_cue_spacing_bundle/data/field_dataset_policy_summary.json
```

## Result

```text
policy label:                         field_cue_spacing_context_not_resolution_benchmark
profiles:                             4
cue count:                            19
pair count:                           39
same-time threshold:                  0.15 ns
same-time lateral pairs:              21
time-separated lateral pairs:         15
same-x / vertical pairs:               3
min same-time lateral spacing:        269.973 mm
min distinct-x spacing, any time:      96.657 mm
min short-pair same-time spacing:     269.973 mm
min long-pair same-time spacing:      589.941 mm
geometry classification:              independent_2d_line_profiles
resolution benchmark ready:           false
field FWI ready:                      false
3D HPC ready:                         false
gpu priority:                         none
```

Run 094:

```text
policy label:                         field_cue_spacing_context_threshold_robust_not_resolution_benchmark
threshold count:                      7
thresholds:                           0.050,0.100,0.150,0.200,0.300,0.500,1.000 ns
min spacing across thresholds:        96.657 mm
max same-time lateral pair count:     32
all thresholds wider than close scale true
resolution benchmark ready:           false
field FWI ready:                      false
3D HPC ready:                         false
gpu priority:                         none
```

Publication/policy promotion:

```text
095 policy label:                    field_publication_claim_bundle_2d_qc_cue_spacing_early_time_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
095 figure rows:                     18
095 claim boundaries:                17
095 cue-spacing context ready:       true
095 resolution benchmark ready:      false
095 field FWI ready:                 false
096 policy label:                    field_2d_qc_not_3d_or_fwi
096 publication figure rows:         18
096 publication claim boundaries:    17
096 publication cue-spacing policy:  field_cue_spacing_context_threshold_robust_not_resolution_benchmark
096 publication cue min spacing:     96.657 mm
096 publication cue field FWI ready: false
```

## Interpretation

The visible measured-field cue spacings are much wider than the synthetic
close25-close50 stress scale when the cues are compared at similar times. The
closest distinct-x field pair is about 96.7 mm, but it is time-separated, so it
should not be used as a same-depth close-spacing resolution example.

This result is useful for manuscript context: the local field dataset is
measured 2D QC evidence, not a known-truth close-rebar resolution benchmark.
It does not validate, invalidate, or relabel the synthetic resolution-policy
tables, and it does not create cover-depth, radius, field FWI, or 3D readiness.

Run 094 strengthens that boundary by removing dependence on the single
0.15 ns same-time threshold. Across same-time thresholds from 0.05 to 1.00 ns,
the minimum admitted lateral spacing remains 96.657 mm, still wider than the
synthetic close25-close50 stress scale.

Runs 095-096 promote this cue-spacing evidence into the current structured
field publication bundle and dataset policy. The promotion adds a figure row
and claim boundary, but keeps the same restriction: field cue spacing is
measured-context evidence only, not known-truth rebar spacing, synthetic
resolution validation, cover-depth/radius evidence, field FWI, or 3D input.

## Validation

Focused cue-spacing tests:

```text
tests/test_gssi_field_cue_spacing_context_audit.py
tests/test_gssi_field_cue_spacing_sensitivity_audit.py
5 passed
```

Focused bundle/policy refresh tests:

```text
tests/test_gssi_field_publication_claim_bundle.py
tests/test_gssi_field_dataset_policy_synthesis.py
tests/test_local_2d_field_manuscript_evidence_audit.py
19 passed
```

Figure validation:

```text
093 field_cue_spacing_context_audit.png: 2365x835, dynamic range=255
094 field_cue_spacing_threshold_sensitivity.png: 2331x835, dynamic range=255
```
