# Field Experiment 438: Direct-Intake Live Receipt Audit Validator

Date: 2026-06-30

## Purpose

Validate run `437` from saved artifacts.

The validator checks the source chain, directory/file row shape, clean empty
receipt state, blocked field-evidence gates, ordered actions, nonblank figure,
and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/438_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation passes:                         5
blocking failures:                         0
live receipt audit validation ready:       true
live directories present:                  5
expected files:                            33
expected files present:                    0
expected files missing:                    33
unexpected live files:                     0
remaining pre-ingest blockers:             4
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

## Decision

Use run `438` as the artifact validator for the run `437` live receipt audit.
The intake is validated as clean but empty, so parser, provenance, archive,
field FWI, and field 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit_validator.py
3 passed
```

Figure check:

```text
2285x840, dynamic range=255
```
