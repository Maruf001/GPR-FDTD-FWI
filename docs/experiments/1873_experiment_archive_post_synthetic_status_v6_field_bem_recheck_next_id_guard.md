# 1873 Experiment Archive Post-Synthetic-Status-V6-Field BEM Recheck Next ID Guard

Date: 2026-07-02

## Purpose

Verify that run `1872` consumed the previously advertised next safe experiment
ID, allocate this guard at `1873`, and advance the next safe output ID to
`1874` without renumbering or repairing existing duplicate numeric IDs.

## Result

```text
previous next safe ID:             1872
consumed numeric ID:               1872
current guard ID:                  1873
source BEM live/missing files:     0 / 2
source BEM recheck rows ready:     0
required guards:                   8 / 8
renumbering performed now:         false
FDTD executed now:                 false
field transfer ready:              false
3D/HPC ready:                      false
gpu priority:                      none
next safe after current guard:     1874
```

## Decision

Use output ID `1874` for the next numbered experiment output. Keep the known
duplicate-ID collision inventory unchanged and do not renumber existing
artifacts in this guard.

## Artifacts

```text
outputs/experiments/1873_experiment_archive_post_synthetic_status_v6_field_bem_recheck_next_id_guard
outputs/experiments/1873_experiment_archive_post_synthetic_status_v6_field_bem_recheck_next_id_guard/data/experiment_archive_post_synthetic_status_v6_field_bem_recheck_next_id_guard_guard_rows.csv
outputs/experiments/1873_experiment_archive_post_synthetic_status_v6_field_bem_recheck_next_id_guard/data/experiment_archive_post_synthetic_status_v6_field_bem_recheck_next_id_guard_summary.json
outputs/experiments/1873_experiment_archive_post_synthetic_status_v6_field_bem_recheck_next_id_guard/figures/experiment_archive_post_synthetic_status_v6_field_bem_recheck_next_id_guard.png
```
