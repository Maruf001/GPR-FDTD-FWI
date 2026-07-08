# 1869 Experiment Archive Post-Status-V6 BEM Recheck Next ID Guard

Date: 2026-07-02

## Purpose

Verify that run `1868` consumed the previously advertised next safe experiment
ID, allocate this guard at `1869`, and advance the next safe output ID to
`1870` without renumbering or repairing existing duplicate numeric IDs.

## Result

```text
previous next safe ID:             1868
consumed numeric ID:               1868
current guard ID:                  1869
source BEM live/missing files:     0 / 2
source BEM ready recheck rows:     0
required guards:                   8 / 8
renumbering performed now:         false
FDTD executed now:                 false
field transfer ready:              false
3D/HPC ready:                      false
gpu priority:                      none
next safe after current guard:     1870
```

## Decision

Use output ID `1870` for the next numbered experiment output. Keep the known
duplicate-ID collision inventory unchanged and do not renumber existing
artifacts in this guard.

## Artifacts

```text
outputs/experiments/1869_experiment_archive_post_status_v6_bem_recheck_next_id_guard
outputs/experiments/1869_experiment_archive_post_status_v6_bem_recheck_next_id_guard/data/experiment_archive_post_status_v6_bem_recheck_next_id_guard_guard_rows.csv
outputs/experiments/1869_experiment_archive_post_status_v6_bem_recheck_next_id_guard/data/experiment_archive_post_status_v6_bem_recheck_next_id_guard_summary.json
outputs/experiments/1869_experiment_archive_post_status_v6_bem_recheck_next_id_guard/figures/experiment_archive_post_status_v6_bem_recheck_next_id_guard.png
```
