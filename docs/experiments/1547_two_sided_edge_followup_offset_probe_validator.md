# Experiment 1547: Two-Sided Edge Follow-Up Offset Probe Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1546` executed follow-up offset probe from artifacts.

## Output

```text
outputs/experiments/1547_local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_probe_validator
```

## Result

```text
validation checks:                   7
passed checks:                       7
failed checks:                       0
validation ready:                    true
source planned cases:                20
source grid models:                  20
source objective rows:               120
source candidate rows:               480
source any-failure models:           20
source all-objective-failure models: 0
below-45 all far cases suppressed:   false
above-45 all far cases suppressed:   false
new physical claim ready:            false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

The validator checks source identity, executed row counts, offset and case
matrix stability, failure taxonomy, edge summary rows, blocked downstream
states, figure validation, and script snapshots.

## Interpretation

The executed follow-up offset probe is internally consistent. It found partial
objective failures in all 20 planned cases and no all-objective failures, so
the wider suppression-window claim remains unsupported.

## Decision

Use run `1547` as the validator for the run `1546` executed follow-up offset
probe. Sensitivity hardening remains required before closing the block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_probe_validator.py
3 passed
```

Figure check:

```text
3365x895, dynamic range=255
```
