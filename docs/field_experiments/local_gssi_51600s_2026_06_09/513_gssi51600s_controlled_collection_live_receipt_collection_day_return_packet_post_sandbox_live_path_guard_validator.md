# Field Experiment 513: Return-Packet Post-Sandbox Live-Path Guard Validator

Date: 2026-06-30

## Purpose

Validate run `512`, the guard that confirms the output-local sandbox completion
did not populate the live external-return paths.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/513_gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard_validator_summary.json
data/figure_validation.csv
figures/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard_validator.png
scripts/
```

## Result

```text
validation checks:                    5
failed checks:                        0
guard rows:                           33
file families:                        5
live paths under return root:         33
live files present:                   0
sandbox files present:                33
sandbox/live path overlaps:           0
sandbox files under live return root: 0
synthetic-only files:                 33
measured field evidence files:        0
live receipt ready:                   false
controlled field evidence ready:      false
field FWI ready:                      false
field 3D/HPC ready:                   false
```

All five validation checks pass:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source return-packet live-path guard ready | pass |
| 2 | guard row shape | pass |
| 3 | live return paths remain empty | pass |
| 4 | evidence and downstream blocked | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

Run `513` confirms that run `512` is a valid guard artifact: the expected live
return paths are locked and empty, the sandbox files remain separated from
those paths, and no downstream field workflow is ready.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_post_sandbox_live_path_guard_validator.py

6 passed
```

Figure check:

```text
2321x836, dynamic range=255
```
