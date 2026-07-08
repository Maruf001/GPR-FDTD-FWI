# 1863 Experiment Archive Post-Synthetic-Field-Recheck Next ID Guard

Date: 2026-07-02

## Purpose

Verify that experiment `1862` consumed the previously advertised next safe ID
and advance the archive guard after allocating this guard artifact at `1863`.
No renumbering, deletion, duplicate cleanup, GPU work, FDTD execution, or
field transfer is performed.

## Result

```text
previous next safe ID after 1861:       1862
consumed numeric ID:                    1862
current guard numeric ID:               1863
consumed output/doc entries:            1 / 1
current output/doc entries:             1 / 1
next safe output ID after current:       1864
source candidate questions:             10
source top question:                    synthetic_publication_bundle_current
source immediate GPU candidates:        0
source conditional GPU candidates:      0
renumbering performed now:              False
FDTD executed now:                      False
field transfer ready:                   False
ready for 3D/HPC:                       False
```

## Decision

Use `1864` as the next safe numeric output ID for subsequent experiment
outputs. Existing duplicate numeric IDs remain recorded but unrepaired in this
guard.

## Artifacts

```text
outputs/experiments/1863_experiment_archive_post_synthetic_field_recheck_next_id_guard
outputs/experiments/1863_experiment_archive_post_synthetic_field_recheck_next_id_guard/data/experiment_archive_post_synthetic_field_recheck_next_id_guard_guard_rows.csv
outputs/experiments/1863_experiment_archive_post_synthetic_field_recheck_next_id_guard/data/experiment_archive_post_synthetic_field_recheck_next_id_guard_summary.json
outputs/experiments/1863_experiment_archive_post_synthetic_field_recheck_next_id_guard/figures/experiment_archive_post_synthetic_field_recheck_next_id_guard.png
```
