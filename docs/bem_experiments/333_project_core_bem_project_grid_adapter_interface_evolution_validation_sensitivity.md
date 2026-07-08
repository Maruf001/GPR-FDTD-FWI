# BEM Experiment 333: Project-Grid Adapter Interface Evolution Validation Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `332` interface-evolution validator with controlled damaged
variants.

This run checks that the validator accepts the exact run `331` artifacts and
rejects damaged versions with count drift, missing old-item successors,
changed output-product semantics, missing payload emissions, failed source
validation checks, false downstream promotion, invalid figure metadata, and
missing script snapshots.

This is an artifact sensitivity test. It does not run FDTD, GPU/HPC work,
field data, field FWI, neural-network training, or synthetic 2D archive
promotion.

## Output

```text
outputs/bem_experiments/333_project_core_bem_project_grid_adapter_interface_evolution_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_project_grid_adapter_interface_evolution_validation_sensitivity_scenarios.csv
data/project_core_bem_project_grid_adapter_interface_evolution_validation_sensitivity_summary.json
figures/project_core_bem_project_grid_adapter_interface_evolution_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                    11
expected pass:                1
observed pass:                1
expected failures:            10
observed failures:            10
unexpected outcomes:          0
sensitivity ready:            true
accepts exact run 331:        true
rejects damaged variants:     true
field claim ready:            false
3D validation ready:          false
GPU work ready:               false
field FWI ready:              false
```

## Interpretation

The interface-evolution validator accepts the exact run `331` audit and rejects
damaged variants covering count drift, old-item successor loss,
output-product semantics drift, payload emission loss, source-validation
failure, downstream promotion, figure validation, and script snapshots.

## Decision

Use runs `331-333` as the guarded interface-evolution block. Future adapter
work should continue from the controlled grid-aware payload interface, not from
field, archive, 3D, GPU, or field-FWI claims.

## Validation

Focused tests:

```text
tests/test_project_core_bem_project_grid_adapter_interface_evolution_validation_sensitivity.py
3 passed
```

Figure validation:

```text
3329x913, dynamic range=255
```
