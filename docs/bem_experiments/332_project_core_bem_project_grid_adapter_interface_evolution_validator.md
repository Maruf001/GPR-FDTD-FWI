# BEM Experiment 332: Project-Grid Adapter Interface Evolution Validator

Date: 2026-06-28

## Purpose

Validate the saved run `331` interface-evolution audit from artifacts.

This run checks that the run `331` mapping is internally consistent, that all
old adapter contract items have successors, that the later payload smoke emits
all later interface items, and that downstream claim guardrails remain blocked.

This is an artifact validator. It does not run FDTD, GPU/HPC work, field data,
field FWI, neural-network training, or synthetic 2D archive promotion.

## Output

```text
outputs/bem_experiments/332_project_core_bem_project_grid_adapter_interface_evolution_validator
```

Key artifacts:

```text
data/project_core_bem_project_grid_adapter_interface_evolution_validator_checks.csv
data/project_core_bem_project_grid_adapter_interface_evolution_validator_summary.json
figures/project_core_bem_project_grid_adapter_interface_evolution_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  8
passed checks:                      8
failed checks:                      0
interface validation ready:         true
old interface items:                7
new interface items:                8
run 093 emitted items:              8
mapped old items:                   7
new payload-output items:           1
field claim ready:                  false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

## Interpretation

The saved run `331` interface-evolution audit is internally consistent. All
seven old items have successors, the later interface has eight emitted payload
items, and the new adapter-output frequency-bin product remains explicit.

## Decision

Use runs `331-332` as the guarded interface-evolution block. Later adapter work
can refer to this map, but field, archive, 3D, GPU, and field-FWI claims remain
blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_project_grid_adapter_interface_evolution_validator.py
3 passed
```

Figure validation:

```text
3401x933, dynamic range=255
```
