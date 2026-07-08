# BEM Experiment 330: Project-Grid Adapter Lineage Validation Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `329` lineage validator with controlled damaged variants.

This run uses saved BEM artifacts only. It does not run FDTD, launch GPU/HPC
work, use field data, use the synthetic 2D experiment archive, or run field FWI.

## Output

```text
outputs/bem_experiments/330_project_core_bem_project_grid_adapter_lineage_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_project_grid_adapter_lineage_validation_sensitivity_scenarios.csv
data/project_core_bem_project_grid_adapter_lineage_validation_sensitivity_summary.json
figures/project_core_bem_project_grid_adapter_lineage_validation_sensitivity.png
docs/PROJECT_CORE_BEM_PROJECT_GRID_ADAPTER_LINEAGE_VALIDATION_SENSITIVITY.md
```

## Result

```text
scenarios:                10
expected pass:            1
observed pass:            1
expected failures:        9
observed failures:        9
unexpected outcomes:      0
sensitivity ready:        true
accepts exact run 328:    true
rejects damaged variants: true
field claim ready:        false
3D validation ready:      false
GPU work ready:           false
field FWI ready:          false
```

Damaged variants cover lineage-count drift, implementation-readiness drift,
raw-analytic false promotion, guardrail drift, downstream promotion, figure
validation drift, and script-snapshot drift.

## Interpretation

The lineage validator accepts the exact run `328` audit and rejects all damaged
variants tested here.

## Decision

Use runs `328-330` as the guarded project-grid adapter lineage block. Future
BEM adapter work should continue from the guarded payload/field-surface
adapters.

## Validation

Focused tests:

```text
tests/test_project_core_bem_project_grid_adapter_lineage_audit.py
tests/test_project_core_bem_project_grid_adapter_lineage_validator.py
tests/test_project_core_bem_project_grid_adapter_lineage_validation_sensitivity.py

9 passed
```

Figure validation:

```text
3293x889, dynamic range=255
```
