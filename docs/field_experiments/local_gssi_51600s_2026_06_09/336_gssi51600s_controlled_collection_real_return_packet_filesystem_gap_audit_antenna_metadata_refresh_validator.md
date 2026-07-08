# Field Experiment 336: Antenna-Aware Filesystem Gap Audit Validator

Date: 2026-06-29

## Purpose

Validate the saved run `335` 61-item filesystem gap audit from artifacts.

This run does not stage measured files, run provenance acceptance, run archive
acceptance, promote controlled field evidence, run field FWI, launch GPU work,
or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/336_gssi51600s_controlled_collection_real_return_packet_filesystem_gap_audit_antenna_metadata_refresh_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_filesystem_gap_audit_antenna_metadata_refresh_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_filesystem_gap_audit_antenna_metadata_refresh_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_filesystem_gap_audit_antenna_metadata_refresh_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  8
passed checks:                      8
failed checks:                      0
validation ready:                   true
packet items required:              61
present packet items:               0
missing packet items:               61
metadata requirements:              36
antenna metadata addendum items:    4
open action groups:                 7
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

## Interpretation

The saved run `335` audit validates from artifacts. It preserves the guarded
61-item packet contract, zero present packet items, seven open action groups,
four antenna metadata addendum items, and blocked downstream field states.

## Decision

Use this validator as the artifact-level guard for the antenna-aware filesystem
gap audit. Sensitivity hardening remains required before closing the block.

## Validation

Focused validator test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_filesystem_gap_audit_antenna_metadata_refresh_validator.py
2 passed
```

Figure validation:

```text
3617x929, dynamic range=255
```
