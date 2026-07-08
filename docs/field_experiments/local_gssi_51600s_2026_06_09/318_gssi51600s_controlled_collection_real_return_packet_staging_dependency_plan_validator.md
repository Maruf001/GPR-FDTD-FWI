# Field Experiment 318: Real-Return Packet Staging Dependency Plan Validator

Date: 2026-06-29

## Purpose

Validate the saved run `317` controlled field return-packet staging dependency
plan from artifacts.

This run checks the stage order, dependency graph, missing-item counts,
downstream blocked states, figure validation, and script snapshots. It does not
stage measured files, run provenance acceptance, run archive acceptance,
promote controlled field evidence, run field FWI, launch GPU work, or start
field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/318_gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_staging_dependency_plan_validator.png
scripts/
```

## Result

```text
validation checks:             7
passed checks:                 7
failed checks:                 0
validation ready:              true
stage count:                   7
dependency edges:              9
missing packet items:          57
missing measured DZT files:    9
missing metadata requirements: 32
field evidence ready:          false
field FWI ready:               false
field 3D/HPC ready:            false
```

## Interpretation

The saved field staging plan is internally consistent: it has seven ordered
stages, nine dependency edges, 57 missing packet items, and no field-evidence
promotion.

## Decision

Use run `318` as the validator for the run `317` controlled field staging
dependency plan. Sensitivity hardening remains required before closing this
field staging-plan block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_staging_dependency_plan_validator.py
3 passed
```

Figure validation:

```text
3581x949, dynamic range=255
```
