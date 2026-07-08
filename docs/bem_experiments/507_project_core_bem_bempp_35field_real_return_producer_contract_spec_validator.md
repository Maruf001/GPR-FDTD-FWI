# BEM Experiment 507: Bempp 35-Field Real-Return Producer Contract Spec Validator

Date: 2026-06-30

## Purpose

Validate run `506`, the 35-field BEM/FDTD real-return producer contract spec.

Run `506` made the accepted return-file implementation target explicit: four
279-row real-return files over the 31-receiver by nine-frequency grid, with BEM
and FDTD exporters plus an accepted return-file writer still missing. This
validator checks that the saved contract is internally consistent and remains
non-promotional.

## Output

```text
outputs/bem_experiments/507_project_core_bem_bempp_35field_real_return_producer_contract_spec_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_35field_real_return_producer_contract_spec_validator_checks.csv
data/project_core_bem_bempp_35field_real_return_producer_contract_spec_validator_summary.json
figures/project_core_bem_bempp_35field_real_return_producer_contract_spec_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                      5
validation checks passed:               5
blocking failures:                      0
producer-contract validation ready:     true
required return files:                  4
required real entries:                  1116
implementation blockers:               3
real return production ready:           false
real BEM/FDTD comparison ready:         false
3D validation ready:                    false
GPU/HPC ready:                          false
field FWI ready:                        false
GPU priority:                           none
```

The validator confirms the four required return files, the 31-by-9 schema, the
three open implementation blockers, and the blocked downstream state.

## Decision

Use run `507` as the artifact guard for run `506`. The next BEM progress must
come from implementing or receiving the exact exporters and return-file writer,
not from reinterpreting existing metadata as real comparison evidence.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_35field_real_return_producer_contract_spec.py
tests/test_project_core_bem_bempp_35field_real_return_producer_contract_spec_validator.py
8 passed
```

Figure check:

```text
2177x835, dynamic range=255
```
