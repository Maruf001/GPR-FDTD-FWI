# BEM Experiment 485: Post Synthetic Return-File Fill Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded synthetic return-file consumer smoke from runs `482-484` into
the BEM claim boundary.

## Output

```text
outputs/bem_experiments/485_project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_claim_boundary_claim_rows.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_claim_boundary_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claims:                                      33
guarded claims:                              30
blocked claims:                              3
synthetic fill smoke ready:                  true
synthetic fill validator ready:              true
synthetic fill sensitivity ready:            true
synthetic return files:                      4
filled synthetic entries:                    1116
valid source-hash entries:                   558
finite scattered-norm entries:               558
scorecard rows:                              279
receiver count:                              31
frequency count:                             9
synthetic values are evidence:               false
real return files present:                   false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

## Interpretation

The claim boundary now records that the four-file return contract can be filled
and consumed synthetically. The new guarded claim does not promote synthetic
values to evidence.

## Decision

Use this as the current BEM claim boundary after the synthetic return-file fill
block. Real BEM/FDTD comparison and downstream escalation remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_claim_boundary.py
4 passed
```

Figure check:

```text
4013x894, dynamic range=255
```
