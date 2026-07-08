# 1875 Experiment Archive Post-Synthetic-Status-V6-Field-BEM-Guard Synthetic Next ID Guard

Date: 2026-07-02

## Purpose

Verify that run `1874` consumed the previously advertised next safe experiment
ID, allocate this guard at `1875`, and advance the next safe output ID to
`1876` without renumbering or repairing existing duplicate numeric IDs.

## Result

```text
previous next safe ID:             1874
consumed numeric ID:               1874
current guard ID:                  1875
source synthetic candidate count:  10
source top question:               synthetic_publication_bundle_current
source GPU candidates:             0 immediate / 0 conditional
required guards:                   8 / 8
renumbering performed now:         false
FDTD executed now:                 false
field transfer ready:              false
3D/HPC ready:                      false
gpu priority:                      none
next safe after current guard:     1876
```

## Decision

Use output ID `1876` for the next numbered experiment output. Keep the known
duplicate-ID collision inventory unchanged and do not renumber existing
artifacts in this guard.

## Artifacts

```text
outputs/experiments/1875_experiment_archive_post_synthetic_status_v6_field_bem_guard_synthetic_next_id_guard
outputs/experiments/1875_experiment_archive_post_synthetic_status_v6_field_bem_guard_synthetic_next_id_guard/data/experiment_archive_post_synthetic_status_v6_field_bem_guard_synthetic_next_id_guard_guard_rows.csv
outputs/experiments/1875_experiment_archive_post_synthetic_status_v6_field_bem_guard_synthetic_next_id_guard/data/experiment_archive_post_synthetic_status_v6_field_bem_guard_synthetic_next_id_guard_summary.json
outputs/experiments/1875_experiment_archive_post_synthetic_status_v6_field_bem_guard_synthetic_next_id_guard/figures/experiment_archive_post_synthetic_status_v6_field_bem_guard_synthetic_next_id_guard.png
```
