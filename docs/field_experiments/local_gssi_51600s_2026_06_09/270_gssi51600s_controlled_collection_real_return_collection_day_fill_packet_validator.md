# Field Experiment 270: Controlled Collection Fill Packet Validator

Date: 2026-06-28

## Purpose

Validate the saved run `269` collection-day fill packet from a consumer
perspective.

This run uses saved artifacts only. It does not ingest real field data, run
field FWI, launch 3D/HPC work, or use GPU compute.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/270_gssi51600s_controlled_collection_real_return_collection_day_fill_packet_validator
```

Key artifacts:

```text
data/field_controlled_collection_real_return_collection_day_fill_packet_validator_checks.csv
data/field_controlled_collection_real_return_collection_day_fill_packet_validator_summary.json
data/figure_validation.csv
figures/field_controlled_collection_real_return_collection_day_fill_packet_validator.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_COLLECTION_DAY_FILL_PACKET_VALIDATOR.md
scripts/run_gssi_field_controlled_collection_real_return_collection_day_fill_packet_validator.py
scripts/test_gssi_field_controlled_collection_real_return_collection_day_fill_packet_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              8
passed checks:                       8
failed checks:                       0
validation ready:                    true
source fill packet ready:            true
real files still required:           9
metadata values still required:      32
checksums still required:            9
provenance acceptance ready:         false
real archive acceptance ready:       false
controlled evidence ready:           false
field FWI ready:                     false
field 3D/HPC ready:                  false
GPU priority:                        none
```

Validated checks:

| Check | Result |
| --- | --- |
| source policy and row counts | pass |
| real DZT files required and placeholders forbidden | pass |
| measured metadata values required | pass |
| checksum rows required | pass |
| acceptance gates blocked until fill | pass |
| acceptance and downstream gates closed | pass |
| figure nonblank | pass |
| script snapshots present | pass |

## Interpretation

The fill packet validates as an operational worklist: it requires nine real
DZT files, 32 measured metadata values, and nine checksums while keeping
provenance, archive acceptance, controlled evidence, field FWI, 3D/HPC, and
GPU escalation blocked.

## Decision

Use run `270` as the guarded validator for the run `269` fill packet. Treat
the packet as a collection-day worklist only, not accepted field evidence.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_collection_day_fill_packet_validator.py
3 passed
```

Figure validation:

```text
2969x881, dynamic range=255
```
