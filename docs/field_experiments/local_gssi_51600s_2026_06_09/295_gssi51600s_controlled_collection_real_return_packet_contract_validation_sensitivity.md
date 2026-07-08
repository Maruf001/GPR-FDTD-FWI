# Field Experiment 295: Real Return Packet Contract Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `294` validator with controlled damaged variants.

The exact run `293` packet contract should pass. Damaged variants should fail
when they change packet counts, remove rows, drift requirement types, change
stage assignment, falsely complete measured requirements, falsely promote field
states, lose the synthetic-only boundary, promote GPU priority, damage figure
validation, or remove script snapshots.

This run does not stage real DZT files, promote field evidence, run field FWI,
launch 3D/HPC work, or start GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/295_gssi51600s_controlled_collection_real_return_packet_contract_validation_sensitivity
```

Key artifacts:

```text
data/field_controlled_collection_real_return_packet_contract_validation_sensitivity_scenarios.csv
data/field_controlled_collection_real_return_packet_contract_validation_sensitivity_summary.json
figures/field_controlled_collection_real_return_packet_contract_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                    14
expected pass:                1
observed pass:                1
expected failures:            13
observed failures:            13
unexpected outcomes:          0
sensitivity ready:            true
accepts exact run 293:        true
rejects damaged variants:     true
real return execution ready:  false
field FWI ready:              false
3D/HPC ready:                 false
GPU priority:                 none
figure size:                  3329x877
figure dynamic range:         255
```

## Interpretation

The validator accepts the exact run `293` field packet contract and rejects all
controlled corruptions. This guards the packet contract without promoting the
real field archive.

## Decision

Use runs `293-295` as the guarded field real-return packet contract. Keep
provenance acceptance, real archive acceptance, controlled field evidence,
field FWI, field 3D/HPC, and GPU work blocked until an actual measured packet
is staged and validators pass.
