# Local 2D Experiment 1397: Reduced Sentinel Provenance Lock Sensitivity

Date: 2026-06-27

## Purpose

Stress-test the row-key provenance lock from run `1396` with controlled table
mutations.

Run `1396` locked the 11-row reduced sentinel to the 88-row full core pack by
stable row-key digests. This run checks that the lock is stable to harmless row
reordering and sensitive to real drift: duplicate keys, key-field mutation,
reintroducing a removed row, and row deletion.

This is a CPU-only table provenance audit. It does not run FDTD, FWI, GPU work,
field transfer, field FWI, or 3D/HPC.

## Output

```text
outputs/experiments/1397_local_2d_state_consistent_reduced_sentinel_provenance_lock_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_reduced_sentinel_lock_sensitivity_rows.csv
data/local_2d_state_consistent_reduced_sentinel_lock_sensitivity_summary.json
figures/local_2d_state_consistent_reduced_sentinel_provenance_lock_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_REDUCED_SENTINEL_PROVENANCE_LOCK_SENSITIVITY.md
scripts/run_local_2d_state_consistent_reduced_sentinel_provenance_lock_sensitivity.py
scripts/test_local_2d_state_consistent_reduced_sentinel_provenance_lock_sensitivity.py
```

## Result

```text
scenarios:                         6
expected passes:                   2
observed passes:                   2
expected failures:                 4
observed failures:                 4
unexpected outcomes:               0
row-order digest stable:           true
mutation failures caught:          4
mutation digest changes:           4
lock sensitivity ready:            true
reduced sentinel fast smoke ready: true
full pack remains authoritative:   true
GPU ready:                         false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

| Scenario | Expected pass | Observed pass | Reduced rows | Unique keys | Reduced digest matches baseline | Blocking failures |
| --- | --- | --- | ---: | ---: | --- | ---: |
| exact_reduced_lock | true | true | 11 | 11 | true | 0 |
| reversed_reduced_order | true | true | 11 | 11 | true | 0 |
| duplicate_first_drop_last | false | false | 11 | 10 | false | 2 |
| mutate_first_key_field | false | false | 11 | 11 | false | 1 |
| reintroduce_removed_row | false | false | 11 | 11 | false | 2 |
| drop_last_row | false | false | 10 | 10 | false | 3 |

## Interpretation

The provenance lock behaves correctly. It is stable to row ordering because row
keys are sorted before digesting. It catches duplicate keys, changed key
fields, reintroduced removed rows, and dropped rows.

## Decision

Use the reduced sentinel provenance lock for consumer-side drift detection.
Keep the 88-row full core pack authoritative for boundary decisions. Do not
promote GPU work, field transfer, field FWI, or 3D/HPC from this fast-smoke
lock.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_reduced_sentinel_provenance_lock_sensitivity.py
4 passed
```

Figure validation:

```text
local_2d_state_consistent_reduced_sentinel_provenance_lock_sensitivity.png
2897x851, dynamic range=255
```
