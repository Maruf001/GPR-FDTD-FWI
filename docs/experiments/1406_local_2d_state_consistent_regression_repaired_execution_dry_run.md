# Local 2D Experiment 1406: State-Consistent Repaired Regression Execution Dry Run

Date: 2026-06-28

## Purpose

Repeat the run `1404` execution dry run against the repaired packet from run
`1405`.

This run checks that the materialized 88-row core table actually resolves from
the repaired route packet. It does not run new FDTD/FWI inversions, launch
GPU/HPC work, compare against field data, or promote field transfer.

## Output

```text
outputs/experiments/1406_local_2d_state_consistent_regression_repaired_execution_dry_run
```

Key artifacts:

```text
data/local_2d_state_consistent_regression_repaired_execution_dry_run_routes.csv
data/local_2d_state_consistent_regression_repaired_execution_dry_run_summary.json
figures/local_2d_state_consistent_regression_repaired_execution_dry_run.png
docs/LOCAL_2D_STATE_CONSISTENT_REGRESSION_REPAIRED_EXECUTION_DRY_RUN.md
scripts/run_local_2d_state_consistent_regression_repaired_execution_dry_run.py
scripts/test_local_2d_state_consistent_regression_repaired_execution_dry_run.py
```

## Result

```text
source materialized core rows:       88
dry-run routes:                     6
dry-run passes:                     6
dry-run failures:                   0
missing tables:                     0
row-count mismatches:               0
schema failures:                    0
locally executable routes:          4
blocked-by-design routes:           2
repaired execution dry run ready:   true
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

| Route | Change type | Expected rows | Observed rows | Mode |
| ---: | --- | ---: | ---: | --- |
| 1 | consumer_wiring_schema_parsing_plotting | 11 | 11 | ready_fast_smoke |
| 2 | harmless_row_order_change | 11 | 11 | ready_fast_smoke |
| 3 | row_key_or_digest_drift | 88 | 88 | ready_full_pack_gate |
| 4 | boundary_objective_margin_or_token_change | 88 | 88 | ready_full_pack_gate |
| 5 | physical_claim_or_broad_radius_tolerance | 88 | 88 | blocked_requires_new_design |
| 6 | gpu_field_transfer_field_fwi_or_3d_hpc | 88 | 88 | blocked_current_2d_evidence |

## Interpretation

The repaired packet now resolves cleanly. The table mismatch found in run
`1404` is closed: full-pack routes now point to the materialized 88-row core
regression table from run `1405`.

Four routes are locally executable table checks. Two routes are still blocked by
design: one needs a new physical design before any broad-radius or physical
claim can be promoted, and one remains blocked for GPU, field transfer, field
FWI, and 3D/HPC.

## Decision

Use runs `1405` and `1406` as the repaired local 2D regression execution-packet
guard.

Keep the full pack authoritative, keep the reduced sentinel fast-smoke-only, and
keep physical-claim promotion, GPU work, field transfer, field FWI, and 3D/HPC
blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_regression_repaired_execution_dry_run.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_regression_repaired_execution_dry_run.py: pass
tests/test_local_2d_state_consistent_regression_repaired_execution_dry_run.py: pass
```

Figure check:

```text
2752x838, dynamic range=255
```
