# Experiment 833: Synthetic Publication Source Figure Notes Backfill

Date: 2026-06-18

## Purpose

Backfill `figures/FIGURE_NOTES.md` for the source figures referenced by the
current synthetic 2D publication bundle:

```text
1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation
```

This is a targeted manuscript-handoff hygiene pass. It does not regenerate
figures, run FDTD/FWI, use GPU kernels, or create a new synthetic acquisition
claim.

## Output

```text
outputs/experiments/1325_synthetic_publication_source_figure_notes_backfill_report
```

Key artifacts:

```text
data/synthetic_publication_source_figure_notes_backfill_rows.csv
data/synthetic_publication_source_figure_notes_backfill_summary.json
run_manifest.json
```

## Result

```text
policy label:              synthetic_publication_source_figure_notes_backfill_complete_skip_existing
source figures audited:    9
generated notes:           8
skipped existing notes:    1
missing figures:           0
notes present after:       9
gpu priority:              none
ready for handoff:         true
```

## Interpretation

The current synthetic publication bundle already had its own summary figure
notes, but most referenced source figures did not. This run fixes the
paper-facing source-figure provenance gap using skip-existing behavior and
leaves existing images untouched.

The refreshed archive-health report now counts fewer
`figure_images_missing_figure_notes` issues, but this was not a broad
historical cleanup. It covered only figures referenced by the current synthetic
publication bundle.
