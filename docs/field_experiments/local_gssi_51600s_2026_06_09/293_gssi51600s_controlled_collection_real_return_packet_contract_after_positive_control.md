# Field Experiment 293: Real Return Packet Contract After Positive Control

Date: 2026-06-29

## Purpose

Convert the guarded post-positive-control real-return gate into a current
file/value/gate packet contract.

The positive-control mechanics are guarded, but the current real archive still
contains zero measured packet items. This run defines the packet that must be
staged before provenance acceptance, real archive acceptance, controlled field
evidence, field FWI, 3D/HPC, or GPU work can proceed.

This run does not stage real DZT files, promote field evidence, run field FWI,
launch 3D/HPC work, or start GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/293_gssi51600s_controlled_collection_real_return_packet_contract_after_positive_control
```

Key artifacts:

```text
data/field_controlled_collection_real_return_packet_contract_after_positive_control_packet_rows.csv
data/field_controlled_collection_real_return_packet_contract_after_positive_control_acceptance_rows.csv
data/field_controlled_collection_real_return_packet_contract_after_positive_control_summary.json
figures/field_controlled_collection_real_return_packet_contract_after_positive_control.png
scripts/script_snapshot_manifest.json
```

## Result

```text
packet contract ready:              true
packet items:                       57
acceptance checks:                  189
measured requirements:              50
measured requirements complete:     0
real DZT files:                     9
controlled profile repeats:         3
time-zero references:               3
amplitude references:               3
metadata values:                    32
checksum rows:                      9
acceptance gates:                   7
real packet files present:          false
real return execution ready:        false
field FWI ready:                    false
3D/HPC ready:                       false
GPU priority:                       none
figure size:                        3491x914
figure dynamic range:               255
```

## Interpretation

The field side now has a current real-return packet contract: 57 packet items,
50 measured requirements, nine real DZT files, 32 metadata values, nine
checksums, seven acceptance gates, and 189 acceptance checks.

The contract is ready, but no real measured packet item is complete in the
current archive.

## Decision

Use run `293` as the current field return target. Keep provenance acceptance,
real archive acceptance, controlled field evidence, field FWI, field 3D/HPC,
and GPU work blocked until the packet is staged and validators pass.
