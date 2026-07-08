# Field Experiment 321: Post Staging Dependency Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `320` field post-staging dependency claim boundary from
artifacts.

This run checks source identity, claim counts, the staging dependency claim
row, staging metrics, blocked claim rows, downstream blocked states, figure
validation, and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/321_gssi51600s_controlled_collection_real_return_post_staging_dependency_claim_boundary_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_staging_dependency_claim_boundary_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_post_staging_dependency_claim_boundary_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_post_staging_dependency_claim_boundary_validator.png
scripts/
```

## Result

```text
validation checks:                   7
passed checks:                       7
failed checks:                       0
validation ready:                    true
claims:                              14
guarded claims:                      10
blocked claims:                      4
staging sensitivity ready:           true
accepts exact run 317:               true
rejects damaged variants:            true
stages:                              7
dependency edges:                    9
missing packet items:                57
missing measured DZT files:          9
missing metadata requirements:       32
missing checksum rows:               9
missing acceptance results:          7
real packet files present:           false
provenance acceptance ready:         false
real archive acceptance ready:       false
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
gpu priority:                        none
```

## Interpretation

The saved field post-staging claim boundary is internally consistent. The
staging dependency plan is guarded, and field execution remains blocked by the
absent 57-item measured packet.

## Decision

Use run `321` as the validator for the run `320` field post-staging claim
boundary. Sensitivity hardening remains required before closing the block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_staging_dependency_claim_boundary_validator.py
3 passed
```

Figure validation:

```text
3761x929, dynamic range=255
```
