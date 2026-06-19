# Figure Notes

## `synthetic_2d_archive_corpus_card.png`

This is a CPU-only methods card for the existing synthetic 2D
experiment archive. It reads the current archive-health report,
publication bundle, next-question matrix, and source-figure notes
audit; it does not run FDTD, FWI, or GPU kernels.

Policy label: `synthetic_2d_archive_corpus_card_current_ready_legacy_hygiene_caveats`.
Archive runs: `1325`.
Physics/diagnostic runs: `802`.
Current publication figures: `9`.
Current source notes: `9`.
Legacy issue count: `130`.
GPU priority: `none`.

Outputs:

- Range table: `synthetic_2d_archive_corpus_ranges.csv`.
- Summary: `synthetic_2d_archive_corpus_card_summary.json`.
- Figure validation: `figure_validation.csv`.

Scope boundary:

The card supports methods and corpus description. Legacy archive
hygiene caveats should be reported as historical caveats, not as a
reason to regenerate old runs or launch broad GPU experiments.

