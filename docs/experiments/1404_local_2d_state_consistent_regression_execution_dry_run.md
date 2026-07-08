# Local 2D Experiment 1404: State-Consistent Regression Execution Dry Run

Date: 2026-06-28

## Purpose

Resolve the run `1401` regression execution packet against the actual CSV
tables selected by each route.

This run checks operational table readiness only. It does not run new FDTD/FWI
inversions, launch GPU/HPC work, compare against field data, or promote field
transfer.

## Output

```text
outputs/experiments/1404_local_2d_state_consistent_regression_execution_dry_run
```

Key artifacts:

```text
data/local_2d_state_consistent_regression_execution_dry_run_routes.csv
data/local_2d_state_consistent_regression_execution_dry_run_summary.json
figures/local_2d_state_consistent_regression_execution_dry_run.png
docs/LOCAL_2D_STATE_CONSISTENT_REGRESSION_EXECUTION_DRY_RUN.md
scripts/run_local_2d_state_consistent_regression_execution_dry_run.py
scripts/test_local_2d_state_consistent_regression_execution_dry_run.py
```

## Result

```text
source routes:                      6
dry-run routes:                     6
dry-run passes:                     2
dry-run failures:                   4
missing tables:                     0
row-count mismatches:               4
schema failures:                    0
fast-smoke routes:                  2
full-pack gate routes:              2
new-design-required routes:         1
current-evidence-blocked routes:    1
locally executable routes:          2
execution dry run ready:            false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

The two reduced-sentinel routes resolve correctly to an 11-row table. The four
full-pack routes do not: the packet expects 88 rows, but the selected CSV file
contains 116 rows.

| Route | Change type | Expected rows | Observed rows | Dry-run pass |
| ---: | --- | ---: | ---: | --- |
| 1 | consumer_wiring_schema_parsing_plotting | 11 | 11 | true |
| 2 | harmless_row_order_change | 11 | 11 | true |
| 3 | row_key_or_digest_drift | 88 | 116 | false |
| 4 | boundary_objective_margin_or_token_change | 88 | 116 | false |
| 5 | physical_claim_or_broad_radius_tolerance | 88 | 116 | false |
| 6 | gpu_field_transfer_field_fwi_or_3d_hpc | 88 | 116 | false |

## Interpretation

The regression packet was internally consistent at the router/inventory level,
but it is not yet a resolved execution packet. The selected full-pack CSV is the
broader 116-row case table, while the contract says the executable full core
regression pack has 88 rows.

This is a concrete table-materialization problem. It is not evidence for a new
physics claim and it does not justify GPU, field transfer, field FWI, or 3D/HPC
work.

## Decision

Repair the packet before using it as an execution input. The next run should
materialize or select an 88-row core regression table, then rebuild and validate
the packet against that table.

Keep physical-claim promotion, GPU work, field transfer, field FWI, and 3D/HPC
blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_regression_execution_dry_run.py
5 passed
```

Python compile check:

```text
run_local_2d_state_consistent_regression_execution_dry_run.py: pass
tests/test_local_2d_state_consistent_regression_execution_dry_run.py: pass
```

Figure check:

```text
2788x838, dynamic range=255
```
