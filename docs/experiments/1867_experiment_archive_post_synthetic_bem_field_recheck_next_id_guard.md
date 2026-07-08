# 1867 Experiment Archive Post-Synthetic-BEM-Field-Recheck Next ID Guard

Date: 2026-07-02

## Purpose

Verify that run `1866` consumed the previously advertised next safe experiment
ID, allocate this guard at `1867`, and advance the next safe output ID to
`1868` without renumbering or repairing existing duplicate numeric IDs.

## Result

```text
previous next safe ID:             1866
consumed numeric ID:               1866
current guard ID:                  1867
source synthetic candidate count:  10
source top question:               synthetic_publication_bundle_current
source GPU candidates:             0 immediate / 0 conditional
required guards:                   8 / 8
renumbering performed now:         false
FDTD executed now:                 false
field transfer ready:              false
3D/HPC ready:                      false
gpu priority:                      none
next safe after current guard:     1868
```

## Decision

Use output ID `1868` for the next numbered experiment output. Keep the known
duplicate-ID collision inventory unchanged and do not renumber existing
artifacts in this guard.

## Artifacts

```text
outputs/experiments/1867_experiment_archive_post_synthetic_bem_field_recheck_next_id_guard
outputs/experiments/1867_experiment_archive_post_synthetic_bem_field_recheck_next_id_guard/data/experiment_archive_post_synthetic_bem_field_recheck_next_id_guard_guard_rows.csv
outputs/experiments/1867_experiment_archive_post_synthetic_bem_field_recheck_next_id_guard/data/experiment_archive_post_synthetic_bem_field_recheck_next_id_guard_summary.json
outputs/experiments/1867_experiment_archive_post_synthetic_bem_field_recheck_next_id_guard/figures/experiment_archive_post_synthetic_bem_field_recheck_next_id_guard.png
```
