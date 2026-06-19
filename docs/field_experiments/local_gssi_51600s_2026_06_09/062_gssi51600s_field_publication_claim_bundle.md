# Field Experiment 062: GSSI 51600S Field Publication Claim Bundle Refresh

Date: 2026-06-17

## Purpose

CPU-only refresh of the field publication claim bundle after the long-profile
holdout sensitivity runs 060 and 061. The older bundle 059 remained valid but
did not include structured rows for the all-anchor time-window and spatial-width
sensitivity evidence.

This run packages field QC figures and claim boundaries only. It does not
launch FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/062_gssi51600s_field_publication_claim_bundle
```

Artifacts:

```text
data/field_publication_figure_rows.csv
data/field_publication_claim_boundaries.csv
data/field_publication_claim_bundle_summary.json
data/figure_validation.csv
figures/field_publication_claim_bundle.png
run_manifest.json
```

## Result

Policy label:

```text
field_publication_claim_bundle_2d_qc_sensitivity_ready_not_fwi
```

Summary:

```text
figure rows:                          7
claim boundaries:                     6
geometry classification:              independent_2d_line_profiles
long holdout policy:                  all candidate anchors supported
long time-window sensitivity ready:   true
long spatial-width sensitivity ready: true
ready for manuscript supplement:      true
gpu priority:                         none
```

Structured figure rows now include:

```text
015 survey geometry boundary
035 short content-backed waveform QC
049 short supported corrected-stack intervals
057 long pattern-only visual QC
058 long repeat-limited-anchor holdout QC
060 long all-anchor time-window sensitivity
061 long all-anchor spatial-width sensitivity
```

## Interpretation

Run 062 supersedes run 059 as the current structured field paper bundle because
it includes both sensitivity checks that were added after 059. The claim
boundary remains conservative: this is measured 2D line-profile QC evidence and
not field FWI, 3D reconstruction, radius, cover-depth, or absolute time-zero
evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_publication_claim_bundle.py: 3 passed
```

Figure validation:

```text
field_publication_claim_bundle.png: 2569x869,
nonwhite=0.2643, dynamic range=255
```
