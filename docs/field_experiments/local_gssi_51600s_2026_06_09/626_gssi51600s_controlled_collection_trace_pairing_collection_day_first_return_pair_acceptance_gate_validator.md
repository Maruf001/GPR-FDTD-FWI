# Field Experiment 626: Controlled Collection First-Return Pair Acceptance Gate Validator

Date: 2026-07-01

## Purpose

Validate the saved run `625` first-return pair acceptance gate from artifacts.

This validator does not create measured files, run field preprocessing, run
field FWI, launch 3D/HPC work, or use GPU kernels.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/626_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_pair_acceptance_gate_validator
```

## Result

```text
validation checks:                 6
passed checks:                     6
failed checks:                     0
acceptance pairs:                  9
accepted pairs:                    0
blocked pairs:                     9
missing DZT files:                 9
missing metadata files:            9
required acceptance checks:        108
passed acceptance checks:          0
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

## Interpretation

The saved first-return pair acceptance gate validates as nine blocked
DZT/metadata pairs with zero accepted measured pairs.

## Decision

Keep controlled field evidence, field FWI, and field 3D/HPC blocked until
measured pairs pass acceptance.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_pair_acceptance_gate_validator.py
3 passed
```

Figure check:

```text
2465x862, dynamic range=255
```
