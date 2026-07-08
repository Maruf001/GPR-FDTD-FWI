# BEM Experiment 195: Deeper-Offset Tabulated Surface Validator

Date: 2026-06-27

## Purpose

Validate the run `194` tabulated field-surface repair candidate from a consumer
perspective.

This is a CPU-only validation run. It does not rerun FDTD/BEM solvers, compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/195_project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_validator
```

Key artifacts:

```text
data/project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_validation_checks.csv
data/project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_validator_summary.json
figures/project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_validator.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_LARGER_RADIUS_DEEPER_OFFSET_TABULATED_SURFACE_VALIDATOR.md
scripts/run_project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_validator.py
scripts/test_project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_validator.py
```

## Result

```text
validation checks:                  11
validation passes:                  11
blocking failures:                   0
source best policy:                  dense_5mm_plus_exact
source best leave-one L2:            0.5654888528068279
source minimum ready sample count:   19
tabulated-surface validation ready:  true
contract refresh ready:              false
field transfer ready:                false
3D validation ready:                 false
GPU work ready:                      false
field FWI ready:                     false
```

The validator confirms:

| Check family | Result |
| --- | --- |
| Surface-policy count | Passed |
| Ready-policy count | Passed |
| Exact source/receiver-only policy fails with extrapolation | Passed |
| Dense 10 mm policy is ready without extrapolation | Passed |
| Dense 5 mm policy is best and ready | Passed |
| Best L2 matches summary | Passed |
| Best L2 is below the `0.75` acceptance gate | Passed |
| Best policy improves over the Sommerfeld baseline | Passed |
| Minimum ready sample count is 19 | Passed |
| Repair is ready but contract refresh remains blocked | Passed |
| Field, 3D, GPU, and field FWI remain blocked | Passed |

## Interpretation

The tabulated-surface repair is consumer-valid as a single-case repair
candidate. The important mechanism is also clear: exact source/receiver-only
sampling fails because leave-one validation must extrapolate held-out
source/receiver positions, while dense 10 mm and 5 mm policies pass without
held-out extrapolation.

This validates the run `194` result structure. It does not validate
generalization and does not refresh the analytic BEM shell-support contract.

## Decision

Use run `195` as the validator for the tabulated-surface repair candidate.
Require negative-control sensitivity before any claim refresh. Keep contract
refresh, field transfer, 3D validation, GPU/HPC, field FWI, and synthetic
`outputs/experiments` promotion blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_probe.py
tests/test_project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_validator.py
7 passed
```

Figure validation:

```text
project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_validator.png
2681x858, dynamic range=255
```
