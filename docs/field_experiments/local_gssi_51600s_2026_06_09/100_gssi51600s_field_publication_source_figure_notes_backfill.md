# Field Experiment 100: Publication Source Figure Notes Backfill

Date: 2026-06-18

## Purpose

Backfill `figures/FIGURE_NOTES.md` for the source figures referenced by the
current field publication bundle:

```text
098_gssi51600s_field_publication_claim_bundle_post_timing_anchor_conflict
```

This is a targeted manuscript-handoff hygiene pass. It does not regenerate
field figures, run FDTD/FWI, use GPU kernels, or promote 3D, cover-depth,
radius, absolute time-zero, or measured-field inversion claims.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/100_gssi51600s_field_publication_source_figure_notes_backfill
```

Key artifacts:

```text
data/field_publication_source_figure_notes_backfill_rows.csv
data/field_publication_source_figure_notes_backfill_summary.json
run_manifest.json
```

## Result

```text
policy label:              field_publication_source_figure_notes_backfill_complete_skip_existing
source figures audited:    19
generated notes:           18
skipped existing notes:    1
missing figures:           0
notes present after:       19
gpu priority:              none
ready for handoff:         true
```

## Interpretation

The current field publication bundle already had its own summary figure notes,
but most referenced source figures did not. This run fixes the paper-facing
source-figure provenance gap using skip-existing behavior and leaves existing
figures untouched.

The resulting notes describe each source figure's bundle key, source run,
policy/status, support metric, allowed use, and no-FWI/no-3D/no-depth/radius
scope boundary.
