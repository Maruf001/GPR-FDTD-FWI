# Local 2D Experiment 1396: Reduced Sentinel Provenance Lock

Date: 2026-06-27

## Purpose

Record stable row-key digests for the accepted local 2D state-consistency fast
smoke suite.

Runs `1392` through `1395` reduced the optional sentinel suite to 11 rows and
defined its safe-use boundary. This run makes that boundary easier to enforce
by locking the row-key digests for the 88-row full core regression pack, the
11-row reduced sentinel, and the two removed redundant rows.

This is a CPU-only table provenance audit. It does not run FDTD, FWI, GPU work,
field transfer, field FWI, or 3D/HPC.

## Output

```text
outputs/experiments/1396_local_2d_state_consistent_reduced_sentinel_provenance_lock
```

Key artifacts:

```text
data/local_2d_state_consistent_reduced_sentinel_provenance_lock_rows.csv
data/local_2d_state_consistent_reduced_sentinel_provenance_lock_checks.csv
data/local_2d_state_consistent_reduced_sentinel_locked_keys.csv
data/local_2d_state_consistent_reduced_sentinel_provenance_lock_summary.json
figures/local_2d_state_consistent_reduced_sentinel_provenance_lock.png
docs/LOCAL_2D_STATE_CONSISTENT_REDUCED_SENTINEL_PROVENANCE_LOCK.md
scripts/run_local_2d_state_consistent_reduced_sentinel_provenance_lock.py
scripts/test_local_2d_state_consistent_reduced_sentinel_provenance_lock.py
```

## Result

```text
row key fields:                     run_id;perturbation_label;objective_label;regression_role
full core pack rows:                88
full core pack digest:              04dd3b7066163d5c064883c5c830233cd2fbe9962de2faccd03105066f70e054
reduced sentinel rows:              11
reduced sentinel digest:            fa907308dbcccd6c4d775d7b1783c6cd47c015336512f6a9ccb282a9a027db0a
removed redundant rows:             2
removed redundant digest:           f26d5bb431cb93a9f539fe53a683c5e8bc78629251ed6caa4df98eed3f1fc30c
validation checks:                  8
validation passes:                  8
blocking failures:                  0
provenance lock ready:              true
reduced sentinel fast smoke ready:  true
full pack remains authoritative:    true
sentinel replaces full pack:        false
broad radius tolerance promoted:    false
GPU ready:                          false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

Lock items:

| Item | Rows | Unique keys | Digest |
| --- | ---: | ---: | --- |
| full_core_pack | 88 | 88 | `04dd3b7066163d5c064883c5c830233cd2fbe9962de2faccd03105066f70e054` |
| reduced_sentinel | 11 | 11 | `fa907308dbcccd6c4d775d7b1783c6cd47c015336512f6a9ccb282a9a027db0a` |
| removed_redundant_rows | 2 | 2 | `f26d5bb431cb93a9f539fe53a683c5e8bc78629251ed6caa4df98eed3f1fc30c` |

## Interpretation

The adopted 11-row reduced sentinel is locked to the current 88-row full core
pack by stable row-key digests. It remains valid as optional fast smoke only.
The full 88-row pack remains authoritative for boundary, objective, margin,
token-definition, GPU, field-transfer, field-FWI, and 3D/HPC decisions.

## Decision

Use this lock file for consumer-side drift detection. Do not promote broad
radius tolerance, GPU work, field transfer, field FWI, or 3D/HPC from the
reduced sentinel.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_reduced_sentinel_provenance_lock.py
4 passed
```

Figure validation:

```text
local_2d_state_consistent_reduced_sentinel_provenance_lock.png
2896x851, dynamic range=255
```
