# Field Experiment 333: Antenna-Aware Staging Dependency Plan Validator

Date: 2026-06-29

## Purpose

Validate the saved run `332` antenna-aware field staging dependency plan from
artifacts.

This run does not stage measured files, run provenance acceptance, run archive
acceptance, promote controlled field evidence, run field FWI, launch GPU work,
or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/333_gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_antenna_metadata_refresh_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_antenna_metadata_refresh_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_antenna_metadata_refresh_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_antenna_metadata_refresh_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  7
passed checks:                      7
failed checks:                      0
validation ready:                   true
stage count:                        7
dependency edges:                   9
packet items required:              61
missing packet items:               61
missing measured DZT files:         9
missing metadata requirements:      36
antenna metadata addendum items:    4
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

## Interpretation

The saved run `332` artifacts are internally consistent. The validator confirms
the source identity, seven-stage order, nine dependency edges, 61 missing
packet items, 36 missing metadata requirements, four antenna metadata addendum
items, blocked downstream states, figure validation, and script snapshots.

## Decision

Use this validator as the artifact-level guard for the refreshed staging plan.
Sensitivity hardening remains required before closing the block.

## Validation

Focused validator test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_staging_dependency_plan_antenna_metadata_refresh_validator.py
2 passed
```

Figure validation:

```text
3725x949, dynamic range=255
```
