# BEM Experiment 479: Post 35-Field Return-File Manifest Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded return-file manifest from runs `476-478` into the current BEM
claim boundary.

## Output

```text
outputs/bem_experiments/479_project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_manifest_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_manifest_claim_boundary_claim_rows.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_manifest_claim_boundary_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_manifest_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claims:                                      32
guarded claims:                              29
blocked claims:                              3
return-file manifest ready:                  true
manifest validation ready:                   true
manifest sensitivity ready:                  true
required files:                              4
template files:                              4
template entries:                            1116
required real input cells:                   1116
filled template entries:                     0
missing template entries:                    1116
source-hash template entries:                558
scattered-norm template entries:             558
receivers:                                   31
frequencies:                                 9
real return files present:                   false
real return values present:                  false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

The new guarded claim records that the 35-field comparison has four concrete
return-file templates, but all real values and source hashes remain blank.

## Decision

Use this as the current BEM claim boundary after the return-file manifest
block. Real comparison, 3D validation, GPU/HPC work, field transfer, and field
FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_manifest_claim_boundary.py
4 passed
```

Figure check:

```text
3941x899, dynamic range=255
```
