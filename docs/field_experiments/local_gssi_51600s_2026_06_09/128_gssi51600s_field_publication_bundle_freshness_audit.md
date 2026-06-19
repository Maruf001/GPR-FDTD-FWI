# Field Experiment 128: GSSI 51600S Field Publication Bundle Freshness Audit

Date: 2026-06-18

## Purpose

Check whether the curated field publication figure bundle should be refreshed
with the latest short-anchor morphology-chain figures from runs `124-127`.

This was a CPU saved-artifact audit. It read the current publication bundle
and saved morphology summaries only. It did not regenerate the publication
bundle, run DZT preprocessing, FDTD, FWI, GPU kernels, 3D/HPC jobs, or
neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/128_gssi51600s_field_publication_bundle_freshness_audit
```

Key artifacts:

```text
data/field_publication_bundle_freshness_candidates.csv
data/field_publication_bundle_freshness_summary.json
figures/field_publication_bundle_freshness_audit.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         gssi51600s_field_publication_bundle_freshness_audit_curated_refresh_needed_not_automatic
current bundle figures:               22
candidate latest morphology figures:   4
candidates already in bundle:          0
candidate missing figures:             0
candidate QC-ready figures:            4
primary refresh candidates:            2
guardrail refresh candidates:          2
candidate field-FWI-ready figures:     0
curated refresh decision ready:        true
automatic bundle refresh ready:        false
field FWI ready:                       false
3D/HPC ready:                          false
gpu priority:                          none
```

Interpretation: the latest morphology chain is not in the curated 22-figure
publication bundle. If the field supplement is refreshed, runs `126-127`
should be considered first as primary signed-morphology/threshold-margin
figures, while runs `124-125` are guardrail candidates. Do not auto-promote
them into the bundle or into field FWI, 3D/HPC, radius, geometry, or cover-depth
claims.

## Validation

```text
tests/test_gssi_field_publication_bundle_freshness_audit.py
2 passed
```

Figure validation:

```text
field_publication_bundle_freshness_audit.png: 2263x835,
nonwhite=0.1492, dynamic range=255
```
