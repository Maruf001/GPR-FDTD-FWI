# Field Experiment 320: Post Staging Dependency Claim Boundary

Date: 2026-06-29

## Purpose

Integrate the guarded controlled-field return-packet staging dependency block
from runs `317-319` into the current field claim boundary.

This run uses saved artifacts only. It does not stage measured files, run
provenance acceptance, promote field evidence, run field FWI, launch GPU work,
or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/320_gssi51600s_controlled_collection_real_return_post_staging_dependency_claim_boundary
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_staging_dependency_claim_boundary_claim_rows.csv
data/gssi51600s_controlled_collection_real_return_post_staging_dependency_claim_boundary_summary.json
figures/gssi51600s_controlled_collection_real_return_post_staging_dependency_claim_boundary.png
scripts/
```

## Result

```text
claims:                              14
guarded claims:                      10
blocked claims:                      4
base claims:                         13
base guarded claims:                 9
base blocked claims:                 4
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

The field claim boundary now includes the guarded seven-stage staging
dependency plan. The plan is useful as a measured-packet execution sequence,
but it does not promote the archive to evidence because no measured packet
items are present.

## Decision

Use run `320` as the current field claim boundary after the staging dependency
block. Do not promote field evidence or run field FWI until the measured packet
passes the acceptance gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_staging_dependency_claim_boundary.py
3 passed
```

Figure validation:

```text
3581x953, dynamic range=255
```
