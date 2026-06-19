# Field Experiment 104: Source Figure Notes Backfill After Timing-Window Bundle

Date: 2026-06-18

## Purpose

Audit the source figures referenced by the current field publication bundle
after experiment 102 added the timing-window family figure.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/104_gssi51600s_field_publication_source_figure_notes_backfill_post_timing_window_family
```

Key artifacts:

```text
data/field_publication_source_figure_notes_backfill_rows.csv
data/field_publication_source_figure_notes_backfill_summary.json
run_manifest.json
```

## Result

```text
policy label:           field_publication_source_figure_notes_backfill_complete_skip_existing
bundle run:             102_gssi51600s_field_publication_claim_bundle_post_timing_window_family
source figures audited: 20
generated notes:        0
skipped existing notes: 20
missing figures:        0
notes present after:    20
gpu priority:           none
ready for handoff:      true
```

## Interpretation

The current field publication bundle now has complete source-figure provenance
coverage. This run did not regenerate figures or promote new field inversion
claims.
