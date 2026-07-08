# Field Experiment 130: GSSI 51600S Field Publication Claim Bundle Post Signed-Morphology Timing Margin

Date: 2026-06-18

## Purpose

Curate the latest short-anchor signed-morphology evidence into the field
publication claim bundle after the run `128` freshness audit and the run `129`
timing-margin audit. This is a saved-artifact packaging run, not a new field
inversion or GPU experiment.

The run reads existing field outputs only, including the current event-support
table from run `110`, morphology guardrails from runs `124-127`, and the
timing-margin audit from run `129`.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/130_gssi51600s_field_publication_claim_bundle_post_signed_morphology_timing_margin
```

Key artifacts:

```text
data/field_publication_figure_rows.csv
data/field_publication_claim_boundaries.csv
data/field_publication_claim_bundle_summary.json
figures/field_publication_claim_bundle.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                       field_publication_claim_bundle_2d_qc_short_timing_margin_short_morphology_hpc_dimensionality_timing_discriminant_timing_window_timing_anchor_cue_spacing_early_time_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
figure rows:                        27
claim boundaries:                   24
event-support source:               run 110
event-support rows:                 11
short signed morphology included:   true
timing-margin figure included:      true
timing-margin content-QC ready:     true
timing-margin conservative ready:   false
field FWI ready:                    false
3D/HPC ready:                       false
gpu priority:                       none
```

Interpretation: the field publication bundle now deliberately includes the
short-anchor waveform-coherence, radius-degeneracy, signed-morphology,
threshold-sensitivity, and timing-margin figures. The allowed claim remains
measured-field 2D QC and content-only morphology timing support. The bundle
still blocks absolute time-zero, conservative timing promotion, amplitude
calibration, radius/geometry/cover-depth recovery, field FWI, 3D inversion,
HPC workload, and synthetic-policy relabeling.

## Validation

```text
tests/test_gssi_field_publication_claim_bundle.py
16 passed
```

Figure validation:

```text
field_publication_claim_bundle.png: 2484x1852,
nonwhite=0.0687, dynamic range=255
```
