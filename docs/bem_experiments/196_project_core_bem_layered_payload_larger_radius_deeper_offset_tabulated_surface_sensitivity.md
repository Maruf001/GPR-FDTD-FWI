# BEM Experiment 196: Deeper-Offset Tabulated Surface Sensitivity

Date: 2026-06-27

## Purpose

Stress-test the run `195` tabulated field-surface validator with damaged
variants of the run `194` repair candidate.

This is a CPU-only sensitivity run. It does not rerun FDTD/BEM solvers, compare
against field data, launch GPU/HPC work, run 3D validation, run field FWI, or
promote results to synthetic `outputs/experiments`.

## Output

```text
outputs/bem_experiments/196_project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_sensitivity
```

Key artifacts:

```text
data/project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_sensitivity_rows.csv
data/project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_sensitivity_summary.json
figures/project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_sensitivity.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_LARGER_RADIUS_DEEPER_OFFSET_TABULATED_SURFACE_SENSITIVITY.md
scripts/run_project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_sensitivity.py
scripts/test_project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_sensitivity.py
```

## Result

```text
sensitivity scenarios:              10
expected pass scenarios:             1
observed pass scenarios:             1
expected failure scenarios:          9
observed failure scenarios:          9
unexpected outcomes:                 0
tabulated-surface sensitivity ready: true
contract refresh ready:              false
field transfer ready:                false
3D validation ready:                 false
GPU work ready:                      false
field FWI ready:                     false
```

The exact run `194` result passes. These damaged variants fail as expected:

| Scenario | Failed check family |
| --- | --- |
| Missing dense 5 mm policy | Policy count, ready count, best-policy, best-L2 checks |
| Exact-only policy marked ready | Ready count and exact-only extrapolation checks |
| Exact-only extrapolation removed | Exact-only extrapolation check |
| Dense 10 mm policy marked not ready | Ready count and 10 mm readiness checks |
| Dense 10 mm policy marked extrapolated | 10 mm no-extrapolation check |
| Summary best L2 moved above gate | Best-L2 consistency and gate checks |
| No Sommerfeld improvement | Baseline-improvement check |
| Contract refresh marked ready | Premature contract-refresh check |
| Field transfer marked ready | Premature field/3D/GPU check |

## Interpretation

The run `195` validator is sensitive to the main ways the tabulated-surface
repair could be misread or corrupted: missing dense policy coverage, incorrect
extrapolation state, an above-gate best L2, no improvement over the Sommerfeld
baseline, and premature promotion flags.

This completes the single-case guard package for the tabulated-surface repair.
It still does not prove generalization.

## Decision

Use runs `194`-`196` as the current tabulated-surface repair guard package.
Keep analytic contract refresh, field transfer, 3D validation, GPU/HPC, field
FWI, and synthetic `outputs/experiments` promotion blocked until
generalization is tested.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_probe.py
tests/test_project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_validator.py
tests/test_project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_sensitivity.py
11 passed
```

Figure validation:

```text
project_core_bem_layered_payload_larger_radius_deeper_offset_tabulated_surface_sensitivity.png
2753x865, dynamic range=255
```
