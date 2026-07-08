# BEM Experiment 508: Bempp 35-Field Real-Return Producer Contract Spec Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `507` validator for the run `506` real-return producer
contract spec.

Run `507` validated the saved producer contract. This run verifies that the
validator rejects damaged contract artifacts and premature real-return
promotion.

## Output

```text
outputs/bem_experiments/508_project_core_bem_bempp_35field_real_return_producer_contract_spec_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_bempp_35field_real_return_producer_contract_spec_validation_sensitivity_rows.csv
data/project_core_bem_bempp_35field_real_return_producer_contract_spec_validation_sensitivity_summary.json
figures/project_core_bem_bempp_35field_real_return_producer_contract_spec_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                         9
expected pass scenarios:                       1
expected failure scenarios:                    8
unexpected scenarios:                          0
producer-contract validation sensitivity:      true
exact source artifacts pass:                   true
real-return promotion rejected:                true
real return production ready:                  false
real BEM/FDTD comparison ready:                false
3D validation ready:                           false
GPU/HPC ready:                                 false
field FWI ready:                               false
GPU priority:                                  none
```

The exact run `506` artifacts pass. Damaged variants fail as expected for a
missing return-file row, entry-count drift, schema frequency drift, premature
BEM-exporter availability, exact-producer promotion, real-return production
promotion, figure damage, and script-snapshot damage.

## Decision

Use runs `506-508` as the guarded real-return producer-contract block. The next
BEM implementation step is to build a non-promotional exporter/writer skeleton
or receive real return files; existing metadata still cannot be promoted as
real BEM/FDTD comparison evidence.

## Validation

Focused tests:

```text
tests/test_project_core_bem_bempp_35field_real_return_producer_contract_spec.py
tests/test_project_core_bem_bempp_35field_real_return_producer_contract_spec_validator.py
tests/test_project_core_bem_bempp_35field_real_return_producer_contract_spec_validation_sensitivity.py
11 passed
```

Figure check:

```text
2357x856, dynamic range=255
```
