# BEM Experiment 198: Tabulated Surface Offset Generalization Validator

Date: 2026-06-27

## Purpose

Validate the run `197` generalized tabulated field-surface repair from a
consumer perspective.

This is a CPU-only validation run. It does not rerun FDTD/BEM solvers, compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/198_project_core_bem_layered_payload_tabulated_surface_offset_generalization_validator
```

Key artifacts:

```text
data/project_core_bem_layered_payload_tabulated_surface_offset_generalization_validation_checks.csv
data/project_core_bem_layered_payload_tabulated_surface_offset_generalization_validator_summary.json
figures/project_core_bem_layered_payload_tabulated_surface_offset_generalization_validator.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_TABULATED_SURFACE_OFFSET_GENERALIZATION_VALIDATOR.md
scripts/run_project_core_bem_layered_payload_tabulated_surface_offset_generalization_validator.py
scripts/test_project_core_bem_layered_payload_tabulated_surface_offset_generalization_validator.py
```

## Result

```text
validation checks:                  11
validation passes:                  11
blocking failures:                   0
source offset cases:                 5
source ready cases:                  5
source worst best case:              z_minus_2p5mm
source worst best leave-one L2:      0.650662226077945
generalization validation ready:     true
contract refresh ready:              false
field transfer ready:                false
3D validation ready:                 false
GPU work ready:                      false
field FWI ready:                     false
```

The validator confirms:

| Check family | Result |
| --- | --- |
| Offset case count | Passed |
| Support mode count | Passed |
| Support row count | Passed |
| Ready row count | Passed |
| Every case has a ready best support | Passed |
| No held-out extrapolation | Passed |
| Worst best case matches summary | Passed |
| Worst best L2 matches summary and passes gate | Passed |
| Worst best margin is positive | Passed |
| Generalization ready but contract refresh remains blocked | Passed |
| Field, 3D, GPU, and field FWI remain blocked | Passed |

## Interpretation

The run `197` offset-generalization result is consumer-valid. Every offset case
has a ready best support, the worst best-case L2 remains below the `0.75`
acceptance gate, and the 10 mm tabulated policy avoids held-out extrapolation.

This validates the result structure. It does not refresh the analytic BEM
contract and does not make field or 3D claims.

## Decision

Use run `198` as the validator for the generalized tabulated-surface repair.
Add negative-control sensitivity before any claim refresh. Keep analytic
contract refresh, field transfer, 3D validation, GPU/HPC, field FWI, and
synthetic `outputs/experiments` promotion blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_tabulated_surface_offset_generalization.py
tests/test_project_core_bem_layered_payload_tabulated_surface_offset_generalization_validator.py
8 passed
```

Figure validation:

```text
project_core_bem_layered_payload_tabulated_surface_offset_generalization_validator.png
2681x857, dynamic range=255
```
