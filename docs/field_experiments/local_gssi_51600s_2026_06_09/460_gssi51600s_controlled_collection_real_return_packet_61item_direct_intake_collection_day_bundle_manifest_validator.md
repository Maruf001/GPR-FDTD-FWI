# Field Experiment 460: Direct-Intake Collection-Day Bundle Manifest Validator

Date: 2026-06-30

## Purpose

Validate the run `459` collection-day bundle manifest from a consumer
perspective.

Run `459` joined the 33 required live field-file entries with the 24 validated
metadata JSON templates. This run checks that the bundle has the expected shape,
links metadata templates correctly, and still accepts zero live field evidence.

This run does not copy measured files, write to live staging, accept
provenance, build a field archive, run field FWI, or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/460_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_bundle_manifest_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_bundle_manifest_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_bundle_manifest_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_collection_day_bundle_manifest_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source bundle manifest ready:             true
validation checks:                        5
passed checks:                            5
failed checks:                            0
bundle file entries:                      33
DZT file entries:                         9
metadata JSON entries:                    24
metadata templates linked:                24
live files present:                       0
receipt checks ready:                     0
evidence-ready entries:                   0
controlled field evidence ready:          false
field FWI ready:                          false
field 3D/HPC ready:                       false
GPU priority:                             none
validation ready:                         true
```

The five checks confirm source readiness, the 33-entry bundle shape, the
9-DZT/24-JSON split, the 24 metadata template links, zero live files, zero
receipt-ready entries, zero evidence-ready entries, blocked downstream states,
and nonblank figure/script snapshots.

## Interpretation

The collection-day bundle is valid as a handoff manifest and not as field
evidence. It identifies the nine measured DZT files and 24 completed metadata
JSON files still required before any receipt, parser, provenance, or archive
gate can pass.

## Decision

Use runs `459-460` as the guarded collection-day bundle block. Keep field
evidence, provenance acceptance, archive acceptance, field FWI, GPU work, and
field 3D/HPC blocked until the 33 live files are copied and the guarded gates
are rerun.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_collection_day_bundle_manifest_validator.py
5 passed
```

Figure check:

```text
2357x847, dynamic range=255
```
