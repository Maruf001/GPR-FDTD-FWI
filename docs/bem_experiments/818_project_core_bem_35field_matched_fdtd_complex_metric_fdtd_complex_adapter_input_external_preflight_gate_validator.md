# BEM Experiment 818: Complex FDTD External Input Preflight Gate Validator

Date: 2026-07-01

## Purpose

Validate the saved run `817` external complex FDTD input preflight gate.

The validator checks the fail-closed absent-file state, zero accepted rows, zero
value/provenance cells, blocked comparison states, figure validation, and script
snapshots.

## Output

```text
outputs/bem_experiments/818_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_preflight_gate_validator
```

## Result

```text
validation checks:                       6
passed checks:                           6
failed checks:                           0
preflight items:                         1
expected rows:                           279
external input file present:             false
external input rows:                     0
external input accepted:                 false
finite FDTD value cells:                 0
provenance/status cells:                 0
completed stage files ready:             false
real BEM/FDTD comparison ready:          false
field transfer ready:                    false
3D/HPC ready:                            false
gpu priority:                            none
```

## Interpretation

The saved preflight gate validates from artifacts and keeps the branch
fail-closed until a real external input file appears.

## Decision

Use this validator before accepting a real complex FDTD input CSV.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_preflight_gate_validator.py

3 passed
```

Figure check:

```text
2825x897, dynamic range=255
```
