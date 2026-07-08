# Field Experiment 294: Real Return Packet Contract Validator

Date: 2026-06-29

## Purpose

Validate the saved run `293` field return packet contract from artifacts.

This run checks packet counts, requirement-type counts, stage split, current
empty archive state, blocked field states, figure validation, and script
snapshots.

This run does not stage real DZT files, promote field evidence, run field FWI,
launch 3D/HPC work, or start GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/294_gssi51600s_controlled_collection_real_return_packet_contract_validator
```

Key artifacts:

```text
data/field_controlled_collection_real_return_packet_contract_validator_checks.csv
data/field_controlled_collection_real_return_packet_contract_validator_summary.json
figures/field_controlled_collection_real_return_packet_contract_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:             7
passed checks:                 7
failed checks:                 0
validation ready:              true
packet items:                  57
acceptance checks:             189
measured requirements:         50
real DZT files:                9
metadata values:               32
checksum rows:                 9
acceptance gates:              7
real return execution ready:   false
field FWI ready:               false
3D/HPC ready:                  false
GPU priority:                  none
figure size:                   3365x893
figure dynamic range:          255
```

## Interpretation

The run `293` field packet contract validates from saved artifacts. Counts,
stages, current empty archive state, blocked field states, figure output, and
script snapshots are stable.

## Decision

Use run `294` as the validator for the field return packet contract.
Sensitivity hardening remains required before treating the packet contract as
guarded.
