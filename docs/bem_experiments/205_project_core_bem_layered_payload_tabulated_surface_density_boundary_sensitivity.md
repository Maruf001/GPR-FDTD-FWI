# BEM Experiment 205: Tabulated Surface Density Boundary Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `204` density-boundary validator with damaged variants of
the run `203` result.

This is a CPU-only guard run. It does not rerun FDTD/BEM solvers, compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/205_project_core_bem_layered_payload_tabulated_surface_density_boundary_sensitivity
```

Key artifacts:

```text
data/project_core_bem_layered_payload_tabulated_surface_density_boundary_sensitivity_rows.csv
data/project_core_bem_layered_payload_tabulated_surface_density_boundary_sensitivity_summary.json
figures/project_core_bem_layered_payload_tabulated_surface_density_boundary_sensitivity.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_TABULATED_SURFACE_DENSITY_BOUNDARY_SENSITIVITY.md
scripts/run_project_core_bem_layered_payload_tabulated_surface_density_boundary_sensitivity.py
scripts/test_project_core_bem_layered_payload_tabulated_surface_density_boundary_sensitivity.py
```

## Result

```text
sensitivity scenarios:              11
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         10
observed failure scenarios:         10
unexpected outcomes:                0
density-boundary sensitivity ready: true
analytic contract refresh ready:    false
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

The exact density-boundary result passes. Ten damaged variants fail:

| Scenario | Expected | Observed | Failed checks |
| --- | --- | --- | --- |
| exact density boundary | pass | pass | none |
| missing 10 mm policy summary | fail | fail | 15 mm/10 mm sample relation, 10 mm minimum policy |
| support/policy row-count drift | fail | fail | row count |
| exact policy marked ready | fail | fail | exact-only failure/extrapolation |
| 20 mm policy promoted | fail | fail | 20 mm boundary failure |
| 15 mm sample relation broken | fail | fail | 15 mm/10 mm sample relation |
| minimum policy changed from 10 mm | fail | fail | 10 mm minimum policy |
| lower-sample policy marked ready | fail | fail | no lower-sample all-case-ready policy |
| density boundary marked not ready | fail | fail | density-ready flag |
| analytic contract refresh marked ready | fail | fail | analytic refresh block |
| field transfer marked ready | fail | fail | field/3D/GPU/FWI block |

## Interpretation

The run `204` validator is sensitive to the important failure modes: row-count
drift, wrong policy readiness, broken 15 mm versus 10 mm sample-count logic,
premature analytic contract refresh, and premature field transfer.

## Decision

Use runs `203`-`205` as the guarded BEM tabulated-surface density-boundary
package. The practical policy remains 10 mm plus exact. Analytic replacement,
field transfer, 3D validation, GPU/HPC, field FWI, and synthetic
`outputs/experiments` promotion remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_tabulated_surface_density_boundary_sensitivity.py
4 passed
```

Figure validation:

```text
project_core_bem_layered_payload_tabulated_surface_density_boundary_sensitivity.png
2897x865, dynamic range=255
```
