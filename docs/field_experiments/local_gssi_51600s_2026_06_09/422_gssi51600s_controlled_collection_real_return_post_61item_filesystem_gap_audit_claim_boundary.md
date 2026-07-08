# Field Experiment 422: Post Filesystem-Gap-Audit Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded filesystem gap audit from runs `419-421` into the current
field claim boundary.

This run makes the field-side conclusion explicit: the real-packet workflow is
well specified and guarded, but the required measured files are still absent.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/422_gssi51600s_controlled_collection_real_return_post_61item_filesystem_gap_audit_claim_boundary
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_filesystem_gap_audit_claim_boundary_claims.csv
data/gssi51600s_controlled_collection_real_return_post_61item_filesystem_gap_audit_claim_boundary_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_filesystem_gap_audit_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claim count:                                28
guarded claims:                             24
blocked claims:                             4
direct real inputs required:                33
generated follow-ups required:              16
open filesystem gaps:                       33
matching candidate files:                   95
real-return candidates:                     0
blank-template candidates:                  62
synthetic-reference candidates:             33
accepted measured-evidence files:           0
claim boundary ready:                       true
real packet files present:                  false
real packet accepted:                       false
controlled field evidence ready:            false
field FWI ready:                            false
field 3D/HPC ready:                         false
GPU priority:                               none
```

The new guarded claim records that all 33 required direct real-input slots
remain filesystem gaps. The files currently found by name are blank templates
or synthetic references, not measured field returns.

## Decision

Use run `422` as the current field claim boundary after the filesystem gap
audit. Do not promote the archive to field evidence, provenance acceptance,
archive acceptance, field FWI, GPU work, or field 3D/HPC.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_filesystem_gap_audit_claim_boundary.py
4 passed
```

Figure check:

```text
3869x884, dynamic range=255
```
