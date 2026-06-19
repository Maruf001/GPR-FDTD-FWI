# Field Experiment 068-071: GSSI 51600S Band-Limited Repeatability Audit

Date: 2026-06-18

## Purpose

CPU-only field-data audit of which measured frequency bands support the current
short-profile relative time-zero correction and the long-profile pattern-only
shift. This is a band-selection and repeatability-QC step, not field FWI, 3D
reconstruction, cover-depth estimation, or radius inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/068_gssi51600s_field_bandlimited_repeatability_audit
outputs/field_experiments/local_gssi_51600s_2026_06_09/069_gssi51600s_field_dataset_policy_synthesis_post_bandlimited_audit
outputs/field_experiments/local_gssi_51600s_2026_06_09/070_gssi51600s_field_publication_claim_bundle_post_bandlimited_audit
outputs/field_experiments/local_gssi_51600s_2026_06_09/071_gssi51600s_field_dataset_policy_synthesis_post_bandlimited_bundle
```

Artifacts:

```text
068/data/field_bandlimited_repeatability_rows.csv
068/data/field_bandlimited_repeatability_summary.json
068/figures/field_bandlimited_repeatability.png
069/data/field_dataset_policy_evidence.csv
069/data/field_dataset_policy_summary.json
069/figures/field_dataset_policy.png
070/data/field_publication_figure_rows.csv
070/data/field_publication_claim_boundaries.csv
070/data/field_publication_claim_bundle_summary.json
071/data/field_dataset_policy_evidence.csv
071/data/field_dataset_policy_summary.json
```

## Result

Run 068:

```text
policy label:                   field_bandlimited_repeatability_short_pair_supported_long_pattern_only
time window:                    0.55-3.40 ns
short 014/016 raw |corr|:        0.545551
short 014/016 corrected |corr|:  0.771287
short 014/016 gain:             0.225736
short supported bands:          low, mid_low, mid_high, broad
long 015/013 raw |corr|:         0.789502
long 015/013 pattern |corr|:     0.905584
long 015/013 pattern gain:       0.116082
long pattern-supported bands:   mid_low, mid_high, high, broad
field GPU/FWI priority:         none
```

The short high band was not promoted because retained energy was below the
support threshold. The long pair remains pattern-only despite good band-limited
agreement because profile 013 still lacks usable phase-anchor picks.

Run 069:

```text
policy label:                   field_2d_qc_not_3d_or_fwi
band policy included:           field_bandlimited_repeatability_short_pair_supported_long_pattern_only
short supported band count:     4
long pattern band count:        4
survey classification:          independent_2d_line_profiles
field GPU/FWI priority:         none
```

Runs 070-071:

```text
publication bundle policy:       field_publication_claim_bundle_2d_qc_bandlimited_relaxed_anchor_ready_not_fwi
publication figure rows:         9
publication claim boundaries:    8
band figure included:            true
publication bundle ready:        true
current dataset policy label:    field_2d_qc_not_3d_or_fwi
field GPU/FWI priority:          none
```

## Interpretation

For field figures or later field-to-synthetic visual comparison, the current
short-pair evidence supports low through mid-high and broad-band measured QC
after the accepted relative time-zero transfer. It does not support treating
the highest band alone as a robust short-pair field figure basis.

The long-pair band result is useful, but only as pattern support for the
already documented +0.06 ns alignment. It does not upgrade long-profile
time-zero calibration and must stay out of measured-data FWI or 3D claims.

## Validation

Focused tests:

```text
tests/test_gssi_field_bandlimited_repeatability_audit.py
tests/test_gssi_field_publication_claim_bundle.py
tests/test_gssi_field_dataset_policy_synthesis.py
12 passed
```

Figure validation:

```text
068 field_bandlimited_repeatability.png: 2195x1549, dynamic range=255
069 field_dataset_policy.png: 12259x835, dynamic range=255
070 field_publication_claim_bundle.png: 2569x869, dynamic range=255
071 field_dataset_policy.png: 12259x835, dynamic range=255
```
