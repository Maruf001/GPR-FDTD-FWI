# BEM Experiment 505: Bempp 35-Field Exact Producer Coverage Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `504` validator for the run `503` Bempp 35-field exact
producer coverage audit.

Run `503` found historical Bempp-side metadata that reaches the target 31
receiver by nine frequency grid in one Bempp-tagged row, but no exact producer
that writes the accepted 35-field `real_return_files` contract. Run `504`
validated that result. This run damages the saved inputs to make sure the
validator rejects premature producer promotion and downstream claim promotion.

## Output

```text
outputs/bem_experiments/505_project_core_bem_bempp_35field_exact_producer_coverage_audit_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_bempp_35field_exact_producer_coverage_audit_validation_sensitivity_rows.csv
data/project_core_bem_bempp_35field_exact_producer_coverage_audit_validation_sensitivity_summary.json
figures/project_core_bem_bempp_35field_exact_producer_coverage_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                    11
expected pass scenarios:                  1
expected failure scenarios:               10
unexpected scenarios:                     0
validation sensitivity ready:             true
exact source artifacts pass:              true
exact producer promotion rejected:        true
downstream promotion rejected:            true
exact Bempp 35-field producer ready:      false
real return production ready:             false
real BEM/FDTD comparison ready:           false
3D validation ready:                      false
GPU/HPC ready:                            false
field FWI ready:                          false
GPU priority:                             none
```

The exact run `503` artifacts pass. Damaged variants fail as expected for
candidate-count drift, grid-metadata count drift, Bempp-runtime count drift,
target-grid match-count drift, exact-producer promotion, removal of the
Bempp-tagged 31x9 metadata match, frequency-coverage shortfall, downstream
comparison promotion, figure damage, and script-snapshot damage.

## Decision

Use runs `503-505` as the guarded Bempp 35-field exact-producer coverage block.
The conclusion remains unchanged: historical metadata is useful context, but an
explicit 9-frequency Bempp export and accepted return-file writer are still
needed before real BEM/FDTD comparison evidence can be claimed.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_35field_exact_producer_coverage_audit.py
tests/test_project_core_bem_bempp_35field_exact_producer_coverage_audit_validator.py
tests/test_project_core_bem_bempp_35field_exact_producer_coverage_audit_validation_sensitivity.py
12 passed
```

Figure check:

```text
2465x875, dynamic range=255
```
