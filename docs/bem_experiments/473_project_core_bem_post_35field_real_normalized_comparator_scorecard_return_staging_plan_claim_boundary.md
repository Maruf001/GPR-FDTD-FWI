# BEM Experiment 473: Post-Scorecard Return Staging Plan Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded 35-field scorecard return staging plan from runs `470-472`
into the BEM claim boundary.

## Output

```text
outputs/bem_experiments/473_project_core_bem_post_35field_real_normalized_comparator_scorecard_return_staging_plan_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_staging_plan_claim_boundary_claim_rows.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_staging_plan_claim_boundary_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_staging_plan_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claims:                                      31
guarded claims:                              28
blocked claims:                              3
return staging plan ready:                   true
staging-plan validation ready:               true
staging-plan sensitivity ready:              true
worksheet rows:                              279
required real-return cells:                  1116
stage actions:                               6
cell-stage groups:                           4
dependency edges:                            7
filled real-return cells:                    0
missing real-return cells:                   1116
source-hash stage cells:                     558
scattered-norm stage cells:                  558
computed comparator rows:                    279
evidence-review rows:                        279
sensitivity scenarios:                       22
sensitivity expected failures:               21
sensitivity unexpected outcomes:             0
real return values present:                  false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field transfer ready:                        false
field FWI ready:                             false
```

The new guarded claim records the return order for the 1116 required cells, but
still blocks evidence promotion because none of those values have been
returned.

## Decision

Use this as the current BEM claim boundary after the scorecard return
staging-plan block. Fill the 1116 real-return requirements before any real
comparison, 3D validation, GPU/HPC, field transfer, or field FWI work.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_return_staging_plan_claim_boundary.py
4 passed
```

Figure check:

```text
3941x899, dynamic range=255
```
