# Experiment 1382: Local 2D State-Consistent Acceptance Status Synthesis

Date: 2026-06-27

## Purpose

Convert the margin-guard result from run `1381` into an explicit acceptance
status table for the recent local 2D state-consistency branch.

This run does not rerun the optimizer, launch broad batches, run GPU work, use
field data, run field FWI, perform 3D/HPC work, or train neural networks.

## Output

```text
outputs/experiments/1382_local_2d_state_consistent_acceptance_status_synthesis
```

Key artifacts:

```text
data/local_2d_state_consistent_acceptance_status_rows.csv
data/local_2d_state_consistent_acceptance_status_by_run.csv
data/local_2d_state_consistent_acceptance_status_summary.json
figures/local_2d_state_consistent_acceptance_status_synthesis.png
docs/LOCAL_2D_STATE_CONSISTENT_ACCEPTANCE_STATUS_SYNTHESIS.md
scripts/run_local_2d_state_consistent_acceptance_status_synthesis.py
scripts/test_local_2d_state_consistent_acceptance_status_synthesis.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source rows:                                  116
source run ids:                               1375, 1376, 1377, 1378, 1379
margin threshold:                             0.0
promoted corrected-state rows:                12
truth-selected observation rows not promoted: 66
held rows with missing margin:                6
uncertain non-positive-margin rows:           0
rejected wrong-geometry rows:                 32
promoted run count:                           4
acceptance policy ready:                      true
broad radius tolerance promoted:              false
broad batch ready:                            false
GPU work ready:                               false
field transfer ready:                         false
field FWI ready:                              false
```

Run-level status:

| Run | Rows | Promote | Observe only | Hold | Reject |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1375 | 12 | 0 | 0 | 6 | 6 |
| 1376 | 18 | 2 | 16 | 0 | 0 |
| 1377 | 34 | 2 | 26 | 0 | 6 |
| 1378 | 22 | 2 | 11 | 0 | 9 |
| 1379 | 30 | 6 | 13 | 0 | 11 |

## Interpretation

The acceptance boundary is now explicit. The promoted evidence is only the
corrected-state mechanism with a positive finite wrong-minus-truth margin.

The 66 truth-selected perturbation rows remain useful observations, but they
are not promoted into a broad neighbor-radius tolerance claim. The six
missing-margin rows remain held rather than accepted. The 32 rows where the
truth geometry was not selected are rejected.

## Decision

Use this status table as the local 2D acceptance rule for the current
state-consistency branch:

```text
promote corrected-state positive-margin rows only
hold missing or non-positive margins
reject wrong-geometry selections
do not promote broad radius tolerance from this branch
```

Do not launch broad local 2D batches, GPU work, field transfer, field FWI, or
3D/HPC work from this evidence.

## Milestone Snapshot

This result-driven local 2D milestone froze:

```text
run_local_2d_state_consistent_acceptance_status_synthesis.py
sha256: 3d3910e8163c686e6d3baf97c76811a21ce57b37555fa3dc6a2185eb2606a50b

test_local_2d_state_consistent_acceptance_status_synthesis.py
sha256: b7f2af78833dd6017ab4f865120c088f1fa282d04f384bd522d1ddbe1376fb9f
```

Subsequent related local 2D state-consistency experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_acceptance_status_synthesis.py
4 passed
```

Figure check:

```text
local_2d_state_consistent_acceptance_status_synthesis.png
2716x846, dynamic range=255
```
