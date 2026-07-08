# Field Experiment 627: Controlled Collection First-Return Pair Acceptance Gate Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `626` validator with damaged acceptance-gate states and
premature promotion states.

This run reads saved artifacts only. It does not create measured files, run
field preprocessing, run field FWI, launch 3D/HPC work, or use GPU kernels.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/627_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_pair_acceptance_gate_validation_sensitivity
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

The validator accepts only the exact nine-pair missing-file acceptance-gate
state. It rejects false pair acceptance, false DZT or metadata presence,
acceptance-check count damage, false passed-check promotion, parent-directory
damage, controlled-field-evidence promotion, field FWI promotion, field 3D/HPC
promotion, GPU-priority promotion, figure damage, and script-snapshot damage.

## Decision

Use runs `625-627` as the guarded first-return pair acceptance-gate block.
Keep controlled field evidence, field FWI, and field 3D/HPC blocked until all
nine measured pairs pass acceptance.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_pair_acceptance_gate_validation_sensitivity.py
3 passed
```

Figure check:

```text
2645x872, dynamic range=255
```
