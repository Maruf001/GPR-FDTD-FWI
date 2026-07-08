# Local 2D Experiment 1405: State-Consistent Regression Packet Core-Table Repair

Date: 2026-06-28

## Purpose

Repair the run `1404` dry-run failure by materializing the 88-row core
regression table and rewriting the full-pack routes to use it.

This run does not run new FDTD/FWI inversions, launch GPU/HPC work, compare
against field data, or promote field transfer.

## Output

```text
outputs/experiments/1405_local_2d_state_consistent_regression_packet_core_table_repair
```

Key artifacts:

```text
data/local_2d_state_consistent_materialized_core_regression_rows.csv
data/local_2d_state_consistent_regression_packet_core_table_repair_routes.csv
data/local_2d_state_consistent_regression_packet_core_table_repair_tables.csv
data/local_2d_state_consistent_regression_packet_core_table_repair_summary.json
figures/local_2d_state_consistent_regression_packet_core_table_repair.png
docs/LOCAL_2D_STATE_CONSISTENT_REGRESSION_PACKET_CORE_TABLE_REPAIR.md
scripts/run_local_2d_state_consistent_regression_packet_core_table_repair.py
scripts/test_local_2d_state_consistent_regression_packet_core_table_repair.py
```

## Result

```text
source case rows:                    116
materialized core rows:              88
expanded observation-only rows cut:  28
source dry-run row mismatches:       4
routes:                              6
reduced routes unchanged:            2
full routes repaired:                4
materialized table matches contract: true
repaired packet ready for dry run:   true
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

The repair keeps the two 11-row reduced-sentinel routes unchanged. The four
full-pack routes now point to:

```text
outputs/experiments/1405_local_2d_state_consistent_regression_packet_core_table_repair/data/local_2d_state_consistent_materialized_core_regression_rows.csv
```

## Interpretation

Run `1404` showed that the old packet selected a 116-row case table where the
contract required an 88-row full core regression table. This run fixes the table
selection without changing the scientific claim boundary.

The 28 excluded rows are expanded observation-only rows. The repaired packet is
ready for a repeat execution dry run, but it does not promote physical claims,
GPU work, field transfer, field FWI, or 3D/HPC.

## Decision

Use this repaired packet as the candidate input for a repeat execution dry run.

Keep the full pack authoritative, keep the reduced sentinel fast-smoke-only, and
keep physical-claim promotion, GPU work, field transfer, field FWI, and 3D/HPC
blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_regression_packet_core_table_repair.py
5 passed
```

Python compile check:

```text
run_local_2d_state_consistent_regression_packet_core_table_repair.py: pass
tests/test_local_2d_state_consistent_regression_packet_core_table_repair.py: pass
```

Figure check:

```text
2932x838, dynamic range=255
```
