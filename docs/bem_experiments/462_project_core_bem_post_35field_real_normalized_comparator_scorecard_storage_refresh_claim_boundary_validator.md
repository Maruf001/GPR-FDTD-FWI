# BEM Experiment 462: Post Storage-Refresh Claim-Boundary Validator

Date: 2026-06-29

## Purpose

Validate the run `461` BEM claim boundary from saved artifacts.

## Output

```text
outputs/bem_experiments/462_project_core_bem_post_35field_real_normalized_comparator_scorecard_storage_refresh_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_storage_refresh_claim_boundary_validator_checks.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_storage_refresh_claim_boundary_validator_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_storage_refresh_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           5
validation checks passed:                    5
blocking failures:                           0
claim-boundary validation ready:             true
claims:                                      29
guarded claims:                              26
blocked claims:                              3
scorecard storage refresh ready:             true
recommended storage significant digits:      17
minimum safe scorecard significant digits:   13
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

The validator confirms claim counts, the storage-refresh claim text/support,
the 279-row storage-refresh metrics, downstream blocked states, figure
validation, and script snapshots.

## Decision

Use this validator as the artifact guard for run `461`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_storage_refresh_claim_boundary_validator.py
5 passed
```

Figure check:

```text
2645x839, dynamic range=255
```
