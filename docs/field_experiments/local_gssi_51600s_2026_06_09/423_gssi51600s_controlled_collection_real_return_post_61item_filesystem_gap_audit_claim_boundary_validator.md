# Field Experiment 423: Post Filesystem-Gap-Audit Claim-Boundary Validator

Date: 2026-06-29

## Purpose

Validate the run `422` field claim-boundary artifact.

The validator checks the claim counts, the inserted filesystem-gap claim, the
gap-audit metrics, the downstream blocked states, and the figure and script
snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/423_gssi51600s_controlled_collection_real_return_post_61item_filesystem_gap_audit_claim_boundary_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_filesystem_gap_audit_claim_boundary_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_post_61item_filesystem_gap_audit_claim_boundary_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_filesystem_gap_audit_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                          5
validation passes:                          5
blocking failures:                          0
validation ready:                           true
claim count:                                28
guarded claims:                             24
blocked claims:                             4
direct real inputs required:                33
open filesystem gaps:                       33
real-return candidates:                     0
real packet files present:                  false
controlled field evidence ready:            false
field FWI ready:                            false
field 3D/HPC ready:                         false
GPU priority:                               none
```

The validator accepts the exact run `422` boundary and confirms that the field
workflow remains blocked for missing measured files.

## Decision

Use run `423` as the artifact guard for run `422`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_filesystem_gap_audit_claim_boundary_validator.py
4 passed
```

Figure check:

```text
2141x839, dynamic range=255
```
