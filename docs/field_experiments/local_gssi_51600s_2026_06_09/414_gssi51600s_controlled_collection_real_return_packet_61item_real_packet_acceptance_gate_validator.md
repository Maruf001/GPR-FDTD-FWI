# Field Experiment 414: Real Packet Acceptance-Gate Validator

Date: 2026-06-29

## Purpose

Validate the saved run `413` field real-packet acceptance gate from artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/414_gssi51600s_controlled_collection_real_return_packet_61item_real_packet_acceptance_gate_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_real_packet_acceptance_gate_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_real_packet_acceptance_gate_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_real_packet_acceptance_gate_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           4
validation checks passed:                    4
blocking failures:                           0
acceptance-gate validation ready:            true
acceptance rows:                             49
direct real-input rows:                      33
generated follow-up rows:                    16
measured-evidence rows ready:                0
real packet files present:                   false
real packet accepted:                        false
controlled field evidence ready:             false
field FWI ready:                             false
field 3D/HPC ready:                          false
gpu priority:                                none
```

## Interpretation

The validator confirms the gate shape, zero-accepted state, downstream blocks,
figure, and script snapshots.

## Decision

Use this validator as the artifact guard for run `413`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_real_packet_acceptance_gate_validator.py
4 passed
```

Figure check:

```text
2537x840, dynamic range=255
```
