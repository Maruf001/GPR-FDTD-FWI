# Field Experiment 624: Controlled Collection First-Return Pair Watchlist Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `623` validator with damaged pair-watchlist states and
premature field-promotion states.

This run reads saved artifacts only. It does not create measured files, parse
DZT files, run field FWI, or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/624_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_pair_watchlist_validation_sensitivity
```

## Result

```text
sensitivity scenarios:                 15
expected pass scenarios:               1
expected fail scenarios:               14
observed pass scenarios:               1
observed fail scenarios:               14
unexpected outcomes:                   0
damaged scenarios:                     14
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

## Interpretation

The validator accepts only the exact no-data first-return watchlist state. It
rejects watchlist-readiness damage, pair removal, category damage, false
complete-pair promotion, partial-pair promotion, false DZT or metadata
presence, dirty-tree promotion, field-evidence promotion, field FWI promotion,
field 3D/HPC promotion, GPU-priority promotion, figure damage, and
script-snapshot damage.

## Decision

Use runs `622-624` as the guarded first-return pair watchlist block. Keep
controlled field evidence, field FWI, and field 3D/HPC blocked until measured
pairs arrive and pass preflight.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_pair_watchlist_validation_sensitivity.py
3 passed
```

Figure check:

```text
2610x867, dynamic range=255
```
