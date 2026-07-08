# Local 2D Experiment 1409: State-Consistent Repaired Execution Claim Boundary Refresh

Date: 2026-06-28

## Purpose

Convert the repaired regression execution packet from runs `1405`-`1408` into a
compact claim-boundary checkpoint.

This run does not run new FDTD/FWI inversions, launch GPU/HPC work, compare
against field data, or promote physical claims from a table-execution repair.

## Output

```text
outputs/experiments/1409_local_2d_state_consistent_repaired_execution_claim_boundary_refresh
```

Key artifacts:

```text
data/local_2d_state_consistent_repaired_execution_claim_boundary_rows.csv
data/local_2d_state_consistent_repaired_execution_claim_boundary_summary.json
figures/local_2d_state_consistent_repaired_execution_claim_boundary_refresh.png
docs/LOCAL_2D_STATE_CONSISTENT_REPAIRED_EXECUTION_CLAIM_BOUNDARY_REFRESH.md
scripts/run_local_2d_state_consistent_repaired_execution_claim_boundary_refresh.py
scripts/test_local_2d_state_consistent_repaired_execution_claim_boundary_refresh.py
```

## Result

```text
claims evaluated:                  5
ready claims:                      1
blocked claims:                    4
recommended guards:                1
recommended guard:                 repaired_regression_execution_packet_guard
original packet row mismatches:    4
materialized core rows:            88
claim-boundary refresh ready:      true
full pack remains authoritative:   true
sentinel replaces full pack:       false
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The only ready claim is the repaired regression execution-packet guard. The
original packet remains blocked because it pointed full-pack routes at a
116-row table while the contract required 88 rows.

## Interpretation

Runs `1405`-`1408` repair and guard a local 2D table-execution problem. They do
not create a new physical result, broaden detector claims, replace the full
pack with the sentinel, or justify GPU/field/3D escalation.

## Decision

Use the repaired 88-row full-core packet with the 11-row sentinel fast-smoke
layer as the current local 2D regression execution guard.

Keep the full pack authoritative. Keep physical-claim promotion, GPU work,
field transfer, field FWI, and 3D/HPC blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_repaired_execution_claim_boundary_refresh.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_repaired_execution_claim_boundary_refresh.py: pass
tests/test_local_2d_state_consistent_repaired_execution_claim_boundary_refresh.py: pass
```

Figure check:

```text
2645x838, dynamic range=255
```
