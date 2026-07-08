# Field Experiment 623: Controlled Collection First-Return Pair Watchlist Validator

Date: 2026-07-01

## Purpose

Validate the saved run `622` first-return pair watchlist from artifacts.

This validator does not create measured files, parse DZT files, run field FWI,
or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/623_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_pair_watchlist_validator
```

## Result

```text
validation checks:                    6
passed checks:                        6
failed checks:                        0
DZT/metadata pairs:                   9
complete pairs:                       0
partial pairs:                        0
DZT files present:                    0
metadata files present:               0
controlled field evidence ready:      false
field FWI ready:                      false
field 3D/HPC ready:                   false
gpu priority:                         none
```

## Interpretation

The watchlist validates as nine absent measured DZT/metadata pairs. It remains
an intake checklist, not measured field evidence.

## Decision

Keep controlled field evidence, field FWI, and field 3D/HPC blocked until
measured pairs arrive and pass preflight.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_pair_watchlist_validator.py
3 passed
```

Figure check:

```text
2322x835, dynamic range=255
```
