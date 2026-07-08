# BEM Experiment 504: Bempp 35-Field Exact Producer Coverage Audit Validator

Date: 2026-06-29

## Purpose

Validate the run `503` coverage audit.

The validator checks coverage counts, confirms that no exact 35-field Bempp
producer candidate exists, preserves the blocked downstream state, and verifies
the figure and script snapshots.

## Output

```text
outputs/bem_experiments/504_project_core_bem_bempp_35field_exact_producer_coverage_audit_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_35field_exact_producer_coverage_audit_validator_checks.csv
data/project_core_bem_bempp_35field_exact_producer_coverage_audit_validator_summary.json
figures/project_core_bem_bempp_35field_exact_producer_coverage_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                          4
validation passes:                          4
blocking failures:                          0
validation ready:                           true
audited candidate summaries:                145
Bempp runtime candidates:                   54
Bempp-tagged 31x9 metadata matches:         1
exact 35-field Bempp producer candidates:   0
exact Bempp 35-field producer ready:        false
real return production ready:               false
real BEM/FDTD comparison ready:             false
3D validation ready:                        false
GPU/HPC ready:                              false
field FWI ready:                            false
```

## Decision

Use run `504` as the artifact guard for run `503`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_35field_exact_producer_coverage_audit_validator.py
4 passed
```

Figure check:

```text
2105x805, dynamic range=255
```
