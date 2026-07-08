# Local 2D Experiment 1392: Reduced Sentinel Candidate

Date: 2026-06-27

## Purpose

Remove the individually redundant rows identified by run `1391` and validate
whether the reduced sentinel candidate still covers all required tokens while
preserving the margin-risk add-ons.

This is a CPU-only table audit. It does not run FDTD, FWI, GPU work, field
transfer, field FWI, or 3D/HPC.

## Output

```text
outputs/experiments/1392_local_2d_state_consistent_reduced_sentinel_candidate
```

Key artifacts:

```text
data/local_2d_state_consistent_reduced_sentinel_rows.csv
data/local_2d_state_consistent_reduced_sentinel_removed_rows.csv
data/local_2d_state_consistent_reduced_sentinel_role_summary.csv
data/local_2d_state_consistent_reduced_sentinel_candidate_summary.json
figures/local_2d_state_consistent_reduced_sentinel_candidate.png
docs/LOCAL_2D_STATE_CONSISTENT_REDUCED_SENTINEL_CANDIDATE.md
scripts/run_local_2d_state_consistent_reduced_sentinel_candidate.py
scripts/test_local_2d_state_consistent_reduced_sentinel_candidate.py
```

## Result

```text
source sentinel rows:              13
removed redundant rows:            2
reduced sentinel rows:             11
required coverage tokens:          32
uncovered coverage tokens:         0
margin-risk add-ons preserved:     2
category coverage rows preserved:  9
reduced candidate ready:           true
sentinel replaces full pack:       false
full pack remains authoritative:   true
GPU ready:                         false
field FWI ready:                   false
```

Removed rows:

| Sentinel | Run | Role | Perturbation | Reason |
| ---: | ---: | --- | --- | --- |
| 2 | 1375 | core_negative_rejection | ff_max_geometry_instability_nominal | individually redundant under run `1391` leave-one-out |
| 5 | 1378 | core_negative_rejection | far_neighbor_radius_minus_1p75mm | individually redundant under run `1391` leave-one-out |

## Interpretation

Removing both individually redundant category rows still leaves complete
coverage of all 32 required tokens and preserves both margin-risk add-ons. The
reduced candidate has 11 rows: nine category-coverage rows and two margin-risk
rows.

This is a smaller optional fast-smoke candidate. It still does not replace the
full 88-row core regression pack.

## Decision

Use this as a reduced optional fast-smoke candidate, pending consumer
validation. The full 88-row core pack remains authoritative, and broad radius
tolerance, GPU work, field transfer, field FWI, and 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_reduced_sentinel_candidate.py
5 passed
```

Figure validation:

```text
local_2d_state_consistent_reduced_sentinel_candidate.png
2248x847, dynamic range=255
```
