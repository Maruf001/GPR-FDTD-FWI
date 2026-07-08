# Field Experiment 133: GSSI 51600S Field Publication Claim Bundle Post Signal-Contrast Sensitivity

Date: 2026-06-18

## Purpose

Refresh the curated field publication claim bundle after the run `131`
short-anchor signal-contrast audit and the run `132` contrast-window
sensitivity audit.

This is a saved-artifact packaging run. It reads existing field outputs only
and does not run FDTD, FWI, GPU kernels, 3D/HPC work, or neural-network
training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/133_gssi51600s_field_publication_claim_bundle_post_signal_contrast_sensitivity
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
policy label:                         field_publication_claim_bundle_2d_qc_short_signal_contrast_short_timing_margin_short_morphology_hpc_dimensionality_timing_discriminant_timing_window_timing_anchor_cue_spacing_early_time_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
figure rows:                          29
claim boundaries:                     25
event-support source:                 run 110
short signal contrast included:       true
short signal supported windows:       4 / 4
short signal min RMS ratio:           4.129473194969804
short signal sensitivity combos:      27
all-supported sensitivity combos:     13
window-invariant contrast ready:      false
absolute amplitude calibration ready: false
field FWI ready:                      false
3D/HPC ready:                         false
gpu priority:                         none
```

Interpretation: run `133` supersedes run `130` as the current curated field
publication bundle. It packages the short-anchor waveform-coherence,
radius-degeneracy, signed-morphology, threshold-sensitivity, timing-margin,
signal-contrast, and signal-contrast sensitivity figures into one scoped field
supplement bundle. The allowed claim remains measured-field 2D timing and
morphology QC. The bundle still blocks absolute time-zero, conservative timing
promotion, amplitude calibration, strict window-invariant contrast,
radius/geometry/cover-depth recovery, field FWI, 3D inversion, HPC workload,
and synthetic-policy relabeling.

## Validation

```text
tests/test_gssi_field_publication_claim_bundle.py
17 passed
```

Figure validation:

```text
field_publication_claim_bundle.png: 2484x1968,
nonwhite=0.0701, dynamic range=255
```
