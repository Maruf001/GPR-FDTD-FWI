# BEM Experiment 467: Post-Scorecard Intake Worksheet Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded 35-field normalized-comparator scorecard intake worksheet from
runs `464-466` into the BEM claim boundary.

## Output

```text
outputs/bem_experiments/467_project_core_bem_post_35field_real_normalized_comparator_scorecard_intake_worksheet_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_intake_worksheet_claim_boundary_claim_rows.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_intake_worksheet_claim_boundary_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_intake_worksheet_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claims:                                      30
guarded claims:                              27
blocked claims:                              3
scorecard intake worksheet ready:            true
worksheet validation ready:                  true
worksheet sensitivity ready:                 true
worksheet rows:                              279
receivers:                                   31
frequencies:                                 9
required real-return fields per row:         4
required real-return cells:                  1116
filled real-return cells:                    0
missing real-return cells:                   1116
completed worksheet rows:                    0
comparison-ready rows:                       0
template rows currently evidence:            0
hash requirements:                           558
norm requirements:                           558
reference coefficient text:                  0.019078784028338909
sensitivity scenarios:                       40
sensitivity expected failures:               39
sensitivity unexpected outcomes:             0
real return values present:                  false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field transfer ready:                        false
field FWI ready:                             false
```

The new guarded claim records that the future real-return scorecard has a
validated worksheet, but no real values or evidence rows are present yet.

## Decision

Use this as the current BEM claim boundary after the scorecard intake worksheet
block. Fill the 1116 real-return requirements before any real comparison, 3D
validation, GPU/HPC, field transfer, or field FWI work.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_intake_worksheet_claim_boundary.py
4 passed
```

Figure check:

```text
3941x899, dynamic range=255
```
