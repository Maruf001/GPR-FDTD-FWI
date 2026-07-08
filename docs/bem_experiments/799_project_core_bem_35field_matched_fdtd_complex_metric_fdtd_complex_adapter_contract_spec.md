# BEM Experiment 799: Complex-Metric FDTD Complex Adapter Contract Spec

Date: 2026-07-01

## Purpose

Define the required contract for a new complex FDTD adapter that can complete
the five-stage complex-metric packet from run `790`.

Run `796` showed that the older matched-FDTD route can reuse identity and
strict hash guards, but cannot directly fill the `fdtd_real` and `fdtd_imag`
fields required by the current packet. This run turns that decision into an
explicit adapter contract.

## Output

```text
outputs/bem_experiments/799_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_contract_spec
```

## Result

```text
source partial export ready:                 true
source route audit ready:                    true
source route sensitivity ready:              true
adapter input required columns:              12
completed stage output fill columns:         11
identity columns:                            4
complex value columns:                       2
provenance/guard columns:                    6
mapping steps:                               5
ready mapping steps:                         1
guards:                                      8
ready guards:                                4
partial stage files:                         5
partial metric rows:                         279
FDTD complex value cells required:           558
FDTD provenance/status cells required:       1395
new complex FDTD adapter required:           true
complex FDTD adapter contract ready:         true
complex FDTD adapter implementation ready:   false
completed stage files ready:                 false
real BEM/FDTD comparison ready:              false
field transfer ready:                        false
3D/HPC ready:                                false
gpu priority:                                none
```

## Decision

Use this contract before implementing the complex FDTD adapter. The contract is
ready, but adapter execution, completed stage files, real BEM/FDTD comparison,
field transfer, and 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_contract_spec.py
3 passed
```

Figure check:

```text
3293x918, dynamic range=255
```
