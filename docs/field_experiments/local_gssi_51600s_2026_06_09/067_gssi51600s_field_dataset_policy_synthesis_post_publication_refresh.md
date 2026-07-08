# Field Experiment 067: GSSI 51600S Dataset Policy After Publication Bundle Refresh

Date: 2026-06-18

## Purpose

CPU-only dataset-level policy refresh after run 066 packaged the relaxed
long-profile phase-anchor audit as paper-facing negative QC.

This run does not launch FDTD, FWI, GPU kernels, 3D reconstruction, or field
geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/067_gssi51600s_field_dataset_policy_synthesis_post_publication_refresh
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

Updated publication-bundle evidence:

```text
publication bundle policy:          field_publication_claim_bundle_2d_qc_relaxed_anchor_negative_ready_not_fwi
publication figure rows:            8
publication claim boundaries:       7
publication bundle ready:           true
field GPU/FWI priority:             none
```

Relaxed-anchor evidence remains:

```text
relaxed-anchor policy:              long_profile_relaxed_phase_anchor_low_snr_not_time_zero
relaxed picks:                      10
relaxed low-SNR picks:              10
relaxed boundary solution count:    1
```

## Interpretation

The dataset policy is unchanged in substance but is now aligned with the
current paper-facing field bundle:

```text
The local GSSI 51600S data are independent 2D line-profile QC and timing
evidence. They are not a 3D survey, measured-data FWI benchmark, cover-depth
estimate, or field radius estimate.
```

## Validation

Focused tests:

```text
tests/test_gssi_field_publication_claim_bundle.py
tests/test_gssi_field_dataset_policy_synthesis.py
8 passed
```

Figure validation:

```text
field_dataset_policy.png: 12259x835,
nonwhite=0.2570, dynamic range=255
```
