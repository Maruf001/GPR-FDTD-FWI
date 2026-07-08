# BEM Experiment 329: Project-Grid Adapter Lineage Validator

Date: 2026-06-28

## Purpose

Validate the saved run `328` project-grid adapter lineage audit from artifacts.

This run uses saved BEM artifacts only. It does not run FDTD, launch GPU/HPC
work, use field data, use the synthetic 2D experiment archive, or run field FWI.

## Output

```text
outputs/bem_experiments/329_project_core_bem_project_grid_adapter_lineage_validator
```

Key artifacts:

```text
data/project_core_bem_project_grid_adapter_lineage_validator_checks.csv
data/project_core_bem_project_grid_adapter_lineage_validator_summary.json
figures/project_core_bem_project_grid_adapter_lineage_validator.png
docs/PROJECT_CORE_BEM_PROJECT_GRID_ADAPTER_LINEAGE_VALIDATOR.md
```

## Result

```text
validation checks:                7
passed checks:                    7
failed checks:                    0
validation ready:                 true
lineage rows:                     11
accepted lineage rows:            10
blocked lineage rows:             1
blocked lineage step:             raw_bem_compatible_analytic_field_probe
run 037 contract ready:           true
run 038 smoke ready:              true
raw analytic field adapter ready: false
project-domain surface ready:     true
current payload contract ready:   true
implementation branch ready:      true
field claim ready:                false
3D validation ready:              false
GPU work ready:                   false
field FWI ready:                  false
```

## Interpretation

Run `328` validates as the current lineage view for the run `037` adapter
contract. The implementation branch is ready through the guarded payload path,
while the raw analytic-field path remains blocked.

## Decision

Use runs `328-329` as the guarded project-grid adapter lineage block. Continue
future BEM work from the guarded payload/field-surface adapters and keep
archive, field, 3D, GPU, and field-FWI claims blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_project_grid_adapter_lineage_audit.py
tests/test_project_core_bem_project_grid_adapter_lineage_validator.py

6 passed
```

Figure validation:

```text
3401x929, dynamic range=255
```
