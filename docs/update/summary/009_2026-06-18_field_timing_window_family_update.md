# Field Timing-Window Family Update

Date: 2026-06-18

## Scope

This update records the local DGX-side field-data work after the current 3D/HPC
planning was split off. No GPU experiment, field FWI, or 3D run was launched.

## New Field Evidence

Run 101 classifies timing evidence by window family:

```text
policy label:                         field_timing_window_family_classification_ready_not_absolute
strict early near-zero lags:          6/6
short non-raw supported windows:      18/18
raw/no-correction supported windows:  0/3
long windows rejecting short transfer: 3/3
absolute time-zero ready:             false
field FWI ready:                      false
gpu priority:                         none
```

Interpretation: early/direct/ringdown windows behave as a common-mode negative
control, short content windows support the relative timing correction, and long
windows reject transferring the short-pair correction. This supports a timing
scope boundary only.

## Promoted Endpoints

Runs 102-104 promote that evidence into the current field evidence chain:

```text
102 publication bundle: 20 figures, 19 claim boundaries, ready, gpu none
103 dataset policy:     field_2d_qc_not_3d_or_fwi
104 source notes:       20/20 source figures have FIGURE_NOTES.md
```

The current field table package is:

```text
outputs/summary_tables/009_local_2d_field_manuscript_table_pack_post_timing_window_family
```

Key table-pack counts:

```text
claim rows:       30
figure rows:      29
metric rows:      16
field figures:    20
field claims:     19
field notes:      20/20
ready:            true
gpu priority:     none
```

The current cross-domain scope map is:

```text
outputs/summary_tables/010_local_2d_field_cross_domain_scope_map_post_timing_window_family
```

Key scope-map counts:

```text
scope rows:                         7
field minimum same-time spacing:     96.657 mm
synthetic close-spacing context max: 50.000 mm
field/synthetic spacing ratio:       1.933
short timing-window support:         18/18
long rejection of short transfer:    3/3
field resolution benchmark ready:    false
field FWI ready:                     false
synthetic immediate GPU candidates:  0
synthetic conditional GPU candidates: 0
ready:                              true
gpu priority:                       none
```

Interpretation: synthetic known-truth resolution/ambiguity claims and
measured-field timing/spacing QC can sit in the same manuscript evidence
package, but they must not be merged into a single field-validation claim.

The current field methods data card is:

```text
outputs/summary_tables/011_local_gssi_field_dataset_card_post_timing_window_family
```

Key data-card counts:

```text
profiles:                 4
total traces:             2169
samples per trace:        510
scan spacing:             3.333 mm
antenna frequency:        1600 MHz
dielectric setting:       2.25
center wavelength:        124.914 mm
samples per wavelength:   37.478
trace-derived length:     7.215945 m
survey classification:    independent_2d_line_profiles
ready for 2D QC:          true
ready for 3D/HPC:         false
ready for field FWI:      false
```

The current synthetic methods corpus card is:

```text
outputs/summary_tables/012_synthetic_2d_archive_corpus_card_post_field_timing_refresh
```

Key synthetic corpus-card counts:

```text
archive runs:                       1325
physics/diagnostic runs:             802
analysis/report runs:                181
reporting/audit/checkpoint runs:     188
unclear run-type count:              154
image-bearing runs:                 1111
figure-note coverage:               963/1111
legacy issue count:                  130
current publication figures:          9/9
current claim boundaries:             11
current source figure notes:           9/9
synthetic immediate GPU candidates:    0
synthetic conditional GPU candidates:  0
```

Interpretation: the current synthetic paper-facing endpoint is ready and
source-note covered. Legacy archive hygiene caveats remain historical; they are
not a reason to regenerate old runs or launch broad GPU experiments.

## Timing Discriminant Scorecard

Run 105 adds a row-level timing discriminant scorecard over the existing field
timing evidence:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/105_gssi51600s_field_timing_discriminant_scorecard
```

Key scorecard counts:

```text
policy label:                         field_timing_discriminant_scorecard_ready_not_absolute
score rows:                           4
strict early near-zero windows:       6/6
early minimum uniqueness margin:      3.017058e-05
short non-raw supported windows:      18/18
raw/no-correction supported windows:  0/3
short nominal relative offset:        0.127701 ns
short minimum matrix improvement:     0.125152
long windows rejecting short transfer: 3/3
long best offset median:              0.060000 ns
long/short offset separation:         0.067701 ns
absolute time-zero ready:             false
field FWI ready:                      false
gpu priority:                         none
```

Interpretation: this strengthens the timing-language boundary. Early windows
are useful as common-mode controls, but the low early uniqueness margin blocks
an absolute time-zero claim. Short non-raw windows support the relative
correction, raw/no-correction is rejected, and long windows support only a
separate pattern-timing statement.

## Field Claim Viability Scorecard

The current field claim-viability scorecard is:

```text
outputs/summary_tables/013_local_gssi_field_claim_viability_scorecard_post_timing_discriminant
```

Key scorecard counts:

```text
policy label:                    local_gssi_field_claim_viability_scorecard_ready_no_field_fwi
claim rows:                      13
supported rows:                   3
scope-limited rows:               5
context-only rows:                1
rejected-control rows:            1
blocked rows:                     3
ready for 2D field QC:            true
ready for absolute time-zero:     false
ready for cover-depth recovery:   false
ready for radius recovery:        false
ready for field FWI:              false
ready for 3D/HPC:                 false
gpu priority:                     none
```

Interpretation: the field data now have a compact manuscript-facing claim
separation table. They support 2D line-profile QC, short-pair relative timing,
and the current publication field-figure bundle. Timing, spacing, event-support,
and apparent-depth rows remain scope-limited or contextual. Absolute time-zero,
cover-depth recovery, radius recovery, field FWI, and field-side HPC/3D claims
remain blocked.

## Decision

The measured GSSI field data should continue to be used as 2D line-profile QC,
repeatability, timing-boundary, and manuscript supplement evidence. It is still
not a calibrated absolute time-zero, cover-depth, radius, field FWI, 3D, or HPC
inversion benchmark.
