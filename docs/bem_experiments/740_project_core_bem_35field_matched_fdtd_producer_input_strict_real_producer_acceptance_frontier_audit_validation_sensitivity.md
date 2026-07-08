# BEM Experiment 740: Strict Real-Producer Acceptance Frontier Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `739` validator.

The damaged cases cover missing error families, missing actions, row-count
drift, strict-hash damage, erased real-data blockers, damaged synthetic
positive-control counts, false strict-acceptance completion, false real
evidence, false exporter/comparison/GPU readiness, blank figure output, and
missing script snapshots.

## Output

```text
outputs/bem_experiments/740_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_acceptance_frontier_audit_validation_sensitivity
```

## Result

```text
cases:                                18
expected pass:                        1
expected fail:                        17
actual pass:                          1
actual fail:                          17
unexpected outcomes:                  0
real BEM/FDTD comparison ready:       false
GPU/HPC ready:                        false
field transfer ready:                 false
field FWI ready:                      false
```

## Decision

Runs `738-740` are the guarded strict real-producer acceptance-frontier block.
The validator rejects false real-file acceptance, false comparison readiness,
and false downstream promotion.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_acceptance_frontier_audit_validation_sensitivity.py
3 passed
```

