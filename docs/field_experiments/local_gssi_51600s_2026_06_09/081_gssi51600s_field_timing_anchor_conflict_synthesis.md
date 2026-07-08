# Field Experiment 081: Timing-Anchor Conflict Synthesis

Date: 2026-06-18

## Purpose

Synthesize the current field timing-anchor evidence into one CPU-only endpoint.
This run compares the short-profile content-backed relative time-zero estimate,
the early/common-mode direct-ringdown alignment, and the long-profile
pattern-only shift. It does not launch FDTD, FWI, GPU kernels, 3D inversion,
radius recovery, cover-depth recovery, or synthetic relabeling.

## Output

```text
097_gssi51600s_field_timing_anchor_conflict_synthesis
```

Key artifacts:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/097_gssi51600s_field_timing_anchor_conflict_synthesis/data/field_timing_anchor_conflict_summary.json
outputs/field_experiments/local_gssi_51600s_2026_06_09/097_gssi51600s_field_timing_anchor_conflict_synthesis/data/field_timing_anchor_conflict_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/097_gssi51600s_field_timing_anchor_conflict_synthesis/data/field_timing_anchor_guardrail_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/097_gssi51600s_field_timing_anchor_conflict_synthesis/data/field_timing_anchor_claim_boundaries.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/097_gssi51600s_field_timing_anchor_conflict_synthesis/figures/field_timing_anchor_conflict.png
```

## Result

```text
policy label:                         field_timing_anchor_conflict_short_relative_not_absolute
anchor rows:                          7
guardrail rows:                       7
claim boundaries:                     4
short content-backed offset:          0.127701 ns
short conservative half-width:        0.058939 ns
early/common-mode shift:              0.000000 ns
long pattern-only offset:             0.060000 ns
early vs short delta:                 0.127701 ns
early vs short delta / half-width:    2.167
long vs short delta:                  0.067701 ns
long vs short delta / half-width:     1.149
long vs early delta:                  0.060000 ns
early agrees with content budget:     false
long rejects short transfer:          true
perturbation budget supported:        true
absolute time-zero ready:             false
cover-depth ready:                    false
radius ready:                         false
field FWI ready:                      false
gpu priority:                         none
```

## Interpretation

The field timing anchors are not interchangeable. The short 014/016
content-backed offset remains the supported relative time-zero QC estimate, but
the early/common-mode direct-ringdown alignment sits at zero lag and differs by
2.17 conservative half-widths. The long 015/013 pair has a stable +0.06 ns
pattern-only shift, but that is still 1.15 half-widths away from the short
content-backed offset and rejects short-transfer behavior across all tested
windows.

The correct manuscript boundary is therefore sharper than "field timing is
uncertain": the field contains distinct timing cues with distinct scopes. They
should not be averaged or reconciled into one absolute time-zero, cover-depth,
radius, field FWI, or 3D inversion claim.

## Validation

Focused tests:

```text
tests/test_gssi_field_timing_anchor_conflict_synthesis.py
tests/test_gssi_field_early_time_anchor_audit.py
tests/test_gssi_field_time_zero_uncertainty_budget.py
tests/test_gssi_field_time_zero_perturbation_sensitivity.py
13 passed
```

Figure validation:

```text
field_timing_anchor_conflict.png: 2535x903, dynamic range=255
```

## Promotion

Runs `098-099` promote this timing-anchor boundary into the structured field
publication bundle and dataset policy:

```text
098_gssi51600s_field_publication_claim_bundle_post_timing_anchor_conflict
099_gssi51600s_field_dataset_policy_synthesis_post_timing_anchor_bundle
```

The promoted bundle has 19 field figure rows and 18 field claim boundaries.
The dataset policy remains `field_2d_qc_not_3d_or_fwi`; the timing-anchor
synthesis is manuscript scope evidence, not absolute time-zero calibration or
field FWI input.
