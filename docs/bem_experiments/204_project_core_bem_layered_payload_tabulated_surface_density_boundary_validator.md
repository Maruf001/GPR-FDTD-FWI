# BEM Experiment 204: Tabulated Surface Density Boundary Validator

Date: 2026-06-28

## Purpose

Validate the run `203` tabulated-surface density-boundary result from a
consumer perspective.

This is a CPU-only validation run. It does not rerun FDTD/BEM solvers, compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/204_project_core_bem_layered_payload_tabulated_surface_density_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_layered_payload_tabulated_surface_density_boundary_validation_checks.csv
data/project_core_bem_layered_payload_tabulated_surface_density_boundary_validator_summary.json
figures/project_core_bem_layered_payload_tabulated_surface_density_boundary_validator.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_TABULATED_SURFACE_DENSITY_BOUNDARY_VALIDATOR.md
scripts/run_project_core_bem_layered_payload_tabulated_surface_density_boundary_validator.py
scripts/test_project_core_bem_layered_payload_tabulated_surface_density_boundary_validator.py
```

## Result

```text
validation checks:                  11
validation passes:                  11
blocking failures:                  0
minimum all-case-ready policy:      dense_10mm_plus_exact
minimum all-case-ready samples:     19
minimum all-case-ready worst L2:    0.650662226077945
best overall policy:                dense_5mm_plus_exact
density-boundary validation ready:  true
density-boundary sensitivity ready: true
analytic contract refresh ready:    false
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

The validator confirms:

| Check family | Result |
| --- | --- |
| Support/policy row count | Passed |
| Case, support-mode, and policy counts | Passed |
| Exact source/receiver-only policy fails with held-out extrapolation | Passed |
| 20 mm plus exact policy fails the all-case boundary | Passed |
| 15 mm plus exact is ready but not lower-sample than 10 mm | Passed |
| 10 mm plus exact is the minimum all-case-ready policy | Passed |
| 5 mm plus exact is the best observed accuracy reference | Passed |
| No lower-sample all-case-ready policy beats 10 mm | Passed |
| Density boundary marked ready | Passed |
| Analytic contract refresh remains blocked | Passed |
| Field, 3D, GPU, and field FWI remain blocked | Passed |

## Interpretation

The density-boundary result is consumer-valid. The expected failing and passing
policies are separated, 10 mm plus exact is the cheapest all-case-ready policy
by sample count, 5 mm plus exact remains the higher-cost accuracy reference,
and downstream promotion flags remain blocked.

## Decision

Use run `204` as the validator for the run `203` density boundary. Add
negative-control sensitivity before using the density boundary in downstream
contract or presentation language.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_tabulated_surface_density_boundary_validator.py
5 passed
```

Figure validation:

```text
project_core_bem_layered_payload_tabulated_surface_density_boundary_validator.png
2717x855, dynamic range=255
```
