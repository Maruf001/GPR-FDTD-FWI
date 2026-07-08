# BEM Experiment 497: Post Real Return-File Filesystem Gap-Audit Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded run `494-496` filesystem gap audit into the current BEM claim
boundary.

## Output

```text
outputs/bem_experiments/497_project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_claim_boundary_claim_rows.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_claim_boundary_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claim count:                                 35
guarded claims:                              32
blocked claims:                              3
claim boundary ready:                        true
required real return files:                  4
required real paths present:                 0
open filesystem gaps:                        4
matching filename candidates:                8
real return-file candidates:                 0
blank-template candidates:                   4
synthetic-reference candidates:              4
accepted real files:                         0
accepted real entries:                       0
accepted real scorecard rows:                0
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

The added guarded claim states that the required real-return filenames are
present only as blank templates and synthetic references. No real-return file is
available for evidence.

## Decision

Use this as the current BEM claim boundary after the real return-file
filesystem gap audit.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_claim_boundary.py
4 passed
```

Figure check:

```text
4049x894, dynamic range=255
```
