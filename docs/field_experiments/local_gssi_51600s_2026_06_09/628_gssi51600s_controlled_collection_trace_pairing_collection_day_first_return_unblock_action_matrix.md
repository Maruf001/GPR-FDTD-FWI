# Field Experiment 628: First-Return Unblock Action Matrix

Date: 2026-07-01

## Purpose

Convert the guarded first-return acceptance gate `625-627` into a path-level
operator action matrix for the nine blocked measured DZT/paired metadata
returns.

This run reads saved watchlist and acceptance-gate artifacts. It does not
create field evidence, run field FWI, or launch 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/628_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_unblock_action_matrix
```

## Result

```text
source acceptance gate ready:        true
source validation ready:             true
source sensitivity ready:            true
action pairs:                        9
open action pairs:                   9
ready-for-recheck pairs:             0
missing DZT files:                   9
missing metadata files:              9
missing artifacts:                   18
parent directories ready:            9
controlled-profile pairs:            3
time-zero pairs:                     3
amplitude-reference pairs:           3
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
```

## Decision

Use this as an operator checklist only. Keep controlled field evidence, field
FWI, and field 3D/HPC blocked until the DZT/metadata files arrive and the
acceptance gate passes.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_unblock_action_matrix.py
3 passed
```

Figure check:

```text
2825x857, dynamic range=255
```
