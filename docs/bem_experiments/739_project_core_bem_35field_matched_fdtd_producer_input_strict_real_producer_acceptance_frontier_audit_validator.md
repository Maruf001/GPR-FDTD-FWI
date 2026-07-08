# BEM Experiment 739: Strict Real-Producer Acceptance Frontier Audit Validator

Date: 2026-07-01

## Purpose

Validate run `738` from saved artifacts.

## Output

```text
outputs/bem_experiments/739_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_acceptance_frontier_audit_validator
```

## Result

```text
checks:                               8
passed:                               8
failed:                               0
required live files:                  2
required rows:                        558
remaining real-data errors:           2232
completed actions:                    2
synthetic accepted rows:              558
real BEM/FDTD comparison ready:       false
GPU/HPC ready:                        false
field transfer ready:                 false
field FWI ready:                      false
```

## Decision

Run `738` is valid as the strict real-producer acceptance frontier. Real
comparison remains blocked until real live files are returned and accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_acceptance_frontier_audit_validator.py
3 passed
```

